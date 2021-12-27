from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import cooldown
from discord_slash.cog_ext import cog_slash as jeanne_slash
from discord import Embed, File
from glob import glob
from discord.ext.commands import Cog, is_nsfw
from random import choice
from requests import get
from requests.api import delete
from assets.needed import illegal_tags

class nsfw(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @jeanne_slash(description="Get a random hentai from Jeanne")
    @is_nsfw()
    async def hentai(self, ctx):
        file_path_type = ["./Media/Hentai/*.jpg", "./Media/Hentai/*.mp4"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        hentai = Embed(color=0xFFC0CB)
        hentai.set_footer(text="Powered by JeanneBot\nAny loli images must be reported with the 'report_loli' command with the media link")
        await ctx.send(file=file, embed=hentai) 

    @jeanne_slash(description="Report a loli image if the hentai command fetches a loli image")
    @cooldown(1, 3600, BucketType.user)
    async def report_loli(self, ctx, media_link):
        print(f"Media link {media_link} has been reported for returning loli hentai")
        await ctx.send("Report sent", delete_after=3)



    @jeanne_slash(description="Get a random hentai from Yande.re")
    @is_nsfw()
    async def yandere(self, ctx, tag=None):
        try:
            if tag == None:
                yandere_api = choice(get(
                    "https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub").json())

            elif any(word in tag.lower() for word in illegal_tags):
                blacklisted_tags = Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            
            elif tag=="02":
                await ctx.send("Tag has been blacklisted due to it returning extreme content and guro")

            else:
                yandere_api = choice(get(
                    "https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub+" + tag).json())

            yandere = Embed(color=0xFFC0CB)
            yandere.set_image(url=yandere_api["file_url"])
            yandere.set_footer(text="Fetched from Yande.re")
            await ctx.send(embed=yandere)
        except IndexError:
            notag = Embed(
                description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Danbooru tag format or if the tag exists")
            await ctx.send(embed=notag)

    @jeanne_slash(description="Get a random hentai from Gelbooru")
    @is_nsfw()
    async def gelbooru(self, ctx, tag=None):
        try:
            if tag == None:
                gelbooru_api = choice(get(
                    "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub").json())

            elif any(word in tag for word in illegal_tags):
                blacklisted_tags = Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            else:
                gelbooru_api = choice(get(
                    "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub+" + tag).json())

            gelbooru = Embed(color=0xFFC0CB)
            gelbooru.set_image(url=gelbooru_api["file_url"])
            gelbooru.set_footer(text="Fetched from Gelbooru")
            await ctx.send(embed=gelbooru)
        except IndexError:
            notag = Embed(
                description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Danbooru tag format or if the tag exists")
            await ctx.send(embed=notag)

    @jeanne_slash(description="Get a random hentai from Danbooru")
    @is_nsfw()
    async def danbooru(self, ctx, tag=None):
        try:
            if tag == None:
                danbooru_api = choice(get(
                    "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub").json())

            elif any(word in tag for word in illegal_tags):
                blacklisted_tags = Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            else:
                danbooru_api = choice(get(
                    "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub+" + tag).json())

            danbooru = Embed(color=0xFFC0CB)
            danbooru.set_image(url=danbooru_api["file_url"])
            danbooru.set_footer(text="Fetched from Danbooru")
            await ctx.send(embed=danbooru)
        except IndexError:
            notag = Embed(
                description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Danbooru tag format or if the tag exists")
            await ctx.send(embed=notag)

    


def setup(bot):
    bot.add_cog(nsfw(bot))
