from json import loads
from random import choice
from discord import *
from discord.ext.commands import Cog, Bot
from requests import get
from db_functions import check_botbanned_user
from typing import Literal, Optional


class nsfw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Get a random hentai from Jeanne", nsfw=True)
    async def hentai(self, ctx: Interaction, rating: Optional[Literal["questionable", "explicit"]] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:

            if rating == None:
                rating = ["questionable", "explicit"]
                rating = choice(rating)

            gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
            response = get(gelbooru_api)
            ret = loads(response.text)
            gelbooru_image = choice(ret['post'])["file_url"]

            yandere_image = choice(get(
                f"https://yande.re/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub").json())['file_url']

            konachan_image = choice(
                get(f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:{rating}+-loli+-shota+-cub").json())['file_url']

            h = [gelbooru_image, yandere_image, konachan_image]

            hentai:str = choice(h)

            if hentai == gelbooru_image:
                source = 'Gelbooru'

            elif hentai == yandere_image:
                source = 'Yande.re'

            elif hentai == konachan_image:
                source = 'Konachan'

            if hentai.endswith('mp4'):
                await ctx.followup.send(hentai)
            else:
                embed = Embed(color=0xFFC0CB).set_image(url=hentai).set_footer(
                    text="Fetched from {}".format(source))
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="Get a random media content from Gelbooru", nsfw=True)
    async def gelbooru(self, ctx: Interaction, rating: Optional[Literal["questionable", "explicit"]], tag: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            try:

                if rating == None:
                    rating = ["questionable", "explicit"]
                    rating = choice(rating)

                if tag == None:
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub"
                else:
                    formated_tag = tag.replace(" ", "_")
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:{rating}+-loli+-shota+-cub+" + formated_tag

                response = get(gelbooru_api)
                ret = loads(response.text)
                image = str(choice(ret['post'])["file_url"])

                if image.endswith('mp4'):
                    await ctx.followup.send(image)

                else:

                    embed = Embed(color=0xFFC0CB).set_image(
                        url=image).set_footer(text="Fetched from Gelbooru")
                    await ctx.followup.send(embed=embed)
            except:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.followup.send(embed=no_tag)

    @app_commands.command(description="Get a random hentai from Yande.re", nsfw=True)
    async def yandere(self, ctx: Interaction, rating: Optional[Literal["questionable", "explicit"]], tag: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
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
                    await ctx.followup.send("Tag has been blacklisted due to it returning extreme content and guro")

                else:
                    formated_tag = tag.replace(" ", "_")
                    yandere_api = choice(get(
                        f"https://yande.re/post.json?limit=100&tags=rating:{rating}+-loli+-shota+-cub+" + formated_tag).json())

                yandere = Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api['file_url'])
                yandere.set_footer(text="Fetched from Yande.re")
                await ctx.followup.send(embed=yandere)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.followup.send(embed=no_tag)

    @app_commands.command(description="Get a random hentai from Konachan")
    async def konachan(self, ctx: Interaction, rating: Optional[Literal["questionable", "explicit"]], tag: Optional[str] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            try:
                if rating == None:
                    rating = ["questionable", "explicit"]
                    rating = choice(rating)
                if tag == None:
                    konachan_api = choice(get(
                        f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags=rating:{rating}+-loli+-shota+-cub").json())

                else:
                    formated_tag = tag.replace(" ", "_")
                    konachan_api = choice(get(
                        f"https://konachan.com/post.json?s=post&q=indexlimit=100&tags=rating:{rating}+-loli+-shota+-cub+{formated_tag}").json())

                konachan = Embed(color=0xFFC0CB)
                konachan.set_image(url=konachan_api['file_url'])
                konachan.set_footer(text="Fetched from Konachan")
                await ctx.followup.send(embed=konachan)
            except IndexError:
                no_tag = Embed(
                    description="The tag could not be found", color=Color.red())
                await ctx.followup.send(embed=no_tag)


async def setup(bot: Bot):
    await bot.add_cog(nsfw(bot))
