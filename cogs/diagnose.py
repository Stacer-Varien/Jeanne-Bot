from discord import Interaction, TextChannel, app_commands as Jeanne
from discord.ext.commands import Bot, Cog
from discord.app_commands import locale_str as T
from functions import (
    ServerSettings,
    check_botbanned_app_command,
    get_command_locale,
    is_suspended,
)
import languages.en.serverops as en
import languages.fr.serverops as fr
import languages.de.serverops as de


PERMISSION_LABELS = {
    "view_channel": "View Channels",
    "send_messages": "Send Messages",
    "embed_links": "Embed Links",
    "read_message_history": "Read Message History",
    "manage_messages": "Manage Messages",
    "manage_roles": "Manage Roles",
    "manage_channels": "Manage Channels",
    "kick_members": "Kick Members",
    "ban_members": "Ban Members",
    "moderate_members": "Moderate Members",
    "manage_guild": "Manage Server",
}

CORE_BOT_PERMISSIONS = (
    "view_channel",
    "send_messages",
    "embed_links",
    "read_message_history",
)

MODERATION_BOT_PERMISSIONS = (
    "manage_messages",
    "kick_members",
    "ban_members",
    "moderate_members",
)

LOCALE_WORDS = {
    "en": {
        "ok": "OK",
        "missing": "Missing",
        "enabled": "Enabled",
        "disabled": "Disabled",
        "none": "None",
        "needs": "Needs attention",
        "can_configure": "You can configure server settings.",
        "limited_moderation": "You do not have ban, kick, moderate, or manage-message permissions.",
        "bot_top_role": "Bot top role",
        "your_top_role": "Your top role",
        "role_risk": "Members at or above Jeanne's top role cannot be moderated by Jeanne.",
        "role_ok": "Jeanne's top role is above every non-owner member.",
        "language": "Language override",
        "currency": "Currency display",
        "disabled_modules": "Disabled modules",
        "channel_current": "Current channel",
        "members_intent": "Members intent",
        "message_content_intent": "Message content intent",
        "guilds_intent": "Guilds intent",
        "guild_messages_intent": "Guild messages intent",
    },
    "fr": {
        "ok": "OK",
        "missing": "Manquant",
        "enabled": "Activé",
        "disabled": "Désactivé",
        "none": "Aucun",
        "needs": "À vérifier",
        "can_configure": "Vous pouvez configurer les paramètres du serveur.",
        "limited_moderation": "Vous n'avez pas les permissions bannir, expulser, modérer ou gérer les messages.",
        "bot_top_role": "Rôle le plus haut du bot",
        "your_top_role": "Votre rôle le plus haut",
        "role_risk": "Les membres au niveau ou au-dessus du rôle de Jeanne ne peuvent pas être modérés par Jeanne.",
        "role_ok": "Le rôle de Jeanne est au-dessus de tous les membres non propriétaires.",
        "language": "Langue forcée",
        "currency": "Affichage de la monnaie",
        "disabled_modules": "Modules désactivés",
        "channel_current": "Canal actuel",
        "members_intent": "Intent membres",
        "message_content_intent": "Intent contenu des messages",
        "guilds_intent": "Intent serveurs",
        "guild_messages_intent": "Intent messages serveur",
    },
    "de": {
        "ok": "OK",
        "missing": "Fehlt",
        "enabled": "Aktiviert",
        "disabled": "Deaktiviert",
        "none": "Keine",
        "needs": "Prüfen",
        "can_configure": "Du kannst Server-Einstellungen konfigurieren.",
        "limited_moderation": "Dir fehlen Bann-, Kick-, Moderations- oder Nachrichtenverwaltungsrechte.",
        "bot_top_role": "Höchste Bot-Rolle",
        "your_top_role": "Deine höchste Rolle",
        "role_risk": "Mitglieder auf oder über Jeannes höchster Rolle können von Jeanne nicht moderiert werden.",
        "role_ok": "Jeannes höchste Rolle liegt über allen Nicht-Owner-Mitgliedern.",
        "language": "Sprach-Override",
        "currency": "Währungsanzeige",
        "disabled_modules": "Deaktivierte Module",
        "channel_current": "Aktueller Kanal",
        "members_intent": "Mitglieder-Intent",
        "message_content_intent": "Nachrichteninhalt-Intent",
        "guilds_intent": "Server-Intent",
        "guild_messages_intent": "Servernachrichten-Intent",
    },
}


def _language(ctx: Interaction):
    locale = get_command_locale(ctx)
    if locale == "fr":
        return fr
    if locale == "de":
        return de
    return en


def _words(ctx: Interaction) -> dict:
    return LOCALE_WORDS[get_command_locale(ctx)]


def _missing_permissions(permissions, names: tuple[str, ...]) -> list[str]:
    return [
        PERMISSION_LABELS[name]
        for name in names
        if not getattr(permissions, name, False)
    ]


def _state(words: dict, enabled: bool) -> str:
    return words["enabled"] if enabled else words["disabled"]


