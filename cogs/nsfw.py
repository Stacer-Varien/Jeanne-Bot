import aiohttp
import discord
import random
from discord.ext import commands


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['h'])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hentai(self, ctx):
        embed = discord.Embed(colour=0xB900FF)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/hentai/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                                ['data']['url'])
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NSFW(bot))
