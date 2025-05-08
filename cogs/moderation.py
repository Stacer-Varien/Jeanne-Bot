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
from discord.app_commands import locale_str as T
import languages.en.moderation as en
import languages.fr.moderation as fr


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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).commit_ban(
                ctx, member, reason, time, delete_message_history
            )
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).commit_ban(
                ctx, member, reason, time, delete_message_history
            )

    async def check_banned(self, ctx: Interaction, member: User):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).check_banned(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).check_banned(ctx, member)

    @Jeanne.command(
        name=T("ban_name"),
        description=T("ban_desc"),
        extras={"bot_perms": "Ban Members", "member_perms": "Ban Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.autocomplete(reason=AutoCompleteChoices.default_ban_options)
    @Jeanne.describe(
        member=T("member_param_desc"),
        reason=T("reason_param_desc"),
        delete_message_history=T("delete_message_history_param_desc"),
        time=T("time_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        reason=T("reason_param_name"),
        delete_message_history=T("delete_message_history_param_name"),
        time=T("time_param_name"),
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).ban(
                ctx, member, reason, delete_message_history, time
            )
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).ban(
                ctx, member, reason, delete_message_history, time
            )

    @ban.error
    async def ban_user_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (HTTPException, ValueError)
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.moderation(self.bot).ban_user_error(ctx)
            elif ctx.locale.value == "fr":
                await fr.moderation(self.bot).ban_user_error(ctx)

    @Jeanne.command(
        name=T("warn_name"),
        description=T("warn_desc"),
        extras={"bot_perms": "Kick Members", "member_perms": "Kick Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        reason=T("reason_param_name"),
    )
    @Jeanne.checks.has_permissions(kick_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def warn(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[Jeanne.Range[str, None, 512]] = None,
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).warn(ctx, member, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).warn(ctx, member, reason)

    @Jeanne.command(
        name=T("list_warns_name"),
        description=T("list_warns_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
    )
    @Jeanne.autocomplete(member=AutoCompleteChoices.warned_users)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def listwarns(self, ctx: Interaction, member: Optional[str]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).listwarns(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).listwarns(ctx, member)

    @listwarns.error
    async def listwarns_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (ValueError, AttributeError)
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.moderation(self.bot).listwarns_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.moderation(self.bot).listwarns_error(ctx, error)

    @Jeanne.command(
        name=T("clear_warn_name"),
        description=T("clear_warn_desc"),
        extras={"bot_perms": "Kick Members", "member_perms": "Kick Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
        warn_id=T("warn_id_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        warn_id=T("warn_id_param_name"),
    )
    @Jeanne.checks.has_permissions(kick_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def clearwarn(self, ctx: Interaction, member: Member, warn_id: int):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).clearwarn(ctx, member, warn_id)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).clearwarn(ctx, member, warn_id)

    @Jeanne.command(
        name=T("kick_name"),
        description=T("kick_desc"),
        extras={"bot_perms": "Kick Members", "member_perms": "Kick Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        reason=T("reason_param_name"),
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).kick(ctx, member, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).kick(ctx, member, reason)

    @Jeanne.command(
        name=T("prune_name"),
        description=T("prune_desc"),
        extras={
            "bot_perms": "Manage Messages, Read Message History",
            "member_perms": "Manage Messages, Read Message History",
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        limit=T("limit_param_desc"),
        member=T("member_param_desc"),
    )
    @Jeanne.rename(
        limit=T("limit_param_name"),
        member=T("member_param_name"),
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).prune(ctx, limit, member)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).prune(ctx, limit, member)

    @Jeanne.command(
        name=T("change_nickname_name"),
        description=T("change_nickname_desc"),
        extras={"bot_perms": "Manage Nicknames", "member_perms": "Manage Nicknames"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
        nickname=T("nickname_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        nickname=T("nickname_param_name"),
    )
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).changenickname(ctx, member, nickname)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).changenickname(ctx, member, nickname)

    @Jeanne.command(
        name=T("unban_name"),
        description=T("unban_desc"),
        extras={"bot_perms": "Ban Members", "member_perms": "Ban Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        user_id=T("user_id_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        user_id=T("user_id_param_name"),
        reason=T("reason_param_name"),
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).unban(ctx, user_id, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).unban(ctx, user_id, reason)

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
        name=T("timeout_name"),
        description=T("timeout_desc"),
        extras={"bot_perms": "Moderate Members", "member_perms": "Moderate Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
        time=T("time_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        time=T("time_param_name"),
        reason=T("reason_param_name"),
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).timeout(ctx, member, time, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).timeout(ctx, member, time, reason)

    @timeout.error
    async def timeout_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, InvalidTimespan
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.moderation(self.bot).timeout_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.moderation(self.bot).timeout_error(ctx, error)

    @Jeanne.command(
        name=T("timeout_remove_name"),
        description=T("timeout_remove_desc"),
        extras={"bot_perms": "Moderate Members", "member_perms": "Moderate Members"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        reason=T("reason_param_name"),
    )
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).timeoutremove(ctx, member, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).timeoutremove(ctx, member, reason)

    @Jeanne.command(
        name=T("massban_name"),
        description=T("massban_desc"),
        extras={"bot_perms": "Ban Members", "member_perms": "Administrator"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        user_ids=T("user_ids_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        user_ids=T("user_ids_param_name"),
        reason=T("reason_param_name"),
    )
    @Jeanne.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def massban(self, ctx: Interaction, user_ids: str, reason: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).massban(ctx, user_ids, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).massban(ctx, user_ids, reason)

    @massban.error
    async def massban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.moderation(self.bot).massban_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.moderation(self.bot).massban_error(ctx, error)

    @Jeanne.command(
        name=T("massunban_name"),
        description=T("massunban_desc"),
        extras={"bot_perms": "Ban Members", "member_perms": "Administrator"},
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        user_ids=T("user_ids_param_desc"),
        reason=T("reason_param_desc"),
    )
    @Jeanne.rename(
        user_ids=T("user_ids_param_name"),
        reason=T("reason_param_name"),
    )
    @Jeanne.checks.cooldown(1, 1800, key=lambda i: (i.guild.id))
    @Jeanne.checks.bot_has_permissions(ban_members=True)
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def massunban(self, ctx: Interaction, user_ids: str, reason: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.moderation(self.bot).massunban(ctx, user_ids, reason)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).massunban(ctx, user_ids, reason)

    @massunban.error
    async def massunban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.moderation(self.bot).massunban_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.moderation(self.bot).massunban_error(ctx, error)


async def setup(bot: Bot):
    await bot.add_cog(moderation(bot))
