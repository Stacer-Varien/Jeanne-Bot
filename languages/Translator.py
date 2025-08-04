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
            "role_parm_desc": {
                "en-GB": "Which role?",
                "en-US": "Which role?",
                "fr": "Quel rôle?",
            },
            "level_parm_desc": {
                "en-GB": "Which level?",
                "en-US": "Which level?",
                "fr": "Quel niveau?",
            },
            "level_parm_name": {
                "en-GB": "level",
                "en-US": "level",
                "fr": "niveau",
            },
            "add_blacklist_ch_channel_desc": {
                "en-GB": "Which channel do you want to blacklist?",
                "en-US": "Which channel do you want to blacklist?",
                "fr": "Quel canal voulez-vous mettre sur liste noire?",
            },
            "remove_blacklist_ch_channel_desc": {
                "en-GB": "Which channel do you want to remove from the blacklist?",
                "en-US": "Which channel do you want to remove from the blacklist?",
                "fr": "Quel canal voulez-vous retirer de la liste noire?",
            },
            "clone_name_desc": {
                "en-GB": "If you want to change the name, what will you name it?",
                "en-US": "If you want to change the name, what will you name it?",
                "fr": "Si vous voulez changer le nom, comment l'appellerez-vous ?",
            },
            "background list_name": {
                "en-GB": "background list",
                "en-US": "background list",
                "fr": "background liste",
            },
            "guess_group_name free_name": {
                "en-GB": "guess free",
                "en-US": "guess free",
                "fr": "deviner libre",
            },
            "guess_group_name bet_name": {
                "en-GB": "guess bet",
                "en-US": "guess bet",
                "fr": "deviner pari",
            },
            "dice_group_name free_name": {
                "en-GB": "dice free",
                "en-US": "dice free",
                "fr": "dé libre",
            },
            "dice_group_name bet_name": {
                "en-GB": "dice bet",
                "en-US": "dice bet",
                "fr": "dé pari",
            },
            "flip_group_name free_name": {
                "en-GB": "flip free",
                "en-US": "flip free",
                "fr": "lancer libre",
            },
            "flip_group_name bet_name": {
                "en-GB": "flip bet",
                "en-US": "flip bet",
                "fr": "lancer pari",
            },
            "blackjack_group_name free_name": {
                "en-GB": "blackjack free",
                "en-US": "blackjack free",
                "fr": "blackjack libre",
            },
            "blackjack_group_name bet_name": {
                "en-GB": "blackjack bet",
                "en-US": "blackjack bet",
                "fr": "blackjack pari",
            },
            "guess_group_name": {"en-GB": "guess", "en-US": "guess", "fr": "deviner"},
            "dice_group_name": {"en-GB": "dice", "en-US": "dice", "fr": "dé"},
            "flip_group_name": {"en-GB": "flip", "en-US": "flip", "fr": "lancer"},
            "blackjack_group_name": {
                "en-GB": "blackjack",
                "en-US": "blackjack",
                "fr": "blackjack",
            },
            "help_group_name command_name": {
                "en-GB": "help command",
                "en-US": "help command",
                "fr": "aide commande",
            },
            "help_group_name support_name": {
                "en-GB": "help support",
                "en-US": "help support",
                "fr": "aide soutien",
            },
            "help_group_name": {
                "en-GB": "help",
                "en-US": "help",
                "fr": "aide",
            },
            "free_name": {"en-GB": "free", "en-US": "free", "fr": "libre"},
            "bet_name": {"en-GB": "bet", "en-US": "bet", "fr": "parier"},
            "guess_free_desc": {
                "en-GB": "Guess my number and you can win 20 QP",
                "en-US": "Guess my number and you can win 20 QP",
                "fr": "Devinez mon nombre et vous pouvez gagner 20 QP",
            },
            "guess_bet_desc": {
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
            # fun commands
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
            "simprate_desc": {
                "en-GB": "Check how much of a simp you or a member is",
                "en-US": "Check how much of a simp you or a member is",
                "fr": "Vérifiez à quel point vous ou un membre êtes un simp",
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
            "animeme_desc": {
                "en-GB": "Get a random animeme",
                "en-US": "Get a random animeme",
                "fr": "Obtenez un animeme aléatoire",
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
            "command_name": {"en-GB": "command", "en-US": "command", "fr": "commande"},
            "help_command_desc": {
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
            "disable_command_param_desc": {
                "en-GB": "Which command do you want to disable?",
                "en-US": "Which command do you want to disable?",
                "fr": "Quelle commande voulez-vous désactiver?",
            },
            "enable_command_param_desc": {
                "en-GB": "Which command do you want to enable?",
                "en-US": "Which command do you want to enable?",
                "fr": "Quelle commande voulez-vous activer?",
            },
            "support_name": {"en-GB": "support", "en-US": "support", "fr": "soutien"},
            "support_desc": {
                "en-GB": "Need help? Visit the website or join the server for further assistance.",
                "en-US": "Need help? Visit the website or join the server for further assistance.",
                "fr": "Besoin d'aide? Visitez le site web ou rejoignez le serveur pour plus d'assistance.",
            },
            # hentai commands
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
            # info commands
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
            "avatar_desc": {
                "en-GB": "See your avatar or another member's avatar",
                "en-US": "See your avatar or another member's avatar",
                "fr": "Voir votre avatar ou l'avatar d'un autre membre",
            },
            "ping_desc": {
                "en-GB": "Check how fast I respond to a command",
                "en-US": "Check how fast I respond to a command",
                "fr": "Vérifiez la rapidité de ma réponse à une commande",
            },
            "sticker_desc": {
                "en-GB": "Views a sticker",
                "en-US": "Views a sticker",
                "fr": "Voir un sticker",
            },
            "welcoming_channel_parm_desc": {
                "en-GB": "Which channel should welcome new members?",
                "en-US": "Which channel should welcome new members?",
                "fr": "Quel canal devrait accueillir les nouveaux membres?",
            },
            "leaving_channel_parm_desc": {
                "en-GB": "Which channel should say goodbye to members?",
                "en-US": "Which channel should say goodbye to members?",
                "fr": "Quel canal devrait dire au revoir aux membres?",
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
            # inventory commands
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
            # levelling commands
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
            "textchannel_name": {
                "en-GB": "textchannel",
                "en-US": "textchannel",
                "fr": "canal_texte",
            },
            "create": {"en-GB": "create", "en-US": "create", "fr": "créer"},
            "create textchannel_name": {
                "en-GB": "create textchannel",
                "en-US": "create textchannel",
                "fr": "créer un canal texte",
            },
            "create voicechannel_name": {
                "en-GB": "create voicechannel",
                "en-US": "create voicechannel",
                "fr": "créer un canal vocal",
            },
            "create category_name": {
                "en-GB": "create category",
                "en-US": "create category",
                "fr": "créer une catégorie",
            },
            "create stagechannel_name": {
                "en-GB": "create stagechannel",
                "en-US": "create stagechannel",
                "fr": "créer stagechannel",
            },
            "create forum_name": {
                "en-GB": "create forum",
                "en-US": "create forum",
                "fr": "créer forum",
            },
            "role_parm_name": {
                "en-GB": "role",
                "en-US": "role",
                "fr": "rôle",
            },
            "description_parm_name": {
                "en-GB": "description",
                "en-US": "description",
                "fr": "description",
            },
            "create role_name": {
                "en-GB": "create role",
                "en-US": "create role",
                "fr": "créer rôle",
            },
            "create thread": {
                "en-GB": "create thread",
                "en-US": "create thread",
                "fr": "créer thread",
            },
            "create thread public_thread_name": {
                "en-GB": "create thread public",
                "en-US": "create thread public",
                "fr": "créer thread public",
            },
            "create thread private_thread_name": {
                "en-GB": "create thread private",
                "en-US": "create thread private",
                "fr": "créer thread privé",
            },
            "create emoji_name": {
                "en-GB": "create emoji",
                "en-US": "create emoji",
                "fr": "créer emoji",
            },
            "create sticker_name": {
                "en-GB": "create sticker",
                "en-US": "create sticker",
                "fr": "créer sticker",
            },
            "textchannel_description": {
                "en-GB": "Create a text channel",
                "en-US": "Create a text channel",
                "fr": "Créer un canal texte",
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
            "rename_category_parm_desc": {
                "en-GB": "Which category?",
                "en-US": "Which category?",
                "fr": "Quelle catégorie?",
            },
            "slowmode_parm_name": {
                "en-GB": "slowmode",
                "en-US": "slowmode",
                "fr": "slowmode",
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
            "delete_channel_name": {
                "en-GB": "channel",
                "en-US": "channel",
                "fr": "canal",
            },
            "delete_role_name": {
                "en-GB": "role",
                "en-US": "role",
                "fr": "rôle",
            },
            "delete_emoji_name": {
                "en-GB": "emoji",
                "en-US": "emoji",
                "fr": "emoji",
            },
            "delete_sticker_name": {
                "en-GB": "sticker",
                "en-US": "sticker",
                "fr": "autocollant",
            },
            "edit_textchannel_name": {
                "en-GB": "textchannel",
                "en-US": "textchannel",
                "fr": "canal-texte",
            },
            "edit_voicechannel_name": {
                "en-GB": "voice-channel",
                "en-US": "voice-channel",
                "fr": "canal-vocal",
            },
            "edit_role_name": {
                "en-GB": "role",
                "en-US": "role",
                "fr": "rôle",
            },
            "edit_server_name": {
                "en-GB": "server",
                "en-US": "server",
                "fr": "serveur",
            },
            "set_welcomer_name": {
                "en-GB": "welcomer",
                "en-US": "welcomer",
                "fr": "accueil",
            },
            "set_modlog_name": {
                "en-GB": "modlog",
                "en-US": "modlog",
                "fr": "journal-mod",
            },
            "set_welcomingmsg_name": {
                "en-GB": "welcomingmsg",
                "en-US": "welcomingmsg",
                "fr": "message-accueil",
            },
            "set_leavingmsg_name": {
                "en-GB": "leavingmsg",
                "en-US": "leavingmsg",
                "fr": "message-départ",
            },
            "set_rolereward_message_name": {
                "en-GB": "rolereward-message",
                "en-US": "rolereward-message",
                "fr": "message-récompense-rôle",
            },
            "set_levelupdate_name": {
                "en-GB": "levelupdate",
                "en-US": "levelupdate",
                "fr": "niveau-mise-à-jour",
            },
            "set_confessionchannel_name": {
                "en-GB": "confession-channel",
                "en-US": "confession-channel",
                "fr": "canal-confession",
            },
            "set_confessionchannel_desc": {
                "en-GB": "Set the channel for confessions",
                "en-US": "Set the channel for confessions",
                "fr": "Définir le canal pour les confessions",
            },
            "set_brightness_name": {
                "en-GB": "profile-brightness",
                "en-US": "profile-brightness",
                "fr": "profile-luminosité",
            },
            "set_bio_name": {
                "en-GB": "profile-bio",
                "en-US": "profile-bio",
                "fr": "profile-bio",
            },
            "set_color_name": {
                "en-GB": "profile-color",
                "en-US": "profile-color",
                "fr": "profile-couleur",
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
            "edit edit_textchannel_name": {
                "en-GB": "edit textchannel",
                "en-US": "edit textchannel",
                "fr": "modifier canaltexte",
            },
            "edit edit_voicechannel_name": {
                "en-GB": "edit voicechannel",
                "en-US": "edit voicechannel",
                "fr": "modifier canalvocal",
            },
            "edit edit_role_name": {
                "en-GB": "edit role",
                "en-US": "edit role",
                "fr": "modifier rôle",
            },
            "edit edit_server_name": {
                "en-GB": "edit server",
                "en-US": "edit server",
                "fr": "modifier serveur",
            },
            "delete delete_channel_name": {
                "en-GB": "delete channel",
                "en-US": "delete channel",
                "fr": "supprimer canal",
            },
            "delete delete_role_name": {
                "en-GB": "delete role",
                "en-US": "delete role",
                "fr": "supprimer rôle",
            },
            "delete delete_emoji_name": {
                "en-GB": "delete emoji",
                "en-US": "delete emoji",
                "fr": "supprimer emoji",
            },
            "delete delete_sticker_name": {
                "en-GB": "delete sticker",
                "en-US": "delete sticker",
                "fr": "supprimer sticker",
            },
            "set": {
                "en-GB": "set",
                "en-US": "set",
                "fr": "définir",
            },
            "set set_welcomer_name": {
                "en-GB": "set welcomer",
                "en-US": "set welcomer",
                "fr": "définir accueil",
            },
            "set set_modlog_name": {
                "en-GB": "set modlog",
                "en-US": "set modlog",
                "fr": "définir modlog",
            },
            "set set_welcomingmsg_name": {
                "en-GB": "set welcomingmsg",
                "en-US": "set welcomingmsg",
                "fr": "définir welcomingmsg",
            },
            "set set_leavingmsg_name": {
                "en-GB": "set leavingmsg",
                "en-US": "set leavingmsg",
                "fr": "définir leavingmsg",
            },
            "set set_rolereward_message_name": {
                "en-GB": "set rolereward message",
                "en-US": "set rolereward message",
                "fr": "définir rolereward message",
            },
            "set set_levelupdate_name": {
                "en-GB": "set levelupdate",
                "en-US": "set levelupdate",
                "fr": "définir levelupdate",
            },
            "set set_confessionchannel_name": {
                "en-GB": "set confession-channel",
                "en-US": "set confession-channel",
                "fr": "définir confession-channel",
            },
            "set set_brightness_name": {
                "en-GB": "set profile-brightness",
                "en-US": "set profile-brightness",
                "fr": "définir profile-luminosité",
            },
            "set_color_description": {
                "en-GB": "Set your profile color",
                "en-US": "Set your profile color",
                "fr": "Définir votre profile couleur",
            },
            "set set_bio_name": {
                "en-GB": "set profile-bio",
                "en-US": "set profile-bio",
                "fr": "définir profile-bio",
            },
            "set set_color_name": {
                "en-GB": "set profile-color",
                "en-US": "set profile-color",
                "fr": "définir profile-couleur",
            },
            "rename": {
                "en-GB": "rename",
                "en-US": "rename",
                "fr": "renommer",
            },
            "rename rename_emoji_name": {
                "en-GB": "rename emoji",
                "en-US": "rename emoji",
                "fr": "renommer emoji",
            },
            "rename rename_category_name": {
                "en-GB": "rename category",
                "en-US": "rename category",
                "fr": "renommer catégorie",
            },
            "rename rename_sticker_name": {
                "en-GB": "rename sticker",
                "en-US": "rename sticker",
                "fr": "renommer sticker",
            },
            "command": {
                "en-GB": "command",
                "en-US": "command",
                "fr": "commande",
            },
            "command disable_command_name": {
                "en-GB": "disable command",
                "en-US": "disable command",
                "fr": "désactiver commande",
            },
            "command enable_command_name": {
                "en-GB": "enable command",
                "en-US": "enable command",
                "fr": "activer commande",
            },
            "command list_disabled_commands_name": {
                "en-GB": "list disabled commands",
                "en-US": "list disabled commands",
                "fr": "lister commandes désactivées",
            },
            "level role_reward_group_name add_role_reward_name": {
                "en-GB": "add role reward",
                "en-US": "add role reward",
                "fr": "ajouter role reward",
            },
            "level role_reward_group_name remove_role_reward_name": {
                "en-GB": "remove role reward",
                "en-US": "remove role reward",
                "fr": "supprimer role reward",
            },
            "level role_reward_group_name list_role_rewards_name": {
                "en-GB": "list role rewards",
                "en-US": "list role rewards",
                "fr": "lister role rewards",
            },
            "level blacklist_channel_group_name add_blacklist_channel_name": {
                "en-GB": "add blacklist channel",
                "en-US": "add blacklist channel",
                "fr": "ajouter blacklist canal",
            },
            "level blacklist_channel_group_name remove_blacklist_channel_name": {
                "en-GB": "remove blacklist channel",
                "en-US": "remove blacklist channel",
                "fr": "supprimer blacklist canal",
            },
            "level blacklist_channel_group_name list_blacklist_channels_name": {
                "en-GB": "list blacklist channels",
                "en-US": "list blacklist channels",
                "fr": "lister canaux liste noire",
            },
            "embed generate_name": {
                "en-GB": "embed generate",
                "en-US": "embed generate",
                "fr": "embed générer",
            },
            "embed edit_name": {
                "en-GB": "embed edit",
                "en-US": "embed edit",
                "fr": "embed modifier",
            },
            "weather_name": {
                "en-GB": "weather",
                "en-US": "weather",
                "fr": "météo",
            },
            "calculator_name": {
                "en-GB": "calculator",
                "en-US": "calculator",
                "fr": "calculatrice",
            },
            "invite_name": {
                "en-GB": "invite",
                "en-US": "invite",
                "fr": "inviter",
            },
            "botreport_name": {
                "en-GB": "botreport",
                "en-US": "botreport",
                "fr": "rapportbot",
            },
            "reminder": {
                "en-GB": "reminder",
                "en-US": "reminder",
                "fr": "rappel",
            },
            "reminder reminder_add_name": {
                "en-GB": "reminder add",
                "en-US": "reminder add",
                "fr": "rappel ajouter",
            },
            "reminder reminder_list_name": {
                "en-GB": "reminder list",
                "en-US": "reminder list",
                "fr": "rappels liste",
            },
            "reminder reminder_cancel_name": {
                "en-GB": "reminder cancel",
                "en-US": "reminder cancel",
                "fr": "rappel annuler",
            },
            "clone_name": {
                "en-GB": "clone",
                "en-US": "clone",
                "fr": "cloner",
            },
            "remove_name": {"en-GB": "remove", "en-US": "remove", "fr": "supprimer"},
            "remove_role_description": {
                "en-GB": "Remove a role from a member",
                "en-US": "Remove a role from a member",
                "fr": "Supprimer un rôle d'un membre",
            },
            "remove_description": {
                "en-GB": "Remove a feature from the server",
                "en-US": "Remove a feature from the server",
                "fr": "Supprimer une fonctionnalité du serveur",
            },
            "clone_description": {
                "en-GB": "Clone a channel",
                "en-US": "Clone a channel",
                "fr": "Cloner un canal",
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
            "disable_command_description": {
                "en-GB": "Disables a command",
                "en-US": "Disables a command",
                "fr": "Désactive une commande",
            },
            "enable_command_description": {
                "en-GB": "Enables a command",
                "en-US": "Enables a command",
                "fr": "Active une commande",
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
            "level": {
                "en-GB": "level",
                "en-US": "level",
                "fr": "niveau",
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
            "description_parm_desc": {
                "en-GB": "What is the description for the server?",
                "en-US": "What is the description for the server?",
                "fr": "Quelle est la description du serveur?",
            },
            "avatar_parm_desc": {
                "en-GB": "Insert an image for the avatar",
                "en-US": "Insert an image for the avatar",
                "fr": "Insérez une image pour l'avatar",
            },
            "splash_parm_desc": {
                "en-GB": "Insert an image for the splash",
                "en-US": "Insert an image for the splash",
                "fr": "Insérez une image pour le splash",
            },
            "banner_parm_desc": {
                "en-GB": "Insert an image for the banner",
                "en-US": "Insert an image for the banner",
                "fr": "Insérez une image pour la bannière",
            },
            "verification_level_parm_desc": {
                "en-GB": "What is the verification level?",
                "en-US": "What is the verification level?",
                "fr": "Quel est le niveau de vérification?",
            },
            "message_id_parm_desc": {
                "en-GB": "What is the message ID?",
                "en-US": "What is the message ID?",
                "fr": "Quel est l'ID du message?",
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
                "fr": "Supprime sticker",
            },
            "set_welcomer_description": {
                "en-GB": "Sets a welcomer and/or leaver channel",
                "en-US": "Sets a welcomer and/or leaver channel",
                "fr": "Définit un canal d'accueil et/ou de départ",
            },
            "set_modlog_description": {
                "en-GB": "Sets a modlog channel",
                "en-US": "Sets a modlog channel",
                "fr": "Définit un canal de journalisation des modérateurs",
            },
            "set_welcomingmsg_description": {
                "en-GB": "Sets a welcoming message when someone joins the server",
                "en-US": "Sets a welcoming message when someone joins the server",
                "fr": "Définit un message d'accueil lorsqu'une personne rejoint le serveur",
            },
            "set_leavingmsg_description": {
                "en-GB": "Sets a leaving message when someone leaves the server",
                "en-US": "Sets a leaving message when someone leaves the server",
                "fr": "Définit un message de départ lorsqu'une personne quitte le serveur",
            },
            "set_rolereward_message_description": {
                "en-GB": "Sets a role reward message when a user levels up",
                "en-US": "Sets a role reward message when a user levels up",
                "fr": "Définit un message de récompense de rôle lorsqu'un utilisateur monte de niveau",
            },
            "set_levelupdate_description": {
                "en-GB": "Sets a level up message when a user levels up",
                "en-US": "Sets a level up message when a user levels up",
                "fr": "Définit un message de montée de niveau lorsqu'un utilisateur monte de niveau",
            },
            "set_confessionchannel_description": {
                "en-GB": "Sets a confession channel",
                "en-US": "Sets a confession channel",
                "fr": "Définit un canal de confession",
            },
            "set_brightness_description": {
                "en-GB": "Sets your profile-brightness (50 - 150)",
                "en-US": "Sets your profile-brightness (50 - 150)",
                "fr": "Définit la profile-luminosité (50 - 150)",
            },
            "set_bio_description": {
                "en-GB": "Set your profile bio",
                "en-US": "Set your profile bio",
                "fr": "Définit la profile-bio",
            },
            "rename_emoji_description": {
                "en-GB": "Renames an emoji",
                "en-US": "Renames an emoji",
                "fr": "Renomme un emoji",
            },
            "rename_category_description": {
                "en-GB": "Renames a category",
                "en-US": "Renames a category",
                "fr": "Renomme une catégorie",
            },
            "rename_sticker_description": {
                "en-GB": "Renames a sticker",
                "en-US": "Renames a sticker",
                "fr": "Renomme sticker",
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
                "fr": "délai",
            },
            "timeout_remove_name": {
                "en-GB": "timeout-remove",
                "en-US": "timeout-remove",
                "fr": "retirer-sourdine",
            },
            "massban_name": {
                "en-GB": "massban",
                "en-US": "massban",
                "fr": "massban",
            },
            "massunban_name": {
                "en-GB": "massunban",
                "en-US": "massunban",
                "fr": "massunban",
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
            "delete": {
                "en-GB": "delete",
                "en-US": "delete",
                "fr": "supprimer",
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
            "unban_reason_parm": {
                "en-GB": "Why are they being unbanned?",
                "en-US": "Why are they being unbanned?",
                "fr": "Why are they being unbanned?",
            },
            "timeout_desc": {
                "en-GB": "Timeout a member",
                "en-US": "Timeout a member",
                "fr": "Mettre un membre en sourdine",
            },
            "timeout_remove_desc": {
                "en-GB": "Removes a member from timeout",
                "en-US": "Removes a member from timeout",
                "fr": "Supprime un membre du délai d'attente",
            },
            "timeout_remove_reason_desc": {
                "en-GB": "Why are you removing them from timeout?",
                "en-US": "Why are you removing them from timeout?",
                "fr": "Pourquoi les retirer du délai d'attente?",
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
                "fr": "warn_id",
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
                "fr": "user_id",
            },
            "user_ids_param_name": {
                "en-GB": "user_ids",
                "en-US": "user_ids",
                "fr": "user_ids",
            },
            "member_param_desc": {
                "en-GB": "What is the member or user ID?",
                "en-US": "What is the member or user ID?",
                "fr": "Quel est le membre ou l'ID utilisateur?",
            },
            "reason_param_desc": {
                "en-GB": "What did they do? You can also make a custom reason",
                "en-US": "What did they do? You can also make a custom reason",
                "fr": "Qu'ont-ils fait? Vous pouvez également créer une raison personnalisée",
            },
            "delete_msg_history_param_desc": {
                "en-GB": "Delete messages from past 7 days?",
                "en-US": "Delete messages from past 7 days?",
                "fr": "Supprimer les messages des 7 derniers jours?",
            },
            "temp_time_param_desc": {
                "en-GB": "How long should they be tempbanned? (1m, 1h30m, etc)",
                "en-US": "How long should they be tempbanned? (1m, 1h30m, etc)",
                "fr": "Combien de temps doivent-ils être temporairement bannis? (1m, 1h30m, etc)",
            },
            "timeout_time_desc": {
                "en-GB": "How long should they be on timeout? (1m, 1h30m, etc) Max is 27 days",
                "en-US": "How long should they be on timeout? (1m, 1h30m, etc) Max is 27 days",
                "fr": "Combien de temps doivent-ils être en pause? (1m, 1h30m, etc) Max est 27 jours",
            },
            "warn_id_param_desc": {
                "en-GB": "What is their warn ID you want to remove?",
                "en-US": "What is their warn ID you want to remove?",
                "fr": "Quel est leur ID d'avertissement que vous souhaitez supprimer?",
            },
            "limit_param_desc": {
                "en-GB": "How many messages? (max is 100)",
                "en-US": "How many messages? (max is 100)",
                "fr": "Combien de messages? (max est 100)",
            },
            "nickname_param_desc": {
                "en-GB": "What is their new nickname?",
                "en-US": "What is their new nickname?",
                "fr": "Quel est leur nouveau surnom?",
            },
            "user_id_param_desc": {
                "en-GB": "Which user do you want to unban?",
                "en-US": "Which user do you want to unban?",
                "fr": "Quel utilisateur voulez-vous débannir?",
            },
            "user_ids_param_desc": {
                "en-GB": "How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
                "en-US": "How many user IDs? Leave a space after each ID (min is 5 and max is 25)",
                "fr": "Combien d'IDs utilisateur? Laissez un espace après chaque ID (min est 5 et max est 25)",
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
            "hug_member_parm_desc": {
                "en-GB": "Who are you hugging?",
                "en-US": "Who are you hugging?",
                "fr": "Qui câlinez-vous?",
            },
            "slap_member_parm_desc": {
                "en-GB": "Who are you slapping?",
                "en-US": "Who are you slapping?",
                "fr": "Qui giflez-vous?",
            },
            "poke_member_parm_desc": {
                "en-GB": "Who are you poking?",
                "en-US": "Who are you poking?",
                "fr": "Qui poussez-vous?",
            },
            "pat_member_parm_desc": {
                "en-GB": "Who are you patting?",
                "en-US": "Who are you patting?",
                "fr": "Qui tapotez-vous?",
            },
            "kiss_member_parm_desc": {
                "en-GB": "Who are you kissing?",
                "en-US": "Who are you kissing?",
                "fr": "Qui embrassez-vous?",
            },
            "tickle_member_parm_desc": {
                "en-GB": "Who are you tickling?",
                "en-US": "Who are you tickling?",
                "fr": "Qui chatouillez-vous?",
            },
            "baka_member_parm_desc": {
                "en-GB": "Who are you calling a baka?",
                "en-US": "Who are you calling a baka?",
                "fr": "Qui traitez-vous de baka?",
            },
            "feed_member_parm_desc": {
                "en-GB": "Who are you feeding?",
                "en-US": "Who are you feeding?",
                "fr": "Qui nourrissez-vous?",
            },
            "bite_member_parm_desc": {
                "en-GB": "Who are you biting?",
                "en-US": "Who are you biting?",
                "fr": "Qui mordez-vous?",
            },
            "cuddle_member_parm_desc": {
                "en-GB": "Who are you cuddling with?",
                "en-US": "Who are you cuddling with?",
                "fr": "Avec qui câlinez-vous?",
            },
            "dance_member_parm_desc": {
                "en-GB": "Who are you dancing with?",
                "en-US": "Who are you dancing with?",
                "fr": "Avec qui dansez-vous?",
            },
            "generate_name": {
                "en-GB": "generate",
                "en-US": "generate",
                "fr": "générer",
            },
            "generate_desc": {
                "en-GB": "Generates an embed message. Use Discohook.app for JSON generation.",
                "en-US": "Generates an embed message. Use Discohook.app for JSON generation.",
                "fr": "Génère un message embed. Utilisez Discohook.app pour générer le JSON.",
            },
            "edit_desc": {
                "en-GB": "Edits an embed message. Use Discohook.org for JSON generation.",
                "en-US": "Edits an embed message. Use Discohook.org for JSON generation.",
                "fr": "Modifie un message embed. Utilisez Discohook.org pour générer le JSON.",
            },
            "generate_channel_parm_name": {
                "en-GB": "channel",
                "en-US": "channel",
                "fr": "canal",
            },
            "channel_parm_name": {
                "en-GB": "channel",
                "en-US": "channel",
                "fr": "canal",
            },
            "welcomer_channel_parm_name": {
                "en-GB": "welcomer_channel",
                "en-US": "welcomer_channel",
                "fr": "canal_de_bienvenue",
            },
            "leaving_channel_parm_name": {
                "en-GB": "leaving_channel",
                "en-US": "leaving_channel",
                "fr": "canal_de_depart",
            },
            "generate_jsonscript_parm_name": {
                "en-GB": "jsonscript",
                "en-US": "jsonscript",
                "fr": "jsonscript",
            },
            "generate_jsonscript_parm_desc": {
                "en-GB": "Insert JSON script",
                "en-US": "Insert JSON script",
                "fr": "Insérer un script JSON",
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
            "edit": {"en-GB": "edit", "en-US": "edit", "fr": "éditer"},
            "edit_embed_desc": {
                "en-GB": "Edits an embed message. Use Discohook.org for JSON generation.",
                "en-US": "Edits an embed message. Use Discohook.org for JSON generation.",
                "fr": "Modifie un message embed. Utilisez Discohook.org pour générer le JSON.",
            },
            "channel_parm_desc": {
                "en-US": "Which channel?",
                "en-GB": "Which channel?",
                "fr": "Quel canal?",
            },
            "edit_channel_parm_desc": {
                "en-GB": "Channel of the message",
                "en-US": "Channel of the message",
                "fr": "Canal du message",
            },
            "message_id_parm_name": {
                "en-GB": "message_id",
                "en-US": "message_id",
                "fr": "message_id",
            },
            "edit_messageid_parm_desc": {
                "en-GB": "Message ID of the embed",
                "en-US": "Message ID of the embed",
                "fr": "ID du message de l'embed",
            },
            "jsonfile_parm_name": {
                "en-GB": "jsonfile",
                "en-US": "jsonfile",
                "fr": "fichierjson",
            },
            "jsonfile_parm_desc": {
                "en-GB": "Insert JSON file",
                "en-US": "Insert JSON file",
                "fr": "Insérer un fichier JSON",
            },
            "jsonscript_parm_desc": {
                "en-GB": "Insert JSON script",
                "en-US": "Insert JSON script",
                "fr": "Insérer un script JSON",
            },
            "message_parm_desc": {
                "en-GB": "What is the level reward message?",
                "en-US": "What is the level reward message?",
                "fr": "Quel est le message de récompense de niveau ?",
            },
            "levelmsg_parm_name": {
                "en-GB": "levelmsg",
                "en-US": "levelmsg",
                "fr": "message_niveau",
            },
            "levelmsg_parm_desc": {
                "en-GB": "What is the level up message?",
                "en-US": "What is the level up message?",
                "fr": "Quel est le message de montée de niveau ?",
            },
            "brightness_parm_desc": {
                "en-GB": "What is the brightness?",
                "en-US": "What is the brightness?",
                "fr": "Quelle est la luminosité ?",
            },
            "bio_parm_desc": {
                "en-GB": "Your bio text",
                "en-US": "Your bio text",
                "fr": "Votre texte de bio",
            },
            "rename_parm_desc": {
                "en-GB": "What is the new name?",
                "en-US": "What is the new name?",
                "fr": "Quel est le nouveau nom ?",
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
            "time_parm_name": {
                "en-GB": "time",
                "en-US": "time",
                "fr": "temps",
            },
            "reminder_cancel_rmd_id_parm_name": {
                "en-GB": "reminder_id",
                "en-US": "reminder_id",
                "fr": "id_rappel",
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
                "en-GB": "reminder id",
                "en-US": "reminder id",
                "fr": "id_rappel",
            },
            "reminder_cancel_rmd_id_parm_desc": {
                "en-GB": "Reminder ID",
                "en-US": "Reminder ID",
                "fr": "ID du rappel",
            },
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
                "fr": "Métrique ou Impérial? (Par défaut métrique)",
            },
            "weather_three_day_parm_name": {
                "en-GB": "three_day",
                "en-US": "three_day",
                "fr": "trois_jours",
            },
            "weather_three_day_parm_desc": {
                "en-GB": "Show 3 day forecast?",
                "en-US": "Show 3 day forecast?",
                "fr": "Afficher la prévision sur 3 jours?",
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
            "invite_desc": {
                "en-GB": "Invite me to your server or join the support server",
                "en-US": "Invite me to your server or join the support server",
                "fr": "Invitez-moi sur votre serveur ou rejoignez le serveur de support",
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
                "fr": "Vérifiez la signification d'un mot (Anglais seulement)",
            },
            "dictionary_word_parm_name": {
                "en-GB": "word",
                "en-US": "word",
                "fr": "mot",
            },
            "dictionary_word_parm_desc": {
                "en-GB": "Word to look up",
                "en-US": "Word to look up",
                "fr": "Mot à rechercher",
            },
            "confess_name": {
                "en-GB": "confess",
                "en-US": "confess",
                "fr": "confesser",
            },
            "confess_desc": {
                "en-GB": "Confess something anonymously or not",
                "en-US": "Confess something anonymously or not",
                "fr": "Confessez quelque chose de manière anonyme ou non",
            },
            "confession_parm_name": {
                "en-GB": "confession",
                "en-US": "confession",
                "fr": "confession",
            },
            "anonymous_parm_name": {
                "en-GB": "anonymous",
                "en-US": "anonymous",
                "fr": "anonyme",
            },
            "confession_parm_desc": {
                "en-GB": "What do you want to confess?",
                "en-US": "What do you want to confess?",
                "fr": "Que voulez-vous confesser?",
            },
            "anonymous_parm_desc": {
                "en-GB": "Do you want to confess anonymously?",
                "en-US": "Do you want to confess anonymously?",
                "fr": "Voulez-vous confesser anonymement?",
            },
            "reportconfession_id_parm_desc": {
                "en-GB": "What is the confession ID you want to report?",
                "en-US": "What is the confession ID you want to report?",
                "fr": "Quel est l'ID de la confession que vous souhaitez signaler?",
            },
            "reportconfession_name": {
                "en-GB": "report-confession",
                "en-US": "report-confession",
                "fr": "rapport-confession",
            },
            "reportconfession_desc": {
                "en-GB": "Report a confession",
                "en-US": "Report a confession",
                "fr": "Signaler une confession",
            },
            "reportconfession_id_parm_name": {
                "en-GB": "confession_id",
                "en-US": "confession_id",
                "fr": "id_confession",
            },
            "reportconfession_rsn_parm_desc": {
                "en-GB": "Why are you reporting this confession?",
                "en-US": "Why are you reporting this confession?",
                "fr": "Pourquoi signalez-vous cette confession?",
            },
            "add_role_description": {
                "en-GB": "Adds a role to a member",
                "en-US": "Adds a role to a member",
                "fr": "Ajoute un rôle à un membre",
            },
        }
        return translations.get(string.message, {}).get(locale.value)
