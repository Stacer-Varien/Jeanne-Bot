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

