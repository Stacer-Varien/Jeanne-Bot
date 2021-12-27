from discord import Embed
from requests import get
from random import choice
from discord.ext.commands import command as jeanne, BucketType, is_nsfw, cooldown, Cog
from assets.needed import illegal_tags
    

class nsfw(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne()
    @is_nsfw()
    @cooldown(1, 10, BucketType.user)
    async def hentai(self, ctx):
        yandere_api=choice(get("https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub+").json())
        gelbooru_api=choice(get("https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub+").json())
        danbooru_api=choice(get("https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub+").json())

        apis=[yandere_api, gelbooru_api, danbooru_api]

        await ctx.send(choice(apis)["file_url"])

    @jeanne()
    @cooldown(1, 3600, BucketType.user)
    async def report_loli(self, ctx, *, media_link):
        print(f"Media link {media_link} has been reported for returning loli hentai")
        await ctx.send("Report sent", delete_after=3)    

    @jeanne(aliases=["hentai+"])
    @is_nsfw()
    @cooldown(1, 10, BucketType.user)
    async def hentai_plus(self, ctx):
        yandere_api=choice(get("https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub+").json())
        gelbooru_api=choice(get("https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub+").json())
        danbooru_api=choice(get("https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub+").json())
        apis=[yandere_api, gelbooru_api, danbooru_api]

        await ctx.send(f'{choice(apis)["file_url"]}\n{choice(apis)["file_url"]}\n{choice(apis)["file_url"]}')

    @jeanne()
    @is_nsfw()
    @cooldown(1, 10, BucketType.user)
    async def yandere(self, ctx, *, tag=None):
        try:
            if tag == None:
                yandere_hentai = choice(get("https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub+").json())

            elif any(word in tag for word in illegal_tags):
                blacklisted_tags = Embed(
                    description="This tag is currently blacklisted")
                await ctx.send(embed=blacklisted_tags)
            
            elif tag=="02":
                await ctx.send("Tag has been blacklisted due to it returning extreme content and guro")

            else:
                yandere_hentai = choice(get("https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub+" + tag).json())

            yandere = Embed(color=0xFFC0CB)
            yandere.set_image(url=yandere_hentai["file_url"])
            yandere.set_footer(text="Fetched from Yande.re")
            await ctx.send(embed=yandere)
        except IndexError:
            notag = Embed(
                description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Yande.re tag format or if the tag exists")
            await ctx.send(embed=notag)

    @jeanne()
    @is_nsfw()
    @cooldown(1, 10, BucketType.user)
    async def gelbooru(self, ctx, *, tag=None):
        try:
            if tag == None:
                gelbooru_api = choice(get(
                    "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -loli-shota-cub+").json())

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
                description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Gelbooru tag format or if the tag exists")
            await ctx.send(embed=notag)

    @jeanne()
    @is_nsfw()
    @cooldown(1, 10, BucketType.user)
    async def danbooru(self, ctx, *, tag=None):
        try:
            if tag == None:
                danbooru_api = choice(get(
                    "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub+").json())

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
