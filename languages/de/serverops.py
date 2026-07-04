from discord import Color, Embed


DOCS_URL = "https://jeannebot.vercel.app/help"
SUPPORT_URL = "https://discord.gg/jh7jkuk2pp"

TEXT = {
    "setup_title": "Server-Einrichtung",
    "setup_description": "Privates Einrichtungspanel für diesen Server.",
    "status_channels": "Konfigurierte Kanäle",
    "status_language": "Sprache",
    "status_modules": "Module",
    "status_currency": "Währungsanzeige",
    "not_set": "Nicht gesetzt",
    "missing_channel": "Kanal fehlt",
    "auto_language": "Auto (Serversprache)",
    "disabled_none": "Keine Module deaktiviert",
    "area_placeholder": "Wähle aus, welchen Kanal du konfigurieren willst",
    "channel_placeholder": "Wähle den Kanal aus",
    "language_placeholder": "Wähle eine Serversprache",
    "module_placeholder": "Modul aktivieren oder deaktivieren",
    "currency_button": "Währung",
    "refresh_button": "Aktualisieren",
    "unauthorized": "Nur die Person, die dieses Panel geöffnet hat, kann es benutzen.",
    "select_area_first": "Wähle zuerst einen Bereich und danach den Kanal.",
    "updated": "Einstellung aktualisiert.",
    "currency_modal_title": "Währungsanzeige",
    "currency_name_label": "Währungsname",
    "currency_emoji_label": "Währungs-Emoji",
    "diagnose_title": "Server-Diagnose",
    "diagnose_description": "Betriebschecks für Jeanne in diesem Server.",
    "bot_permissions": "Bot-Berechtigungen",
    "member_permissions": "Deine Berechtigungen",
    "channel_health": "Kanalstatus",
    "role_hierarchy": "Rollenhierarchie",
    "configured_channels": "Status konfigurierter Kanäle",
    "settings": "Server-Einstellungen",
    "intents": "Gateway-Intents",
    "case_not_found": "Ich konnte diesen Moderationsfall nicht finden.",
    "case_no_cases": "Keine Moderationsfälle gefunden.",
    "case_view_title": "Moderationsfall",
    "case_recent_title": "Neue Moderationsfälle",
    "case_user_title": "Moderationsfälle für Benutzer",
    "target": "Ziel",
    "moderator": "Moderator",
    "reason": "Grund",
    "duration": "Dauer",
    "status": "Status",
    "warn_id": "Warn-ID",
    "date": "Datum",
}

AREA_LABELS = {
    "welcome": "Willkommen",
    "leave": "Verlassen",
    "modlog": "Modlog",
    "level": "Level",
    "confession": "Beichten",
}

LANGUAGE_LABELS = {
    "auto": "Auto",
    "en": "Englisch",
    "fr": "Französisch",
    "de": "Deutsch",
}


def channel_status(state: dict) -> str:
    if state["channel"]:
        return state["channel"].mention
    if state["missing"]:
        return f"{TEXT['missing_channel']} `{state['channel_id']}`"
    return TEXT["not_set"]


def setup_embed(guild, settings, status: dict) -> Embed:
    embed = Embed(
        title=TEXT["setup_title"],
        description=TEXT["setup_description"],
        color=Color.blurple(),
    )
    embed.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)
    embed.add_field(
        name=TEXT["status_channels"],
        value="\n".join(
            f"**{AREA_LABELS[key]}:** {channel_status(status[key])}"
            for key in ("welcome", "leave", "modlog", "level", "confession")
        ),
        inline=False,
    )
    language = status["language_override"]
    embed.add_field(
        name=TEXT["status_language"],
        value=TEXT["auto_language"] if language == "auto" else LANGUAGE_LABELS[language],
        inline=True,
    )
    disabled = status["disabled_modules"]
    embed.add_field(
        name=TEXT["status_modules"],
        value=(
            TEXT["disabled_none"]
            if not disabled
            else ", ".join(settings.MODULES[module] for module in disabled)
        ),
        inline=True,
    )
    currency_value = settings.format_currency(1).replace("1 ", "", 1)
    embed.add_field(name=TEXT["status_currency"], value=currency_value, inline=True)
    return embed


def diagnose_embed(guild, report: dict) -> Embed:
    embed = Embed(
        title=TEXT["diagnose_title"],
        description=TEXT["diagnose_description"],
        color=Color.blurple(),
    )
    embed.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)
    for key in (
        "bot_permissions",
        "member_permissions",
        "channel_health",
        "role_hierarchy",
        "configured_channels",
        "settings",
        "intents",
    ):
        embed.add_field(
            name=TEXT[key],
            value="\n".join(report[key])[:1024] or "OK",
            inline=False,
        )
    return embed


def case_embed(case: tuple, target: str, moderator: str) -> Embed:
    embed = Embed(title=f"{TEXT['case_view_title']} #{case[1]}", color=Color.red())
    embed.add_field(name="Aktion", value=str(case[2]).title(), inline=True)
    embed.add_field(name=TEXT["target"], value=target, inline=True)
    embed.add_field(name=TEXT["moderator"], value=moderator, inline=True)
    embed.add_field(name=TEXT["reason"], value=case[5] or "Nicht angegeben", inline=False)
    embed.add_field(name=TEXT["date"], value=f"<t:{case[6]}:F>", inline=True)
    embed.add_field(name=TEXT["status"], value=case[8] or "aktiv", inline=True)
    if case[7]:
        embed.add_field(name=TEXT["duration"], value=case[7], inline=True)
    if case[9] is not None:
        embed.add_field(name=TEXT["warn_id"], value=str(case[9]), inline=True)
    return embed


def case_list_embed(title: str, lines: list[str]) -> Embed:
    if not lines:
        return Embed(description=TEXT["case_no_cases"], color=Color.red())
    return Embed(title=title, description="\n".join(lines)[:4096], color=Color.red())
