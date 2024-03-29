from random import randint
from discord import (
    Color,
    Embed,
    HTTPException,
    Interaction,
    Member,
    Message,
    NotFound,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot, GroupCog
from discord.utils import utcnow
from datetime import datetime, timedelta
from humanfriendly import InvalidTimespan, format_timespan, parse_timespan
from functions import Botban, Command, Logger, Moderation
from assets.components import Confirmation
from typing import Optional
from discord.ext import tasks


class BanCog(GroupCog, name="ban"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Ban someone outside the server")
    @Jeanne.describe(user_id="What is the user ID?", reason="What did they do?")
    @Jeanne.checks.has_permissions(ban_members=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    async def user(
        self,
        ctx: Interaction,
        user_id: str,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.user.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        user = await self.bot.fetch_user(int(user_id))
        reason = reason if reason else "Unspecified"

        if int(user_id) == ctx.guild.owner.id:
            failed = Embed(
                description="You can't ban the owner of the server...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return

        if int(user_id) == ctx.user.id:
            failed = Embed(description="You cannot ban yourself...", color=Color.red())
            await ctx.followup.send(embed=failed)
            return

        try:
            banned = await ctx.guild.fetch_ban(user)
            if banned:
                already_banned = Embed(
                    description=f"{user} is already banned here", color=Color.red()
                )
                await ctx.followup.send(embed=already_banned)
        except NotFound:
            view = Confirmation(ctx.user)
            confirm = Embed(
                description="Is {} the one you want to ban from your server?".format(
                    user
                ),
                color=Color.dark_red(),
            ).set_thumbnail(url=user.display_avatar)
            await ctx.followup.send(embed=confirm, view=view)
            await view.wait()

            if view.value == None:
                cancelled = Embed(description="Ban cancelled", color=Color.red())
                await ctx.edit_original_response(embed=cancelled, view=None)

            elif view.value == True:
                await ctx.guild.ban(user, reason="{} | {}".format(reason, ctx.user))

                ban = Embed(title="User Banned", color=0xFF0000)
                ban.add_field(name="Name", value=user, inline=True)
                ban.add_field(name="ID", value=user.id, inline=True)
                ban.add_field(name="Moderator", value=ctx.user, inline=True)
                ban.add_field(name="Reason", value=reason, inline=False)
                ban.set_thumbnail(url=user.display_avatar)

                modlog_id = Logger(ctx.guild).get_modlog_channel

                if modlog_id == None:
                    await ctx.edit_original_response(embed=ban, view=None)
                    return

                modlog = ctx.guild.get_channel(modlog_id)
                banned = Embed(
                    description=f"{user} has been banned. Check {modlog.mention}",
                    color=0xFF0000,
                )
                await ctx.edit_original_response(embed=banned, view=None)
                await modlog.send(embed=ban)

            elif view.value == False:
                cancelled = Embed(description="Ban cancelled", color=Color.red())
                await ctx.edit_original_response(embed=cancelled, view=None)

    @Jeanne.command(description="Ban someone in this server")
    @Jeanne.describe(
        member="Which member are you banning?",
        reason="What did they do?",
        time="How long should they be tempbanned? (1m, 1h30m, etc)",
    )
    @Jeanne.checks.has_permissions(ban_members=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    async def member(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
        time: Optional[str] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.member.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        if member == ctx.user:
            failed = Embed(description="You can't ban yourself")
            await ctx.followup.send(embed=failed)
            return

        if member.id == ctx.guild.owner.id:
            failed = Embed(
                description="You can't ban the owner of the server...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return

        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="{}'s position is higher than you...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return

        try:
            banmsg = Embed(
                description=f"You are banned from **{ctx.guild.name}** for **{reason}**"
            )
            await member.send(embed=banmsg)
        except:
            pass

        reason = reason if reason else "Unspecified"

        await member.ban(reason="{} | {}".format(reason, ctx.user))

        ban = Embed(title="Member Banned", color=0xFF0000)
        ban.add_field(name="Name", value=member, inline=True)
        ban.add_field(name="ID", value=member.id, inline=True)
        ban.add_field(name="Moderator", value=ctx.user, inline=True)
        ban.add_field(name="Reason", value=reason, inline=False)
        if time:
            try:
                a = parse_timespan(time)
                Moderation(ctx.guild, member).softban_member(time)
                time = format_timespan(a)
            except:
                time = "Invalid time added. User is banned permanently!"
            ban.add_field(name="Duration", value=time, inline=True)
        ban.set_thumbnail(url=member.display_avatar)

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=ban)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        banned = Embed(
            description=f"{member} has been banned. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=banned)
        await modlog.send(embed=ban)

    @user.error
    async def ban_user_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (HTTPException, ValueError)
        ):
            if Command(ctx.guild).check_disabled(self.user.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return

            embed = Embed()
            embed.description = "Invalid user ID given\nPlease try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)


class ListWarns(GroupCog, name="list-warns"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="View warnings in the server or a member")
    async def server(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.server.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        record = Moderation(ctx.guild).fetch_warnings_server()
        if record == None:
            await ctx.followup.send("No warnings up to date")
            return
        embed = Embed(title=f"Currently warned members", colour=Color.red())
        embed.description = ""
        for i in record:
            warned_member = await self.bot.fetch_user(i[0])
            warn_points = i[2]

            embed.description += (
                f"**{warned_member}**\n**Warn points**: {warn_points}\n\n"
            )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="View warnings that a member has")
    @Jeanne.describe(member="Which member are you checking the warns?")
    async def user(self, ctx: Interaction, member: Optional[Member]) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.user.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        member = ctx.user if member is None else member

        record = Moderation(ctx.guild, member).fetch_warnings_user()
        if record == None:
            await ctx.followup.send(f"{member} has no warn IDs")
            return

        embed = Embed(title=f"{member}'s warnings", colour=0xFF0000)
        embed.description = ""
        embed.set_thumbnail(url=member.display_avatar)
        for i in record:
            moderator = await self.bot.fetch_user(i[2])
            reason = i[3]
            warn_id = i[4]
            try:
                date = f"<t:{i[5]}:F>"
            except:
                date = "None due to new update"

        embed.add_field(
            name=f"`{warn_id}`",
            value=f"**Moderator:** {moderator}\n**Reason:** {reason}\n**Date:** {date}",
            inline=False,
        )
        await ctx.followup.send(embed=embed)


class moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_db.start()

    @tasks.loop(seconds=60, reconnect=True)
    async def check_db(self):
        for bans in Moderation().get_softban_data():
            if int(round(datetime.now().timestamp())) > int(bans[2]):
                guild = await self.bot.fetch_guild(bans[1])

                member = await self.bot.fetch_user(bans[0])

                await guild.unban(member, reason="Softban expired")

                await Moderation(guild, member).remove_softban()

                mod_channel = Logger(guild).get_modlog_channel

                if mod_channel != None:
                    unmute = Embed(title="Member unbanned", color=0xFF0000)
                    unmute.add_field(name="Member", value=member, inline=True)
                    unmute.add_field(name="ID", value=member.id, inline=True)
                    unmute.add_field(
                        name="Reason", value="Softban expired", inline=True
                    )
                    unmute.set_thumbnail(url=member.display_avatar)

                    modlog = await guild.fetch_channel(mod_channel)

                    await modlog.send(embed=unmute)
                else:
                    continue

    @check_db.before_loop
    async def before_check_db(self):
        await self.bot.wait_until_ready()

    @Jeanne.command(description="Warn a member")
    @Jeanne.describe(member="Which member are you warning?", reason="What did they do?")
    @Jeanne.checks.has_permissions(kick_members=True)
    async def warn(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 512]] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.warn.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="{}'s position is higher than you...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member.id == ctx.guild.owner.id:
            failed = Embed(
                description="You can't warn the owner of the server...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.user:
            failed = Embed(description="You can't warn yourself")
            await ctx.followup.send(embed=failed)
            return

        reason = reason if reason else "Unspecified"

        warn_id = randint(0, 100000)
        date = round(datetime.now().timestamp())
        await Moderation(ctx.guild).warn_user(
            member, ctx.user.id, reason, warn_id, date
        )

        warn = Embed(title="Member warned", color=0xFF0000)
        warn.add_field(name="Member", value=member, inline=True)
        warn.add_field(name="ID", value=member.id, inline=True)
        warn.add_field(name="Moderator", value=ctx.user, inline=True)
        warn.add_field(name="Reason", value=reason, inline=False)
        warn.add_field(name="Warn ID", value=warn_id, inline=True)
        warn.add_field(name="Date", value="<t:{}:F>".format(date), inline=True)
        warn.set_thumbnail(url=member.display_avatar)

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=warn)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        warned = Embed(
            description=f"{member} has been warned. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=warned)
        await modlog.send(embed=warn)

    @Jeanne.command(name="clear-warn", description="Revoke a warn by warn ID")
    @Jeanne.describe(
        member="Which member got warned?",
        warn_id="What is their warn ID you want to remove?",
    )
    @Jeanne.checks.has_permissions(kick_members=True)
    async def clearwarn(self, ctx: Interaction, member: Member, warn_id: int):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.clearwarn.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        mod = Moderation(ctx.guild)
        result = mod.check_warn_id(member, warn_id)

        if result == None:
            await ctx.followup.send("Invalid warn ID")
            return

        await mod.revoke_warn(member, warn_id)

        revoked_warn = Embed(
            title="Warn removed",
            description=f"{ctx.user} has revoked warn ID ({warn_id})",
        )

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=revoked_warn)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        revoke = Embed(
            description=f"Warn revoked. Check {modlog.mention}", color=0xFF0000
        )
        await modlog.send(embed=revoke)
        await ctx.followup.send(embed=revoked_warn)

    @Jeanne.command(description="Kick a member out of the server")
    @Jeanne.describe(
        member="Which member are you kicking?", reason="Why are they being kicked?"
    )
    @Jeanne.checks.has_permissions(kick_members=True)
    @Jeanne.checks.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.kick.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        if member.id == ctx.user.id:
            failed = Embed(description="You can't kick yourself out")
            await ctx.followup.send(embed=failed)
            return
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="{}'s position is higher than you...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member.id == ctx.guild.owner.id:
            failed = Embed(
                description="You cannot kick the owner of the server out...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.user:
            failed = Embed(description="You can't kick yourself out")
            await ctx.followup.send(embed=failed)
            return

        reason = reason if reason else "Unspecified"

        try:
            kickmsg = Embed(
                description=f"You are kicked from **{ctx.guild.name}** for **{reason}**"
            )
            await member.send(embed=kickmsg)
        except:
            pass

        # await member.kick(reason="{} | {}".format(reason, ctx.user))
        await ctx.guild.kick(member, reason="{} | {}".format(reason, ctx.user))
        kick = Embed(title="Member Kicked", color=0xFF0000)
        kick.add_field(name="Member", value=member, inline=True)
        kick.add_field(name="ID", value=member.id, inline=True)
        kick.add_field(name="Moderator", value=ctx.user, inline=True)
        kick.add_field(name="Reason", value=reason, inline=True)
        kick.set_thumbnail(url=member.display_avatar)

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=kick)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        kicked = Embed(
            description=f"{member} has been kicked. Check {modlog.mention}",
            color=0xFF0000,
        )
        await modlog.send(embed=kick)
        await ctx.followup.send(embed=kicked)

    @Jeanne.command(description="Bulk delete messages")
    @Jeanne.describe(
        limit="How many messages? (max is 100)",
        member="Which member's messages you want to delete?",
    )
    @Jeanne.checks.has_permissions(manage_messages=True)
    @Jeanne.checks.bot_has_permissions(manage_messages=True)
    async def prune(
        self,
        ctx: Interaction,
        limit: Optional[Jeanne.Range[int, None, 100]] = None,
        member: Optional[Member] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.prune.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        limit = (limit + 1) if limit else 101

        if member:

            def is_member(m: Message):
                return m.author == member

            await ctx.channel.purge(limit=limit, check=is_member)
            return

        await ctx.channel.purge(limit=limit)

    @Jeanne.command(name="change-nickname", description="Change someone's nickname")
    @Jeanne.describe(member="Which member?", nickname="What is their new nickname")
    @Jeanne.checks.has_permissions(manage_nicknames=True)
    @Jeanne.checks.bot_has_permissions(manage_nicknames=True)
    async def changenickname(
        self,
        ctx: Interaction,
        member: Member,
        nickname: Optional[Jeanne.Range[str, 1, 32]],
    ):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.changenickname.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        if (not nickname) or (nickname == None):
            await member.edit(nick=None)
            setnick = Embed(color=0x00FF68)
            setnick.add_field(
                name="Nickname changed",
                value=f"{member}'s nickname has been removed",
                inline=False,
            )
            await ctx.followup.send(embed=setnick)
            return

        if member.nick == None:
            embed = Embed(color=Color.red())
            embed.description = f"{member} has no nickname"
            await ctx.followup.send(embed=embed)
            return

        await member.edit(nick=nickname)
        setnick = Embed(color=0x00FF68)
        setnick.add_field(
            name="Nickname changed",
            value=f"{member}'s nickname is now `{nickname}`",
            inline=False,
        )
        await ctx.followup.send(embed=setnick)

    @Jeanne.command(description="Unbans a user")
    @Jeanne.describe(
        user_id="What is the user ID you want to unban?",
        reason="Why are they being unbanned?",
    )
    @Jeanne.checks.has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: Interaction,
        user_id: str,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.unban.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        reason = reason if reason else "Unspecified"

        user = await self.bot.fetch_user(int(user_id))
        await ctx.guild.unban(user, reason="{} | {}".format(reason, ctx.user))
        unban = Embed(title="User Unbanned", color=0xFF0000)
        unban.add_field(name="Name", value=user, inline=True)
        unban.add_field(name="ID", value=user.id, inline=True)
        unban.add_field(name="Moderator", value=ctx.user, inline=True)
        unban.add_field(name="Reason", value=reason, inline=False)
        unban.set_thumbnail(url=user.display_avatar)

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=unban)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        unbanned = Embed(
            description=f"{user} has been unbanned. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=unbanned)
        await modlog.send(embed=unban)

    @Jeanne.command(description="Timeout a member")
    @Jeanne.describe(
        member="Which member?",
        time="How long should they be on timeout (1m, 1h30m, etc)",
        reason="Why are they on timeout?",
    )
    @Jeanne.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx: Interaction,
        member: Member,
        time: Optional[str] = None,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.timeout.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        if member == ctx.user:
            failed = Embed(description="You can't time yourself out")
            await ctx.followup.send(embed=failed)

            return
        reason = reason if reason else "Unspecified"

        if not time or (parse_timespan(time) > 2505600.0):
            time = "28d"

        timed = parse_timespan(time)
        await member.edit(
            timed_out_until=utcnow() + timedelta(seconds=timed),
            reason="{} | {}".format(reason, ctx.user),
        )
        mute = Embed(title="Member Timeout", color=0xFF0000)
        mute.add_field(name="Member", value=member, inline=True)
        mute.add_field(name="ID", value=member.id, inline=True)
        mute.add_field(name="Moderator", value=ctx.user, inline=True)
        mute.add_field(name="Duration", value=time, inline=True)
        mute.add_field(name="Reason", value=reason, inline=False)
        mute.set_thumbnail(url=member.display_avatar)

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=mute)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        muted = Embed(
            description=f"{member} has been put on timeout. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=muted)
        await modlog.send(embed=mute)

    @timeout.error
    async def timeout_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, InvalidTimespan
        ):
            if Command(ctx.guild).check_disabled(self.timeout.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return

            embed = Embed()
            embed.description = "Invalid time added. Please try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Untimeouts a member")
    @Jeanne.describe(member="Which member?", reason="Why are they untimeouted?")
    @Jeanne.checks.has_permissions(moderate_members=True)
    @Jeanne.checks.bot_has_permissions(moderate_members=True)
    async def untimeout(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.untimeout.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        reason = reason if reason else "Unspecified"

        if member == ctx.user:
            failed = Embed(description="You can't untime yourself out")
            await ctx.followup.send(embed=failed)
            return

        await member.edit(
            timed_out_until=None, reason="{} | {}".format(reason, ctx.user)
        )
        unmute = Embed(title="Member Untimeout", color=0xFF0000)
        unmute.add_field(name="Member", value=member, inline=True)
        unmute.add_field(name="ID", value=member.id, inline=True)
        unmute.add_field(name="Moderator", value=ctx.user, inline=True)
        unmute.add_field(name="Reason", value=reason, inline=False)
        unmute.set_thumbnail(url=member.display_avatar)

        modlog_id = Logger(ctx.guild).get_modlog_channel

        if modlog_id == None:
            await ctx.followup.send(embed=unmute)
            return

        modlog = ctx.guild.get_channel(modlog_id)
        unmuted = Embed(
            description=f"{member} has been untimeouted. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=unmuted)
        await modlog.send(embed=unmute)

    @Jeanne.command(description="Ban multiple members at once")
    @Jeanne.describe(
        user_ids="How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
        reason="Why are they being banned?",
    )
    @Jeanne.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    async def massban(self, ctx: Interaction, user_ids: str, reason: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.massban.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        ids = user_ids.split()[:25]

        if len(ids) < 5:
            embed = Embed(
                description=f"There are too few IDs. Please add more and try again after <t:{round((datetime.now() + timedelta(minutes=30)).timestamp())}:R>"
            )
            await ctx.followup.send(embed=embed)
            return

        banned_ids = {entry.user.id async for entry in ctx.guild.bans()}
        author_id = ctx.user.id
        guild_owner_id = ctx.guild.owner.id

        to_ban_ids = [
            user_id
            for user_id in ids
            if user_id not in banned_ids
            and user_id != str(author_id)
            and user_id != str(guild_owner_id)
        ]

        if not to_ban_ids:
            embed = Embed(description="No users can be banned.", color=Color.red())
            await ctx.followup.send(embed=embed)
            return

        view = Confirmation(ctx.user)
        alert = Embed(
            title="BEWARE",
            description="The developer is **NOT** responsible in any way or form if you mess up, even if it was misused.\n\nDo you want to proceed?",
            color=Color.red(),
        )
        await ctx.followup.send(embed=alert, view=view)

        await view.wait()

        if view.value == True:
            em = Embed(
                description="Banning user IDs now <a:loading:1161038734620373062>",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=em, view=None)

            ban_count = 0
            failed_ids = []
            banned = []

            for user_id in to_ban_ids:
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    await ctx.guild.ban(user, reason=reason)
                    banned.append(f"{user} | `{user.id}`")
                    ban_count += 1
                except Exception:
                    failed_ids.append(user_id)
                    continue

            if ban_count > 0:
                embed = Embed(
                    title="List of banned users",
                    color=Color.red(),
                )
                embed.description = "\n".join(banned)
                embed.add_field(name="Reason", value=reason, inline=False)
                if failed_ids:
                    embed.add_field(
                        name="Failed to ban",
                        value="\n".join(failed_ids),
                        inline=False,
                    )
            else:
                embed = Embed(description="No users were banned.", color=Color.red())

            modlog_id = Logger(ctx.guild).get_modlog_channel
            if modlog_id == None:
                await ctx.edit_original_response(embed=embed)
                return

            modlog = ctx.guild.get_channel(modlog_id)
            await ctx.edit_original_response(
                embed=Embed(
                    description=f"Successfully banned {ban_count} user(s). Check {modlog.mention}",
                    color=Color.red(),
                )
            )
            await modlog.send(embed=embed)

        elif view.value in [False, None]:
            cancelled = Embed(description="Massban cancelled", color=Color.red())
            await ctx.edit_original_response(embed=cancelled, view=None)

    @massban.error
    async def massban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.massban.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return

            await ctx.response.defer()
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"A massban command was already used here in this server.\nTry again after <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="Unban multiple members at once")
    @Jeanne.describe(
        user_ids="How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
        reason="Why are they being banned?",
    )
    @Jeanne.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    @Jeanne.checks.has_permissions(administrator=True)
    async def massunban(self, ctx: Interaction, user_ids: str, reason: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.massunban.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.response.defer()
        ids = user_ids.split()[:25]

        if len(ids) < 5:
            embed = Embed(
                description=f"There are too few IDs. Please add more and try again after <t:{round((datetime.now() + timedelta(minutes=30)).timestamp())}:R>"
            )
            await ctx.followup.send(embed=embed)
            return

        banned_ids = {entry.user.id async for entry in ctx.guild.bans()}
        author_id = ctx.user.id
        guild_owner_id = ctx.guild.owner.id

        to_ban_ids = [
            user_id
            for user_id in ids
            if user_id not in banned_ids
            and user_id != str(author_id)
            and user_id != str(guild_owner_id)
        ]

        if not to_ban_ids:
            embed = Embed(description="No users can be unbanned.", color=Color.red())
            await ctx.followup.send(embed=embed)
            return

        view = Confirmation(ctx.user)
        alert = Embed(
            title="BEWARE",
            description="The developer is **NOT** responsible in any way or form if you mess up, even if it was misused.\n\nDo you want to proceed?",
            color=Color.red(),
        )
        await ctx.followup.send(embed=alert, view=view)

        await view.wait()

        if view.value == True:
            em = Embed(
                description="Unbanning user IDs now <a:loading:1161038734620373062>",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=em, view=None)

            unban_count = 0
            failed_ids = []
            unbanned = []

            for user_id in to_ban_ids:
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    await ctx.guild.unban(user, reason=reason)
                    unbanned.append(f"{user} | `{user.id}`")
                    unban_count += 1
                except Exception:
                    failed_ids.append(user_id)
                    continue

            if unban_count > 0:
                embed = Embed(
                    title="List of unbanned users",
                    color=Color.red(),
                )
                embed.description = "\n".join(unbanned)
                embed.add_field(name="Reason", value=reason, inline=False)
                if failed_ids:
                    embed.add_field(
                        name="Failed to unban",
                        value="\n".join(failed_ids),
                        inline=False,
                    )
            else:
                embed = Embed(description="No users were unbanned.", color=Color.red())

            modlog_id = Logger(ctx.guild).get_modlog_channel
            if modlog_id == None:
                await ctx.edit_original_response(embed=embed)
                return

            modlog = ctx.guild.get_channel(modlog_id)
            await ctx.edit_original_response(
                embed=Embed(
                    description=f"Successfully unbanned {unban_count} user(s). Check {modlog.mention}",
                    color=Color.red(),
                )
            )
            await modlog.send(embed=embed)

        elif view.value in [False, None]:
            cancelled = Embed(description="Massunban cancelled", color=Color.red())
            await ctx.edit_original_response(embed=cancelled, view=None)

    @massunban.error
    async def massunban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.massunban.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"A massunban command was already used here in this server.\nTry again after <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)


async def setup(bot: Bot):
    await bot.add_cog(BanCog(bot))
    await bot.add_cog(ListWarns(bot))
    await bot.add_cog(moderation(bot))
