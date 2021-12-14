import discord, random
from asyncio import TimeoutError
from discord import Embed
from discord.ext import commands
from discord.ext.commands.converter import clean_content


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball', '8b'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx, *, question=None):
        responses = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', 'Dont count on it.', 'My reply is no.',
            'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
        ]
        if not question:
            noquestion = discord.Embed(
                description="Please add a question")
            await ctx.send(embed=noquestion)
        else:
            embed = discord.Embed(color=0x0000FF)
            embed.add_field(name="Question:", value=f'{question}', inline=False)
            embed.add_field(
                name="Answer:", value=f'{random.choice(responses)}', inline=False)
            await ctx.send(embed=embed)


    @commands.command(aliases=['rd', 'dice'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolldice(self, ctx):
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled", value="You rolled a {}!".format(
            random.randint(1, 6)), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def combine(self, ctx, name1: clean_content, name2: clean_content):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = (discord.Embed(color=0x36393e, description=f"{ship}"))
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.send(embed=emb)

    @commands.command(aliases=['coinflip', 'headsortails', 'piece'])
    async def flip(self, ctx):
        await ctx.send(embed=discord.Embed(color=0x0000FF,
                                           description=f"`{random.choice(['Heads', 'Tails'])}`"))

    @commands.command(aliases=["pick"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        if len(choices) == 1:
            nochoices = discord.Embed(
                description="Please add more than 1 choices")
            await ctx.send(embed=nochoices)
        
        else:
            choose = discord.Embed(
                description=f"I chose **{random.choice(choices)}**")
            await ctx.send(embed=choose)


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reverse(self, ctx, *, text):
        await ctx.send(text[::-1])   

    @commands.command()
    async def guess(self, ctx):
        guessit=Embed(description="Guess my number!\nYou have 5 seconds to guess it")
        await ctx.send(embed=guessit)
        if ctx.author.id == self.bot.user.id:
            return

        def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 10)


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



def setup(bot):
    bot.add_cog(fun(bot))
