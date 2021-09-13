import aiohttp
import discord
import random
from discord.ext import commands
from discord.ext.commands.converter import clean_content


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball', 'test', '8b'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', 'Dont count on it.', 'My reply is no.',
            'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
        ]
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

    @commands.command(aliases=['meme', 'animememe'])
    async def animeme(self, ctx):
        embed = discord.Embed(colour=0x0000FF)
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/Animemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children']
                                [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hentai(self, ctx):
        if ctx.invoked_subcommand != None:
            return
        embed = discord.Embed(colour=0xB900FF)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/hentai/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                                ['data']['url'])
                await ctx.send(embed=embed)


    @commands.command(aliases=["pick"])
    async def choose(self, ctx, *choices: str):
        if len(choices)>1:
            choose = discord.Embed(description=f"I chose **{random.choice(choices)}**")
            await ctx.send(embed=choose)

        elif len(choices)==1:
            nochoices = discord.Embed(
                description="Please add more than 1 choices")
        await ctx.send(embed=nochoices)

def setup(bot):
    bot.add_cog(fun(bot))
