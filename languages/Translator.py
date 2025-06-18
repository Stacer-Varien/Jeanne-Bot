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
            #global
            "name_parm_name": {"en-GB": "name", "en-US": "name", "fr": "nom"},
            "name_parm_desc": {
                "en-GB": "What will you name it?",
                "en-US": "What will you name it?",
                "fr": "Quel nom lui donnerez-vous?",
            },
            "member_parm_name": {"en-GB": "member", "en-US": "member", "fr": "membre"},
            "member_parm_desc": {
                "en-GB": "Which member?",
                "en-US": "Which member?",
                "fr": "Quel membre?",
            },
            #currency commands
            "guess_group_name free_name": {
                "en-GB": "guess free",
                "en-US": "guess free",
                "fr": "deviner libre",
            },
            "guess_group_name": {"en-GB": "guess", "en-US": "guess", "fr": "deviner"},
            "dice_group_name": {"en-GB": "dice", "en-US": "dice", "fr": "dé"},
            "flip_group_name": {"en-GB": "flip", "en-US": "flip", "fr": "lancer"},
            "blackjack_group_name": {
                "en-GB": "blackjack",
                "en-US": "blackjack",
                "fr": "blackjack",
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
                "fr": "Devinez mon nombre et vous pouvez gagner avec des paris",
            },
            "bet_parm_name": {"en-GB": "bet", "en-US": "bet", "fr": "parier"},
            "bet_parm_desc": {
                "en-GB": "How much are you betting?",
                "en-US": "How much are you betting?",
                "fr": "Combien pariez-vous?",
            },
            "dice_free_desc": {
                "en-GB": "Roll a dice and earn 20 QP for free",
                "en-US": "Roll a dice and earn 20 QP for free",
                "fr": "Lancez un dé et gagnez 20 QP gratuitement",
            },
            "dice_bet_desc": {
                "en-GB": "Roll a dice and win with betting",
                "en-US": "Roll a dice and win with betting",
                "fr": "Lancez un dé et gagnez avec des paris",
            },
            "flip_free_desc": {
                "en-GB": "Flip a coin and earn 20 QP for free",
                "en-US": "Flip a coin and earn 20 QP for free",
                "fr": "Lancez une pièce et gagnez 20 QP gratuitement",
            },
            "flip_bet_desc": {
                "en-GB": "Flip a coin and earn with betting",
                "en-US": "Flip a coin and earn with betting",
                "fr": "Lancez une pièce et gagnez avec des paris",
            },
            "bj_free_desc": {
                "en-GB": "Play blackjack for free and earn 20 QP",
                "en-US": "Play blackjack for free and earn 20 QP",
                "fr": "Jouez au blackjack gratuitement et gagnez 20 QP",
            },
            "bj_bet_desc": {
                "en-GB": "Play a game of blackjack and win with betting",
                "en-US": "Play a game of blackjack and win with betting",
                "fr": "Jouez au blackjack et gagnez avec des paris",
            },
            "daily_name": {"en-GB": "daily", "en-US": "daily", "fr": "quotidien"},
            "daily_desc": {
                "en-GB": "Claim your daily QP reward",
                "en-US": "Claim your daily QP reward",
                "fr": "Réclamez votre récompense quotidienne de QP",
            },
            "balance_name": {"en-GB": "balance", "en-US": "balance", "fr": "solde"},
            "balance_desc": {
                "en-GB": "Check your or another user's balance",
                "en-US": "Check your or another user's balance",
                "fr": "Vérifiez votre solde ou celui d'un autre utilisateur",
            },
            "vote_name": {"en-GB": "vote", "en-US": "vote", "fr": "voter"},
            "vote_desc": {
                "en-GB": "Vote for Jeanne on Top.gg",
                "en-US": "Vote for Jeanne on Top.gg",
                "fr": "Votez pour Jeanne sur Top.gg",
            },
            #fun commands
            "8ball_name": {"en-GB": "8ball", "en-US": "8ball", "fr": "8ball"},
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
            "reverse_name": {"en-GB": "reverse", "en-US": "reverse", "fr": "inverse"},
            "reverse_desc": {
                "en-GB": "Say something and I will say it in reversed text",
                "en-US": "Say something and I will say it in reversed text",
                "fr": "Dites quelque chose et je le dirai dans un texte inversé",
            },
            "text_parm_name": {"en-GB": "text", "en-US": "text", "fr": "texte"},
            "text_parm_desc": {
                "en-GB": "What are you reversing?",
                "en-US": "What are you reversing?",
                "fr": "Qu'est-ce que vous inversez?",
            },
            "combine_name": {"en-GB": "combine", "en-US": "combine", "fr": "combiner"},
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
            "choose_name": {"en-GB": "choose", "en-US": "choose", "fr": "choisir"},
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
            "animeme_name": {"en-GB": "animeme", "en-US": "animeme", "fr": "animeme"},
            "animeme_desc": {
                "en-GB": "Get a random animeme",
                "en-US": "Get a random animeme",
                "fr": "Obtenez un animeme aléatoire",
            },
            "gayrate_name": {
                "en-GB": "gayrate",
                "en-US": "gayrate",
                "fr": "taux_de_gay",
            },
            "gayrate_desc": {
                "en-GB": "Get a random gay rate for you or someone else",
                "en-US": "Get a random gay rate for you or someone else",
                "fr": "Obtenez un taux de gay aléatoire pour vous ou quelqu'un d'autre",
            },
            "gayrate_name": {
                "en-GB": "gayrate",
                "en-US": "gayrate",
                "fr": "taux_de_gay",
            },
            "gayrate_desc": {
                "en-GB": "Get a random gay rate for you or someone else",
                "en-US": "Get a random gay rate for you or someone else",
                "fr": "Obtenez un taux de gay aléatoire pour vous ou quelqu'un d'autre",
            },
            "help_group_name": {"en-GB": "help", "en-US": "help", "fr": "aide"},
            "command_name": {"en-GB": "command", "en-US": "command", "fr": "commande"},
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
            "support_name": {"en-GB": "support", "en-US": "support", "fr": "soutien"},
            "support_desc": {
                "en-GB": "Need help? Visit the website or join the server for further assistance.",
                "en-US": "Need help? Visit the website or join the server for further assistance.",
                "fr": "Besoin d'aide ? Visitez le site web ou rejoignez le serveur pour plus d'assistance.",
            },
            #hentai commands
            "hentai_name": {"en-GB": "hentai", "en-US": "hentai", "fr": "hentai"},
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
            "tag_parm_name": {"en-GB": "tag", "en-US": "tag", "fr": "tag"},
            "tag_parm_desc": {
                "en-GB": "Add your tag",
                "en-US": "Add your tag",
                "fr": "Ajoutez votre tags",
            },
            "plus_parm_name": {"en-GB": "plus", "en-US": "plus", "fr": "plus"},
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
            #image commands
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
                "fr": "Obtenez une image de Medusa aléatoire",
            },
            "morgan_desc": {
                "en-GB": "Get a random image of Morgan Le Fay",
                "en-US": "Get a random image of Morgan Le Fay",
                "fr": "Obtenez une image de Morgan Le Fay aléatoire",
            },
            "safebooru_desc": {
                "en-GB": "Get a random image from Safebooru",
                "en-US": "Get a random image from Safebooru",
                "fr": "Obtenez une image aléatoire de Safebooru",
            },
            #info commands
            "stats_name": {"en-GB": "stats", "en-US": "stats", "fr": "stats"},
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
            "avatar_name": {
                "en-GB": "avatar",
                "en-US": "avatar",
                "fr": "avatar",
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
            "sticker_name": {
                "en-GB": "sticker",
                "en-US": "sticker",
                "fr": "sticker",
            },
            "sticker_desc": {
                "en-GB": "Views a sticker",
                "en-US": "Views a sticker",
                "fr": "Voir un sticker",
            },
            "sticker_parm_desc": {
                "en-GB": "Insert message ID with the sticker or name of the sticker in the server",
                "en-US": "Insert message ID with the sticker or name of the sticker in the server",
                "fr": "Insérez l'ID du message avec l'autocollant ou le nom de l'autocollant dans le serveur",
            },
            "emoji_desc": {
                "en-GB": "View an emoji",
                "en-US": "View an emoji",
                "fr": "Voir un emoji",
            },
            "emoji_parm_desc": {
                "en-GB": "What is the name of the emoji?",
                "en-US": "What is the name of the emoji?",
                "fr": "Quel est le nom de l'emoji?",
            },
            #inventory commands
            "country_name": {"en-GB": "country", "en-US": "country", "fr": "pays"},
            "country_desc": {
                "en-GB": "Buy a country badge",
                "en-US": "Buy a country badge",
                "fr": "Acheter un badge de pays",
            },
            "backgrounds_name": {
                "en-GB": "backgrounds",
                "en-US": "backgrounds",
                "fr": "backgrounds",
            },
            "backgrounds_desc": {
                "en-GB": "Check all the wallpapers available",
                "en-US": "Check all the wallpapers available",
                "fr": "Vérifiez tous les fonds d'écran disponibles",
            },
            "buy-custom_name": {
                "en-GB": "buy-custom",
                "en-US": "buy-custom",
                "fr": "buy-custom",
            },
            "buy-custom_desc": {
                "en-GB": "Buy a custom background pic for your level card",
                "en-US": "Buy a custom background pic for your level card",
                "fr": "Acheter une image d'arrière-plan personnalisée pour votre carte de niveau",
            },
            "list_name": {"en-GB": "list", "en-US": "list", "fr": "liste"},
            "list_desc": {
                "en-GB": "Check which backgrounds you have",
                "en-US": "Check which backgrounds you have",
                "fr": "Vérifiez quels fonds d'écran vous avez",
            },
            "link_parm_name": {"en-GB": "link", "en-US": "link", "fr": "lien"},
            "link_parm_desc": {
                "en-GB": "Add an image link",
                "en-US": "Add an image link",
                "fr": "Ajouter un lien d'image",
            },
            #levelling commands
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
            "profile_name": {"en-GB": "profile", "en-US": "profile", "fr": "profil"},
            "profile_desc": {
                "en-GB": "See your profile or someone else's profile",
                "en-US": "See your profile or someone else's profile",
                "fr": "Voir votre profil ou celui de quelqu'un d'autre",
            },
            #manage commands. will continue later
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
            "name_parm_name": {"en-GB": "name", "en-US": "name", "fr": "nom"},
            "name_parm_desc": {
                "en-GB": "What will you name it?",
                "en-US": "What will you name it?",
                "fr": "Quel nom lui donnerez-vous?",
            },
            "topic_parm_name": {"en-GB": "topic", "en-US": "topic", "fr": "sujet"},
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
            "add_blacklist_ch_description": {
                "en-GB": "Blacklists a channel for gaining XP",
                "en-US": "Blacklists a channel for gaining XP",
                "fr": "Met en liste noire un canal pour gagner de l'XP",
            },
            "clone_channel_desc": {
                "en-GB": "Clone a channel",
                "en-US": "Clone a channel",
                "fr": "Cloner un canal",
            },
            "clone_channel_name": {"en-GB": "clone", "en-US": "clone", "fr": "cloner"},
            "voicechannel_name": {
                "en-GB": "voicechannel",
                "en-US": "voicechannel",
                "fr": "canal_vocal",
            },
            "category_name": {
                "en-GB": "category",
                "en-US": "category",
                "fr": "catégorie",
            },
            "stagechannel_name": {
                "en-GB": "stagechannel",
                "en-US": "stagechannel",
                "fr": "canal_scène",
            },
            "forum_name": {"en-GB": "forum", "en-US": "forum", "fr": "forum"},
            "role_name": {"en-GB": "role", "en-US": "role", "fr": "rôle"},
            "public_thread_name": {
                "en-GB": "public-thread",
                "en-US": "public-thread",
                "fr": "fil-public",
            },
            "private_thread_name": {
                "en-GB": "private-thread",
                "en-US": "private-thread",
                "fr": "fil-privé",
            },
            "emoji_name": {"en-GB": "emoji", "en-US": "emoji", "fr": "emoji"},
            "sticker_name": {
                "en-GB": "sticker",
                "en-US": "sticker",
                "fr": "autocollant",
            },
            "delete_channel_name": {
                "en-GB": "delete-channel",
                "en-US": "delete-channel",
                "fr": "supprimer-canal",
            },
            "delete_role_name": {
                "en-GB": "delete-role",
                "en-US": "delete-role",
                "fr": "supprimer-rôle",
            },
            "delete_emoji_name": {
                "en-GB": "delete-emoji",
                "en-US": "delete-emoji",
                "fr": "supprimer-emoji",
            },
            "delete_sticker_name": {
                "en-GB": "delete-sticker",
                "en-US": "delete-sticker",
                "fr": "supprimer-autocollant",
            },
            "edit_textchannel_name": {
                "en-GB": "edit-textchannel",
                "en-US": "edit-textchannel",
                "fr": "modifier-canal-texte",
            },
            "edit_voicechannel_name": {
                "en-GB": "edit-voicechannel",
                "en-US": "edit-voicechannel",
                "fr": "modifier-canal-vocal",
            },
            "edit_role_name": {
                "en-GB": "edit-role",
                "en-US": "edit-role",
                "fr": "modifier-rôle",
            },
            "edit_server_name": {
                "en-GB": "edit-server",
                "en-US": "edit-server",
                "fr": "modifier-serveur",
            },
            "set_welcomer_name": {
                "en-GB": "set-welcomer",
                "en-US": "set-welcomer",
                "fr": "définir-accueil",
            },
            "set_modlog_name": {
                "en-GB": "set-modlog",
                "en-US": "set-modlog",
                "fr": "définir-journal-mod",
            },
            "set_welcomingmsg_name": {
                "en-GB": "set-welcomingmsg",
                "en-US": "set-welcomingmsg",
                "fr": "définir-message-accueil",
            },
            "set_leavingmsg_name": {
                "en-GB": "set-leavingmsg",
                "en-US": "set-leavingmsg",
                "fr": "définir-message-départ",
            },
            "set_rolereward_message_name": {
                "en-GB": "set-rolereward-message",
                "en-US": "set-rolereward-message",
                "fr": "définir-message-récompense-rôle",
            },
            "set_levelupdate_name": {
                "en-GB": "set-levelupdate",
                "en-US": "set-levelupdate",
                "fr": "définir-niveau-mise-à-jour",
            },
            "set_confessionchannel_name": {
                "en-GB": "set-confessionchannel",
                "en-US": "set-confessionchannel",
                "fr": "définir-canal-confession",
            },
            "set_brightness_name": {
                "en-GB": "set-brightness",
                "en-US": "set-brightness",
                "fr": "définir-luminosité",
            },
            "set_bio_name": {
                "en-GB": "set-bio",
                "en-US": "set-bio",
                "fr": "définir-bio",
            },
            "set_color_name": {
                "en-GB": "set-color",
                "en-US": "set-color",
                "fr": "définir-couleur",
            },
            "add_role_name": {
                "en-GB": "add-role",
                "en-US": "add-role",
                "fr": "ajouter-rôle",
            },
            "remove_role_name": {
                "en-GB": "remove-role",
                "en-US": "remove-role",
                "fr": "supprimer-rôle",
            },
            "remove_name": {"en-GB": "remove", "en-US": "remove", "fr": "supprimer"},
            "remove_description": {
                "en-GB": "Remove a role from a member",
                "en-US": "Remove a role from a member",
                "fr": "Supprimer un rôle d'un membre",
            },
            "list_disabled_commands_name": {
                "en-GB": "list-disabled",
                "en-US": "list-disabled",
                "fr": "lister-désactivé",
            },
            "list_disabled_cmds_description": {
                "en-GB": "List all disabled commands in the server",
                "en-US": "List all disabled commands in the server",
                "fr": "Lister toutes les commandes désactivées sur le serveur",
            },
            "blacklist_channel_group_name": {
                "en-GB": "blacklist-channel",
                "en-US": "blacklist-channel",
                "fr": "liste-noire-canal",
            },
            "add_blacklist_channel_name": {
                "en-GB": "add",
                "en-US": "add",
                "fr": "ajouter",
            },
            "remove_blacklist_channel_name": {
                "en-GB": "remove",
                "en-US": "remove",
                "fr": "supprimer",
            },
            "list_blacklist_channels_name": {
                "en-GB": "list",
                "en-US": "list",
                "fr": "liste",
            },
            "list_blacklist_channels_desc": {
                "en-GB": "List all blacklisted channels for gaining XP",
                "en-US": "List all blacklisted channels for gaining XP",
                "fr": "Lister tous les canaux mis en liste noire pour gagner de l'XP",
            },
            "add_role_reward_level_name": {
                "en-GB": "add",
                "en-US": "add",
                "fr": "ajouter",
            },
            "add_role_reward_name": {"en-GB": "add", "en-US": "add", "fr": "ajouter"},
            "add_role_reward_description": {
                "en-GB": "Add a role reward for a level",
                "en-US": "Add a role reward for a level",
                "fr": "Ajouter une récompense de rôle pour un niveau",
            },
            "add_role_reward_role_desc": {
                "en-GB": "What role do you want to add?",
                "en-US": "What role do you want to add?",
                "fr": "Quel rôle voulez-vous ajouter?",
            },
            "add_role_reward_role_name": {
                "en-GB": "role",
                "en-US": "role",
                "fr": "rôle",
            },
            "remove_role_reward_role_name": {
                "en-GB": "role",
                "en-US": "role",
                "fr": "rôle",
            },
            "remove_role_reward_description": {
                "en-GB": "Remove a role reward for a level",
                "en-US": "Remove a role reward for a level",
                "fr": "Supprimer une récompense de rôle pour un niveau",
            },
            "remove_role_reward_role_desc": {
                "en-GB": "What role do you want to remove?",
                "en-US": "What role do you want to remove?",
                "fr": "Quel rôle voulez-vous supprimer?",
            },
            "list_role_rewards_name": {"en-GB": "list", "en-US": "list", "fr": "liste"},
            "list_role_rewards_description": {
                "en-GB": "List all role rewards for levels",
                "en-US": "List all role rewards for levels",
                "fr": "Lister toutes les récompenses de rôle pour les niveaux",
            },
            "role_reward_group_name": {
                "en-GB": "role-reward",
                "en-US": "role-reward",
                "fr": "récompense-rôle",
            },
            "add_blacklist_ch_channel_name": {
                "en-GB": "add",
                "en-US": "add",
                "fr": "ajouter",
            },
            "remove_blacklist_channel_name": {
                "en-GB": "remove",
                "en-US": "remove",
                "fr": "supprimer",
            },
            "remove_blacklist_ch_description": {
                "en-GB": "Remove a channel from the blacklist for gaining XP",
                "en-US": "Remove a channel from the blacklist for gaining XP",
                "fr": "Supprimer un canal de la liste noire pour gagner de l'XP",
            },
            "remove_blacklist_ch_channel_desc": {
                "en-GB": "What channel do you want to remove?",
                "en-US": "What channel do you want to remove?",
                "fr": "Quel canal voulez-vous supprimer?",
            },
            "remove_blcklist_ch_channel_name": {
                "en-GB": "channel",
                "en-US": "channel",
                "fr": "canal",
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
            "color_parm_name": {"en-GB": "color", "en-US": "color", "fr": "couleur"},
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
            "ban_name": {"en-GB": "ban", "en-US": "ban", "fr": "bannir"},
            "warn_name": {"en-GB": "warn", "en-US": "warn", "fr": "avertir"},
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
            "kick_name": {"en-GB": "kick", "en-US": "kick", "fr": "expulser"},
            "prune_name": {"en-GB": "prune", "en-US": "prune", "fr": "purger"},
            "change_nickname_name": {
                "en-GB": "change-nickname",
                "en-US": "change-nickname",
                "fr": "changer-surnom",
            },
            "unban_name": {"en-GB": "unban", "en-US": "unban", "fr": "débannir"},
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
            "member_param_name": {"en-GB": "member", "en-US": "member", "fr": "membre"},
            "reason_param_name": {"en-GB": "reason", "en-US": "reason", "fr": "raison"},
            "delete_msg_history_param_name": {
                "en-GB": "delete_message_history",
                "en-US": "delete_message_history",
                "fr": "supprimer_historique_messages",
            },
            "time_param_name": {"en-GB": "time", "en-US": "time", "fr": "temps"},
            "warn_id_param_name": {
                "en-GB": "warn_id",
                "en-US": "warn_id",
                "fr": "id_avertissement",
            },
            "limit_param_name": {"en-GB": "limit", "en-US": "limit", "fr": "limite"},
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
            "delete_msg_history_param_desc": {
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
            "hug_name": {"en-GB": "hug", "en-US": "hug", "fr": "câlin"},
            "slap_name": {"en-GB": "slap", "en-US": "slap", "fr": "gifler"},
            "smug_name": {"en-GB": "smug", "en-US": "smug", "fr": "suffisant"},
            "poke_name": {"en-GB": "poke", "en-US": "poke", "fr": "pousser"},
            "pat_name": {"en-GB": "pat", "en-US": "pat", "fr": "tapoter"},
            "kiss_name": {"en-GB": "kiss", "en-US": "kiss", "fr": "embrasser"},
            "tickle_name": {"en-GB": "tickle", "en-US": "tickle", "fr": "chatouiller"},
            "baka_name": {"en-GB": "baka", "en-US": "baka", "fr": "baka"},
            "feed_name": {"en-GB": "feed", "en-US": "feed", "fr": "nourrir"},
            "cry_name": {"en-GB": "cry", "en-US": "cry", "fr": "pleurer"},
            "bite_name": {"en-GB": "bite", "en-US": "bite", "fr": "mordre"},
            "blush_name": {"en-GB": "blush", "en-US": "blush", "fr": "rougir"},
            "cuddle_name": {"en-GB": "cuddle", "en-US": "cuddle", "fr": "câliner"},
            "dance_name": {"en-GB": "dance", "en-US": "dance", "fr": "danser"},
            "hug_desc": {
                "en-GB": "Hug someone or yourself",
                "en-US": "Hug someone or yourself",
                "fr": "Faites un câlin à quelqu'un ou à vous-même",
            },
            "slap_desc": {
                "en-GB": "Slap someone or yourself",
                "en-US": "Slap someone or yourself",
                "fr": "Gifle quelqu'un ou vous-même",
            },
            "smug_desc": {
                "en-GB": "Show a smug expression",
                "en-US": "Show a smug expression",
                "fr": "Affichez une expression suffisante",
            },
            "poke_desc": {
                "en-GB": "Poke someone or yourself",
                "en-US": "Poke someone or yourself",
                "fr": "Poussez quelqu'un ou vous-même",
            },
            "pat_desc": {
                "en-GB": "Pat someone or yourself",
                "en-US": "Pat someone or yourself",
                "fr": "Tapotez quelqu'un ou vous-même",
            },
            "kiss_desc": {
                "en-GB": "Kiss someone or yourself",
                "en-US": "Kiss someone or yourself",
                "fr": "Embrassez quelqu'un ou vous-même",
            },
            "tickle_desc": {
                "en-GB": "Tickle someone or yourself",
                "en-US": "Tickle someone or yourself",
                "fr": "Chatouillez quelqu'un ou vous-même",
            },
            "baka_desc": {
                "en-GB": "Call someone or yourself a baka!",
                "en-US": "Call someone or yourself a baka!",
                "fr": "Traitez quelqu'un ou vous-même de baka !",
            },
            "feed_desc": {
                "en-GB": "Feed someone or yourself",
                "en-US": "Feed someone or yourself",
                "fr": "Nourrissez quelqu'un ou vous-même",
            },
            "cry_desc": {
                "en-GB": "Show a crying expression",
                "en-US": "Show a crying expression",
                "fr": "Affichez une expression de pleurs",
            },
            "bite_desc": {
                "en-GB": "Bite someone or yourself",
                "en-US": "Bite someone or yourself",
                "fr": "Mordez quelqu'un ou vous-même",
            },
            "blush_desc": {
                "en-GB": "Show a blushing expression",
                "en-US": "Show a blushing expression",
                "fr": "Affichez une expression rougissante",
            },
            "cuddle_desc": {
                "en-GB": "Cuddle with someone or yourself",
                "en-US": "Cuddle with someone or yourself",
                "fr": "Câlinez quelqu'un ou vous-même",
            },
            "dance_desc": {
                "en-GB": "Dance with someone or yourself",
                "en-US": "Dance with someone or yourself",
                "fr": "Dansez avec quelqu'un ou vous-même",
            },
            "member_parm_name": {"en-GB": "member", "en-US": "member", "fr": "membre"},
            "hug_member_parm_desc": {
                "en-GB": "Who are you hugging?",
                "en-US": "Who are you hugging?",
                "fr": "Qui câlinez-vous ?",
            },
            "slap_member_parm_desc": {
                "en-GB": "Who are you slapping?",
                "en-US": "Who are you slapping?",
                "fr": "Qui giflez-vous ?",
            },
            "poke_member_parm_desc": {
                "en-GB": "Who are you poking?",
                "en-US": "Who are you poking?",
                "fr": "Qui poussez-vous ?",
            },
            "pat_member_parm_desc": {
                "en-GB": "Who are you patting?",
                "en-US": "Who are you patting?",
                "fr": "Qui tapotez-vous ?",
            },
            "kiss_member_parm_desc": {
                "en-GB": "Who are you kissing?",
                "en-US": "Who are you kissing?",
                "fr": "Qui embrassez-vous ?",
            },
            "tickle_member_parm_desc": {
                "en-GB": "Who are you tickling?",
                "en-US": "Who are you tickling?",
                "fr": "Qui chatouillez-vous ?",
            },
            "baka_member_parm_desc": {
                "en-GB": "Who are you calling a baka?",
                "en-US": "Who are you calling a baka?",
                "fr": "Qui traitez-vous de baka ?",
            },
            "feed_member_parm_desc": {
                "en-GB": "Who are you feeding?",
                "en-US": "Who are you feeding?",
                "fr": "Qui nourrissez-vous ?",
            },
            "bite_member_parm_desc": {
                "en-GB": "Who are you biting?",
                "en-US": "Who are you biting?",
                "fr": "Qui mordez-vous ?",
            },
            "cuddle_member_parm_desc": {
                "en-GB": "Who are you cuddling with?",
                "en-US": "Who are you cuddling with?",
                "fr": "Avec qui câlinez-vous ?",
            },
            "dance_member_parm_desc": {
                "en-GB": "Who are you dancing with?",
                "en-US": "Who are you dancing with?",
                "fr": "Avec qui dansez-vous ?",
            },
            "generate_name": {
                "en-GB": "generate",
                "en-US": "generate",
                "fr": "générer",
            },
            "generate_desc": {
                "en-GB": "Generates an embed message. Use Discohook.org for JSON generation.",
                "en-US": "Generates an embed message. Use Discohook.org for JSON generation.",
                "fr": "Génère un message embed. Utilisez Discohook.org pour générer le JSON.",
            },
            "generate_channel_parm_name": {
                "en-GB": "channel",
                "en-US": "channel",
                "fr": "canal",
            },
            "generate_channel_parm_desc": {
                "en-GB": "Target channel",
                "en-US": "Target channel",
                "fr": "Canal cible",
            },
            "generate_jsonscript_parm_name": {
                "en-GB": "jsonscript",
                "en-US": "jsonscript",
                "fr": "jsonscript",
            },
            "generate_jsonscript_parm_desc": {
                "en-GB": "JSON script",
                "en-US": "JSON script",
                "fr": "Script JSON",
            },
            "generate_jsonfile_parm_name": {
                "en-GB": "jsonfile",
                "en-US": "jsonfile",
                "fr": "fichierjson",
            },
            "generate_jsonfile_parm_desc": {
                "en-GB": "JSON file",
                "en-US": "JSON file",
                "fr": "Fichier JSON",
            },
            "edit_name": {"en-GB": "edit", "en-US": "edit", "fr": "éditer"},
            "edit_desc": {
                "en-GB": "Edits an embed message. Use Discohook.org for JSON generation.",
                "en-US": "Edits an embed message. Use Discohook.org for JSON generation.",
                "fr": "Modifie un message embed. Utilisez Discohook.org pour générer le JSON.",
            },
            "edit_channel_parm_name": {
                "en-GB": "channel",
                "en-US": "channel",
                "fr": "canal",
            },
            "edit_channel_parm_desc": {
                "en-GB": "Channel of the message",
                "en-US": "Channel of the message",
                "fr": "Canal du message",
            },
            "edit_messageid_parm_name": {
                "en-GB": "messageid",
                "en-US": "messageid",
                "fr": "idmessage",
            },
            "edit_messageid_parm_desc": {
                "en-GB": "Message ID",
                "en-US": "Message ID",
                "fr": "ID du message",
            },
            "edit_jsonscript_parm_name": {
                "en-GB": "jsonscript",
                "en-US": "jsonscript",
                "fr": "jsonscript",
            },
            "edit_jsonscript_parm_desc": {
                "en-GB": "JSON script",
                "en-US": "JSON script",
                "fr": "Script JSON",
            },
            "edit_jsonfile_parm_name": {
                "en-GB": "jsonfile",
                "en-US": "jsonfile",
                "fr": "fichierjson",
            },
            "edit_jsonfile_parm_desc": {
                "en-GB": "JSON file",
                "en-US": "JSON file",
                "fr": "Fichier JSON",
            },
            "reminder_add_name": {"en-GB": "add", "en-US": "add", "fr": "ajouter"},
            "reminder_add_desc": {
                "en-GB": "Add a reminder",
                "en-US": "Add a reminder",
                "fr": "Ajouter un rappel",
            },
            "reminder_add_reason_parm_name": {
                "en-GB": "reason",
                "en-US": "reason",
                "fr": "raison",
            },
            "reminder_add_reason_parm_desc": {
                "en-GB": "Reason for the reminder",
                "en-US": "Reason for the reminder",
                "fr": "Raison du rappel",
            },
            "reminder_add_time_parm_name": {
                "en-GB": "time",
                "en-US": "time",
                "fr": "temps",
            },
            "reminder_add_time_parm_desc": {
                "en-GB": "Time (e.g., 1h, 30m)",
                "en-US": "Time (e.g., 1h, 30m)",
                "fr": "Temps (ex: 1h, 30m)",
            },
            "reminder_list_name": {"en-GB": "list", "en-US": "list", "fr": "liste"},
            "reminder_list_desc": {
                "en-GB": "List all the reminders you have",
                "en-US": "List all the reminders you have",
                "fr": "Lister tous vos rappels",
            },
            "reminder_cancel_name": {
                "en-GB": "cancel",
                "en-US": "cancel",
                "fr": "annuler",
            },
            "reminder_cancel_desc": {
                "en-GB": "Cancel a reminder",
                "en-US": "Cancel a reminder",
                "fr": "Annuler un rappel",
            },
            "reminder_cancel_reminder_id_parm_name": {
                "en-GB": "reminder_id",
                "en-US": "reminder_id",
                "fr": "id_rappel",
            },
            "reminder_cancel_rmd_id_parm_desc": {
                "en-GB": "Reminder ID",
                "en-US": "Reminder ID",
                "fr": "ID du rappel",
            },
            "weather_name": {"en-GB": "weather", "en-US": "weather", "fr": "météo"},
            "weather_desc": {
                "en-GB": "Get weather information on a city",
                "en-US": "Get weather information on a city",
                "fr": "Obtenir les informations météo d'une ville",
            },
            "weather_city_parm_name": {"en-GB": "city", "en-US": "city", "fr": "ville"},
            "weather_city_parm_desc": {
                "en-GB": "Add a city",
                "en-US": "Add a city",
                "fr": "Ajouter une ville",
            },
            "weather_units_parm_name": {
                "en-GB": "units",
                "en-US": "units",
                "fr": "unités",
            },
            "weather_units_parm_desc": {
                "en-GB": "Metric or Imperial? (Default is metric)",
                "en-US": "Metric or Imperial? (Default is metric)",
                "fr": "Métrique ou Impérial ? (Par défaut métrique)",
            },
            "weather_three_day_parm_name": {
                "en-GB": "three_day",
                "en-US": "three_day",
                "fr": "trois_jours",
            },
            "weather_three_day_parm_desc": {
                "en-GB": "Show 3 day forecast?",
                "en-US": "Show 3 day forecast?",
                "fr": "Afficher la prévision sur 3 jours ?",
            },
            "calculator_name": {
                "en-GB": "calculator",
                "en-US": "calculator",
                "fr": "calculatrice",
            },
            "calculator_desc": {
                "en-GB": "Do a calculation",
                "en-US": "Do a calculation",
                "fr": "Faire un calcul",
            },
            "calculator_calculate_parm_name": {
                "en-GB": "calculate",
                "en-US": "calculate",
                "fr": "calcul",
            },
            "calculator_calculate_parm_desc": {
                "en-GB": "Add a calculation",
                "en-US": "Add a calculation",
                "fr": "Ajouter un calcul",
            },
            "invite_name": {"en-GB": "invite", "en-US": "invite", "fr": "inviter"},
            "invite_desc": {
                "en-GB": "Invite me to your server or join the support server",
                "en-US": "Invite me to your server or join the support server",
                "fr": "Invitez-moi sur votre serveur ou rejoignez le serveur de support",
            },
            "botreport_name": {
                "en-GB": "botreport",
                "en-US": "botreport",
                "fr": "rapportbot",
            },
            "botreport_desc": {
                "en-GB": "Submit a bot report if you found something wrong",
                "en-US": "Submit a bot report if you found something wrong",
                "fr": "Soumettez un rapport si vous avez trouvé un problème",
            },
            "botreport_type_parm_name": {
                "en-GB": "type",
                "en-US": "type",
                "fr": "type",
            },
            "botreport_type_parm_desc": {
                "en-GB": "Type of report",
                "en-US": "Type of report",
                "fr": "Type de rapport",
            },
            "dictionary_name": {
                "en-GB": "dictionary",
                "en-US": "dictionary",
                "fr": "dictionnaire",
            },
            "dictionary_desc": {
                "en-GB": "Check the meaning of a word",
                "en-US": "Check the meaning of a word",
                "fr": "Vérifiez la signification d'un mot",
            },
            "dictionary_word_parm_name": {
                "en-GB": "word",
                "en-US": "word",
                "fr": "mot",
            },
            "dictionary_word_parm_desc": {
                "en-GB": "Word to check",
                "en-US": "Word to check",
                "fr": "Mot à vérifier",
            },
        }
        return translations.get(string.message, {}).get(locale.value)
