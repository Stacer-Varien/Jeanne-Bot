from random import choice, randint
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from functions import (
    DevPunishment,
)
from typing import Optional


class fun():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _8ball(self, ctx: Interaction, question: str):
        await ctx.response.defer()
        answers = [
            "C'est certain.",
            "C'est décidément ainsi.",
            "Sans aucun doute.",
            "Oui – définitivement.",
            "Vous pouvez compter dessus.",
            "D'après moi, oui.",
            "Très probable.",
            "Les perspectives sont bonnes.",
            "Oui.",
            "Les signes indiquent oui.",
            "Réponse floue, réessayez.",
            "Demandez à nouveau plus tard.",
            "Mieux vaut ne pas vous le dire maintenant.",
            "Impossible de prédire maintenant.",
            "Concentrez-vous et demandez à nouveau.",
            "Ne comptez pas dessus.",
            "Ma réponse est non.",
            "Mes sources disent non.",
            "Les perspectives ne sont pas si bonnes.",
            "Très douteux.",
            "Pourquoi me demander ? Faites-le simplement !",
            "Pourquoi me demander ? Ne le faites pas !",
            "Ouais... non",
            "Ouais... peu importe",
            "Ouais... je ne sais pas",
            "Oui ? Non ? Je ne sais pas !",
            "Absolument pas, et je suis offensé que vous ayez demandé.",
            "Bien sûr, si les étoiles s'alignent et que les cochons volent.",
            "Seulement les mardis.",
            "La réponse se trouve à l'intérieur... de votre frigo.",
            "Demandez à votre chat.",
            "Réessayez après un café.",
            "404 réponse introuvable.",
            "Vous n'êtes pas prêt pour cette vérité.",
            "Voulez-vous vraiment savoir ?",
            "Hmm... mes circuits magiques buguent.",
            "Je ne suis qu'une boule, pas un thérapeute.",
            "Laissez-moi réfléchir... non.",
            "Oui. Mais aussi non.",
            "Si je vous le disais, je devrais disparaître dans un nuage de fumée.",
        ]

        embed = Embed(color=Color.random())
        embed.add_field(name="Question :", value=question, inline=False)
        embed.add_field(name="Réponse :", value=choice(answers), inline=False)
        await ctx.followup.send(embed=embed)

    async def reverse(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        if any(word in text for word in ["riffak", "reggin", "aggin"]):
            await DevPunishment(ctx.user).add_botbanned_user(
                "Using the reversed version of a common racial slur"
            )
            return
        embed = Embed(description=text[::-1], color=Color.random()).set_footer(
            text=f"Auteur : {ctx.user} | {ctx.user.id}"
        )
        await ctx.followup.send(embed=embed)

    async def combine(self, ctx: Interaction, first_word: str, second_word: str):
        await ctx.response.defer()
        combine1 = (
            first_word[: len(first_word) // 2] + second_word[len(second_word) // 2 :]
        )
        combine2 = (
            first_word[len(first_word) // 2 :] + second_word[: len(second_word) // 2]
        )
        embed = Embed(
            description=f"**1er mot combiné** : {combine1}\n**2ème mot combiné** : {combine2}",
            color=Color.random(),
        ).set_author(name=f"{first_word} + {second_word}")
        await ctx.followup.send(embed=embed)

    async def choose(self, ctx: Interaction, choices: str):
        await ctx.response.defer()
        embed = Embed(
            description=f"J'ai choisi **{choice(choices.split(','))}**",
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)

    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member or ctx.user
        embed = Embed(
            description=f"Le taux de simp de {member} est de {perc}%", color=Color.random()
        )
        if perc >= 75:
            embed.set_image(url="https://i.imgur.com/W4u4Igk.jpg")
        elif perc >= 50:
            embed.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")
        await ctx.followup.send(embed=embed)

    async def gayrate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member or ctx.user
        embed = Embed(
            description=f"Le taux de gay de {member} est de {perc}%", color=Color.random()
        )
        if perc >= 75:
            embed.set_image(url="https://i.imgur.com/itOD0Da.png?1")
        elif perc >= 50:
            embed.set_image(url="https://i.imgur.com/tYAbWCl.jpg")
        await ctx.followup.send(embed=embed)

    async def roast(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        member = member if member else ctx.user
        ROASTS = [
            "a la confiance de quelqu’un qui n’a jamais eu tort — malgré des preuves accablantes",
            "écrit « lol » avec un visage totalement neutre",
            "pourrait trébucher sur un téléphone sans fil",
            "est l’équivalent humain d’un écran de chargement",
            "apporte une cuillère à un combat au couteau",
            "se perdrait dans un couloir à sens unique",
            "a une énergie de personnage principal mais des dialogues de PNJ",
            "dégage des vibes de « j’ai pas lu les instructions »",
            "est la preuve que le mode pilote automatique existe chez les humains",
            "a le temps de réaction d’Internet Explorer",
            "se disputerait avec un panneau STOP et perdrait quand même",
            "a la personnalité d’un poulet sans assaisonnement",
            "pense que « gaslight » est une marque de cuisinière",
            "ne pourrait pas verser de l’eau hors d’une botte même avec les instructions sur le talon",
            "a l’air du genre à applaudir quand l’avion atterrit",
            "a des pensées en Wi-Fi mais une exécution en modem 56k",
            "est la raison pour laquelle les travaux de groupe sont stressants",
            "fonctionne uniquement aux vibes, sans aucune pensée critique",
            "a la palette émotionnelle d’une petite cuillère",
            "appuierait deux fois sur le bouton de l’ascenseur comme si ça aidait",
            "dégage une grosse énergie de « fais-moi confiance frérot »",
            "est le boss final des mauvaises décisions",
            "écrit des paragraphes entiers pour ne rien dire",
            "a la conscience de son environnement d’une pomme de terre",
            "oublierait son propre anniversaire",
            "est littéralement construit comme un personnage placeholder",
            "pense que les céréales sont une soupe et défend cette opinion",
            "a l’ambition mais pas les compétences",
            "est allergique au bon sens",
            "se ferait ratio dans la vraie vie",
            "a l’énergie d’un micro coupé",
            "pourrait rater une tâche avec un seul bouton",
            "fonctionne avec 2 % de batterie et de mauvais choix",
            "a la confiance d’un homme qui ne peut pas être humilié",
            "est la preuve que l’évolution prend parfois des pauses",
            "n’apporte rien à la table mais mange quand même",
            "a l’énergie d’une quête secondaire oubliée",
            "perdrait un concours de regard contre un mur",
            "a l’icône de chargement activée en permanence dans le cerveau",
            "pense que « BRB » est un engagement à long terme",
            "est la version humaine d’une faute de frappe",
            "ne trouverait pas d’eau dans l’océan",
            "a le charisme d’une chaussette humide",
            "est en bons termes avec les mauvaises décisions",
            "a la capacité d’attention d’un poisson rouge sur TikTok",
            "se ferait bannir d’un mode solo",
            "a toujours tort, mais avec confiance",
            "a les vibes d’un protège-écran fissuré",
            "a l’air du genre à dire « vous aussi » quand le serveur dit bon appétit",
            "est construit comme une note de mise à jour que personne n’a demandée",
            "mal orthographierait son propre nom",
            "dégage une grosse énergie de « j’ai atteint mon pic dans le tutoriel »",
            "existe uniquement pour faire baisser la moyenne",
            "a l’intelligence émotionnelle d’un grille-pain",
            "se disputerait avec Google Maps",
            "est un trou scénaristique ambulant",
            "a l’énergie d’un groupe de discussion mort",
            "est la raison pour laquelle les boutons « êtes-vous sûr ? » existent",
        ]
        embed = Embed(color=Color.random())
        if member:
            roast = f"{member} est le genre de personne qui {choice(ROASTS)}"
        else:
            roast = f"Tu es le genre de personne qui {choice(ROASTS)}"
        embed.description = roast
        await ctx.followup.send(embed=embed)

    async def mock(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        mocked = "".join(
            letter.upper() if randint(0, 1) else letter.lower() for letter in text
        )
        embed = Embed(
            title="🗣️ Générateur moqueur",
            description=mocked,
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)
