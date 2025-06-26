from discord import (
    Color,
    Embed,
    HTTPException,
    Interaction,
    User,
    NotFound,
    Member,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot
from humanfriendly import InvalidTimespan
from functions import (
    AutoCompleteChoices,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
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
        extras={
            "en": {
                "name": "ban",
                "description": "Ban someone from or outside the server",
                "bot_perms": "Ban Members",
                "member_perms": "Ban Members",
                "parameters": [
                    {
                        "name": "member",
                        "description": "What is the member or user ID?",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": False,
                    },
                    {
                        "name": "delete_message_history",
                        "description": "Delete messages from past 7 days?",
                        "required": False,
                    },
                    {
                        "name": "time",
                        "description": "How long should they be tempbanned? (1m, 1h30m, etc)",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "ban",
                "description": "Bannir quelqu'un du serveur ou en dehors",
                "bot_perms": "Bannir des membres",
                "member_perms": "Bannir des membres",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel est le membre ou l'identifiant utilisateur ?",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Qu'a-t-il fait? Vous pouvez aussi donner une raison personnalisée",
                        "required": False,
                    },
                    {
                        "name": "supprimer_historique_messages",
                        "description": "Supprimer les messages des 7 derniers jours ?",
                        "required": False,
                    },
                    {
                        "name": "temps",
                        "description": "Combien de temps doivent-ils être temporairement bannis ? (1m, 1h30m, etc)",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.autocomplete(reason=AutoCompleteChoices.default_ban_options)
    @Jeanne.describe(
        member=T("member_param_desc"),
        reason=T("reason_param_desc"),
        delete_message_history=T("delete_msg_history_param_desc"),
        time=T("time_param_desc"),
    )
    @Jeanne.rename(
        member=T("member_param_name"),
        reason=T("reason_param_name"),
        delete_message_history=T("delete_msg_history_param_name"),
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
        reason: Optional[Jeanne.Range[str, None, 470]] = None,
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
        extras={
            "en": {
                "name": "warn",
                "description": "Warn a member",
                "bot_perms": "Kick Members",
                "member_perms": "Kick Members",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "avertir",
                "description": "Avertir un membre",
                "bot_perms": "Expulser des membres",
                "member_perms": "Expulser des membres",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Qu'a-t-il fait ? Vous pouvez aussi donner une raison personnalisée",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc_fr"),
        reason=T("reason_param_desc_fr"),
    )
    @Jeanne.rename(
        member=T("member_param_name_fr"),
        reason=T("reason_param_name_fr"),
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
        extras={
            "en": {
                "name": "list-warns",
                "description": "View warnings in the server or a member",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "liste-avertissements",
                "description": "View warnings in the server or a member",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre?",
                        "required": False,
                    },
                ],
            },
        },
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
        extras={
            "en": {
                "name": "clear-warn",
                "description": "Revoke a warn by warn ID",
                "bot_perms": "Kick Members",
                "member_perms": "Kick Members",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": True,
                    },
                    {
                        "name": "warn_id",
                        "description": "What is the warning ID you want to remove?",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "clear-warn",
                "description": "Révoquer un avertissement par ID d'avertissement",
                "bot_perms": "Expulser des membres",
                "member_perms": "Expulser des membres",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": True,
                    },
                    {
                        "name": "warn_id",
                        "description": "Quel est l'ID d'avertissement que vous souhaitez supprimer ?",
                        "required": True,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc_fr"),
        warn_id=T("warn_id_param_desc_fr"),
    )
    @Jeanne.rename(
        member=T("member_param_name_fr"),
        warn_id=T("warn_id_param_name_fr"),
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
        extras={
            "en": {
                "name": "kick",
                "description": "Kick a member out of the server",
                "bot_perms": "Kick Members",
                "member_perms": "Kick Members",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "expulser",
                "description": "Expulser un membre du serveur",
                "bot_perms": "Expulser des membres",
                "member_perms": "Expulser des membres",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Qu'a-t-il fait ? Vous pouvez aussi donner une raison personnalisée",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc_fr"),
        reason=T("reason_param_desc_fr"),
    )
    @Jeanne.rename(
        member=T("member_param_name_fr"),
        reason=T("reason_param_name_fr"),
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
            "en": {
                "name": "prune",
                "description": "Bulk delete messages",
                "bot_perms": "Manage Messages, Read Message History",
                "member_perms": "Manage Messages, Read Message History",
                "parameters": [
                    {
                        "name": "limit",
                        "description": "How many messages? (max is 100)",
                        "required": False,
                    },
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "purger",
                "description": "Supprimer en masse des messages",
                "bot_perms": "Gérer les messages, Lire l'historique des messages",
                "member_perms": "Gérer les messages, Lire l'historique des messages",
                "parameters": [
                    {
                        "name": "limite",
                        "description": "Combien de messages ? (max est 100)",
                        "required": False,
                    },
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        limit=T("limit_param_desc_fr"),
        member=T("member_param_desc_fr"),
    )
    @Jeanne.rename(
        limit=T("limit_param_name_fr"),
        member=T("member_param_name_fr"),
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
        extras={
            "en": {
                "name": "change-nickname",
                "description": "Change someone's nickname",
                "bot_perms": "Manage Nicknames",
                "member_perms": "Manage Nicknames",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    },
                    {
                        "name": "nickname",
                        "description": "What is their new nickname?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "changer-pseudo",
                "description": "Changer le pseudo de quelqu'un",
                "bot_perms": "Gérer les pseudos",
                "member_perms": "Gérer les pseudos",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": False,
                    },
                    {
                        "name": "pseudo",
                        "description": "Quel est son nouveau pseudo ?",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc_fr"),
        nickname=T("nickname_param_desc_fr"),
    )
    @Jeanne.rename(
        member=T("member_param_name_fr"),
        nickname=T("nickname_param_name_fr"),
    )
    @Jeanne.checks.has_permissions(manage_nicknames=True)
    @Jeanne.checks.bot_has_permissions(manage_nicknames=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def changenickname(
        self,
        ctx: Interaction,
        member: Member,
        nickname: Optional[Jeanne.Range[str, 1, 32]] = None,
    ):
        if ctx.locale.value == "fr":
            await fr.moderation(self.bot).changenickname(ctx, member, nickname)
        else:
            await en.moderation(self.bot).changenickname(ctx, member, nickname)

    @Jeanne.command(
        name=T("unban_name"),
        description=T("unban_desc"),
        extras={
            "en": {
                "name": "unban",
                "description": "Unbans a user",
                "bot_perms": "Ban Members",
                "member_perms": "Ban Members",
                "parameters": [
                    {
                        "name": "user_id",
                        "description": "Which user do you want to unban?",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "déban",
                "description": "Débannir un utilisateur",
                "bot_perms": "Bannir des membres",
                "member_perms": "Bannir des membres",
                "parameters": [
                    {
                        "name": "utilisateur_id",
                        "description": "Quel utilisateur souhaitez-vous débannir ?",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Qu'a-t-il fait ? Vous pouvez aussi donner une raison personnalisée",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        user_id=T("user_id_param_desc"),
        reason=T("unban_reason_parm"),
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
        extras={
            "en": {
                "name": "timeout",
                "description": "Timeout a member",
                "bot_perms": "Moderate Members",
                "member_perms": "Moderate Members",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": True,
                    },
                    {
                        "name": "time",
                        "description": "How long should they be on timeout? (1m, 1h30m, etc)",
                        "required": False,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "délai",
                "description": "Mettre un membre en sourdine",
                "bot_perms": "Modérer les membres",
                "member_perms": "Modérer les membres",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": True,
                    },
                    {
                        "name": "temps",
                        "description": "Combien de temps doivent-ils être en sourdine ? (1m, 1h30m, etc)",
                        "required": False,
                    },
                    {
                        "name": "raison",
                        "description": "Qu'a-t-il fait? Vous pouvez aussi donner une raison personnalisée",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc_fr"),
        time=T("timeout_time_desc"),
        reason=T("reason_param_desc_fr"),
    )
    @Jeanne.rename(
        member=T("member_param_name_fr"),
        time=T("time_param_name_fr"),
        reason=T("reason_param_name_fr"),
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
        extras={
            "en": {
                "name": "timeout-remove",
                "description": "Removes a member from timeout",
                "bot_perms": "Moderate Members",
                "member_perms": "Moderate Members",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "retirer-sourdine",
                "description": "Retirer un membre du délai d'attente",
                "bot_perms": "Modérer les membres",
                "member_perms": "Modérer les membres",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre ?",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Pourquoi les retirer du délai d'attente ?",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(
        member=T("member_param_desc_fr"),
        reason=T("timeout_remove_reason_desc_fr"),
    )
    @Jeanne.rename(
        member=T("member_param_name_fr"),
        reason=T("reason_param_name_fr"),
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
        extras={
            "en": {
                "name": "massban",
                "description": "Ban multiple members at once",
                "bot_perms": "Ban Members",
                "member_perms": "Administrator",
                "parameters": [
                    {
                        "name": "user_ids",
                        "description": "How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "massban",
                "description": "Bannir plusieurs membres à la fois",
                "parameters": [
                    {
                        "name": "user_ids",
                        "description": "Combien d'IDs utilisateur? Laissez un espace après chaque ID (min est 5 et max est 25)",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Pourquoi les retirer du délai d'attente?",
                        "required": True,
                    },
                ],
            },
        },
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
        extras={
            "en": {
                "name": "massunban",
                "description": "Unban multiple users at once",
                "bot_perms": "Ban Members",
                "member_perms": "Administrator",
                "parameters": [
                    {
                        "name": "user_ids",
                        "description": "How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "What did they do? You can also make a custom reason",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "massunban",
                "description": "Débannir plusieurs membres à la fois",
                "bot_perms": "Bannir des membres",
                "member_perms": "Administrateur",
                "parameters": [
                    {
                        "name": "user_ids",
                        "description": "Combien d'IDs utilisateur ? Laissez un espace après chaque ID (min est 5 et max est 25)",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Pourquoi les débannir ? Vous pouvez aussi donner une raison personnalisée",
                        "required": True,
                    },
                ],
            },
        },
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
