from random import randint
from discord import *
from discord.ext.commands import Cog, Bot, GroupCog
from discord.utils import utcnow
from datetime import datetime, timedelta
from humanfriendly import format_timespan, parse_timespan
from db_functions import *
from assets.buttons import Confirmation
from typing import Optional
from discord.ext import tasks

class ListWarns_Group(GroupCog, name="listwarns"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="View warnings in the server or a member")
    async def server(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            record = fetch_warnings_server(ctx.guild.id).fetchall()
            if len(record) == 0:
                await ctx.followup.send(f"No warnings up to date")
            else:
                embed = Embed(
                    title=f"Currently warned members", colour=0xFF0000)
                embed.description = ""
                for i in record:
                    warned_member = await self.bot.fetch_user(i[0])
                    warn_points = i[2]

                    embed.description += f"**{warned_member}**\n**Warn points**: {warn_points}\n\n"
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="View warnings that a member has")
    @app_commands.describe(member="Which member are you checking the warns?")
    async def user(self, ctx: Interaction, member: Optional[Member]) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if member == None:
                member = ctx.user

            record = fetch_warnings_user(member.id, ctx.guild.id).fetchall()
            if len(record) == 0:
                await ctx.followup.send(f"{member} has no warn IDs")

            else:
                embed = Embed(
                    title=f"{member}'s warnings", colour=0xFF0000)
                embed.description = ""
                embed.set_thumbnail(url=member.display_avatar)
                for i in record:
                    moderator = await self.bot.fetch_user(i[2])
                    reason = i[3]
                    warn_id = i[4]
                    date = i[5]

                    if date == None:
                        date = "Unspecified due to new update"

                    embed.add_field(
                        name=f"`{warn_id}`", value=f"**Moderator:** {moderator}\n**Reason:** {reason}\n**Date:** <t:{date}:F>", inline=False)
                await ctx.followup.send(embed=embed)


