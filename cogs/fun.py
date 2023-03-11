from random import choice, randint
from discord import Color, Embed, Interaction, Member, SyncWebhook, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from db_functions import Botban
from assets.needed import eight_ball_answers, filtered_words
from config import BB_WEBHOOK
from assets.imgur import get_animeme_pic
from typing import Optional


class fun(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name='8ball',
        description="Ask 8 ball anything and you will get your awnser")
    @Jeanne.describe(question="Add your question")
    async def _8ball(self, ctx: Interaction, question: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            embed = Embed(color=Color.random())
            embed.add_field(name="Question:",
                            value=f'{question}',
                            inline=False)
            embed.add_field(name="Answer:",
                            value=f'{choice(eight_ball_answers)}',
                            inline=False)
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Say something and I will say it in reversed text")
    @Jeanne.describe(text="What are you reversing?")
    async def reverse(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            if any(word in text for word in filtered_words):
                nope = Embed(description="I am not reversing that",
                             color=Color.red())
                await ctx.followup.send(embed=nope)
            elif "raffik" in text:
                Botban(ctx.user).add_botbanned_user(
                    "Using the reversed version of the 'k-word'")
                botbanned = Embed(
                    title="User has been botbanned!",
                    description="They will no longer use Jeanne,permanently!")
                botbanned.add_field(name="User", value=ctx.user)
                botbanned.add_field(name="ID", value=ctx.user.id, inline=True)
                botbanned.add_field(
                    name="Reason of ban",
                    value="Using the reversed version of the 'k-word'",
                    inline=False)
                botbanned.set_footer(
                    text=
                    "Due to this user botbanned, all data except warnings are immediatley deleted from the database! They will have no chance of appealing their botban and all the commands executed by them are now rendered USELESS!"
                )
                botbanned.set_thumbnail(url=ctx.user.avatar)
                webhook = SyncWebhook.from_url(BB_WEBHOOK)
                webhook.send(embed=botbanned)
            else:
                msg = Embed(
                    description=text[::-1], color=ctx.user.color).set_footer(
                        text="Author: {} | {}".format(ctx.user, ctx.user.id))
                await ctx.followup.send(embed=msg)

    @Jeanne.command(description="Get a random animeme")
    async def animeme(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            animeme = Embed(color=Color.random())
            animeme.set_image(url=get_animeme_pic())
            animeme.set_footer(text="Fetched from animeme1936")
            await ctx.followup.send(embed=animeme)

    @Jeanne.command(description="Combine 2 words to get 2 combined words")
    @Jeanne.describe(first_word="Add first word",
                     second_word="Add second word")
    async def combine(self, ctx: Interaction, first_word: str,
                      second_word: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:

            option_name1letters = first_word[:round(len(first_word) / 2)]
            option_name2letters = second_word[round(len(second_word) / 2):]

            option2_name1letters = first_word[round(len(first_word) / 2):]
            option2_name2letters = second_word[:round(len(second_word) / 2)]

            combine1 = "".join([option_name1letters, option_name2letters])
            combine2 = "".join([option2_name1letters, option2_name2letters])

            combine = Embed(
                description=
                f"**1st combine word**: {combine1}\n**2nd combined word**:{combine2}",
                color=Color.random())
            combine.set_author(name=f"{first_word} + {second_word}")
            await ctx.followup.send(embed=combine)

    @Jeanne.command(
        description="Give me a lot of choices and I will pick one for you")
    @Jeanne.describe(choices="Add your choices here. Separate them with ','")
    async def choose(self, ctx: Interaction, choices: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            choices = choices.split(sep=",")
            choose = Embed(description=f"I chose **{choice(choices)}**",
                           color=Color.random())
            await ctx.followup.send(embed=choose)

    @Jeanne.command(description="Check how much of a simp you are")
    @Jeanne.describe(member="Which member?")
    async def simprate(self,
                       ctx: Interaction,
                       member: Optional[Member] = None):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            perc = randint(0, 100)

            if member == None:
                member = ctx.user

            simp = Embed(description="{}'s simp rate is {}%".format(
                member, perc),
                         color=ctx.user.color)

            if perc > 60:
                simp.set_image(url="https://i.imgur.com/W4u4Igk.jpg")

            elif perc > 40:
                simp.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")

            await ctx.followup.send(embed=simp)

    @Jeanne.command(description="Check how gay you are")
    @Jeanne.describe(member="Which member?")
    async def gayrate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            perc = randint(0, 100)

            if member == None:
                member = ctx.user

            gay = Embed(description="{}'s gay rate is {}%".format(
                member, perc),
                        color=ctx.user.color)

            if perc > 60:
                gay.set_image(url="https://i.imgur.com/itOD0Da.png?1")

            elif perc > 40:
                gay.set_image(url="https://i.imgur.com/tYAbWCl.jpg")

            await ctx.followup.send(embed=gay)


async def setup(bot: Bot):
    await bot.add_cog(fun(bot))
