from random import *
from typing import Optional, Union
from discord import *
from discord.ext.commands import Cog, Bot, hybrid_command, Context
from db_functions import add_botbanned_user, check_botbanned_user
from assets.needed import *
from config import BB_WEBHOOK
from assets.imgur import get_animeme_pic


class slashfun(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name='8ball', aliases=['8b'])
    async def _8ball(self, ctx: Context, question):
        """Ask 8 ball anything and you will get your awnser"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(color=0x0000FF)
            embed.add_field(name="Question:",
                            value=f'{question}', inline=False)
            embed.add_field(
                name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
            await ctx.send(embed=embed)

    @hybrid_command(name='reverse')
    async def reverse(self, ctx: Context, text):
        """Say something and I will say it in reversed text"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if any(word in text for word in filtered_words):
                nope = Embed(description="I am not reversing that",
                             color=Color.red())
                await ctx.send(embed=nope)
            elif "raffik" in text:
                add_botbanned_user(
                    ctx.author.id, "Using the reversed version of the 'k-word'")
                botbanned = Embed(title="User has been botbanned!",
                                  description="They will no longer use Jeanne,permanently!")
                botbanned.add_field(name="User",
                                    value=ctx.author)
                botbanned.add_field(name="ID", value=ctx.author.id,
                                    inline=True)
                botbanned.add_field(name="Reason of ban",
                                    value="Using the reversed version of the 'k-word'",
                                    inline=False)
                botbanned.set_footer(
                    text="Due to this user botbanned, all data except warnings are immediatley deleted from the database! They will have no chance of appealing their botban and all the commands executed bythem are now rendered USELESS!")
                botbanned.set_thumbnail(url=ctx.author.avatar)
                webhook = SyncWebhook.from_url(BB_WEBHOOK)
                webhook.send(embed=botbanned)
            else:
                msg = Embed(description=text[::-1], color=ctx.author.color).set_footer(
                    text="Author: {} | {}".format(ctx.author, ctx.author.id))
                await ctx.send(embed=msg)

    @hybrid_command(name='animeme', aliases=['meme'])
    async def animeme(self, ctx: Context):
        """Get a random animeme"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            animeme = Embed(color=0x0000FF)
            animeme.set_image(url=get_animeme_pic())
            animeme.set_footer(text="Fetched from animeme1936")
            await ctx.send(embed=animeme)

    @hybrid_command(name='combine', aliases=['join'])
    async def combine(self, ctx: Context, first_word, second_word):
        """Combine 2 words to get 2 combined words"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            option_name1letters = first_word[:round(len(first_word) / 2)]
            option_name2letters = second_word[round(len(second_word) / 2):]

            option2_name1letters = first_word[round(len(first_word) / 2):]
            option2_name2letters = second_word[:round(len(second_word) / 2)]

            combine1 = "".join([option_name1letters, option_name2letters])
            combine2 = "".join([option2_name1letters, option2_name2letters])

            combine = Embed(
                description=f"**1st combine word**: {combine1}\n**2nd combined word**:{combine2}", color=0x0000FF)
            combine.set_author(name=f"{first_word} + {second_word}")
            await ctx.send(embed=combine)

    @hybrid_command(name='choose', aliases=['pick'])
    async def choose(self, ctx: Context,*, choices: str):
        """Give me a lot of choices and I will pick one for you. Seperate each choice with ','"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            choices = choices.split(sep=",")
            choose = Embed(
                description=f"I chose **{choice(choices)}**", color=0x0000FF)
            await ctx.send(embed=choose)

    @hybrid_command(name='simp_rate', aliases=['simp', 'howsimp', 'simprate'])
    async def simp_rate(self, ctx: Context, member: Optional[Member]=None)-> None:
        """Check how much of a simp you are"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            perc = randint(0, 100)

            if member == None:
                member = ctx.author

            simp = Embed(description="{}'s simp rate is {}%".format(
                member, perc), color=ctx.author.color)

            if perc > 60:
                simp.set_image(url="https://i.imgur.com/W4u4Igk.jpg")

            elif perc > 40:
                simp.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")

            await ctx.send(embed=simp)

    @hybrid_command(name='gay_rate')
    async def gay_rate(self, ctx: Context, member: Optional[Member] = None)->None:
        """Check how gay you are"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            perc = randint(0, 100)

            if member == None:
                member = ctx.author

            gay = Embed(description="{}'s gay rate is {}%".format(member, perc),
                        color=ctx.author.color)

            if perc > 60:
                gay.set_image(url="https://i.imgur.com/itOD0Da.png?1")

            elif perc > 40:
                gay.set_image(url="https://i.imgur.com/tYAbWCl.jpg")

            await ctx.send(embed=gay)


async def setup(bot: Bot):
    await bot.add_cog(slashfun(bot))