class DiagnoseCog(Cog, name="DiagnoseSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _channel_line(words: dict, label: str, channel: TextChannel, bot_member) -> str:
        permissions = channel.permissions_for(bot_member)
        missing = _missing_permissions(permissions, CORE_BOT_PERMISSIONS)
        if missing:
            return f"**{label}:** {words['missing']} {', '.join(missing)}"
        return f"**{label}:** {words['ok']}"

    def _build_report(self, ctx: Interaction) -> dict:
        words = _words(ctx)
        guild = ctx.guild
        settings = ServerSettings(guild)
        status = settings.setup_status(guild)
        bot_member = guild.me or guild.get_member(self.bot.user.id)
        report = {
            "bot_permissions": [],
            "member_permissions": [],
            "channel_health": [],
            "role_hierarchy": [],
            "configured_channels": [],
            "settings": [],
            "intents": [],
        }

        bot_perms = bot_member.guild_permissions
        core_missing = _missing_permissions(bot_perms, CORE_BOT_PERMISSIONS)
        mod_missing = _missing_permissions(bot_perms, MODERATION_BOT_PERMISSIONS)
        report["bot_permissions"].append(
            f"{words['ok']}: {', '.join(PERMISSION_LABELS[name] for name in CORE_BOT_PERMISSIONS)}"
            if not core_missing
            else f"{words['missing']}: {', '.join(core_missing)}"
        )
        if mod_missing:
            report["bot_permissions"].append(
                f"{words['needs']}: {', '.join(mod_missing)}"
            )

        user_perms = ctx.user.guild_permissions
        if user_perms.manage_guild:
            report["member_permissions"].append(words["can_configure"])
        if not any(
            (
                user_perms.ban_members,
                user_perms.kick_members,
                user_perms.moderate_members,
                user_perms.manage_messages,
            )
        ):
            report["member_permissions"].append(words["limited_moderation"])

        if isinstance(ctx.channel, TextChannel):
            report["channel_health"].append(
                self._channel_line(
                    words, words["channel_current"], ctx.channel, bot_member
                )
            )

        blocked_members = [
            member
            for member in guild.members
            if not member.bot
            and member != guild.owner
            and member.top_role >= bot_member.top_role
        ]
        report["role_hierarchy"].append(f"{words['bot_top_role']}: {bot_member.top_role}")
        report["role_hierarchy"].append(f"{words['your_top_role']}: {ctx.user.top_role}")
        if blocked_members:
            report["role_hierarchy"].append(
                f"{words['needs']}: {len(blocked_members)} member(s). {words['role_risk']}"
            )
        else:
            report["role_hierarchy"].append(words["role_ok"])

        for key in ("welcome", "leave", "modlog", "level", "confession"):
            state = status[key]
            label = getattr(_language(ctx), "AREA_LABELS")[key]
            channel = state["channel"]
            if channel:
                report["configured_channels"].append(
                    self._channel_line(words, label, channel, bot_member)
                )
            elif state["missing"]:
                report["configured_channels"].append(
                    f"**{label}:** {words['missing']} `{state['channel_id']}`"
                )
            else:
                report["configured_channels"].append(
                    f"**{label}:** {words['none']}"
                )

        language = status["language_override"]
        report["settings"].append(f"{words['language']}: {language}")
        report["settings"].append(
            f"{words['currency']}: {settings.format_currency(1).replace('1 ', '', 1)}"
        )
        disabled_modules = status["disabled_modules"]
        report["settings"].append(
            f"{words['disabled_modules']}: "
            + (
                words["none"]
                if not disabled_modules
                else ", ".join(ServerSettings.MODULES[module] for module in disabled_modules)
            )
        )

        intents = self.bot.intents
        report["intents"].append(
            f"{words['guilds_intent']}: {_state(words, intents.guilds)}"
        )
        report["intents"].append(
            f"{words['guild_messages_intent']}: {_state(words, intents.guild_messages)}"
        )
        report["intents"].append(
            f"{words['members_intent']}: {_state(words, intents.members)}"
        )
        report["intents"].append(
            f"{words['message_content_intent']}: {_state(words, intents.message_content)}"
        )
        return report

    @Jeanne.command(
        name=T("diagnose_name"),
        description=T("diagnose_desc"),
        extras={
            "en": {
                "name": "diagnose",
                "description": "Check Jeanne's server setup, permissions, channels, and intents",
                "member_perms": "Manage Server",
            },
            "fr": {
                "name": "diagnostic",
                "description": "Vérifier la configuration, les permissions, les canaux et les intents de Jeanne",
                "member_perms": "Gérer le serveur",
            },
            "de": {
                "name": "diagnose",
                "description": "Jeannes Server-Einrichtung, Berechtigungen, Kanäle und Intents prüfen",
                "member_perms": "Server verwalten",
            },
        },
    )
    @Jeanne.guild_only()
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def diagnose(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        language = _language(ctx)
        report = self._build_report(ctx)
        await ctx.followup.send(embed=language.diagnose_embed(ctx.guild, report))


async def setup(bot: Bot):
    await bot.add_cog(DiagnoseCog(bot))
