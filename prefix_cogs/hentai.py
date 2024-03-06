import argparse
from random import randint
from discord import Color, Embed, HTTPException
from discord.ext.commands import Bot, Cog, group, Context, Range, BucketType
import discord.ext.commands as Jeanne
from functions import BetaTest, Botban, Command, Hentai, shorten_url
from typing import Literal, Optional
from assets.components import ReportContent, ReportSelect


class nsfw(Cog, name="hentai"):
    def __init__(self, bot: Bot):
        self.bot = bot


    @Jeanne.command(description="Get a random hentai from Jeanne", nsfw=True)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def hentai(
        self,
        ctx: Context,
        rating: Optional[Literal["questionable", "explicit", "e", "q"]] = None,
    ) -> None:
        if Botban(ctx.author).check_botbanned_user:
            return

        if Command(ctx.guild).check_disabled(self.hentai.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()

        hentai, source = await Hentai().hentai(rating)
        is_mp4 = hentai.endswith("mp4")

        if is_mp4:
            view = ReportContent(shorten_url(hentai))
            m=await ctx.send(hentai, view=view)
        else:
            embed = (
                Embed(color=Color.purple())
                .set_image(url=hentai)
                .set_footer(
                    text="Fetched from {} • Credits must go to the artist".format(
                        source
                    )
                )
            )
            view = ReportContent(shorten_url(hentai))
            m = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            await m.edit(view=None)

    @hentai.error
    async def hentai_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if Command(ctx.guild).check_disabled(self.hentai.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    plus_parser = argparse.ArgumentParser(add_help=False)
    plus_parser.add_argument(
                "--first", "-f", type=str, help="First Word", required=True,
            )
    plus_parser.add_argument(
                "--second", "-s", type=str, help="Second Word", required=True
            )

    @Jeanne.command(description="Get a random media content from Gelbooru", nsfw=True)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def gelbooru(
        self,
        ctx: Context,
        rating: Optional[Literal["questionable", "explicit"]],
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.gelbooru.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.defer()
        image = await Hentai(plus).gelbooru(rating, tag)

        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            view = ReportSelect(*[img["file_url"] for img in images])

            vids = [i for i in images if "mp4" in i["file_url"]]
            media = [j["file_url"] for j in vids]

            if media:
                m = await ctx.send("\n".join(media), view=view)
                await view.wait()

                if view.value == None:
                    await m.edit(view=None)
                return

            color = Color.random()
            embeds = [
                Embed(color=color, url="https://gelbooru.com")
                .set_image(url=img["file_url"])
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist"
                )
                for img in images
            ]
            await ctx.send(embeds=embeds, view=view)
            await view.wait()

            if view.value == None:
                await m.edit(view=None)
            return

        try:
            view = ReportContent(image)
            if str(image).endswith("mp4"):
                await ctx.send(image, view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)
                return

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist"
                )
            )
            await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.value == None:
                await m.edit(view=None)
        except:
            if str(image).endswith("mp4"):
                await ctx.send(image)
                return

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.send(embed=embed)

    @gelbooru.error
    async def gelbooru_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError)
        ):
            if Command(ctx.guild).check_disabled(self.gelbooru.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if Command(ctx.guild).check_disabled(self.danbooru.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random hentai from Yande.re", nsfw=True)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def yandere(
        self,
        ctx: Context,
        rating: Optional[Literal["questionable", "explicit"]],
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.yandere.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()

        if tag == "02":
            await ctx.send(
                "Tag has been blacklisted due to it returning extreme content"
            )
            return

        image = await Hentai(plus).yandere(rating, tag)

        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            shortened_urls = [shorten_url(img["file_url"]) for img in images]
            view = ReportSelect(*shortened_urls)
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://yande.re")
                .set_image(url=(str(url)))
                .set_footer(
                    text="Fetched from Yande.re • Credits must go to the artist"
                )
                for url in shortened_urls
            ]
            footer_text = "Fetched from Yande.re • Credits must go to the artist"
            try:
                m = await ctx.send(embeds=embeds, view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)

            except:
                footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.send(embeds=embeds)
            return
        color = Color.random()
        shortened_url = shorten_url(str(image))
        embed = Embed(color=color, url="https://yande.re")
        embed.set_image(url=shortened_url)
        footer_text = "Fetched from Yande.re • Credits must go to the artist"
        try:
            view = ReportContent(shortened_url)
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.value == None:
                await m.edit(view=None)
        except:
            footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed)

    @yandere.error
    async def yandere_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            if Command(ctx.guild).check_disabled(self.yandere.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return

        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if Command(ctx.guild).check_disabled(self.danbooru.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random hentai from Konachan", nsfw=True)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def konachan(
        self,
        ctx: Context,
        rating: Optional[Literal["questionable", "explicit"]],
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.author).check_botbanned_user:
            return

        if Command(ctx.guild).check_disabled(self.konachan.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.defer()

        image = await Hentai(plus).konachan(rating, tag)

        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            try:
                shortened_urls = [shorten_url(img["file_url"]) for img in images]
                view = ReportSelect(*shortened_urls)
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url))
                    .set_footer(
                        text="Fetched from Konachan • Credits must go to the artist"
                    )
                    for url in shortened_urls
                ]
                footer_text = "Fetched from Konachan • Credits must go to the artist"

                m = await ctx.send(embeds=embeds, view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)

            except:
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url["image_url"]))
                    .set_footer(
                        text="Fetched from Konachan • Credits must go to the artist"
                    )
                    for url in images
                ]
                footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.send(embeds=embeds)
            return

        color = Color.random()
        embed = Embed(color=color, url="https://konachan.com")
        embed.set_image(url=shorten_url(str(image)))
        footer_text = "Fetched from Konachan • Credits must go to the artist"
        try:
            view = ReportContent(shorten_url(str(image)))
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.value == None:
                await m.edit(view=None)
        except:
            footer_text += "\nIf you see an illegal content, please use /botreport and attach the link when reporting"
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed)

    @konachan.error
    async def konachan_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            if Command(ctx.guild).check_disabled(self.konachan.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if Command(ctx.guild).check_disabled(self.danbooru.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)

    @Jeanne.command(description="Get a random media content from Danbooru", nsfw=True)
    @Jeanne.cooldown(1, 5, type=BucketType.member)
    async def danbooru(
        self,
        ctx: Context,
        rating: Optional[Literal["questionable", "explicit"]],
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.danbooru.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.defer()
        image = await Hentai(plus).danbooru(rating, tag)

        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            view = ReportSelect(*[img["file_url"] for img in images])
            vids = [i for i in images if "mp4" in i["file_url"]]
            media = [j["file_url"] for j in vids]

            if media:
                m = await ctx.send("\n".join(media), view=view)
                await view.wait()
                if view.value == None:
                    await m.edit(view=None)
                return

            color = Color.random()
            embeds = [
                Embed(color=color, url="https://danbooru.donmai.us/")
                .set_image(url=img["file_url"])
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist"
                )
                for img in images
            ]
            await ctx.send(embeds=embeds, view=view)
            return

        try:
            view = ReportContent(image)
            if str(image).endswith("mp4"):
                await ctx.send(image, view=view)
                return

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist"
                )
            )
            m=await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.value == None:
                await m.edit(view=None)
        except:
            if str(image).endswith("mp4"):
                await ctx.send(image)
                return

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist\nIf you see an illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.send(embed=embed)

    @danbooru.error
    async def danbooru_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            if Command(ctx.guild).check_disabled(self.danbooru.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.send(embed=no_tag)
            return

        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if Command(ctx.guild).check_disabled(self.danbooru.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            slow = Embed(
                description="WOAH! Slow down!\nI know you are horny but geez... I am at my limit",
                color=Color.red(),
            )
            await ctx.send(embed=slow)


async def setup(bot: Bot):
    await bot.add_cog(nsfw(bot))
