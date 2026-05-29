from random import choice, randint
from discord import (
    Color,
    Embed,
    HTTPException,
    Interaction,
    NotFound,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot
from functions import (
    Hentai,
    shorten_url,
)
from typing import Optional
from assets.components import ReportContent, ReportContentPlus


class nsfw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def hentai(
        self,
        ctx: Interaction,
    ) -> None:
        await ctx.response.defer()
        hentai, source = Hentai().hentai()
        if hentai.endswith(("mp4", "webm")):
            view = ReportContent(ctx, shorten_url(hentai))
            await ctx.followup.send(hentai, view=view)
            try:
                await ctx.edit_original_response(view=None)
            except (NotFound, HTTPException):
                return
            return

        embed = (
            Embed(color=Color.purple())
            .set_image(url=hentai)
            .set_footer(
                text="Fetched from {} • Credits must go to the artist".format(source)
            )
        )
        view = ReportContent(ctx, shorten_url(hentai))
        await ctx.followup.send(embed=embed, view=view)
        await view.wait()
        if view.value is None:
            try:
                await ctx.edit_original_response(view=None)
            except (NotFound, HTTPException):
                return

    async def rule34(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = Hentai().get_images_rule34(tag)
        if plus:
            images = [
                img for img in (image[randint(1, len(image)) - 1] for _ in range(4))
            ]

            media = [
                j["file_url"]
                for j in images
                if "mp4" in j["file_url"] or "webm" in j["file_url"]
            ]
            view = ReportContentPlus(ctx, *[img["file_url"] for img in images])
            if len(media) >= 1:
                await ctx.followup.send("\n".join(media), view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://rule34.xxx")
                .set_image(url=img["file_url"])
                .set_footer(text="Abgerufen von Rule34 • Credits gehen an den Künstler")
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            return
        try:
            image = choice(image)["file_url"]
            view = ReportContent(ctx, image)
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image, view=view)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(text="Abgerufen von Rule34 • Credits gehen an den Künstler")
            )
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except Exception:
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Abgerufen von Rule34 • Credits gehen an den Künstler\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
                )
            )
            await ctx.followup.send(embed=embed)

    async def gelbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = Hentai().get_images_gelbooru(tag)
        if plus:
            images = [
                img for img in (image[randint(1, len(image)) - 1] for _ in range(4))
            ]

            media = [
                j["file_url"]
                for j in images
                if "mp4" in j["file_url"] or "webm" in j["file_url"]
            ]
            view = ReportContentPlus(ctx, *[img["file_url"] for img in images])
            if len(media) >= 1:
                await ctx.followup.send("\n".join(media), view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://gelbooru.com")
                .set_image(url=img["file_url"])
                .set_footer(text="Abgerufen von Gelbooru • Credits gehen an den Künstler")
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            return
        try:
            image = choice(image)["file_url"]
            view = ReportContent(ctx, image)
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image, view=view)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(text="Abgerufen von Gelbooru • Credits gehen an den Künstler")
            )
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except Exception:
            image = choice(image)["file_url"]
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Abgerufen von Gelbooru • Credits gehen an den Künstler\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
                )
            )
            await ctx.followup.send(embed=embed)

    async def yandere(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        if tag == "02":
            await ctx.followup.send(
                "Der Tag wurde auf die schwarze Liste gesetzt, weil er extreme Inhalte zurückgibt"
            )
            return
        image = Hentai().get_images_yandere(tag)
        if plus:
            selected_images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            images=[img["file_url"] for img in selected_images]
            shortened_urls = [shorten_url(img["file_url"]) for img in images]
            view = ReportContentPlus(ctx, *shortened_urls)
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://yande.re")
                .set_image(url=(str(url)))
                .set_footer(text="Abgerufen von Yande.re • Credits gehen an den Künstler")
                for url in images
            ]
            footer_text = "Abgerufen von Yande.re • Credits gehen an den Künstler"
            try:
                await ctx.followup.send(embeds=embeds, view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return
            except Exception:
                footer_text += "\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.followup.send(embeds=embeds)
            return
        color = Color.random()
        img = choice(image)["file_url"]
        shortened_url = shorten_url(img)
        embed = Embed(color=color, url="https://yande.re")
        embed.set_image(url=img)
        footer_text = "Abgerufen von Yande.re • Credits gehen an den Künstler"
        try:
            view = ReportContent(ctx, shortened_url)
            embed.set_footer(text=footer_text)
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except Exception:
            footer_text += "\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
            embed.set_footer(text=footer_text)
            await ctx.followup.send(embed=embed)

    async def konachan(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = Hentai().get_images_konachan(tag)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            try:
                selected_images = [image[randint(1, len(image)) - 1] for _ in range(4)]
                images=[img["file_url"] for img in selected_images]
                shortened_urls = [shorten_url(img["file_url"]) for img in images]
                view = ReportContentPlus(ctx, *shortened_urls)
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url))
                    .set_footer(
                        text="Abgerufen von Konachan • Credits gehen an den Künstler"
                    )
                    for url in images
                ]
                footer_text = "Abgerufen von Konachan • Credits gehen an den Künstler"
                await ctx.followup.send(embeds=embeds, view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return
            except Exception:
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url["image_url"]))
                    .set_footer(
                        text="Abgerufen von Konachan • Credits gehen an den Künstler"
                    )
                    for url in images
                ]
                footer_text += "\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.followup.send(embeds=embeds)
            return
        color = Color.random()
        img = choice(image)["file_url"]
        url=shorten_url(img)
        embed = Embed(color=color, url="https://konachan.com")
        embed.set_image(url=img)
        footer_text = "Abgerufen von Konachan • Credits gehen an den Künstler"
        try:
            view = ReportContent(ctx, url)
            embed.set_footer(text=footer_text)
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except Exception:
            footer_text += "\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
            embed.set_footer(text=footer_text)
            await ctx.followup.send(embed=embed)

    async def danbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = Hentai().get_images_danbooru(tag)
        if plus:
            images = [
                img
                for img in (image[randint(1, len(image)) - 1] for _ in range(4))
                if ".zip" not in img["file_url"]
            ]
            media = [
                j["file_url"]
                for j in images
                if "mp4" in j["file_url"] or "webm" in j["file_url"]
            ]
            view = ReportContentPlus(ctx, *[img["file_url"] for img in images])
            if media:
                await ctx.followup.send("\n".join(media), view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://danbooru.donmai.us/")
                .set_image(url=img["file_url"])
                .set_footer(text="Abgerufen von Danbooru • Credits gehen an den Künstler")
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            return
        image = choice([img for img in image if ".zip" not in img["file_url"]])[
            "file_url"
        ]
        try:
            view = ReportContent(ctx, image)
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image, view=view)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(text="Abgerufen von Danbooru • Credits gehen an den Künstler")
            )
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except Exception:
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Abgerufen von Danbooru • Credits gehen an den Künstler\nWenn du illegale Inhalte siehst, verwende /botreport und füge den Link bei der Meldung hinzu"
                )
            )
            await ctx.followup.send(embed=embed)

    async def Hentai_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError, type: str
    ):
        if type == "NotFound":
            no_tag = Embed(
                description="Der Hentai konnte nicht gefunden werden", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if type == "cooldown":
            cooldown = Embed(
                description=f"WOAH! Ruhig Blut! Gib mir bitte eine kleine Pause!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)
