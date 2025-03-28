from random import choice, randint
from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot
from functions import (
    DevPunishment,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from assets.images import get_animeme_pic
from typing import Optional


class fun(Cog, name="FunSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name="8ball", description="Ask 8 ball anything and you will get your awnser"
    )
    @Jeanne.describe(question="Add your question")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _8ball(self, ctx: Interaction, question: str):
        await ctx.response.defer()
        eight_ball_answers = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes – definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "Why ask me? Just do it!",
            "Why ask me? Just don't do it!",
            "Yeah... no",
            "Yeah... whatever",
            "Yeah... I don't know",
            "Yes? No? I don't know!",
        ]
        embed = Embed(color=Color.random())
        embed.add_field(name="Question:", value=f"{question}", inline=False)
        embed.add_field(
            name="Answer:", value=f"{choice(eight_ball_answers)}", inline=False
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Say something and I will say it in reversed text")
    @Jeanne.describe(text="What are you reversing?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def reverse(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        filtered_words = ["riffak", "reggin", "aggin"]
        if any(word in text for word in filtered_words):
            await DevPunishment(ctx.user).add_botbanned_user(
                "Using the reversed version of a common racial slur"
            )
            return
        msg = Embed(description=text[::-1], color=Color.random()).set_footer(
            text="Author: {} | {}".format(ctx.user, ctx.user.id)
        )
        await ctx.followup.send(embed=msg)

    @Jeanne.command(description="Get a random animeme")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def animeme(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_animeme_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Combine 2 words to get 2 combined words")
    @Jeanne.describe(first_word="Add first word", second_word="Add second word")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def combine(self, ctx: Interaction, first_word: str, second_word: str):
        await ctx.response.defer()
        option_name1letters = first_word[: round(len(first_word) / 2)]
        option_name2letters = second_word[round(len(second_word) / 2) :]
        option2_name1letters = first_word[round(len(first_word) / 2) :]
        option2_name2letters = second_word[: round(len(second_word) / 2)]
        combine1 = "".join([option_name1letters, option_name2letters])
        combine2 = "".join([option2_name1letters, option2_name2letters])
        combine = Embed(
            description=f"**1st combine word**: {combine1}\n**2nd combined word**:{combine2}",
            color=Color.random(),
        )
        combine.set_author(name=f"{first_word} + {second_word}")
        await ctx.followup.send(embed=combine)

    @Jeanne.command(description="Give me a lot of choices and I will pick one for you")
    @Jeanne.describe(choices="Add your choices here. Separate them with ','")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def choose(self, ctx: Interaction, choices: str):
        await ctx.response.defer()
        choices = choices.split(sep=",")
        choose = Embed(
            description=f"I chose **{choice(choices)}**", color=Color.random()
        )
        await ctx.followup.send(embed=choose)

    @Jeanne.command(description="Check how much of a simp you are")
    @Jeanne.describe(member="Which member?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member if member else ctx.user
        simp = Embed(
            description="{}'s simp rate is {}%".format(member, perc),
            color=Color.random(),
        )
        if perc >= 75:
            simp.set_image(url="https://i.imgur.com/W4u4Igk.jpg")
        elif perc >= 50<75:
            simp.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")
        await ctx.followup.send(embed=simp)

    @Jeanne.command(description="Check how gay you are")
    @Jeanne.describe(member="Which member?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def gayrate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member if member else ctx.user
        gay = Embed(
            description="{}'s gay rate is {}%".format(member, perc),
            color=Color.random(),
        )
        if perc >= 75:
            gay.set_image(url="https://i.imgur.com/itOD0Da.png?1")
        elif perc >= 50<75:
            gay.set_image(url="https://i.imgur.com/tYAbWCl.jpg")
        await ctx.followup.send(embed=gay)


async def setup(bot: Bot):
    await bot.add_cog(fun(bot))
