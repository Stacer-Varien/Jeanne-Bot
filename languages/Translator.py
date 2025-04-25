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
        translations = (
            {
                # currency commands
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
                # fun commands
                "8ball_name": {
                    "en-GB": "8ball",
                    "en-US": "8ball",
                    "fr": "8ball",
                },
                "8ball_desc": {
                    "en-GB": "Ask 8 ball anything and you will get your answer",
                    "en-US": "Ask 8 ball anything and you will get your answer",
                    "fr": "Demandez à 8 ball n'importe quoi et vous obtiendrez votre réponse",
                },
                "question_parm_name": {
                    "en-GB": "question",
                    "en-US": "question",
                    "fr": "question",
                },
                "question_parm_desc": {
                    "en-GB": "Add your question",
                    "en-US": "Add your question",
                    "fr": "Ajoutez votre question",
                },
                "reverse_name": {
                    "en-GB": "reverse",
                    "en-US": "reverse",
                    "fr": "inverse",
                },
                "reverse_desc": {
                    "en-GB": "Say something and I will say it in reversed text",
                    "en-US": "Say something and I will say it in reversed text",
                    "fr": "Dites quelque chose et je le dirai dans un texte inversé",
                },
                "text_parm_name": {
                    "en-GB": "text",
                    "en-US": "text",
                    "fr": "texte",
                },
                "text_parm_desc": {
                    "en-GB": "What are you reversing?",
                    "en-US": "What are you reversing?",
                    "fr": "Qu'est-ce que vous inversez?",
                },
                "combine_name": {
                    "en-GB": "combine",
                    "en-US": "combine",
                    "fr": "combiner",
                },
                "combine_desc": {
                    "en-GB": "Combine 2 words to get 2 combined words",
                    "en-US": "Combine 2 words to get 2 combined words",
                    "fr": "Combinez 2 mots pour obtenir 2 mots combinés",
                },
                "first_word_parm_name": {
                    "en-GB": "first_word",
                    "en-US": "first_word",
                    "fr": "premier_mot",
                },
                "first_word_parm_desc": {
                    "en-GB": "Add first word",
                    "en-US": "Add first word",
                    "fr": "Ajouter le premier mot",
                },
                "second_word_parm_name": {
                    "en-GB": "second_word",
                    "en-US": "second_word",
                    "fr": "deuxième_mot",
                },
                "second_word_parm_desc": {
                    "en-GB": "Add second word",
                    "en-US": "Add second word",
                    "fr": "Ajouter le deuxième mot",
                },
                "choose_name": {
                    "en-GB": "choose",
                    "en-US": "choose",
                    "fr": "choisir",
                },
                "choose_desc": {
                    "en-GB": "Give me a lot of choices and I will pick one for you",
                    "en-US": "Give me a lot of choices and I will pick one for you",
                    "fr": "Donnez-moi beaucoup de choix et je choisirai un pour vous",
                },
                "choices_parm_name": {
                    "en-GB": "choices",
                    "en-US": "choices",
                    "fr": "choix",
                },
                "choices_parm_desc": {
                    "en-GB": "Add your choices here. Separate them with ','",
                    "en-US": "Add your choices here. Separate them with ','",
                    "fr": "Ajoutez vos choix ici. Séparez-les par ','",
                },
                "animeme_name": {
                    "en-GB": "animeme",
                    "en-US": "animeme",
                    "fr": "animeme",
                },
                "animeme_desc": {
                    "en-GB": "Get a random animeme",
                    "en-US": "Get a random animeme",
                    "fr": "Obtenez un animeme aléatoire",
                },
                "simprate_name": {
                    "en-GB": "simprate",
                    "en-US": "simprate",
                    "fr": "taux_de_simp",
                },
                "simprate_desc": {
                    "en-GB": "Get a random simp rate for you or someone else",
                    "en-US": "Get a random simp rate for you or someone else",
                    "fr": "Obtenez un taux de simp aléatoire pour vous ou quelqu'un d'autre",
                },
                "member_parm_name": {
                    "en-GB": "member",
                    "en-US": "member",
                    "fr": "membre",
                },
                "member_parm_desc": {
                    "en-GB": "Which member?",
                    "en-US": "Which member?",
                    "fr": "Quel membre?",
                },
                # help commands
                "command_name": {
                    "en-GB": "command",
                    "en-US": "command",
                    "fr": "commande",
                },
                "command_desc": {
                    "en-GB": "Get help on a certain command",
                    "en-US": "Get help on a certain command",
                    "fr": "Obtenez de l'aide sur une certaine commande",
                },
                "command_parm_name": {
                    "en-GB": "command",
                    "en-US": "command",
                    "fr": "commande",
                },
                "command_parm_desc": {
                    "en-GB": "Which command you need help with?",
                    "en-US": "Which command you need help with?",
                    "fr": "Avec quelle commande avez-vous besoin d'aide?",
                },
                "support_name": {
                    "en-GB": "support",
                    "en-US": "support",
                    "fr": "soutien",
                },
                "support_desc": {
                    "en-GB": "Get help from the website or join the support server for further help",
                    "en-US": "Get help from the website or join the support server for further help",
                    "fr": "Obtenez de l'aide sur le site Web ou rejoignez le serveur d'assistance pour obtenir de l'aide supplémentaire",
                },
                # hentai commands
                "hentai_name": {
                    "en-GB": "hentai",
                    "en-US": "hentai",
                    "fr": "hentai",
                },
                "hentai_desc": {
                    "en-GB": "Get a random hentai from Jeanne",
                    "en-US": "Get a random hentai from Jeanne",
                    "fr": "Obtenez un hentai aléatoire de Jeanne",
                },
                "gelbooru_desc": {
                    "en-GB": "Get a random media content from Gelbooru",
                    "en-US": "Get a random media content from Gelbooru",
                    "fr": "Obtenez un contenu multimédia aléatoire de Gelbooru",
                },
                "yandere_desc": {
                    "en-GB": "Get a random media content from Yandere",
                    "en-US": "Get a random media content from Yandere",
                    "fr": "Obtenez un contenu multimédia aléatoire de Yandere",
                },
                "danbooru_desc": {
                    "en-GB": "Get a random media content from Danbooru",
                    "en-US": "Get a random media content from Danbooru",
                    "fr": "Obtenez un contenu multimédia aléatoire de Danbooru",
                },
                "konachan_desc": {
                    "en-GB": "Get a random media content from Konachan",
                    "en-US": "Get a random media content from Konachan",
                    "fr": "Obtenez un contenu multimédia aléatoire de Konachan",
                },
                "tag_parm_name": {
                    "en-GB": "tag",
                    "en-US": "tag",
                    "fr": "étiquette",
                },
                "tag_parm_desc": {
                    "en-GB": "Add your tag",
                    "en-US": "Add your tag",
                    "fr": "Ajoutez votre étiquette",
                },
                "plus_parm_name": {
                    "en-GB": "plus",
                    "en-US": "plus",
                    "fr": "plus",
                },
                "plus_parm_desc": {
                    "en-GB": "Need more content? (up to 4)",
                    "en-US": "Need more content? (up to 4)",
                    "fr": "Besoin de plus de contenu? (jusqu'à 4)",
                },
                "danbooru_tag_parm_name": {
                    "en-GB": "Add your tag (up to 2 tags)",
                    "en-US": "Add your tag (up to 2 tags)",
                    "fr": "Ajoutez votre étiquette (jusqu'à 2 étiquettes)",
                },
                # image commands
                "kitsune_desc": {
                    "en-GB": "Get a random kitsune image",
                    "en-US": "Get a random kitsune image",
                    "fr": "Obtenez une image de kitsune aléatoire",
                },
                "wallpaper_desc": {
                    "en-GB": "Get a random wallpaper for your PC or phone",
                    "en-US": "Get a random wallpaper for your PC or phone",
                    "fr": "Obtenez un fond d'écran aléatoire pour votre PC ou votre téléphone",
                },
                "jeanne_desc": {
                    "en-GB": "Get a random Jeanne d'Arc image",
                    "en-US": "Get a random Jeanne d'Arc image",
                    "fr": "Obtenez une image de Jeanne d'Arc aléatoire",
                },
                "saber_desc": {
                    "en-GB": "Get a random Saber image",
                    "en-US": "Get a random Saber image",
                    "fr": "Obtenez une image de Saber aléatoire",
                },
                "neko_desc": {
                    "en-GB": "Get a random neko image",
                    "en-US": "Get a random neko image",
                    "fr": "Obtenez une image de neko aléatoire",
                },
                "medusa_desc": {
                    "en-GB": "Get a random Medusa image",
                    "en-US": "Get a random Medusa image",
                    "fr": "Obtenez une image de Méduse aléatoire",
                },
                "morgan_desc": {
                    "en-GB": "Get a random Morgan image",
                    "en-US": "Get a random Morgan image",
                    "fr": "Obtenez une image de Morgan aléatoire",
                },
                "safebooru_desc": {
                    "en-GB": "Get a random image from Safebooru",
                    "en-US": "Get a random image from Safebooru",
                    "fr": "Obtenez une image aléatoire de Safebooru",
                },
                #info commands
                "stats_desc": {"en-GB": "See the bot's status from development to now",
                    "en-US": "See the bot's status from development to now",
                    "fr": "Voir le statut du bot depuis le développement jusqu'à maintenant",
                },
                "userinfo_desc": {
                    "en-GB": "See the information of a member or yourself",
                    "en-US": "See the information of a member or yourself",
                    "fr": "Voir les informations d'un membre ou de vous-même",
                },
                "serverinfo_desc": {
                    "en-GB": "Get information about this server",
                    "en-US": "Get information about this server",
                    "fr": "Obtenez des informations sur ce serveur",
                },
            },
        )

        return translations.get(string.message, {}).get(str(locale), string.message)
