from typing import Optional
from discord import app_commands as Jeanne
from discord import Locale, Embed

class MyTranslator(Jeanne.Translator):

    async def load(self) -> None:
        print("Translator loaded")

    async def unload(self) -> None:
        print("Translator unloaded")

    async def translate(self, string: Jeanne.locale_str, locale: Locale, context: Jeanne.TranslationContext) -> Optional[str]:
        translations = {
            "ping_name": {"en-GB": "ping", "en-US": "ping", "fr": "ping"},
            "ping_desc": {
                "en-GB": "Check how fast I respond to a command",
                "en-US": "Check how fast I respond to a command",
                "fr": "Vérifiez la rapidité de ma réponse à une commande",
            },
        }

        return translations.get(string.message, {}).get(str(locale), string.message)
