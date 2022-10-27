from json import loads
from random import choice
from typing import Optional, Literal
from discord import *
from discord.ext.commands import Cog, Bot, hybrid_command, Context, is_nsfw, hybrid_group
from requests import get
from db_functions import check_botbanned_user


class slashnsfw(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @hybrid_command(name='hentai', aliases=['xxx', 'porn', 'aniporn', 'nsfw'])
    @is_nsfw()
    async def hentai(self, ctx: Context, rating: Optional[Literal["questionable", "explicit"]]=None) -> None:
        """Get a random NSFW media from Jeanne"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:

            if rating == None:
                rating = ["questionable", "explicit"]
                rating = choice(rating)


            gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
            response = get(gelbooru_api)
            ret = loads(response.text)
            gelbooru_image = choice(ret['post'])["file_url"]

            yandere_image = choice(get(f"https://yande.re/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub").json())['file_url']

            konachan_image = choice(
                get(f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:{rating}+-loli+-shota+-cub").json())['file_url']

            h = [gelbooru_image, yandere_image, konachan_image]

            hentai = str(choice(h))

            if hentai == gelbooru_image:
                source = 'Gelbooru'

            elif hentai == yandere_image:
                source = 'Yande.re'

            elif hentai == konachan_image:
                source = 'Konachan'

            if hentai.endswith('mp4'):
                await ctx.send(hentai)
            else:
                embed = Embed(color=0xFFC0CB).set_image(url=hentai).set_footer(text="Fetched from {}".format(source))
                await ctx.send(embed=embed)

    @hybrid_group(fallback='random')
    @is_nsfw()
    async def gelbooru(self, ctx: Context, rating: Optional[Literal["questionable", "explicit"]] = None, tag: Optional[str] = None) -> None:
        """Get a random media content from Gelbooru"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if not rating:
                    rating = ["questionable", "explicit"]
                    rating = choice(rating)

                if tag == None:
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
                else:
                    formated_tag = tag.replace(" ", "_")
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub+{formated_tag}"

                response = get(gelbooru_api)
                ret = loads(response.text)
                image = str(choice(ret['post'])["file_url"])

                if image.endswith('mp4'):
                    await ctx.send(image)

                else:

                    embed = Embed(color=0xFFC0CB).set_image(
                        url=image).set_footer(text="Fetched from Gelbooru")
                    await ctx.send(embed=embed)
            except:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)


    @gelbooru.command(aliases=['q'], with_app_command=False)
    @is_nsfw()
    async def questionable(self, ctx: Context, tag: Optional[str] = None) -> None:
        """Get a random questionable media content from Gelbooru"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if tag == None:
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:questionable+-loli+-shota+-cub"
                else:
                    formated_tag = tag.replace(" ", "_")
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:questionable+-loli+-shota+-cub+{formated_tag}"

                response = get(gelbooru_api)
                ret = loads(response.text)
                image = str(choice(ret['post'])["file_url"])

                if image.endswith('mp4'):
                    await ctx.send(image)

                else:

                    embed = Embed(color=0xFFC0CB).set_image(
                        url=image).set_footer(text="Fetched from Gelbooru")
                    await ctx.send(embed=embed)
            except:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @gelbooru.command(aliases=['e'], with_app_command=False)
    @is_nsfw()
    async def explicit(self, ctx: Context, tag: Optional[str] = None) -> None:
        """Get a random explicit media content from Gelbooru"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if tag == None:
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub"
                else:
                    formated_tag = tag.replace(" ", "_")
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub+{formated_tag}"

                response = get(gelbooru_api)
                ret = loads(response.text)
                image = str(choice(ret['post'])["file_url"])

                if image.endswith('mp4'):
                    await ctx.send(image)

                else:

                    embed = Embed(color=0xFFC0CB).set_image(
                        url=image).set_footer(text="Fetched from Gelbooru")
                    await ctx.send(embed=embed)
            except:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @hybrid_group(fallback='random')
    @is_nsfw()
    async def yandere(self, ctx: Context, rating: Optional[Literal["questionable", "explicit"]] = None, tag: Optional[str] = None) -> None:
        """Get a random media content from Yandere"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if rating == None:
                    rating = ["questionable", "explicit"]
                    rating = choice(rating)

                if tag == None:
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub").json())

                elif tag == "02":
                    await ctx.send("Tag has been blacklisted due to it returning extreme content and guro")

                else:
                    formated_tag = tag.replace(" ", "_")
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub+" + formated_tag).json())

                yandere = Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api['file_url'])
                yandere.set_footer(text="Fetched from Yande.re")
                await ctx.send(embed=yandere)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @yandere.command(aliases=['q'], with_app_command=False)
    @is_nsfw()
    async def questionable(self, ctx: Context, tag: Optional[str] = None) -> None:
        """Get a random questionable media content from Yandere"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if tag == None:
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:questionable+-loli+-shota+-cub").json())

                elif tag == "02":
                    await ctx.send("Tag has been blacklisted due to it returning extreme content and guro")

                else:
                    formated_tag = tag.replace(" ", "_")
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:questionable+-loli+-shota+-cub+{formated_tag}").json())

                yandere = Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api['file_url'])
                yandere.set_footer(text="Fetched from Yande.re")
                await ctx.send(embed=yandere)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @yandere.command(aliases=['e'], with_app_command=False)
    @is_nsfw()
    async def explicit(self, ctx: Context, tag: Optional[str] = None) -> None:
        """Get a random explicit media content from Yandere"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if tag == None:
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub").json())

                elif tag == "02":
                    await ctx.send("Tag has been blacklisted due to it returning extreme content and guro")

                else:
                    formated_tag = tag.replace(" ", "_")
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub+{formated_tag}").json())

                yandere = Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api['file_url'])
                yandere.set_footer(text="Fetched from Yande.re")
                await ctx.send(embed=yandere)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @hybrid_group(fallback='random')
    @is_nsfw()
    async def konachan(self, ctx: Context, rating: Optional[Literal["questionable", "explicit"]] = None, tag: Optional[str] = None) -> None:
        """Get a random media content from Konachan"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if rating == None:
                    rating = ["questionable", "explicit"]
                    rating = choice(rating)

                if tag == None:
                    konachan_api = choice(get(f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags={rating}:questionable+-loli+-shota+-cub").json())

                else:
                    formated_tag = tag.replace(" ", "_")
                    konachan_api = choice(get(
                        f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags={rating}:questionable+-loli+-shota+-cub+{formated_tag}").json())

                konachan = Embed(color=0xFFC0CB)
                konachan.set_image(url=konachan_api['file_url'])
                konachan.set_footer(text="Fetched from Konachan")
                await ctx.send(embed=konachan)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @hybrid_command(with_app_command=False, aliases=['q'])
    @is_nsfw()
    async def questionable(self, ctx: Context, tag: Optional[str] = None) -> None:
        """Get a random questionable media content from Konachan"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if tag == None:
                    konachan_api = choice(get(f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags=rating:questionable+-loli+-shota+-cub").json())

                else:
                    formated_tag = tag.replace(" ", "_")
                    konachan_api = choice(get(
                        f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags=rating:questionable+-loli+-shota+-cub+{formated_tag}").json())

                konachan = Embed(color=0xFFC0CB)
                konachan.set_image(url=konachan_api['file_url'])
                konachan.set_footer(text="Fetched from Konachan")
                await ctx.send(embed=konachan)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

    @hybrid_command(with_app_command=False, aliases=['e'])
    @is_nsfw()
    async def explicit(self, ctx: Context, tag: Optional[str] = None) -> None:
        """Get a random explicit media content from Konachan"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                if tag == None:
                    konachan_api = choice(get(
                        f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags=rating:explicit+-loli+-shota+-cub").json())

                else:
                    formated_tag = tag.replace(" ", "_")
                    konachan_api = choice(get(
                        f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags=rating:explicit+-loli+-shota+-cub+{formated_tag}").json())

                konachan = Embed(color=0xFFC0CB)
                konachan.set_image(url=konachan_api['file_url'])
                konachan.set_footer(text="Fetched from Konachan")
                await ctx.send(embed=konachan)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.send(embed=no_tag)

async def setup(bot:Bot):
    await bot.add_cog(slashnsfw(bot))
