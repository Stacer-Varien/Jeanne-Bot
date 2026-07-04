from discord import Color, Embed, Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Bot, GroupCog
from discord.app_commands import locale_str as T
from functions import (
    Moderation,
    check_botbanned_app_command,
    get_command_locale,
    is_suspended,
)
import languages.en.serverops as en
import languages.fr.serverops as fr
import languages.de.serverops as de


def _language(ctx: Interaction):
    locale = get_command_locale(ctx)
    if locale == "fr":
        return fr
    if locale == "de":
        return de
    return en


async def has_moderation_permissions(ctx: Interaction):
    permissions = ctx.user.guild_permissions
    if any(
        (
            permissions.administrator,
            permissions.ban_members,
            permissions.kick_members,
            permissions.moderate_members,
            permissions.manage_messages,
            permissions.manage_guild,
        )
    ):
        return True
    raise Jeanne.MissingPermissions(["moderation permissions"])


class CaseGroup(GroupCog, name=T("case_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    async def _user_label(self, user_id: int | None) -> str:
        if user_id is None:
            return "Unknown"
        user = self.bot.get_user(int(user_id))
        if user is None:
            try:
                user = await self.bot.fetch_user(int(user_id))
            except Exception:
                user = None
        return f"{user} (`{user_id}`)" if user else f"`{user_id}`"

    @staticmethod
    def _case_line(case: tuple) -> str:
        target = f"<@{case[3]}>" if case[3] else "`Unknown`"
        moderator = f"<@{case[4]}>" if case[4] else "`Unknown`"
        return (
            f"`#{case[1]}` **{case[2]}** {target} by {moderator} "
            f"- <t:{case[6]}:R>"
        )

    @Jeanne.command(
        name=T("case_view_name"),
        description=T("case_view_desc"),
        extras={
            "en": {
                "name": "case view",
                "description": "View a moderation case by case ID",
                "member_perms": "Moderation permissions",
                "parameters": [
                    {"name": "case_id", "description": "Case ID to view", "required": True}
                ],
            },
            "fr": {
                "name": "dossier voir",
                "description": "Voir un dossier de modération par ID",
                "member_perms": "Permissions de modération",
                "parameters": [
                    {
                        "name": "case_id",
                        "description": "ID du dossier à voir",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "fall anzeigen",
                "description": "Einen Moderationsfall nach ID anzeigen",
                "member_perms": "Moderationsberechtigungen",
                "parameters": [
                    {
                        "name": "case_id",
                        "description": "Fall-ID zum Anzeigen",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.rename(case_id=T("case_id_param_name"))
    @Jeanne.describe(case_id=T("case_id_param_desc"))
    @Jeanne.guild_only()
    @Jeanne.check(has_moderation_permissions)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def view(self, ctx: Interaction, case_id: Jeanne.Range[int, 1]):
        await ctx.response.defer(ephemeral=True)
        language = _language(ctx)
        case = Moderation(ctx.guild).fetch_case(case_id)
        if case is None:
            await ctx.followup.send(
                embed=Embed(description=language.TEXT["case_not_found"], color=Color.red())
            )
            return
        target = await self._user_label(case[3])
        moderator = await self._user_label(case[4])
        await ctx.followup.send(embed=language.case_embed(case, target, moderator))

    @Jeanne.command(
        name=T("case_user_name"),
        description=T("case_user_desc"),
        extras={
            "en": {
                "name": "case user",
                "description": "View recent moderation cases for a member",
                "member_perms": "Moderation permissions",
                "parameters": [
                    {"name": "member", "description": "Member to inspect", "required": True},
                    {"name": "limit", "description": "Number of cases", "required": False},
                ],
            },
            "fr": {
                "name": "dossier utilisateur",
                "description": "Voir les dossiers récents d'un membre",
                "member_perms": "Permissions de modération",
                "parameters": [
                    {"name": "membre", "description": "Membre à vérifier", "required": True},
                    {"name": "limite", "description": "Nombre de dossiers", "required": False},
                ],
            },
            "de": {
                "name": "fall benutzer",
                "description": "Neue Moderationsfälle eines Mitglieds anzeigen",
                "member_perms": "Moderationsberechtigungen",
                "parameters": [
                    {
                        "name": "mitglied",
                        "description": "Mitglied zum Prüfen",
                        "required": True,
                    },
                    {"name": "limit", "description": "Anzahl der Fälle", "required": False},
                ],
            },
        },
    )
    @Jeanne.rename(member=T("member_parm_name"), limit=T("limit_param_name"))
    @Jeanne.describe(member=T("member_parm_desc"), limit=T("case_limit_param_desc"))
    @Jeanne.guild_only()
    @Jeanne.check(has_moderation_permissions)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def user(
        self,
        ctx: Interaction,
        member: Member,
        limit: Jeanne.Range[int, 1, 25] = 10,
    ):
        await ctx.response.defer(ephemeral=True)
        language = _language(ctx)
        cases = Moderation(ctx.guild).fetch_cases_user(member, limit)
        lines = [self._case_line(case) for case in cases]
        await ctx.followup.send(
            embed=language.case_list_embed(language.TEXT["case_user_title"], lines)
        )

    @Jeanne.command(
        name=T("case_recent_name"),
        description=T("case_recent_desc"),
        extras={
            "en": {
                "name": "case recent",
                "description": "View recent moderation cases in this server",
                "member_perms": "Moderation permissions",
                "parameters": [
                    {"name": "limit", "description": "Number of cases", "required": False}
                ],
            },
            "fr": {
                "name": "dossier récents",
                "description": "Voir les dossiers de modération récents de ce serveur",
                "member_perms": "Permissions de modération",
                "parameters": [
                    {"name": "limite", "description": "Nombre de dossiers", "required": False}
                ],
            },
            "de": {
                "name": "fall neu",
                "description": "Neue Moderationsfälle dieses Servers anzeigen",
                "member_perms": "Moderationsberechtigungen",
                "parameters": [
                    {"name": "limit", "description": "Anzahl der Fälle", "required": False}
                ],
            },
        },
    )
    @Jeanne.rename(limit=T("limit_param_name"))
    @Jeanne.describe(limit=T("case_limit_param_desc"))
    @Jeanne.guild_only()
    @Jeanne.check(has_moderation_permissions)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def recent(self, ctx: Interaction, limit: Jeanne.Range[int, 1, 25] = 10):
        await ctx.response.defer(ephemeral=True)
        language = _language(ctx)
        cases = Moderation(ctx.guild).fetch_recent_cases(limit)
        lines = [self._case_line(case) for case in cases]
        await ctx.followup.send(
            embed=language.case_list_embed(language.TEXT["case_recent_title"], lines)
        )


async def setup(bot: Bot):
    await bot.add_cog(CaseGroup(bot))