class Ban_Group(GroupCog, name="ban"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Ban someone in this server")
    @app_commands.describe(member="Which member are you banning?", reason="What did they do?", time="How long should they be tempbanned? (1m, 1h30m, etc)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def member(self, ctx: Interaction, member: Member, reason: Optional[str] = None, time: Optional[str] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if member == ctx.user:
                failed = Embed(description="You can't ban yourself")
                await ctx.followup.send(embed=failed)
            elif member.id == ctx.guild.owner.id:
                failed = Embed(
                    description="You can't ban the owner of the server...", color=Color.red())
                await ctx.followup.send(embed=failed)
            elif ctx.user.top_role.position < member.top_role.position:
                failed = Embed(description="{}'s position is higher than you...".format(
                    member), color=Color.red())
                await ctx.followup.send(embed=failed)
            else:
                try:
                    banmsg = Embed(
                        description=f"You are banned from **{ctx.guild.name}** for **{reason}**")
                    await member.send(embed=banmsg)
                except:
                    pass

                if reason == None:
                    reason = 'Unspecified'

                else:
                    reason = reason

                await member.ban(reason="{} | {}".format(reason, ctx.user))

                ban = Embed(title="Member Banned", color=0xFF0000)
                ban.add_field(name="Name", value=member, inline=True)
                ban.add_field(name="ID", value=member.id, inline=True)
                ban.add_field(name="Moderator", value=ctx.user, inline=True)
                ban.add_field(name="Reason", value=reason, inline=False)
                if time:
                    a = parse_timespan(time)
                    softban_member(member.id, ctx.guild.id, time)
                    time = format_timespan(a)
                    ban.add_field(name="Duration", value=time, inline=True)
                ban.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=ban)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    banned = Embed(
                        description=f"{member} has been banned. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=banned)
                    await modlog.send(embed=ban)

    @app_commands.command(description="Ban someone outside the server")
    @app_commands.describe(user_id="What is the user ID?", reason="What did they do?")
    @app_commands.checks.has_permissions(ban_members=True)
    async def user(self, ctx: Interaction, user_id: str, reason: Optional[str] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            user = await self.bot.fetch_user(int(user_id))
            guild = ctx.guild
            if reason == None:
                reason = "Unspecified"
            else:
                reason = reason

            if int(user_id) == ctx.guild.owner.id:
                failed = Embed(
                    description="You can't ban the owner of the server...", color=Color.red())
                await ctx.followup.send(embed=failed)

            elif int(user_id) == ctx.user.id:
                failed = Embed(
                    description="You cannot ban yourself...", color=Color.red())
                await ctx.followup.send(embed=failed)

            else:
                try:
                    banned = await guild.fetch_ban(user)
                except NotFound:
                    banned = False

                if banned:
                    already_banned = Embed(
                        description=f"{user} is already banned here")
                    await ctx.followup.send(embed=already_banned)

                else:
                    view = Confirmation(ctx.user)
                    confirm = Embed(description="Is {} the one you want to ban from your server?".format(
                        user), color=Color.dark_red()).set_thumbnail(url=user.display_avatar)
                    await ctx.followup.send(embed=confirm, view=view)
                    await view.wait()

                    if view.value == None:
                        cancelled = Embed(
                            description="Ban cancelled", color=Color.red())
                        await ctx.edit_original_response(embed=cancelled, view=None)

                    elif view.value == True:
                        await guild.ban(user, reason="{} | {}".format(reason, ctx.user))

                        ban = Embed(title="User Banned", color=0xFF0000)
                        ban.add_field(name="Name", value=user, inline=True)
                        ban.add_field(name="ID", value=user.id, inline=True)
                        ban.add_field(name="Moderator",
                                      value=ctx.user, inline=True)
                        ban.add_field(
                            name="Reason", value=reason, inline=False)
                        ban.set_thumbnail(url=user.display_avatar)

                        modlog_id = get_modlog_channel(ctx.guild.id)

                        if modlog_id == None:
                            await ctx.edit_original_response(embed=ban, view=None)
                        else:
                            modlog = ctx.guild.get_channel(modlog_id)
                            banned = Embed(
                                description=f"{user} has been banned. Check {modlog.mention}", color=0xFF0000)
                            await ctx.edit_original_response(embed=banned, view=None)
                            await modlog.send(embed=ban)

                    elif view.value == False:
                        cancelled = Embed(
                            description="Ban cancelled", color=Color.red())
                        await ctx.edit_original_response(embed=cancelled, view=None)


class Mute_Group(GroupCog, name="mute"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Create a mute role with default mute permissions")
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True, manage_channels=True, manage_permissions=True)
    async def createrole(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if check_mute_role(ctx.guild.id) == True:
                e = Embed(description="Server already has a mute role",
                          color=Color.red())
                await ctx.followup.send(embed=e)
            else:
                mute_role = await ctx.guild.create_role(name="Muted", reason="Mute role automatically created")

                for channel in ctx.guild.channels:
                    try:
                        mute_perms = channel.overwrites_for(mute_role)
                        mute_perms.add_reactions = False
                        mute_perms.attach_files = False
                        mute_perms.send_messages = False
                        mute_perms.create_private_threads = False
                        mute_perms.create_public_threads = False
                        mute_perms.create_private_threads = False
                        mute_perms.send_messages_in_threads = False
                        mute_perms.send_tts_messages = False
                        mute_perms.speak = False
                        mute_perms.request_to_speak = False
                        mute_perms.connect = False
                        await channel.set_permissions(target=mute_role, overwrite=mute_perms)
                    except:
                        continue

                add_mute_role(ctx.guild.id, mute_role.id)
                em = Embed(title="Mute role created",
                           description="A mute role has been created and automatically set. You can customize it to your own fit", color=ctx.user.color)
                await ctx.followup.send(embed=em)

    @app_commands.command(description="Set a mute role that is available in the server")
    @app_commands.describe(role="Which role is gonna be the mute role?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setrole(self, ctx: Interaction, role: Role):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            add_mute_role(ctx.guild.id, role.id)

            e = Embed(title="Mute role set", description="`{}` is the selected mute role".format(
                role.name), color=ctx.user.color)
            await ctx.followup.send(embed=e)

    @app_commands.command(description="Mute a member")
    @app_commands.describe(member="Which member are you muting?", reason="What did they do?", time="How long should they be muted? (1m, 1h30m, etc)")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def member(self, ctx: Interaction, member: Member, time: Optional[str] = None, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member == ctx.user:
                failed = Embed(description="You can't mute yourself")
                await ctx.followup.send(embed=failed)
            elif ctx.user.top_role.position < member.top_role.position:
                failed = Embed(description="{}'s position is higher than you...".format(
                    member), color=Color.red())
                await ctx.followup.send(embed=failed)
            elif member.id == ctx.guild.owner.id:
                failed = Embed(
                    description="You can't mute the owner of the server...".format(member), color=Color.red())
                await ctx.followup.send(embed=failed)

            else:
                if reason == None:
                    reason = "Unspecified"

                if time == None:
                    time = "Indefinitely"
                    mute_member(member.id, ctx.guild.id)
                else:
                    a = parse_timespan(time)
                    mute_member(member.id, ctx.guild.id, time)
                    time = format_timespan(a)

                mute_role = ctx.guild.get_role(check_mute_role(ctx.guild.id))
                await member.add_roles(mute_role, reason=reason)

                mute = Embed(
                    title="Member Muted", color=0xFF0000)
                mute.add_field(name="Member", value=member, inline=True)
                mute.add_field(name="ID", value=member.id, inline=True)
                mute.add_field(
                    name="Moderator", value=ctx.user, inline=True)
                mute.add_field(
                    name="Duration", value=time, inline=True)
                mute.add_field(
                    name="Reason", value=reason, inline=False)
                mute.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=mute)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    muted = Embed(
                        description=f"{member} has been muted. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=muted)
                    await modlog.send(embed=mute)


class moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_db.start()

    @tasks.loop(seconds=5, reconnect=True)
    async def check_db(self):
        for mutes in get_muted_data():
            if int(round(datetime.now().timestamp())) > int(mutes[2]):
                guild = await self.bot.fetch_guild(mutes[1])

                member = await guild.fetch_member(mutes[0])
                mute_role = guild.get_role(check_mute_role(mutes[1]))

                await member.remove_roles(mute_role, reason="Mute expired")

                remove_mute(member.id, guild.id)

                mod_channel = get_modlog_channel(guild.id)

                if mod_channel != None:
                    unmute = Embed(
                        title="Member Unmuted", color=0xFF0000)
                    unmute.add_field(name="Member", value=member, inline=True)
                    unmute.add_field(name="ID", value=member.id, inline=True)
                    unmute.add_field(
                        name="Reason", value="Mute expired", inline=True)
                    unmute.set_thumbnail(url=member.display_avatar)

                    modlog = await guild.fetch_channel(mod_channel)

                    await modlog.send(embed=unmute)

                else:
                    continue

        for bans in get_softban_data():
            if int(round(datetime.now().timestamp())) > int(bans[2]):
                guild = await self.bot.fetch_guild(bans[1])

                member = await self.bot.fetch_user(bans[0])

                await guild.unban(member, reason="Softban expired")

                remove_softban(member.id, guild.id)

                mod_channel = get_modlog_channel(guild.id)

                if mod_channel != None:
                    unmute = Embed(
                        title="Member unbanned", color=0xFF0000)
                    unmute.add_field(name="Member", value=member, inline=True)
                    unmute.add_field(name="ID", value=member.id, inline=True)
                    unmute.add_field(
                        name="Reason", value="Softban expired", inline=True)
                    unmute.set_thumbnail(url=member.display_avatar)

                    modlog = await guild.fetch_channel(mod_channel)

                    await modlog.send(embed=unmute)

                else:
                    continue

    @app_commands.command(description="Warn a member")
    @app_commands.describe(member="Which member are you warning?", reason="What did they do?")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, ctx: Interaction, member: Member, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if ctx.user.top_role.position < member.top_role.position:
                failed = Embed(description="{}'s position is higher than you...".format(
                    member), color=Color.red())
                await ctx.followup.send(embed=failed)
            elif member.id == ctx.guild.owner.id:
                failed = Embed(
                    description="You can't warn the owner of the server...".format(member), color=Color.red())
                await ctx.followup.send(embed=failed)
            elif member == ctx.user:
                failed = Embed(description="You can't warn yourself")
                await ctx.followup.send(embed=failed)
            else:
                if reason == None:
                    reason = "Unspecified"

                warn_id = f"{randint(0,100000)}"
                date = round(datetime.now().timestamp())
                warn_user(ctx.guild.id, member.id,
                          ctx.user.id, reason, warn_id, date)

                warn = Embed(title="Member warned", color=0xFF0000)
                warn.add_field(name="Member",
                               value=member,
                               inline=True)
                warn.add_field(name="ID",
                               value=member.id,
                               inline=True)
                warn.add_field(
                    name="Moderator", value=ctx.user, inline=True)
                warn.add_field(name="Reason",
                               value=reason,
                               inline=False)
                warn.add_field(name="Warn ID",
                               value=warn_id,
                               inline=True)
                warn.add_field(name="Date",
                               value="<t:{}:F>".format(date),
                               inline=True)
                warn.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=warn)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    warned = Embed(
                        description=f"{member} has been warned. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=warned)
                    await modlog.send(embed=warn)

    @app_commands.command(description="Revoke a warn by warn ID")
    @app_commands.describe(warn_id="What is the warn ID you want to remove?")
    @app_commands.checks.has_permissions(kick_members=True)
    async def clearwarn(self, ctx: Interaction, warn_id: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            result = check_warn_id(ctx.guild.id, warn_id)

            if result == None:
                await ctx.followup.send("Invalid warn ID")

            else:
                member = check_warn_id(ctx.guild.id, warn_id)
                revoke_warn(member[0], ctx.guild.id, warn_id)

                revoked_warn = Embed(
                    title="Warn removed!", description=f"{ctx.user} has revoked warn ID ({warn_id})")

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=revoked_warn)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    revoke = Embed(
                        description=f"Warn revoked. Check {modlog.mention}", color=0xFF0000)
                    await modlog.send(embed=revoke)
                    await ctx.followup.send(embed=revoked_warn)

    @app_commands.command(description="Kick a member out of the server")
    @app_commands.describe(member="Which member are you kicking?", reason="Why are they being kicked?")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, ctx: Interaction, member: Member, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member.id == ctx.user.id:
                failed = Embed(description="You can't kick yourself out")
                await ctx.followup.send(embed=failed)
            elif ctx.user.top_role.position < member.top_role.position:
                failed = Embed(description="{}'s position is higher than you...".format(
                    member), color=Color.red())
                await ctx.followup.send(embed=failed)
            elif member.id == ctx.guild.owner.id:
                failed = Embed(
                    description="You cannot kick the owner of the server out...", color=Color.red())
                await ctx.followup.send(embed=failed)
            elif member == ctx.user:
                failed = Embed(description="You can't kick yourself out")
                await ctx.followup.send(embed=failed)
            else:
                if reason == None:
                    reason = 'Unspecified'
                else:
                    reason = reason

                try:
                    kickmsg = Embed(
                        description=f"You are kicked from **{ctx.guild.name}** for **{reason}**")
                    await member.send(embed=kickmsg)
                except:
                    pass

                await member.kick(reason="{} | {}".format(reason, ctx.user))
                kick = Embed(title="Member Kicked", color=0xFF0000)
                kick.add_field(name='Member', value=member, inline=True)
                kick.add_field(name='ID', value=member.id, inline=True)
                kick.add_field(name='Resposible Moderator',
                               value=ctx.user, inline=True)
                kick.add_field(name='Reason', value=reason, inline=True)
                kick.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=kick)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    kicked = Embed(
                        description=f"{member} has been kicked. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=kicked)
                    await modlog.send(embed=kick)

    @app_commands.command(description="Bulk delete messages")
    @app_commands.describe(limit="How many messages? (max is 100)", member="Which member's messages you want to delete?")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def prune(self, ctx: Interaction, limit: Optional[int] = None, member: Optional[Member] = None) -> None:
        await ctx.response.defer(thinking=True)
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if limit == None:
                limit = 100

            elif limit > 100:
                limit = 100

            if member:
                def is_member(m: Message):
                    return m.author == member

                await ctx.channel.purge(limit=limit, check=is_member)

            elif not member:
                await ctx.channel.purge(limit=limit)

    @app_commands.command(description="Change someone's nickname")
    @app_commands.describe(member="Which member?", nickname="What is their new nickname")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def changenickname(self, ctx: Interaction, member: Member, nickname: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await member.edit(nick=nickname)
            setnick = Embed(color=0x00FF68)
            setnick.add_field(name="Nickname changed",
                              value=f"{member}'s nickname is now `{nickname}`", inline=False)
            await ctx.followup.send(embed=setnick)

    @app_commands.command(description="Unbans a user")
    @app_commands.describe(user_id="What is the user ID you want to unban?", reason="Why are they being unbanned?")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, ctx: Interaction, user_id: str, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            user = await self.bot.fetch_user(int(user_id))
            await ctx.guild.unban(user, reason="{} | {}".format(reason, ctx.user))
            unban = Embed(title="User Unbanned", color=0xFF0000)
            unban.add_field(name="Name", value=user, inline=True)
            unban.add_field(name="ID", value=user.id, inline=True)
            unban.add_field(name="Moderator", value=ctx.user, inline=True)
            unban.add_field(name="Reason", value=reason, inline=False)
            unban.set_thumbnail(url=user.display_avatar)

            modlog_id = get_modlog_channel(ctx.guild.id)

            if modlog_id == None:
                await ctx.followup.send(embed=unban)
            else:
                modlog = ctx.guild.get_channel(modlog_id)
                unbanned = Embed(
                    description=f"{user} has been unbanned. Check {modlog.mention}", color=0xFF0000)
                await ctx.followup.send(embed=unbanned)
                await modlog.send(embed=unban)

    @app_commands.command(description="Unmutes a member")
    @app_commands.describe(member="Which member you want to unmute?", reason="Why are they being unmuted?")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx: Interaction, member: Member, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if ctx.user.top_role.position < member.top_role.position:
                failed = Embed(description="{}'s position is higher than you...".format(
                    member), color=Color.red())
                await ctx.followup.send(embed=failed)
            else:
                if reason == None:
                    reason = "Unspecified"

                mute_role = ctx.guild.get_role(check_mute_role(ctx.guild.id))
                await member.remove_roles(mute_role, reason=reason)
                unmute = Embed(
                    title="Member Unmuted", color=0xFF0000)
                unmute.add_field(name="Member", value=member, inline=True)
                unmute.add_field(name="ID", value=member.id, inline=True)
                unmute.add_field(
                    name="Moderator", value=ctx.user, inline=True)
                unmute.add_field(
                    name="Reason", value=reason, inline=False)
                unmute.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=unmute)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    unmuted = Embed(
                        description=f"{member} has been unmuted. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=unmuted)
                    await modlog.send(embed=unmute)

    @app_commands.command(description="Timeout a member using Discord's timeout feature")
    @app_commands.describe(member="Which member?", time="How long should they be on timeout (1m, 1h30m, etc)", reason="Why are they on timeout?")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, ctx: Interaction, member: Member, time: Optional[str] = None, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member == ctx.user:
                failed = Embed(description="You can't mute yourself")
                await ctx.followup.send(embed=failed)

            else:
                if time == None:
                    time = '28d'

                if reason == None:
                    reason = "Unspecified"
                else:
                    reason = reason

                timed = parse_timespan(time)
                await member.edit(timed_out_until=utcnow()+timedelta(seconds=timed), reason="{} | {}".format(reason, ctx.user))
                mute = Embed(
                    title="Member Timeout", color=0xFF0000)
                mute.add_field(name="Member", value=member, inline=True)
                mute.add_field(name="ID", value=member.id, inline=True)
                mute.add_field(
                    name="Moderator", value=ctx.user, inline=True)
                mute.add_field(
                    name="Duration", value=time, inline=True)
                mute.add_field(
                    name="Reason", value=reason, inline=False)
                mute.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=mute)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    muted = Embed(
                        description=f"{member} has been muted. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=muted)
                    await modlog.send(embed=mute)

    @app_commands.command(description="Untimeouts a member")
    @app_commands.describe(member="Which member?", reason="Why are they untimeouted?")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, ctx: Interaction, member: Member, reason: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if reason == None:
                reason = "Unspecified"
            else:
                reason = reason

            if member == ctx.user:
                failed = Embed(description="You can't unmute yourself")
                await ctx.followup.send(embed=failed)

            else:
                await member.edit(timed_out_until=None, reason="{} | {}".format(reason, ctx.user))
                unmute = Embed(
                    title="Member Untimeout", color=0xFF0000)
                unmute.add_field(name="Member", value=member, inline=True)
                unmute.add_field(name="ID", value=member.id, inline=True)
                unmute.add_field(
                    name="Moderator", value=ctx.user, inline=True)
                unmute.add_field(
                    name="Reason", value=reason, inline=False)
                unmute.set_thumbnail(url=member.display_avatar)

                modlog_id = get_modlog_channel(ctx.guild.id)

                if modlog_id == None:
                    await ctx.followup.send(embed=unmute)
                else:
                    modlog = ctx.guild.get_channel(modlog_id)
                    unmuted = Embed(
                        description=f"{member} has been untimeouted. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=unmuted)
                    await modlog.send(embed=unmute)

    @app_commands.command(description="Ban multiple members at once")
    @app_commands.describe(user_ids="How many user IDs? Leave a space after each ID (min is 5 and max is 20)", reason="Why are they being banned?")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    async def massban(self, ctx: Interaction, user_ids: str, reason: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            ids = user_ids.replace(' ', ',').split(',')

            if len(ids) < 5:
                embed = Embed(description="There is very few IDs. Please add more and try again after <t:{}:R>".format(
                    round((datetime.now() + timedelta(minutes=30)).timestamp())))
                await ctx.followup.send(embed=embed)
            else:
                if len(ids) > 20:
                    ids = ids[:20]

                view = Confirmation(ctx.user)
                alert = Embed(title="BEWARE", description="This is an experimental command and the developer is **NOT** responsible in any way or form if you messed up, even if it was misused (but report anyone misusung them to the developer so he can botban them).\n\nDo you want to proceed?", color=Color.red())
                await ctx.followup.send(embed=alert, view=view)

                await view.wait()

                if view.value == True:
                    loading = self.bot.get_emoji(1012677456811016342)
                    em = Embed(description="Banning user IDs now {}".format(
                        loading), color=Color.red())
                    await ctx.edit_original_response(embed=em, view=None)
                    massmb = Embed()
                    massmb.title = "List of users massbanned"
                    massmb.color = Color.red()
                    massmb.description = ""
                    for id in ids:

                        if id == str(ctx.user.id):
                            pass

                        if id == str(ctx.guild.owner.id):
                            pass

                        try:
                            if ctx.guild.get_member(int(id)).top_role.position > ctx.user.top_role.position:
                                pass
                        except:
                            pass

                        try:
                            user = await self.bot.fetch_user(int(id))
                            await ctx.guild.ban(user, reason=reason)

                            massmb.description += "{} | `{}`\n".format(
                                user, user.id)
                        except:
                            continue
                    massmb.add_field(name="Reason", value=reason, inline=False)
                    modlog_id = get_modlog_channel(ctx.guild.id)
                    if modlog_id == None:
                        await ctx.edit_original_response(embed=massmb)
                    else:
                        modlog = await ctx.guild.fetch_channel(modlog_id)
                        muted = Embed(
                            description="Tried to ban {} users. Check {}".format(len(ids), modlog.mention), color=0xFF0000)
                        await ctx.edit_original_response(embed=muted)
                        await modlog.send(embed=massmb)

                elif view.value == False:
                    cancelled = Embed(
                        description="Massban cancelled", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)

                elif view.value == None:
                    cancelled = Embed(
                        description="Massban cancelled due to timeout", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)

    @massban.error
    async def massban_error(self, ctx: Interaction, error:app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"A massban command was already used here in this server.\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.followup.send(embed=cooldown)

    @app_commands.command(description="Unban multiple members at once")
    @app_commands.describe(user_ids="How many user IDs? Leave a space after each ID (min is 5 and max is 20)", reason="Why are they being unbanned?")
    @app_commands.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @app_commands.checks.has_permissions(administrator=True)
    async def massunban(self, ctx: Interaction, user_ids: str, reason: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            ids = user_ids.replace(' ', ',').split(',')
            if len(ids) < 5:
                embed = Embed(description="There is very few IDs. Please add more and try again after <t:{}:R>".format(
                    round((datetime.now() + timedelta(minutes=30)).timestamp())))
                await ctx.followup.send(embed=embed)
            else:
                if len(ids) > 20:
                    ids = ids[:20]

                view = Confirmation(ctx.user)
                alert = Embed(title="BEWARE", description="This is an experimental command and the developer is **NOT** responsible in any way or form if you messed up, even if it was misused (but report anyone misusung them to the developer so he can botban them)", color=Color.red())
                await ctx.followup.send(embed=alert, view=view)

                await view.wait()

                if view.value == True:
                    loading = self.bot.get_emoji(1012677456811016342)
                    em = Embed(description="Unbanning user IDs now {}".format(
                        loading), color=Color.red())
                    await ctx.edit_original_response(embed=em, view=None)
                    massmb = Embed()
                    massmb.title = "List of users massunbanned"
                    massmb.color = Color.red()
                    massmb.description = ""
                    for id in ids:
                        if id == str(ctx.user.id):
                            pass

                        if id == str(ctx.guild.owner.id):
                            pass

                        try:
                            if ctx.guild.get_member(int(id)).top_role.position > ctx.user.top_role.position:
                                pass
                        except:
                            pass

                        try:
                            user = await self.bot.fetch_user(int(id))
                            await ctx.guild.unban(user, reason=reason)

                            massmb.description += "{} | `{}`\n".format(
                                user, user.id)
                        except:
                            continue
                    massmb.add_field(name="Reason", value=reason, inline=False)
                    modlog_id = get_modlog_channel(ctx.guild.id)
                    if modlog_id == None:
                        await ctx.edit_original_response(embed=massmb)
                    else:
                        modlog = await ctx.guild.fetch_channel(modlog_id)
                        muted = Embed(
                            description="Tried to unban {} users. Check {}".format(len(ids), modlog.mention), color=0xFF0000)
                        await ctx.edit_original_response(embed=muted)
                        await modlog.send(embed=massmb)

                elif view.value == False:
                    cancelled = Embed(
                        description="Massunban cancelled", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)

                elif view.value == None:
                    cancelled = Embed(
                        description="Massunban cancelled due to timeout", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)

    @massunban.error
    async def massunban_error(self, ctx: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"A massunban command was already used here in this server.\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.followup.send(embed=cooldown)




async def setup(bot: Bot):
    await bot.add_cog(ListWarns_Group(bot))
    await bot.add_cog(Ban_Group(bot))
    await bot.add_cog(Mute_Group(bot))
    await bot.add_cog(moderation(bot))
