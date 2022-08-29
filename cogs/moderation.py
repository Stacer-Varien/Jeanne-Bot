from random import randint
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.ext.application_checks import *
from nextcord.utils import utcnow
from datetime import datetime, timedelta
from humanfriendly import parse_timespan
from assets.db_functions import *
from assets.buttons import Confirmation
from nextcord.ext.application_checks.errors import *
from nextcord.ext.commands.errors import *


class slashmoderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Warn a member")
    @has_permissions(kick_members=True)
    async def warn(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to warn?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if reason == None:
                reason = "Unspecified"

            if member == ctx.user:
                failed = Embed(description="You can't warn yourself")
                await ctx.followup.send(embed=failed)

            else:
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



    @jeanne_slash(description="Main list_warns command")
    async def list_warns(self, ctx: Interaction):
        pass

    @list_warns.subcommand(description="View warnings in the server or a member")
    async def guild(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            record = fetch_warnings_server(ctx.guild.id)
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

    @list_warns.subcommand(name="user", description="View warnings in the server or a member")
    async def _user_(self, ctx: Interaction, member: Member = SlashOption(description="Who's warnings you wanna see?", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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

    @jeanne_slash(description="Revoke a warn by warn ID")
    @has_permissions(kick_members=True)
    async def revoke_warn(self, ctx: Interaction, warn_id=SlashOption(description="Provide the valid warn ID")):
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


    @jeanne_slash(description="Main ban command")
    async def ban(self, ctx: Interaction):
        pass

    @ban.subcommand(description="Ban someone in this server")
    @has_permissions(ban_members=True)
    async def member(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to ban?", required=True), reason=SlashOption(description='What is the reason?', required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member == ctx.user:
                failed = Embed(description="You can't ban yourself")
                await ctx.followup.send(embed=failed)
            else:
                if reason == None:
                    reason = 'Unspecified'
                
                else:
                    reason=reason
                try:
                    banmsg = Embed(
                        description=f"You are banned from **{ctx.guild.name}** for **{reason}**")
                    await member.send(embed=banmsg)
                except:
                    pass

                await member.ban(reason="{} | {}".format(reason, ctx.user))

                ban = Embed(title="Member Banned", color=0xFF0000)
                ban.add_field(name="Name", value=member, inline=True)
                ban.add_field(name="ID", value=member.id, inline=True)
                ban.add_field(name="Moderator", value=ctx.user, inline=True)
                ban.add_field(name="Reason", value=reason, inline=False)
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

    @ban.subcommand(description="Ban someone outside the server")
    @has_permissions(ban_members=True)
    async def user(self, ctx: Interaction, user_id=SlashOption(description="What is the User ID?", required=True), reason=SlashOption(description="What is the reason", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            user = await self.bot.fetch_user(user_id)
            guild = ctx.guild
            if reason == None:
                reason = "Unspecified"
            else:
                reason=reason

            try:
                banned = await guild.fetch_ban(user)
            except NotFound:
                banned = False

            if banned:
                already_banned = Embed(
                    description=f"{user} is already banned here")
                await ctx.followup.send(embed=already_banned)

            else:
                view = Confirmation()
                confirm = Embed(description="Is {} the one you want to ban from your server?".format(
                    user), color=Color.dark_red()).set_thumbnail(url=user.display_avatar)
                await ctx.followup.send(embed=confirm, view=view)
                await view.wait()

                if view.value is None:
                    cancelled = Embed(
                        description="Ban cancelled", color=Color.red())
                    await ctx.edit_original_message(embed=cancelled, view=None)

                elif view.value is True:
                    await guild.ban(user, reason="{} | {}".format(reason, ctx.user))

                    ban = Embed(title="User Banned", color=0xFF0000)
                    ban.add_field(name="Name", value=user, inline=True)
                    ban.add_field(name="ID", value=user.id, inline=True)
                    ban.add_field(name="Moderator",
                                  value=ctx.user, inline=True)
                    ban.add_field(name="Reason", value=reason, inline=False)
                    ban.set_thumbnail(url=user.display_avatar)

                    modlog_id = get_modlog_channel(ctx.guild.id)

                    if modlog_id == None:
                        await ctx.edit_original_message(embed=ban, view=None)
                    else:
                        modlog = ctx.guild.get_channel(modlog_id)
                        banned = Embed(
                            description=f"{user} has been banned. Check {modlog.mention}", color=0xFF0000)
                        await ctx.edit_original_message(embed=banned, view=None)
                        await modlog.send(embed=ban)

                elif view.value is False:
                    cancelled = Embed(
                        description="Ban cancelled", color=Color.red())
                    await ctx.edit_original_message(embed=cancelled, view=None)


    @jeanne_slash(description="Kick a member out of the server")
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to kick?"), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member == ctx.user:
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


    @jeanne_slash(description="Bulk delete messages")
    @has_permissions(manage_messages=True)
    async def prune(self, ctx: Interaction, limit=SlashOption(description="How many messages are you deleting?", required=False), member: Member = SlashOption(description="Who's messages are you deleting?", required=False)):
        await ctx.response.defer(ephemeral=True)
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if limit == None:
                limit = 100
            
            elif limit > 100:
                nope=Embed(description="Can't delete that much due to Discord API", color=Color.red())
                await ctx.followup.send(embed=nope, ephemeral=True)

            if member:
                def is_member(m):
                    return m.author == member

                await ctx.channel.purge(limit=int(limit), check=is_member)
                await ctx.followup.send("Done bulk deleting messages")

            elif not member:
                await ctx.channel.purge(limit=int(limit))
                await ctx.followup.send("Done bulk deleting messages")


    @jeanne_slash(description="Change someone's nickname")
    @has_permissions(manage_nicknames=True)
    async def change_nickname(self, ctx: Interaction, member: Member = SlashOption(description="Who's nickname are you changing?", required=True), nickname=SlashOption(description="What will be their new name?", required=True)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await member.edit(nick=nickname)
            setnick = Embed(color=0x00FF68)
            setnick.add_field(name="Nickname changed",
                              value=f"{member}'s nickname is now `{nickname}`", inline=False)
            await ctx.followup.send(embed=setnick)


    @jeanne_slash(description="Unbans a user")
    @has_permissions(ban_members=True)
    async def unban(self, ctx: Interaction, user_id=SlashOption(description="Who do you want to unban with ID?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            user = await self.bot.fetch_user(user_id)
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

    @jeanne_slash(description="Mute a member")
    @has_permissions(moderate_members=True)
    async def mute(self, ctx: Interaction, member: Member = SlashOption(description="Who are you muting?", required=True), time=SlashOption(description="How long will the member be muted?", required=False), reason=SlashOption(description="Give a reason", required=False)):
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

                if reason is None:
                    reason = "Unspecified"
                else:
                    reason = reason


                timed = parse_timespan(time)
                await member.edit(timeout=utcnow()+timedelta(seconds=timed), reason="{} | {}".format(reason, ctx.user))
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


    @jeanne_slash()
    @has_permissions(moderate_members=True)
    async def unmute(self, ctx: Interaction, member: Member = SlashOption(description="Who are you unmuting?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if reason == None:
                reason = "Unspecified"
            else:
                reason=reason

            if member == ctx.user:
                failed = Embed(description="You can't unmute yourself")
                await ctx.followup.send(embed=failed)

            else:
                await member.edit(timeout=None, reason="{} | {}".format(reason, ctx.user))
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

def setup(bot):
    bot.add_cog(slashmoderation(bot))
