from asyncio import TimeoutError
from random import choice, randint
from discord import Embed, File
from glob import glob
from discord.ext.commands import Cog
from discord_slash.cog_ext import cog_slash as jeanne_slash
from assets.needed import eight_ball_answers

class fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(name='8ball', description="Ask 8 ball anything and you will get your awnser")
    async def _8ball(self, ctx, question):
        embed = Embed(color=0x0000FF)
        embed.add_field(name="Question:", value=f'{question}', inline=False)
        embed.add_field(
            name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Roll a dice")
    async def dice(self, ctx):
        embed = Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled", value="You rolled a {}!".format(
            randint(1, 6)), inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Type two words to get one combined word")
    async def combine(self, ctx, name1, name2):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = (Embed(color=0x36393e, description=f"{ship}"))
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.send(embed=emb)

    @jeanne_slash(description="Flip a coin")
    async def flip(self, ctx):
        await ctx.send(embed=Embed(color=0x0000FF,
                                           description=f"`{choice(['Heads', 'Tails'])}`"))

    @jeanne_slash(description="Say something and I will say it in reversed text")
    async def reverse(self, ctx, text):
        await ctx.send(text[::-1])

    @jeanne_slash(description="Guess my number")
    async def guess(self, ctx):
        guessit=Embed(description="Guess my number!\nYou have 5 seconds to guess it")
        await ctx.send(embed=guessit)
        if ctx.author.id == self.bot.user.id:
            return

        def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

        answer = randint(1, 10)


        try:
            guess = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
        except TimeoutError:
            timeout=Embed(description=f"Sorry but you took too long. It was {answer}")
            timeout.set_thumbnail(url="https://cdn.discordapp.com/attachments/809862945684717644/920222496324734996/86052023e81b59d10c95b44ce2751273.jpg")
            return await ctx.send(embed=timeout)

        if int(guess.content) == answer:
            correct=Embed(description="YES!")
            correct.set_image(url="https://cdn.discordapp.com/attachments/809862945684717644/920227513827999744/ezgif.com-gif-maker.gif")
            await ctx.send(embed=correct)
        else:
            wrong=Embed(description=f"Wrong answer. It was {answer}")
            wrong.set_thumbnail(url="https://cdn.discordapp.com/attachments/809862945684717644/920222496324734996/86052023e81b59d10c95b44ce2751273.jpg")
            await ctx.send(embed=wrong) 

    @jeanne_slash(description="Get a random animeme")
    async def animeme(self, ctx):
            file_path_type = ["./Media/animemes/*.mp4", "./Media/animemes/*.jpg"]
            animemes = glob(choice(file_path_type))
            random_animeme = choice(animemes)
            file = File(random_animeme)
            animeme = Embed(color=0x0000FF)
            animeme.set_footer(text="Powered by JeanneBot")
            await ctx.send(file=file, embed=animeme)

def setup(bot):
    bot.add_cog(fun(bot))
