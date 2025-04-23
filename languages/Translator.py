from typing import Optional
from discord import app_commands as Jeanne
from discord import Locale


class MyTranslator(Jeanne.Translator):

    async def load(self) -> None:
        print("Translator loaded")

    async def unload(self) -> None:
        print("Translator unloaded")

    async def translate(
        self,
        string: Jeanne.locale_str,
        locale: Locale,
        context: Jeanne.TranslationContext,
    ) -> Optional[str]:
        translations = {#currency commands
            "ping_name": {"en-GB": "ping", "en-US": "ping", "fr": "ping"},
            "ping_desc": {
                "en-GB": "Check how fast I respond to a command",
                "en-US": "Check how fast I respond to a command",
                "fr": "Vérifiez la rapidité de ma réponse à une commande",
            },
            "free_name": {"en-GB": "free", "en-US": "free", "fr": "libre"},
            "bet_name": {"en-GB": "bet", "en-US": "bet", "fr": "parier"},
            "guess_free_desc": {
                "en-GB": "Guess my number and you can win 20 QP",
                "en-US": "Guess my number and you can win 20 QP",
                "fr": "Devinez mon nombre et vous pouvez gagner 20 QP",
            },
            "guess_bet_name": {
                "en-GB": "Guess my number and you can win with betting",
                "en-US": "Guess my number and you can win with betting",
                "fr": "Devinez mon nombre et vous pouvez gagner avec les paris",
            },
            "bet_parm_name": {"en-GB": "bet", "en-US": "bet", "fr": "parier"},
            "bet_parm_desc": {
                "en-GB": "How much are you betting?",
                "en-US": "How much are you betting?",
                "fr": "Combien pariez-vous?",
            },
            "dice_free_desc": {
                "en-GB": "Roll a dice with betting",
                "en-US": "Roll a dice with betting",
                "fr": "Rouler un dé avec des paris",
            },
            "flip_free_desc": {
                "en-GB": "Flip a coin and earn 20 QP for free",
                "en-US": "Flip a coin and earn 20 QP for free",
                "fr": "Lancez une pièce et gagnez 20 QP gratuitement",
            },
            "flip_deb_desc": {
                "en-GB": "Flip a coin and earn with betting",
                "en-US": "Flip a coin and earn with betting",
                "fr": "Lancez une pièce et gagnez avec des paris",
            },
            "bj_free_desc": {
                "en-GB": "Play a game of blackjack and earn 20 QP for free",
                "en-US": "Play a game of blackjack and earn 20 QP for free",
                "fr": "Jouez à un jeu de blackjack et gagnez 20 QP gratuitement",
            },
            "bj_bet_desc": {
                "en-GB": "Play a game of blackjack and win with betting",
                "en-US": "Play a game of blackjack and win with betting",
                "fr": "Jouez à un jeu de blackjack et gagnez avec des paris",
            },
            "daily_name": {"en-GB": "daily", "en-US": "daily", "fr": "quotidien"},
            "daily_desc": {
                "en-GB": "Get your daily QP",
                "en-US": "Get your daily QP",
                "fr": "Obtenez votre QP quotidien",
            },
            "balance_name": {"en-GB": "balance", "en-US": "balance", "fr": "solde"},
            "balance_desc": {
                "en-GB": "Check your QP balance or someone's QP balance",
                "en-US": "Check your QP balance or someone's QP balance",
                "fr": "Vérifiez votre solde QP ou le solde QP de quelqu'un",
            },
            "vote_name": {"en-GB": "vote", "en-US": "vote", "fr": "voter"},
            "vote_desc": {
                "en-GB": "Vote for me in TopGG",
                "en-US": "Vote for me in TopGG",
                "fr": "Votez pour moi dans TopGG",
            },
        }

        return translations.get(string.message, {}).get(str(locale), string.message)
