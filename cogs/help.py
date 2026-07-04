from discord import (
    Color,
    Embed,
    Interaction,
    app_commands as Jeanne,
)
from discord.ext.commands import GroupCog, Bot
from functions import (
    AutoCompleteChoices,
    check_botbanned_app_command,
    get_command_locale,
    is_suspended,
)
import languages.en.help as en
import languages.fr.help as fr
import languages.de.help as de
from discord.app_commands import locale_str as T
from difflib import SequenceMatcher
import re
import unicodedata


class HelpGroup(GroupCog, name=T("help_group_name")):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _normalize_text(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value).encode(
            "ascii", "ignore"
        ).decode("ascii")
        normalized = normalized.lower().replace("/", " ").replace("-", " ")
        normalized = re.sub(r"[^a-z0-9_ ]+", " ", normalized)
        return re.sub(r"\s+", " ", normalized).strip()

    @classmethod
    def _tokenize(cls, value: str) -> list[str]:
        stop_words = {
            "a",
            "an",
            "and",
            "ask",
            "can",
            "command",
            "de",
            "des",
            "do",
            "for",
            "help",
            "how",
            "i",
            "ich",
            "is",
            "je",
            "la",
            "le",
            "les",
            "me",
            "my",
            "on",
            "pour",
            "que",
            "the",
            "to",
            "use",
            "what",
            "wie",
            "with",
        }
        return [
            token
            for token in cls._normalize_text(value).split()
            if len(token) > 2 and token not in stop_words
        ]

    def _build_search_blob(self, command) -> str:
        fields = [command.qualified_name]
        extras = command.extras if isinstance(command.extras, dict) else {}

        for locale in ("en", "fr", "de"):
            locale_data = extras.get(locale, {})
            fields.append(str(locale_data.get("name", "")))
            fields.append(str(locale_data.get("description", "")))
            for parameter in locale_data.get("parameters", []):
                fields.append(str(parameter.get("name", "")))
                fields.append(str(parameter.get("description", "")))

        return self._normalize_text(" ".join(fields))

    def _score_commands(self, question: str):
        query = self._normalize_text(question)
        tokens = self._tokenize(question)
        if not query:
            return []

        scored = []

        for command in self.bot.tree.walk_commands():
            if isinstance(command, Jeanne.Group):
                continue

            qualified_name = command.qualified_name
            normalized_name = self._normalize_text(qualified_name)
            searchable = self._build_search_blob(command)
            score = 0

            if query:
                if query == normalized_name:
                    score += 140
                elif query in normalized_name:
                    score += 90
                elif normalized_name in query:
                    score += 55

                if query in searchable:
                    score += 45

            for token in tokens:
                if token in normalized_name.split():
                    score += 22
                elif token in searchable:
                    score += 28

            if query:
                score += int(
                    SequenceMatcher(None, query, normalized_name).ratio() * 30
                )
            scored.append((score, qualified_name, command))

        return sorted(scored, key=lambda item: item[0], reverse=True)

    def _find_best_command(self, question: str) -> tuple[str | None, list[str]]:
        scored = self._score_commands(question)
        suggestions = [name for _, name, _ in scored[:3]]

        if not scored or scored[0][0] < 35:
            return None, suggestions

        return scored[0][1], suggestions

    def _format_ask_choice(self, ctx: Interaction, qualified_name: str, command) -> str:
        locale = get_command_locale(ctx)
        extras = command.extras if isinstance(command.extras, dict) else {}
        locale_data = extras.get(locale) or extras.get("en", {})
        description = str(locale_data.get("description", "")).strip()
        label = f"/{qualified_name}"

        if description:
            label = f"{label} - {description}"

        return label[:100]

    async def ask_autocomplete(
        self, ctx: Interaction, current: str
    ) -> list[Jeanne.Choice[str]]:
        choices = []
        seen = set()

        for score, qualified_name, command in self._score_commands(current):
            if qualified_name in seen:
                continue
            if current and score < 5:
                break

            seen.add(qualified_name)
            choices.append(
                Jeanne.Choice(
                    name=self._format_ask_choice(ctx, qualified_name, command),
                    value=qualified_name[:100],
                )
            )

        return choices[:25]

    async def _send_ask_error(self, ctx: Interaction, suggestions: list[str]):
        locale = get_command_locale(ctx)
        if locale == "fr":
            description = (
                "Je n'ai pas trouvé de commande correspondante.\n"
                "Essayez avec un nom de commande ou un mot-clé (ex: `ban`, `météo`, `rappel ajouter`)."
            )
            suggestions_name = "Commandes proches"
            footer = "Voir la documentation: https://jeannebot.vercel.app/help"
            view = fr.help_button()
        elif locale == "de":
            description = (
                "Ich konnte keinen passenden Befehl finden.\n"
                "Versuche es mit einem Befehlsnamen oder Stichwort (z. B. `ban`, `wetter`, `reminder add`)."
            )
            suggestions_name = "Ahnliche Befehle"
            footer = "Dokumentation: https://jeannebot.vercel.app/help"
            view = de.help_button()
        else:
            description = (
                "I could not find a matching command.\n"
                "Try a command name or keyword (e.g. `ban`, `weather`, `reminder add`)."
            )
            suggestions_name = "Closest commands"
            footer = "Documentation: https://jeannebot.vercel.app/help"
            view = en.help_button()

        embed = Embed(description=description, color=Color.red())
        if suggestions:
            embed.add_field(
                name=suggestions_name,
                value="\n".join(f"`/{name}`" for name in suggestions),
                inline=False,
            )
        embed.set_footer(text=footer)
        await ctx.response.send_message(embed=embed, view=view)

    @Jeanne.command(
        name=T("command_name"),
        description=T("help_command_desc"),
        extras={
            "en": {
                "name": "help command",
                "description": "Get help on a certain command",
                "parameters": [
                    {
                        "name": "command",
                        "description": "Which command you need help with?",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "aide commande",
                "description": "Obtenez de l'aide sur une certaine commande",
                "parameters": [
                    {
                        "name": "commande",
                        "description": "Avec quelle commande avez-vous besoin d'aide?",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "hilfe befehl",
                "description": "Holen Sie sich Hilfe zu einem bestimmten Befehl",
                "parameters": [
                    {
                        "name": "befehl",
                        "description": "Mit welchem Befehl benötigen Sie Hilfe?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.autocomplete(command=AutoCompleteChoices.command_choices)
    @Jeanne.rename(command=T("command_parm_name"))
    @Jeanne.describe(command=T("command_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def command(self, ctx: Interaction, command: Jeanne.Range[str, 3]):
        locale = get_command_locale(ctx)
        if locale == "fr":
            await fr.HelpGroup(self.bot).command(ctx, command)  
            return
        if locale == "de":
            await de.HelpGroup(self.bot).command(ctx, command)
            return
        await en.HelpGroup(self.bot).command(ctx, command)

    @Jeanne.command(
        name=T("ask_name"),
        description=T("ask_desc"),
        extras={
            "en": {
                "name": "ask",
                "description": "Ask what command to use. Jeanne matches your question to the best command.",
                "parameters": [
                    {
                        "name": "question",
                        "description": "What do you want help with?",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "ask",
                "description": "Demandez quelle commande utiliser. Jeanne associe votre question a la meilleure commande.",
                "parameters": [
                    {
                        "name": "question",
                        "description": "Avec quoi avez-vous besoin d'aide?",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "ask",
                "description": "Frage, welchen Befehl du nutzen sollst. Jeanne ordnet deine Frage dem passendsten Befehl zu.",
                "parameters": [
                    {
                        "name": "question",
                        "description": "Wobei brauchst du Hilfe?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.autocomplete(question=ask_autocomplete)
    @Jeanne.rename(question=T("question_parm_name"))
    @Jeanne.describe(question=T("ask_question_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def ask(self, ctx: Interaction, question: Jeanne.Range[str, 3, 2000]):
        best_match, suggestions = self._find_best_command(question)
        if best_match is None:
            await self._send_ask_error(ctx, suggestions)
            return

        related = [name for name in suggestions if name != best_match][:2]
        locale = get_command_locale(ctx)
        if locale == "fr":
            await fr.HelpGroup(self.bot).command(ctx, best_match, related)
            return
        if locale == "de":
            await de.HelpGroup(self.bot).command(ctx, best_match, related)
            return
        await en.HelpGroup(self.bot).command(ctx, best_match, related)

    @command.error
    async def command_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            locale = get_command_locale(ctx)
            if locale == "fr":
                await fr.HelpGroup(self.bot).command_error(ctx)
                return
            if locale == "de":
                await de.HelpGroup(self.bot).command_error(ctx)
                return
            await en.HelpGroup(self.bot).command_error(ctx)

    @Jeanne.command(
        name=T("support_name"),
        description=T("support_desc"),
        extras={
            "en": {
                "name": "support",
                "description": "Need help? Visit the website or join the server for further assistance.",
            },
            "fr": {
                "name": "aide",
                "description": "Besoin d'aide? Visitez le site web ou rejoignez le serveur pour plus d'assistance.",
            },
            "de": {
                "name": "unterstützung",
                "description": "Brauchen Sie Hilfe? Besuchen Sie die Website oder treten Sie dem Server bei, um weitere Unterstützung zu erhalten.",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def support(self, ctx: Interaction):
        locale = get_command_locale(ctx)
        if locale == "fr":
            await fr.HelpGroup(self.bot).support(ctx)
            return
        if locale == "de":
            await de.HelpGroup(self.bot).support(ctx)
            return
        await en.HelpGroup(self.bot).support(ctx)


async def setup(bot: Bot):
    await bot.add_cog(HelpGroup(bot))
