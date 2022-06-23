from asyncio import TimeoutError
from random import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from glob import glob
from nextcord.ext.commands import Cog
from assets.needed import *
from config import db

class slashfun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(name='8ball', description="Ask 8 ball anything and you will get your awnser")
    async def _8ball(self, ctx: Interaction, question=SlashOption(description="What question do you have?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            embed = Embed(color=0x0000FF)
            embed.add_field(name="Question:", value=f'{question}', inline=False)
            embed.add_field(
                name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Say something and I will say it in reversed text")
    async def reverse(self, ctx: Interaction, text=SlashOption(description="Type something")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            await ctx.followup.send(text[::-1])

    @jeanne_slash(description="Get a random animeme")
    async def animeme(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            file_path_type = ["./Media/Animemes/*.mp4", "./Media/Animemes/*.jpg"]
            animemes = glob(choice(file_path_type))
            random_animeme = choice(animemes)
            file = File(random_animeme)
            animeme = Embed(color=0x0000FF)
            animeme.set_footer(text="Powered by JeanneBot")
            await ctx.followup.send(file=file, embed=animeme)

    @jeanne_slash(description="Combine 2 words to get 2 combined words")
    async def combine(self, ctx: Interaction, first_word=SlashOption(description="Enter first word"), second_word=SlashOption(description="Enter second word")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
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

    @jeanne_slash(description="Give me 2 choices and I will pick for you")
    async def choose(self, ctx: Interaction, first_choice=SlashOption(description="Enter first choice"), second_choice=SlashOption(description="Enter second word")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            pick = [first_choice, second_choice]
            choose = Embed(
                description=f"I chose **{choice(pick)}**", color=0x0000FF)
            await ctx.followup.send(embed=choose)


def setup(bot):
    bot.add_cog(slashfun(bot))
