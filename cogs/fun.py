import discord
import random
from discord.ext import commands
from discord.ext.commands.converter import clean_content
from discord.ext.commands.errors import CommandOnCooldown, NSFWChannelRequired
import requests


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

        if len(question) == 0:
            noquestion = discord.Embed(
                description="Please add a question")
        await ctx.send(embed=noquestion)

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

    @commands.command(aliases=['h'])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hentai(self, ctx):
                yandere_api = random.choice(requests.get("https://yande.re/post.json?tags=").json()) #not full API
                yandere = discord.Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api["file_url"])
                yandere.set_footer(text="Fetched from Yande.re")

                gelbooru_api = random.choice(requests.get("https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=").json()) #not full API
                gelbooru = discord.Embed(color=0xFFC0CB)
                gelbooru.set_image(url=gelbooru_api["file_url"])
                gelbooru.set_footer(text="Fetched from Gelbooru")

                hentai=[yandere, gelbooru]

                await ctx.send(embed=random.choice(hentai))



    @commands.command(aliases=["pick"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        if len(choices)>1:
            choose = discord.Embed(description=f"I chose **{random.choice(choices)}**")
            await ctx.send(embed=choose)

        elif len(choices)==1:
            nochoices = discord.Embed(
                description="Please add more than 1 choices")
        await ctx.send(embed=nochoices)

    @hentai.error
    async def hentai_error(self, ctx, error):
        if isinstance(error, NSFWChannelRequired):
            error = discord.Embed(
                title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
            error.add_field(
                name="Reason", value="Channel is not NSFW enabled")
            await ctx.send(embed=error)
        elif isinstance(error, CommandOnCooldown):
            cooldown = discord.Embed(
                title="Hentai On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
            await ctx.send(embed=cooldown)
    
    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = discord.Embed(
                title="8 Ball On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
            await ctx.send(embed=cooldown)

    @rolldice.error
    async def rolldice_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = discord.Embed(
                title="Roll Dice On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
            await ctx.send(embed=cooldown)

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = discord.Embed(
                title="Choose On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
            await ctx.send(embed=cooldown)

def setup(bot):
    bot.add_cog(fun(bot))
