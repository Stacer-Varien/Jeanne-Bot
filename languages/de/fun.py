from random import choice, randint
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from functions import (
    DevPunishment,
)
from typing import Optional


class fun:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _8ball(self, ctx: Interaction, question: str):
        await ctx.response.defer()
        answers = [
            "Het is zeker.",
            "Het is beslist zo.",
            "Zonder twijfel.",
            "Ja – zeker weten.",
            "Je kunt erop vertrouwen.",
            "Zoals ik het zie, ja.",
            "Waarschijnlijk.",
            "Vooruitzichten zijn goed.",
            "Ja.",
            "Tekenen wijzen op ja.",
            "Antwoord is vaag, probeer opnieuw.",
            "Vraag het later nog eens.",
            "Beter dat ik het je nu niet vertel.",
            "Kan nu niet voorspellen.",
            "Concentreer je en vraag opnieuw.",
            "Reken er niet op.",
            "Mijn antwoord is nee.",
            "Mijn bronnen zeggen nee.",
            "Vooruitzichten niet zo goed.",
            "Zeer twijfelachtig.",
            "Waarom vraag je het mij? Gewoon doen!",
            "Waarom vraag je het mij? Doe het gewoon niet!",
            "Ja... nee",
            "Ja... wat dan ook",
            "Ja... ik weet het niet",
            "Ja? Nee? Ik weet het niet!",
            "Absoluut niet, en ik ben beledigd dat je het vraagt.",
            "Zeker, als de sterren goed staan en varkens kunnen vliegen.",
            "Alleen op dinsdagen.",
            "Het antwoord ligt... in je koelkast.",
            "Vraag het aan je kat.",
            "Probeer het opnieuw na koffie.",
            "404 antwoord niet gevonden.",
            "Je bent nog niet klaar voor die waarheid.",
            "Wil je het echt weten?",
            "Hmm... mijn magische circuits haperen.",
            "Ik ben maar een bal, geen therapeut.",
            "Laat me nadenken... nee.",
            "Ja. Maar ook nee.",
            "Als ik het je vertel, moet ik verdwijnen in een wolk rook.",
        ]

        embed = Embed(color=Color.random())
        embed.add_field(name="Vraag:", value=question, inline=False)
        embed.add_field(name="Antwoord:", value=choice(answers), inline=False)
        await ctx.followup.send(embed=embed)

    async def reverse(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        if any(word in text for word in ["riffak", "reggin", "aggin"]):
            await DevPunishment(ctx.user).add_botbanned_user(
                "Using the reversed version of a common racial slur"
            )
            return
        embed = Embed(description=text[::-1], color=Color.random()).set_footer(
            text=f"Author: {ctx.user} | {ctx.user.id}"
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
            description=f"**1e gecombineerde woord**: {combine1}\n**2e gecombineerde woord**: {combine2}",
            color=Color.random(),
        ).set_author(name=f"{first_word} + {second_word}")
        await ctx.followup.send(embed=embed)

    async def choose(self, ctx: Interaction, choices: str):
        await ctx.response.defer()
        embed = Embed(
            description=f"Ik kies **{choice(choices.split(','))}**",
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)

    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member or ctx.user
        embed = Embed(
            description=f"De simp-percentage van {member} is {perc}%",
            color=Color.random(),
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
            description=f"De gay-percentage van {member} is {perc}%",
            color=Color.random(),
        )
        if perc >= 75:
            embed.set_image(url="https://i.imgur.com/itOD0Da.png?1")
        elif perc >= 50:
            embed.set_image(url="https://i.imgur.com/tYAbWCl.jpg")
        await ctx.followup.send(embed=embed)
