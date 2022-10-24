from random import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog, Bot
from db_functions import add_botbanned_user, check_botbanned_user
from assets.needed import *
from config import BB_WEBHOOK, ANIMEME
from assets.imgur import get_animeme_pic


class slashfun(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @jeanne_slash(name='8ball', description="Ask 8 ball anything and you will get your awnser")
    async def _8ball(self, ctx: Interaction, question=SlashOption(description="What question do you have?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed(color=0x0000FF)
            embed.add_field(name="Question:",
                            value=f'{question}', inline=False)
            embed.add_field(
                name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Say something and I will say it in reversed text")
    async def reverse(self, ctx: Interaction, text=SlashOption(description="Type something")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if any(word in text for word in filtered_words):
                nope = Embed(description="I am not reversing that",
                             color=Color.red())
                await ctx.followup.send(embed=nope)
            elif "raffik" in text:
                add_botbanned_user(
                    ctx.user.id, "Using the reversed version of the 'k-word'")
                botbanned = Embed(title="User has been botbanned!",
                                  description="They will no longer use Jeanne,permanently!")
                botbanned.add_field(name="User",
                                    value=ctx.user)
                botbanned.add_field(name="ID", value=ctx.user.id,
                                    inline=True)
                botbanned.add_field(name="Reason of ban",
                                    value="Using the reversed version of the 'k-word'",
                                    inline=False)
                botbanned.set_footer(
                    text="Due to this user botbanned, all data except warnings are immediatley deleted from the database! They will have no chance of appealing their botban and all the commands executed bythem are now rendered USELESS!")
                botbanned.set_thumbnail(url=ctx.user.avatar)
                webhook = SyncWebhook.from_url(BB_WEBHOOK)
                webhook.send(embed=botbanned)
            else:
                msg = Embed(description=text[::-1], color=ctx.user.color).set_footer(
                    text="Author: {} | {}".format(ctx.user, ctx.user.id))
                await ctx.followup.send(embed=msg)

    @jeanne_slash(description="Get a random animeme")
    async def animeme(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            animeme = Embed(color=0x0000FF)
            animeme.set_image(url=get_animeme_pic())
            animeme.set_footer(text="Fetched from animeme1936")
            await ctx.followup.send(embed=animeme)

    @jeanne_slash(description="Combine 2 words to get 2 combined words")
    async def combine(self, ctx: Interaction, first_word=SlashOption(description="Enter first word"), second_word=SlashOption(description="Enter second word")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
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
            await ctx.followup.send(embed=combine)

    @jeanne_slash(description="Give me a lot of choices and I will pick one for you")
    async def choose(self, ctx: Interaction, choices: str = SlashOption(description="Add your choices here. Seperate them with ',' to split them")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            choices = choices.split(sep=",")
            choose = Embed(
                description=f"I chose **{choice(choices)}**", color=0x0000FF)
            await ctx.followup.send(embed=choose)

    @jeanne_slash(description="Check how much of a simp you are")
    async def simp_rate(self, ctx: Interaction, member: Member = SlashOption(description="Which member you want to check their simp rate?", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            perc = randint(0, 100)

            if member == None:
                member = ctx.user

            simp = Embed(description="{}'s simp rate is {}%".format(
                member, perc), color=ctx.user.color)

            if perc > 60:
                simp.set_image(url="https://i.imgur.com/W4u4Igk.jpg")

            elif perc > 40:
                simp.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")

            await ctx.followup.send(embed=simp)

    @jeanne_slash(description="Check how gay you are")
    async def gay_rate(self, ctx: Interaction, member: Member = SlashOption(description="Which member do you want to check their gay rate?", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            perc = randint(0, 100)

            if member == None:
                member = ctx.user

            gay = Embed(description="{}'s gay rate is {}%".format(member, perc),
                        color=ctx.user.color)

            if perc > 60:
                gay.set_image(url="https://i.imgur.com/itOD0Da.png?1")

            elif perc > 40:
                gay.set_image(url="https://i.imgur.com/tYAbWCl.jpg")

            await ctx.followup.send(embed=gay)


def setup(bot: Bot):
    bot.add_cog(slashfun(bot))
