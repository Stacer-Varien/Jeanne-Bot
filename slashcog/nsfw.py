import discord, random, requests
from discord_slash.context import SlashContext
from discord_slash import cog_ext
from discord import Embed
from discord.ext import commands

badtags = ["+loli", "+shota", "+cub", "+scat",
                   "+shit", "+vore", "+gore", "+guro"]

class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash("Get a random hentai from Yande.re")
    @commands.is_nsfw()
    async def yandere(self, ctx:SlashContext, tag=None):
        try:
            if tag == None:
                yandere_api = random.choice(requests.get(
                    "https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub").json())

            elif any(word in tag.lower() for word in badtags):
                blacklisted_tags = discord.Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            
            elif tag=="02":
                await ctx.send("Tag has been blacklisted due to it returning extreme content and guro")

            else:
                yandere_api = random.choice(requests.get(
                    "https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub+" + tag).json())

            yandere = discord.Embed(color=0xFFC0CB)
            yandere.set_image(url=yandere_api["file_url"])
            yandere.set_footer(text="Fetched from Yande.re")
            await ctx.send(embed=yandere)
        except IndexError:
            await ctx.send(f"{tag} doesn't exist. Please make sure the tag format is the same as the Yande.re tag format or if the tag exists")

    @cog_ext.cog_slash(description="Get a random hentai from Gelbooru")
    @commands.is_nsfw()
    async def gelbooru(self, ctx:SlashContext, tag=None):
        try:
            if tag == None:
                gelbooru_api = random.choice(requests.get(
                    "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub").json())

            elif any(word in tag.lower() for word in badtags):
                blacklisted_tags = discord.Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            else:
                gelbooru_api = random.choice(requests.get(
                    "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub+" + tag).json())

            gelbooru = discord.Embed(color=0xFFC0CB)
            gelbooru.set_image(url=gelbooru_api["file_url"])
            gelbooru.set_footer(text="Fetched from Gelbooru")
            await ctx.send(embed=gelbooru)
        except IndexError:
            await ctx.send(f"{tag} doesn't exist. Please make sure the tag format is the same as the Gelbooru tag format or if the tag exists")

    @cog_ext.cog_slash(description="Get a random hentai from Danbooru")
    @commands.is_nsfw()
    async def danbooru(self, ctx:SlashContext, tag=None):
        try:
            if tag == None:
                danbooru_api = random.choice(requests.get(
                    "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub").json())

            elif any(word in tag.lower() for word in badtags):
                blacklisted_tags = discord.Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            else:
                danbooru_api = random.choice(requests.get(
                    "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub+" + tag).json())

            danbooru = discord.Embed(color=0xFFC0CB)
            danbooru.set_image(url=danbooru_api["file_url"])
            danbooru.set_footer(text="Fetched from Danbooru")
            await ctx.send(embed=danbooru)
        except IndexError:
            await ctx.send(f"{tag} doesn't exist. Please make sure the tag format is the same as the Danbooru tag format or if the tag exists")

    


def setup(bot):
    bot.add_cog(nsfw(bot))
