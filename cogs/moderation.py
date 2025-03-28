import asyncio
from random import randint
from discord import (
    Color,
    Embed,
    HTTPException,
    Interaction,
    User,
    Message,
    NotFound,
    Member,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot
from datetime import datetime, timedelta
from humanfriendly import InvalidTimespan, format_timespan, parse_timespan
from reactionmenu import ViewButton, ViewMenu
from functions import (
    AutoCompleteChoices,
    Moderation,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,  
)
from assets.components import Confirmation
from typing import Optional


class moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def commit_ban(
        self,
        ctx: Interaction,
        member: User,
        reason: str,
        time: Optional[str] = None,
        delete_message_history: Optional[bool] = None,
    ):
        if delete_message_history == True:
            dmh = 604800
        else:
            dmh = 86400

        await ctx.guild.ban(
            member,
            reason="{} | {}".format(reason, ctx.user),
            delete_message_seconds=dmh,
        )
        ban = Embed(title="User Banned", color=0xFF0000)
        ban.add_field(name="Name", value=member, inline=True)
        ban.add_field(name="ID", value=member.id, inline=True)
        ban.add_field(name="Moderator", value=ctx.user, inline=True)
        ban.add_field(name="Reason", value=reason, inline=False)
        if time != None:
            try:
                a = round(parse_timespan(time))
                await Moderation(ctx.guild).softban_member(member, a)
                time = format_timespan(a)
            except:
                time = "Invalid time added. User is banned permanently!"
            ban.add_field(name="Duration", value=time, inline=True)
        ban.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.edit_original_response(embed=ban, view=None)
            return
        banned = Embed(
            description=f"{member} has been banned. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.edit_original_response(embed=banned, view=None)
        await modlog.send(embed=ban)

    async def check_banned(self, ctx: Interaction, member: User):
        try:
            banned = await ctx.guild.fetch_ban(member)
            if banned:
                already_banned = Embed(
                    description=f"{member} is already banned here",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=already_banned)
                return
        except NotFound:
            return False

    @Jeanne.command(
        description="Ban someone from or outside the server",
        extras={"bot_perms": "Ban Members", "member_perms": "Ban Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.autocomplete(reason=AutoCompleteChoices.default_ban_options)
    @Jeanne.describe(
        member="What is the member or user ID?",
        reason="What did they do? You can also make a custom reason",
        delete_message_history="Delete messages from past 7 days?",
        time="How long should they be tempbanned? (1m, 1h30m, etc)",
    )
    @Jeanne.checks.has_permissions(ban_members=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def ban(
        self,
        ctx: Interaction,
        member: User,
        reason: Optional[Jeanne.Range[str, None, 470]] = "Unspecified",
        delete_message_history: Optional[bool] = None,
        time: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        if member == ctx.guild.owner:
            failed = Embed(
                description="You can't ban the owner of the server...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.user:
            failed = Embed(description="You cannot ban yourself...", color=Color.red())
            await ctx.followup.send(embed=failed)
            return

        if member not in ctx.guild.members:
            if await self.check_banned(ctx, member) == False:
                view = Confirmation(ctx.user)
                confirm = Embed(
                    description="Is {} the one you want to ban from your server?".format(
                        member
                    ),
                    color=Color.dark_red(),
                ).set_thumbnail(url=member.display_avatar)
                await ctx.followup.send(embed=confirm, view=view)
                await view.wait()
                if view.value == None:
                    cancelled = Embed(description="Ban cancelled", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)
                    return
                if view.value == True:
                    await self.commit_ban(
                        ctx, member, reason, None, delete_message_history
                    )
                    return

                if view.value == False:
                    cancelled = Embed(description="Ban cancelled", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)
                    return
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="{}'s position is higher than you...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        await self.commit_ban(ctx, member, reason, time, delete_message_history)

    @ban.error
    async def ban_user_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (HTTPException, ValueError)
        ):
            embed = Embed()
            embed.description = "Invalid user ID given\nPlease try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Warn a member",
        extras={"bot_perms": "Kick Members", "member_perms": "Kick Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Which member are you warning?", reason="What did they do?")
    @Jeanne.checks.has_permissions(kick_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def warn(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 512]] = None,
    ) -> None:
        await ctx.response.defer()
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="{}'s position is higher than you...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.guild.owner:
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
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.followup.send(embed=warn)
            return

        warned = Embed(
            description=f"{member} has been warned. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=warned)
        await modlog.send(embed=warn)

    @Jeanne.command(
        name="list-warns",
        description="View warnings in the server or a member",
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        member="Whose warnings do you want to see?",
    )
    @Jeanne.autocomplete(member=AutoCompleteChoices.warned_users)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def listwarns(self, ctx: Interaction, member: Optional[str]):
        await ctx.response.defer()
        if member != None:
            mem = ctx.guild.get_member(int(member))
        record = (
            Moderation(ctx.guild).fetch_warnings_user(mem)
            if member is not None
            else Moderation(ctx.guild).fetch_warnings_server
        )
        if record == None:
            await ctx.followup.send(f"No one has no warn IDs")
            return

        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Page $/&",
        )
        unique_names = set()
        for i in range(0, len(record), 5):
            embed_title = (
                f"{mem}'s warnings"
                if member is not None
                else "Currently warned members"
            )
            embed_color = 0xFF0000 if member else Color.red()

            embed = Embed(title=embed_title, colour=embed_color)

            embed.set_thumbnail(url=mem.display_avatar if member else ctx.guild.icon)
            for j in record[i : i + 5]:
                mod = await self.bot.fetch_user(j[2])
                user = await self.bot.fetch_user(j[0])
                reason = j[3]
                warn_id = j[4]
                points = Moderation(ctx.guild).warnpoints(user)
                date = f"<t:{j[5]}:F>"

                if member == None:
                    if user not in unique_names:
                        unique_names.add(user)
                        embed.add_field(
                            name=f"{user} | {user.id}",
                            value=f"- **Points:** {points}",
                            inline=False,
                        )
                else:
                    embed.add_field(
                        name=f"**Warn ID:** {warn_id}",
                        value=f"- **Moderator:** {mod}\n- **Reason:** {reason}\n- **Date:** {date}",
                        inline=False,
                    )
                    embed.set_footer(text=f"Total warn points: {points}")

            menu.add_page(embed=embed)
        if len(record) < 5:
            await ctx.followup.send(embed=embed)
            return

        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()

    @listwarns.error
    async def listwarns_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (ValueError, AttributeError)
        ):
            embed = Embed(
                description="This member has no warnings or this member does not exist in this server",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="clear-warn",
        description="Revoke a warn by warn ID",
        extras={"bot_perms": "Kick Members", "member_perms": "Kick Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        member="Which member got warned?",
        warn_id="What is their warn ID you want to remove?",
    )
    @Jeanne.checks.has_permissions(kick_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def clearwarn(self, ctx: Interaction, member: Member, warn_id: int):
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
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.followup.send(embed=revoked_warn)
            return

        revoke = Embed(
            description=f"Warn revoked. Check {modlog.mention}", color=0xFF0000
        )
        await modlog.send(embed=revoke)
        await ctx.followup.send(embed=revoked_warn)

    @Jeanne.command(
        description="Kick a member out of the server",
        extras={"bot_perms": "Kick Members", "member_perms": "Kick Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        member="Which member are you kicking?", reason="Why are they being kicked?"
    )
    @Jeanne.checks.has_permissions(kick_members=True)
    @Jeanne.checks.bot_has_permissions(kick_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def kick(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        await ctx.response.defer()
        if member == ctx.user:
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
        if member == ctx.guild.owner:
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
        await ctx.guild.kick(member, reason="{} | {}".format(reason, ctx.user))
        kick = Embed(title="Member Kicked", color=0xFF0000)
        kick.add_field(name="Member", value=member, inline=True)
        kick.add_field(name="ID", value=member.id, inline=True)
        kick.add_field(name="Moderator", value=ctx.user, inline=True)
        kick.add_field(name="Reason", value=reason, inline=True)
        kick.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.followup.send(embed=kick)
            return

        kicked = Embed(
            description=f"{member} has been kicked. Check {modlog.mention}",
            color=0xFF0000,
        )
        await modlog.send(embed=kick)
        await ctx.followup.send(embed=kicked)

    @Jeanne.command(
        description="Bulk delete messages",
        extras={
            "bot_perms": "Manage Messages, Read Message History",
            "member_perms": "Manage Messages, Read Message History",
        },
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        limit="How many messages? (max is 100)",
        member="Which member's messages you want to delete?",
    )
    @Jeanne.checks.has_permissions(manage_messages=True, read_message_history=True)
    @Jeanne.checks.bot_has_permissions(manage_messages=True, read_message_history=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def prune(
        self,
        ctx: Interaction,
        limit: Optional[Jeanne.Range[int, None, 100]] = None,
        member: Optional[Member] = None,
    ) -> None:
        await ctx.response.defer()
        limit = (limit + 1) if limit else 101
        if member:

            def is_member(m: Message):
                return m.author == member

            await ctx.channel.purge(limit=limit, check=is_member)
            return
        await ctx.channel.purge(limit=limit)

    @Jeanne.command(
        name="change-nickname",
        description="Change someone's nickname",
        extras={"bot_perms": "Manage Nicknames", "member_perms": "Manage Nicknames"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Which member?", nickname="What is their new nickname")
    @Jeanne.checks.has_permissions(manage_nicknames=True)
    @Jeanne.checks.bot_has_permissions(manage_nicknames=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def changenickname(
        self,
        ctx: Interaction,
        member: Member,
        nickname: Optional[Jeanne.Range[str, 1, 32]],
    ):
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

    @Jeanne.command(
        description="Unbans a user",
        extras={"bot_perms": "Ban Members", "member_perms": "Ban Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        user_id="Which user do you want to unban?",
        reason="Why are they being unbanned?",
    )
    @Jeanne.autocomplete(user_id=AutoCompleteChoices.banned_users)
    @Jeanne.checks.has_permissions(ban_members=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: Interaction,
        user_id: str,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
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
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.followup.send(embed=unban)
            return

        unbanned = Embed(
            description=f"{user} has been unbanned. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=unbanned)
        await modlog.send(embed=unban)

    @unban.error
    async def unban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, NotFound
        ):
            embed = Embed()
            embed.color = Color.red()
            embed.description = str(error.original)
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Timeout a member",
        extras={"bot_perms": "Moderate Members", "member_perms": "Moderate Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        member="Which member?",
        time="How long should they be on timeout (1m, 1h30m, etc)",
        reason="Why are they on timeout?",
    )
    @Jeanne.checks.has_permissions(moderate_members=True)
    @Jeanne.checks.bot_has_permissions(moderate_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def timeout(
        self,
        ctx: Interaction,
        member: Member,
        time: Optional[str] = None,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        await ctx.response.defer()
        if member == ctx.user:
            failed = Embed(description="You can't time yourself out")
            await ctx.followup.send(embed=failed)
            return
        if member not in ctx.guild.members:
            failed = Embed(description="This person is not in this server")
            await ctx.followup.send(embed=failed)
            return
        reason = reason if reason else "Unspecified"
        if not time or (parse_timespan(time) > 2332800.0):
            time = 2332800.0
        timed = parse_timespan(str(time))
        await member.edit(
            timed_out_until=(datetime.now().astimezone() + timedelta(seconds=timed)),
            reason="{} | {}".format(reason, ctx.user),
        )
        mute = Embed(title="Member Timeout", color=0xFF0000)
        mute.add_field(name="Member", value=member, inline=True)
        mute.add_field(name="ID", value=member.id, inline=True)
        mute.add_field(name="Moderator", value=ctx.user, inline=True)
        mute.add_field(name="Duration", value=format_timespan(timed), inline=True)
        mute.add_field(name="Reason", value=reason, inline=False)
        mute.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.followup.send(embed=mute)
            return

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
            embed = Embed()
            embed.description = "Invalid time added. Please try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="timeout-remove",
        description="Removes a timeout from a member",
        extras={"bot_perms": "Moderate Members", "member_perms": "Moderate Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Which member?", reason="Why is their timeout removed?")
    @Jeanne.checks.has_permissions(moderate_members=True)
    @Jeanne.checks.bot_has_permissions(moderate_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def timeoutremove(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
    ) -> None:
        await ctx.response.defer()
        reason = reason if reason else "Unspecified"
        if member == ctx.user:
            failed = Embed(
                description="You can't untime yourself out", color=Color.red()
            )
            await ctx.followup.send(embed=failed)
            return
        if member.is_timed_out() == False:
            failed = Embed(
                description="This member is not on timeout", color=Color.red()
            )
            await ctx.followup.send(embed=failed)
            return
        await member.edit(
            timed_out_until=None, reason="{} | {}".format(reason, ctx.user)
        )
        unmute = Embed(title="User Untimeout", color=0xFF0000)
        unmute.add_field(name="User", value=member, inline=True)
        unmute.add_field(name="ID", value=member.id, inline=True)
        unmute.add_field(name="Moderator", value=ctx.user, inline=True)
        unmute.add_field(name="Reason", value=reason, inline=False)
        unmute.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog == None:
            await ctx.followup.send(embed=unmute)
            return

        unmuted = Embed(
            description=f"{member} has been untimeouted. Check {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=unmuted)
        await modlog.send(embed=unmute)

    @Jeanne.command(
        description="Ban multiple members at once",
        extras={"bot_perms": "Ban Members", "member_perms": "Ban Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        user_ids="How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
        reason="Why are they being banned?",
    )
    @Jeanne.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def massban(self, ctx: Interaction, user_ids: str, reason: str):
        await ctx.response.defer()
        ids_str = user_ids.split()[:100]
        ids=list(map(int, ids_str))
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
            and user_id != author_id
            and user_id != guild_owner_id
        ]
        if not to_ban_ids:
            embed = Embed(description="No users can be banned.", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        view = Confirmation(ctx.user)
        alert = Embed(
            title="Found users:",
            description="\n".join([f"{self.bot.get_user(i).global_name}" for i in to_ban_ids]),
            color=Color.red(),
        )
        alert.set_footer(text="BEWARE: The developer is **NOT** responsible in any way or form if you mess up, even if it was misused.\n\nDo you want to proceed?")
        await ctx.followup.send(embed=alert, view=view)
        await view.wait()
        if view.value == True:

            em = Embed(
                description="Banning users now <a:loading:1161038734620373062>",
                color=Color.red(),
            )
            to_ban: list[User] = []
            for i in to_ban_ids:
                try:
                    user = await self.bot.fetch_user(i)
                    to_ban.append(user)
                except:
                    continue
            await ctx.edit_original_response(embed=em, view=None)
            ban_results = await ctx.guild.bulk_ban(to_ban, reason=reason)

            if len(ban_results)> 0:
                embed = Embed(
                    title="List of banned users",
                    color=Color.red(),
                )
                banned_users=[]
                for i in ban_results.banned:
                    u=await self.bot.fetch_user(i.id)
                    banned_users.append(f"{u.global_name} | `{i.id}`")
                embed.description = "\n".join(banned_users)
                embed.add_field(name="Reason", value=reason, inline=False)
                if ban_results.failed:
                    failed_banned_users = []
                    for i in ban_results.failed:
                        u = await self.bot.fetch_user(i.id)
                        failed_banned_users.append(f"{u.global_name} | `{i.id}`")
                    embed.add_field(
                        name="Failed to ban",
                        value="\n".join(failed_banned_users),
                        inline=False,
                    )
            else:
                embed = Embed(description="No users were banned.", color=Color.red())
            modlog = Moderation(ctx.guild).get_modlog_channel
            if modlog == None:
                await ctx.edit_original_response(embed=embed)
                return

            await ctx.edit_original_response(
                embed=Embed(
                    description=f"Successfully banned {len(ban_results.banned)} user(s). Check {modlog.mention}",
                    color=Color.red(),
                )
            )
            await modlog.send(embed=embed)
        elif (view.value == False) or (view.value == None):
            cancelled = Embed(description="Massban cancelled", color=Color.red())
            await ctx.edit_original_response(embed=cancelled, view=None)

    @massban.error
    async def massban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"A massban command was already used here in this server.\nTry again after <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(
        description="Unban multiple members at once",
        extras={"bot_perms": "Ban Members", "member_perms": "Ban Members"},
    )
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(
        user_ids="How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
        reason="Why are they being banned?",
    )
    @Jeanne.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def massunban(self, ctx: Interaction, user_ids: str, reason: str):
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
                description="Unbanning users now <a:loading:1161038734620373062>",
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
                    await asyncio.sleep(0.5)
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
            modlog = Moderation(ctx.guild).get_modlog_channel
            if modlog == None:
                await ctx.edit_original_response(embed=embed)
                return

            await ctx.edit_original_response(
                embed=Embed(
                    description=f"Successfully unbanned {unban_count} user(s). Check {modlog.mention}",
                    color=Color.red(),
                )
            )
            await modlog.send(embed=embed)
        elif (view.value == False) or (view.value == None):
            cancelled = Embed(description="Massunban cancelled", color=Color.red())
            await ctx.edit_original_response(embed=cancelled, view=None)

    @massunban.error
    async def massunban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"A massunban command was already used here in this server.\nTry again after <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)


async def setup(bot: Bot):
    await bot.add_cog(moderation(bot))
