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
        translations = {
            # global
            "name_parm_name": {
                "en-GB": "name",
                "en_US": "name",
                "fr": "nom",
            },
            "name_parm_desc": {
                "en-GB": "What will you name it?",
                "en-US": "What will you name it?",
                "fr": "Quel nom lui donnerez-vous?",
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
            # currency commands
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
            # info commands
            "stats_name": {
                "en-GB": "stats",
                "en-US": "stats",
                "fr": "stats",
            },
            "stats_desc": {
                "en-GB": "See the bot's status from development to now",
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
            "serverbanner_desc": {
                "en-GB": "Get the server banner",
                "en-US": "Get the server banner",
                "fr": "Obtenez la bannière du serveur",
            },
            "avatar_desc": {
                "en-GB": "See your avatar or another member's avatar",
                "en-US": "See your avatar or another member's avatar",
                "fr": "Voir votre avatar ou l'avatar d'un autre membre",
            },
            "ping_name": {"en-GB": "ping", "en-US": "ping", "fr": "ping"},
            "ping_desc": {
                "en-GB": "Check how fast I respond to a command",
                "en-US": "Check how fast I respond to a command",
                "fr": "Vérifiez la rapidité de ma réponse à une commande",
            },
            "sticker_desc": {
                "en-GB": "Get a random sticker from the server",
                "en-US": "Get a random sticker from the server",
                "fr": "Obtenez un autocollant aléatoire du serveur",
            },
            "sticker_parm_desc": {
                "en-GB": "Insert message ID with the sticker or name of the sticker in the server",
                "en-US": "Insert message ID with the sticker or name of the sticker in the server",
                "fr": "Insérez l'ID du message avec l'autocollant ou le nom de l'autocollant dans le serveur",
            },
            "emoji_desc": {
                "en-GB": "View an emoji",
                "en_US": "View an emoji",
                "fr": "Voir un emoji",
            },
            "emoji_parm_desc": {
                "en-GB": "What is the name of the emoji?",
                "en-US": "What is the name of the emoji?",
                "fr": "Quel est le nom de l'emoji?",
            },
            # inventory commands
            "country_name": {
                "en-GB": "country",
                "en-US": "country",
                "fr": "pays",
            },
            "country_desc": {
                "en-GB": "Buy a country badge",
                "en-US": "Buy a country badge",
                "fr": "Acheter un badge de pays",
            },
            "backgrounds_desc": {
                "en-GB": "Check all the wallpapers available",
                "en-US": "Check all the wallpapers available",
                "fr": "Vérifiez tous les fonds d'écran disponibles",
            },
            "buy-custom_desc": {
                "en-GB": "Buy a custom background pic for your level card",
                "en-US": "Buy a custom background pic for your level card",
                "fr": "Acheter une image d'arrière-plan personnalisée pour votre carte de niveau",
            },
            "list_name": {
                "en-GB": "list",
                "en-US": "list",
                "fr": "liste",
            },
            "list_desc": {
                "en-GB": "Check which backgrounds you have",
                "en-US": "Check which backgrounds you have",
                "fr": "Vérifiez quels fonds d'écran vous avez",
            },
            "link_parm_name": {
                "en-GB": "link",
                "en-US": "link",
                "fr": "lien",
            },
            "link_parm_desc": {
                "en-GB": "Add an image link",
                "en-US": "Add an image link",
                "fr": "Ajouter un lien d'image",
            },
            # levelling
            "global_desc": {
                "en-GB": "Check the users with the most XP globally",
                "en-US": "Check the users with the most XP globally",
                "fr": "Vérifiez les utilisateurs avec le plus d'XP au niveau mondial",
            },
            "server_desc": {
                "en-GB": "Check the users with the most XP in the server",
                "en-US": "Check the users with the most XP in the server",
                "fr": "Vérifiez les utilisateurs avec le plus d'XP sur le serveur",
            },
            "profile_name": {
                "en-GB": "profile",
                "en-US": "profile",
                "fr": "profil",
            },
            "profile_desc": {
                "en-GB": "See your profile or someone else's profile",
                "en-US": "See your profile or someone else's profile",
                "fr": "Voir votre profil ou celui de quelqu'un d'autre",
            },
            # manage commands
            "textchannel_name": {
                "en-GB": "textchannel",
                "en-US": "textchannel",
                "fr": "canal_texte",
            },
            "textchannel_description": {
                "en-GB": "Create a text channel",
                "en-US": "Create a text channel",
                "fr": "Créer un canal texte",
            },
            "name_parm_name": {
                "en-GB": "name",
                "en-US": "name",
                "fr": "nom",
            },
            "name_parm_desc": {
                "en-GB": "What will you name it?",
                "en-US": "What will you name it?",
                "fr": "Quel nom lui donnerez-vous?",
            },
            "topic_parm_name": {
                "en-GB": "topic",
                "en-US": "topic",
                "fr": "sujet",
            },
            "topic_parm_desc": {
                "en-GB": "What is the channel topic?",
                "en-US": "What is the channel topic?",
                "fr": "Quel est le sujet du canal?",
            },
            "category_parm_name": {
                "en-GB": "category",
                "en-US": "category",
                "fr": "catégorie",
            },
            "category_parm_desc": {
                "en-GB": "Place in which category?",
                "en-US": "Place in which category?",
                "fr": "Dans quelle catégorie?",
            },
            "slowmode_parm_name": {
                "en-GB": "slowmode",
                "en-US": "slowmode",
                "fr": "mode_lent",
            },
            "slowmode_parm_desc": {
                "en-GB": "What is the slowmode (1h, 30m, etc) (Max is 6 hours)",
                "en-US": "What is the slowmode (1h, 30m, etc) (Max is 6 hours)",
                "fr": "Quel est le mode lent (1h, 30m, etc) (Max est de 6 heures)",
            },
            "nsfw_parm_name": {
                "en-GB": "nsfw_enabled",
                "en-US": "nsfw_enabled",
                "fr": "nsfw_activé",
            },
            "nsfw_parm_desc": {
                "en-GB": "Should it be an NSFW channel?",
                "en-US": "Should it be an NSFW channel?",
                "fr": "Doit-il s'agir d'un canal NSFW?",
            },
            "voicechannel_description": {
                "en-GB": "Create a voice channel",
                "en-US": "Create a voice channel",
                "fr": "Créer un canal vocal",
            },
            "users_parm_name": {
                "en-GB": "users",
                "en-US": "users",
                "fr": "utilisateurs",
            },
            "users_parm_desc": {
                "en-GB": "How many users are allowed in the channel?",
                "en-US": "How many users are allowed in the channel?",
                "fr": "Combien d'utilisateurs sont autorisés dans le canal?",
            },
            "category_description": {
                "en-GB": "Create a category",
                "en-US": "Create a category",
                "fr": "Créer une catégorie",
            },
            "stagechannel_description": {
                "en-GB": "Create a stage channel",
                "en-US": "Create a stage channel",
                "fr": "Créer un canal de scène",
            },
            "forum_description": {
                "en-GB": "Create a forum",
                "en-US": "Create a forum",
                "fr": "Créer un forum",
            },
            "role_description": {
                "en-GB": "Create a role",
                "en-US": "Create a role",
                "fr": "Créer un rôle",
            },
            "color_parm_name": {
                "en-GB": "color",
                "en-US": "color",
                "fr": "couleur",
            },
            "color_parm_desc": {
                "en-GB": "What color will it be? (use HEX codes)",
                "en-US": "What color will it be? (use HEX codes)",
                "fr": "Quelle couleur sera-t-elle? (utilisez des codes HEX)",
            },
            "hoisted_parm_name": {
                "en-GB": "hoisted",
                "en-US": "hoisted",
                "fr": "affiché",
            },
            "hoisted_parm_desc": {
                "en-GB": "Should it be shown in member list?",
                "en-US": "Should it be shown in member list?",
                "fr": "Doit-il être affiché dans la liste des membres?",
            },
            "mentionable_parm_name": {
                "en-GB": "mentionable",
                "en-US": "mentionable",
                "fr": "mentionnable",
            },
            "mentionable_parm_desc": {
                "en-GB": "Should it be mentioned?",
                "en-US": "Should it be mentioned?",
                "fr": "Doit-il être mentionné?",
            },
            "public_thread_description": {
                "en-GB": "Make a public thread",
                "en-US": "Make a public thread",
                "fr": "Créer un fil public",
            },
            "private_thread_description": {
                "en-GB": "Make a private thread",
                "en-US": "Make a private thread",
                "fr": "Créer un fil privé",
            },
            "emoji_description": {
                "en-GB": "Make a new emoji",
                "en-US": "Make a new emoji",
                "fr": "Créer un nouvel emoji",
            },
            "sticker_description": {
                "en-GB": "Make a new sticker",
                "en-US": "Make a new sticker",
                "fr": "Créer un nouvel autocollant",
            },
            "delete_channel_description": {
                "en-GB": "Deletes a channel",
                "en-US": "Deletes a channel",
                "fr": "Supprime un canal",
            },
            "delete_role_description": {
                "en-GB": "Deletes a role",
                "en-US": "Deletes a role",
                "fr": "Supprime un rôle",
            },
            "delete_emoji_description": {
                "en-GB": "Deletes an emoji",
                "en-US": "Deletes an emoji",
                "fr": "Supprime un emoji",
            },
            "delete_sticker_description": {
                "en-GB": "Deletes a sticker",
                "en-US": "Deletes a sticker",
                "fr": "Supprime un autocollant",
            },
            "edit_textchannel_description": {
                "en-GB": "Edits a text/news channel",
                "en-US": "Edits a text/news channel",
                "fr": "Modifie un canal texte/actualités",
            },
            "edit_voicechannel_description": {
                "en-GB": "Edits a voice channel",
                "en-US": "Edits a voice channel",
                "fr": "Modifie un canal vocal",
            },
            "edit_role_description": {
                "en-GB": "Edit a role",
                "en-US": "Edit a role",
                "fr": "Modifier un rôle",
            },
            "edit_server_description": {
                "en-GB": "Edits the server",
                "en-US": "Edits the server",
                "fr": "Modifie le serveur",
            },
            "welcomer_description": {
                "en-GB": "Set a welcomer and/or leaver channel",
                "en-US": "Set a welcomer and/or leaver channel",
                "fr": "Définir un canal d'accueil et/ou de départ",
            },
            "modlog_description": {
                "en-GB": "Set a modlog channel",
                "en-US": "Set a modlog channel",
                "fr": "Définir un canal de journalisation des modérateurs",
            },
            "welcomingmsg_description": {
                "en-GB": "Set a welcoming message when someone joins the server",
                "en-US": "Set a welcoming message when someone joins the server",
                "fr": "Définir un message d'accueil lorsqu'une personne rejoint le serveur",
            },
            "leavingmsg_description": {
                "en-GB": "Set a leaving message when someone leaves the server",
                "en-US": "Set a leaving message when someone leaves the server",
                "fr": "Définir un message de départ lorsqu'une personne quitte le serveur",
            },
            "rolereward_message_description": {
                "en-GB": "Set a role reward message. This will be posted in the levelup channel",
                "en-US": "Set a role reward message. This will be posted in the levelup channel",
                "fr": "Définir un message de récompense de rôle. Cela sera publié dans le canal de montée de niveau",
            },
            "levelupdate_description": {
                "en-GB": "Set a level up notification channel",
                "en-US": "Set a level up notification channel",
                "fr": "Définir un canal de notification de montée de niveau",
            },
            "confessionchannel_description": {
                "en-GB": "Set a confession channel",
                "en-US": "Set a confession channel",
                "fr": "Définir un canal de confession",
            },
            "brightness_description": {
                "en-GB": "Change the brightness of your level and profile card background",
                "en-US": "Change the brightness of your level and profile card background",
                "fr": "Changer la luminosité de l'arrière-plan de votre carte de niveau et de profil",
            },
            "bio_description": {
                "en-GB": "Change your profile bio",
                "en-US": "Change your profile bio",
                "fr": "Changer votre biographie de profil",
            },
            "color_description": {
                "en-GB": "Change your level and profile card font and bar color",
                "en-US": "Change your level and profile card font and bar color",
                "fr": "Changer la couleur de la police et de la barre de votre carte de niveau et de profil",
            },
            # Command Names
            "ban_name": {
                "en-GB": "ban",
                "en-US": "ban",
                "fr": "bannir",
            },
            "warn_name": {
                "en-GB": "warn",
                "en-US": "warn",
                "fr": "avertir",
            },
            "list_warns_name": {
                "en-GB": "list-warns",
                "en-US": "list-warns",
                "fr": "liste-avertissements",
            },
            "clear_warn_name": {
                "en-GB": "clear-warn",
                "en-US": "clear-warn",
                "fr": "effacer-avertissement",
            },
            "kick_name": {
                "en-GB": "kick",
                "en-US": "kick",
                "fr": "expulser",
            },
            "prune_name": {
                "en-GB": "prune",
                "en-US": "prune",
                "fr": "purger",
            },
            "change_nickname_name": {
                "en-GB": "change-nickname",
                "en-US": "change-nickname",
                "fr": "changer-surnom",
            },
            "unban_name": {
                "en-GB": "unban",
                "en-US": "unban",
                "fr": "débannir",
            },
            "timeout_name": {
                "en-GB": "timeout",
                "en-US": "timeout",
                "fr": "mettre-en-sourdine",
            },
            "timeout_remove_name": {
                "en-GB": "timeout-remove",
                "en-US": "timeout-remove",
                "fr": "retirer-sourdine",
            },
            "massban_name": {
                "en-GB": "massban",
                "en-US": "massban",
                "fr": "bannissement-massif",
            },
            "massunban_name": {
                "en-GB": "massunban",
                "en-US": "massunban",
                "fr": "débannissement-massif",
            },

            # Command Descriptions
            "ban_desc": {
                "en-GB": "Ban someone from or outside the server",
                "en-US": "Ban someone from or outside the server",
                "fr": "Bannir quelqu'un du serveur ou de l'extérieur",
            },
            "warn_desc": {
                "en-GB": "Warn a member",
                "en-US": "Warn a member",
                "fr": "Avertir un membre",
            },
            "list_warns_desc": {
                "en-GB": "View warnings in the server or a member",
                "en-US": "View warnings in the server or a member",
                "fr": "Voir les avertissements dans le serveur ou d'un membre",
            },
            "clear_warn_desc": {
                "en-GB": "Revoke a warn by warn ID",
                "en-US": "Revoke a warn by warn ID",
                "fr": "Révoquer un avertissement par ID d'avertissement",
            },
            "kick_desc": {
                "en-GB": "Kick a member out of the server",
                "en-US": "Kick a member out of the server",
                "fr": "Expulser un membre du serveur",
            },
            "prune_desc": {
                "en-GB": "Bulk delete messages",
                "en-US": "Bulk delete messages",
                "fr": "Supprimer en masse des messages",
            },
            "change_nickname_desc": {
                "en-GB": "Change someone's nickname",
                "en-US": "Change someone's nickname",
                "fr": "Changer le surnom de quelqu'un",
            },
            "unban_desc": {
                "en-GB": "Unbans a user",
                "en-US": "Unbans a user",
                "fr": "Débannir un utilisateur",
            },
            "timeout_desc": {
                "en-GB": "Timeout a member",
                "en-US": "Timeout a member",
                "fr": "Mettre un membre en sourdine",
            },
            "timeout_remove_desc": {
                "en-GB": "Removes a timeout from a member",
                "en-US": "Removes a timeout from a member",
                "fr": "Retirer une sourdine d'un membre",
            },
            "massban_desc": {
                "en-GB": "Ban multiple members at once",
                "en-US": "Ban multiple members at once",
                "fr": "Bannir plusieurs membres à la fois",
            },
            "massunban_desc": {
                "en-GB": "Unban multiple members at once",
                "en-US": "Unban multiple members at once",
                "fr": "Débannir plusieurs membres à la fois",
            },

            # Parameter Names
            "member_param_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "reason_param_name": {
                "en-GB": "reason",
                "en-US": "reason",
                "fr": "raison",
            },
            "delete_message_history_param_name": {
                "en-GB": "delete_message_history",
                "en-US": "delete_message_history",
                "fr": "supprimer_historique_messages",
            },
            "time_param_name": {
                "en-GB": "time",
                "en-US": "time",
                "fr": "temps",
            },
            "warn_id_param_name": {
                "en-GB": "warn_id",
                "en-US": "warn_id",
                "fr": "id_avertissement",
            },
            "limit_param_name": {
                "en-GB": "limit",
                "en-US": "limit",
                "fr": "limite",
            },
            "nickname_param_name": {
                "en-GB": "nickname",
                "en-US": "nickname",
                "fr": "surnom",
            },
            "user_id_param_name": {
                "en-GB": "user_id",
                "en-US": "user_id",
                "fr": "id_utilisateur",
            },
            "user_ids_param_name": {
                "en-GB": "user_ids",
                "en-US": "user_ids",
                "fr": "ids_utilisateurs",
            },

            # Parameter Descriptions
            "member_param_desc": {
                "en-GB": "What is the member or user ID?",
                "en-US": "What is the member or user ID?",
                "fr": "Quel est le membre ou l'ID utilisateur ?",
            },
            "reason_param_desc": {
                "en-GB": "What did they do? You can also make a custom reason",
                "en-US": "What did they do? You can also make a custom reason",
                "fr": "Qu'ont-ils fait ? Vous pouvez également créer une raison personnalisée",
            },
            "delete_message_history_param_desc": {
                "en-GB": "Delete messages from past 7 days?",
                "en-US": "Delete messages from past 7 days?",
                "fr": "Supprimer les messages des 7 derniers jours ?",
            },
            "time_param_desc": {
                "en-GB": "How long should they be tempbanned? (1m, 1h30m, etc)",
                "en-US": "How long should they be tempbanned? (1m, 1h30m, etc)",
                "fr": "Combien de temps doivent-ils être temporairement bannis ? (1m, 1h30m, etc)",
            },
            "warn_id_param_desc": {
                "en-GB": "What is their warn ID you want to remove?",
                "en-US": "What is their warn ID you want to remove?",
                "fr": "Quel est leur ID d'avertissement que vous souhaitez supprimer ?",
            },
            "limit_param_desc": {
                "en-GB": "How many messages? (max is 100)",
                "en-US": "How many messages? (max is 100)",
                "fr": "Combien de messages ? (max est 100)",
            },
            "nickname_param_desc": {
                "en-GB": "What is their new nickname?",
                "en-US": "What is their new nickname?",
                "fr": "Quel est leur nouveau surnom ?",
            },
            "user_id_param_desc": {
                "en-GB": "Which user do you want to unban?",
                "en-US": "Which user do you want to unban?",
                "fr": "Quel utilisateur voulez-vous débannir ?",
            },
            "user_ids_param_desc": {
                "en-GB": "How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
                "en-US": "How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
                "fr": "Combien d'IDs utilisateur ? Laissez un espace après chaque ID (min est 5 et max est 25)",
            },

            # reactions commands
            "hug_name": {
                "en-GB": "hug",
                "en-US": "hug",
                "fr": "câlin",
            },
            "hug_desc": {
                "en-GB": "Hug someone or yourself",
                "en-US": "Hug someone or yourself",
                "fr": "Faites un câlin à quelqu'un ou à vous-même",
            },
            "hug_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "hug_member_parm_desc": {
                "en-GB": "Who are you hugging?",
                "en-US": "Who are you hugging?",
                "fr": "Qui câlinez-vous ?",
            },

            "slap_name": {
                "en-GB": "slap",
                "en-US": "slap",
                "fr": "gifler",
            },
            "slap_desc": {
                "en-GB": "Slap someone or yourself",
                "en-US": "Slap someone or yourself",
                "fr": "Gifle quelqu'un ou vous-même",
            },
            "slap_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "slap_member_parm_desc": {
                "en-GB": "Who are you slapping?",
                "en-US": "Who are you slapping?",
                "fr": "Qui giflez-vous ?",
            },

            "smug_name": {
                "en-GB": "smug",
                "en-US": "smug",
                "fr": "suffisant",
            },
            "smug_desc": {
                "en-GB": "Show a smug expression",
                "en-US": "Show a smug expression",
                "fr": "Affichez une expression suffisante",
            },

            "poke_name": {
                "en-GB": "poke",
                "en-US": "poke",
                "fr": "pousser",
            },
            "poke_desc": {
                "en-GB": "Poke someone or yourself",
                "en-US": "Poke someone or yourself",
                "fr": "Piquez quelqu'un ou vous-même",
            },
            "poke_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "poke_member_parm_desc": {
                "en-GB": "Who are you poking?",
                "en-US": "Who are you poking?",
                "fr": "Qui piquez-vous ?",
            },

            "pat_name": {
                "en-GB": "pat",
                "en-US": "pat",
                "fr": "tapoter",
            },
            "pat_desc": {
                "en-GB": "Pat someone or yourself",
                "en-US": "Pat someone or yourself",
                "fr": "Tapotez quelqu'un ou vous-même",
            },
            "pat_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "pat_member_parm_desc": {
                "en-GB": "Who are you patting?",
                "en-US": "Who are you patting?",
                "fr": "Qui tapotez-vous ?",
            },

            "kiss_name": {
                "en-GB": "kiss",
                "en-US": "kiss",
                "fr": "embrasser",
            },
            "kiss_desc": {
                "en-GB": "Kiss someone or yourself",
                "en-US": "Kiss someone or yourself",
                "fr": "Embrassez quelqu'un ou vous-même",
            },
            "kiss_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "kiss_member_parm_desc": {
                "en-GB": "Who are you kissing?",
                "en-US": "Who are you kissing?",
                "fr": "Qui embrassez-vous ?",
            },

            "tickle_name": {
                "en-GB": "tickle",
                "en-US": "tickle",
                "fr": "chatouiller",
            },
            "tickle_desc": {
                "en-GB": "Tickle someone or yourself",
                "en-US": "Tickle someone or yourself",
                "fr": "Chatouillez quelqu'un ou vous-même",
            },
            "tickle_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "tickle_member_parm_desc": {
                "en-GB": "Who are you tickling?",
                "en-US": "Who are you tickling?",
                "fr": "Qui chatouillez-vous ?",
            },

            "baka_name": {
                "en-GB": "baka",
                "en-US": "baka",
                "fr": "baka",
            },
            "baka_desc": {
                "en-GB": "Call someone or yourself a baka!",
                "en-US": "Call someone or yourself a baka!",
                "fr": "Traitez quelqu'un ou vous-même de baka !",
            },
            "baka_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "baka_member_parm_desc": {
                "en-GB": "Who are you calling a baka?",
                "en-US": "Who are you calling a baka?",
                "fr": "Qui traitez-vous de baka ?",
            },

            "feed_name": {
                "en-GB": "feed",
                "en-US": "feed",
                "fr": "nourrir",
            },
            "feed_desc": {
                "en-GB": "Feed someone or yourself",
                "en-US": "Feed someone or yourself",
                "fr": "Nourrissez quelqu'un ou vous-même",
            },
            "feed_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "feed_member_parm_desc": {
                "en-GB": "Who are you feeding?",
                "en-US": "Who are you feeding?",
                "fr": "Qui nourrissez-vous ?",
            },

            "cry_name": {
                "en-GB": "cry",
                "en-US": "cry",
                "fr": "pleurer",
            },
            "cry_desc": {
                "en-GB": "Show a crying expression",
                "en-US": "Show a crying expression",
                "fr": "Affichez une expression de pleurs",
            },

            "bite_name": {
                "en-GB": "bite",
                "en-US": "bite",
                "fr": "mordre",
            },
            "bite_desc": {
                "en-GB": "Bite someone or yourself",
                "en-US": "Bite someone or yourself",
                "fr": "Mordez quelqu'un ou vous-même",
            },
            "bite_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "bite_member_parm_desc": {
                "en-GB": "Who are you biting?",
                "en-US": "Who are you biting?",
                "fr": "Qui mordez-vous ?",
            },

            "blush_name": {
                "en-GB": "blush",
                "en-US": "blush",
                "fr": "rougir",
            },
            "blush_desc": {
                "en-GB": "Show a blushing expression",
                "en-US": "Show a blushing expression",
                "fr": "Affichez une expression de rougissement",
            },

            "cuddle_name": {
                "en-GB": "cuddle",
                "en-US": "cuddle",
                "fr": "câliner",
            },
            "cuddle_desc": {
                "en-GB": "Cuddle with someone or yourself",
                "en-US": "Cuddle with someone or yourself",
                "fr": "Câlinez quelqu'un ou vous-même",
            },
            "cuddle_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "cuddle_member_parm_desc": {
                "en-GB": "Who are you cuddling with?",
                "en-US": "Who are you cuddling with?",
                "fr": "Avec qui câlinez-vous ?",
            },

            "dance_name": {
                "en-GB": "dance",
                "en-US": "dance",
                "fr": "danser",
            },
            "dance_desc": {
                "en-GB": "Dance with someone or yourself",
                "en-US": "Dance with someone or yourself",
                "fr": "Dansez avec quelqu'un ou vous-même",
            },
            "dance_member_parm_name": {
                "en-GB": "member",
                "en-US": "member",
                "fr": "membre",
            },
            "dance_member_parm_desc": {
                "en-GB": "Who are you dancing with?",
                "en-US": "Who are you dancing with?",
                "fr": "Avec qui dansez-vous ?",
            },
        }

        return translations.get(string.message_id, {}).get(locale.value)
