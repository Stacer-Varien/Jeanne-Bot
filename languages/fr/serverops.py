from discord import Color, Embed


DOCS_URL = "https://jeannebot.vercel.app/help"
SUPPORT_URL = "https://discord.gg/jh7jkuk2pp"

TEXT = {
    "setup_title": "Configuration du serveur",
    "setup_description": "Panneau privé de configuration pour ce serveur.",
    "status_channels": "Canaux configurés",
    "status_language": "Langue",
    "status_modules": "Modules",
    "status_currency": "Affichage de la monnaie",
    "not_set": "Non défini",
    "missing_channel": "Canal manquant",
    "auto_language": "Auto (langue du serveur)",
    "disabled_none": "Aucun module désactivé",
    "area_placeholder": "Choisissez le canal à configurer",
    "channel_placeholder": "Choisissez le canal à utiliser",
    "language_placeholder": "Choisissez une langue serveur",
    "module_placeholder": "Activer ou désactiver un module",
    "currency_button": "Monnaie",
    "refresh_button": "Actualiser",
    "unauthorized": "Seule la personne qui a ouvert ce panneau peut l'utiliser.",
    "select_area_first": "Choisissez d'abord une zone, puis choisissez le canal.",
    "updated": "Paramètre mis à jour.",
    "currency_modal_title": "Affichage de la monnaie",
    "currency_name_label": "Nom de la monnaie",
    "currency_emoji_label": "Emoji de la monnaie",
    "diagnose_title": "Diagnostic du serveur",
    "diagnose_description": "Vérifications opérationnelles pour Jeanne dans ce serveur.",
    "bot_permissions": "Permissions du bot",
    "member_permissions": "Vos permissions",
    "channel_health": "État du canal",
    "role_hierarchy": "Hiérarchie des rôles",
    "configured_channels": "État des canaux configurés",
    "settings": "Paramètres du serveur",
    "intents": "Intents Gateway",
    "case_not_found": "Je n'ai pas trouvé ce dossier de modération.",
    "case_no_cases": "Aucun dossier de modération trouvé.",
    "case_view_title": "Dossier de modération",
    "case_recent_title": "Dossiers de modération récents",
    "case_user_title": "Dossiers de modération utilisateur",
    "target": "Cible",
    "moderator": "Modérateur",
    "reason": "Raison",
    "duration": "Durée",
    "status": "Statut",
    "warn_id": "ID d'avertissement",
    "date": "Date",
}

AREA_LABELS = {
    "welcome": "Bienvenue",
    "leave": "Départs",
    "modlog": "Modlog",
    "level": "Niveaux",
    "confession": "Confessions",
}

LANGUAGE_LABELS = {
    "auto": "Auto",
    "en": "Anglais",
    "fr": "Français",
    "de": "Allemand",
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
    embed.add_field(name="Action", value=str(case[2]).title(), inline=True)
    embed.add_field(name=TEXT["target"], value=target, inline=True)
    embed.add_field(name=TEXT["moderator"], value=moderator, inline=True)
    embed.add_field(name=TEXT["reason"], value=case[5] or "Non spécifiée", inline=False)
    embed.add_field(name=TEXT["date"], value=f"<t:{case[6]}:F>", inline=True)
    embed.add_field(name=TEXT["status"], value=case[8] or "actif", inline=True)
    if case[7]:
        embed.add_field(name=TEXT["duration"], value=case[7], inline=True)
    if case[9] is not None:
        embed.add_field(name=TEXT["warn_id"], value=str(case[9]), inline=True)
    return embed


def case_list_embed(title: str, lines: list[str]) -> Embed:
    if not lines:
        return Embed(description=TEXT["case_no_cases"], color=Color.red())
    return Embed(title=title, description="\n".join(lines)[:4096], color=Color.red())
