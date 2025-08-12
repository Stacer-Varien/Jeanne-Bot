from random import randint
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
        hentai, source = await Hentai().hentai()
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

    async def yandere(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        if tag == "02":
            await ctx.followup.send(
                "Tag is op de zwarte lijst gezet omdat deze extreme inhoud retourneert"
            )
            return
        image = await Hentai(plus).yandere(tag)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            shortened_urls = [shorten_url(img["sample_url"]) for img in images]
            view = ReportContentPlus(ctx, *shortened_urls)
            color = Color.random()
            embeds = [
                Embed(color=color, url="https://yande.re")
                .set_image(url=(str(url)))
                .set_footer(text="Gehaald van Yande.re • Credits gaan naar de artiest")
                for url in shortened_urls
            ]
            footer_text = "Gehaald van Yande.re • Credits gaan naar de artiest"
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
                footer_text += "\nAls je illegale inhoud ziet, gebruik dan /botreport en voeg de link toe bij het rapporteren"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.followup.send(embeds=embeds)
            return
        color = Color.random()
        shortened_url = shorten_url(str(image))
        embed = Embed(color=color, url="https://yande.re")
        embed.set_image(url=shortened_url)
        footer_text = "Gehaald van Yande.re • Credits gaan naar de artiest"
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
            footer_text += "\nAls je illegale inhoud ziet, gebruik dan /botreport en voeg de link toe bij het rapporteren"
            embed.set_footer(text=footer_text)
            await ctx.followup.send(embed=embed)

    async def konachan(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = await Hentai(plus).konachan(tag)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            try:
                shortened_urls = [shorten_url(img["file_url"]) for img in images]
                view = ReportContentPlus(ctx, *shortened_urls)
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url))
                    .set_footer(
                        text="Gehaald van Konachan • Credits gaan naar de artiest"
                    )
                    for url in shortened_urls
                ]
                footer_text = "Gehaald van Konachan • Credits gaan naar de artiest"
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
                        text="Gehaald van Konachan • Credits gaan naar de artiest"
                    )
                    for url in images
                ]
                footer_text += "\nAls je illegale inhoud ziet, gebruik dan /botreport en voeg de link toe bij het rapporteren"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.followup.send(embeds=embeds)
            return
        color = Color.random()
        embed = Embed(color=color, url="https://konachan.com")
        embed.set_image(url=shorten_url(str(image)))
        footer_text = "Gehaald van Konachan • Credits gaan naar de artiest"
        try:
            view = ReportContent(ctx, shorten_url(str(image)))
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
            footer_text += "\nAls je illegale inhoud ziet, gebruik dan /botreport en voeg de link toe bij het rapporteren"
            embed.set_footer(text=footer_text)
            await ctx.followup.send(embed=embed)

    async def danbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = await Hentai(plus).danbooru(tag)
        if plus:
            images = [
                img
                for img in (image[randint(1, len(image)) - 1] for _ in range(4))
                if ".zip" not in img["file_url"]
            ]
            view = ReportContentPlus(ctx, *[img["file_url"] for img in images])
            vids = [
                i for i in images if "mp4" in i["file_url"] or "webm" in i["file_url"]
            ]
            media = [j["file_url"] for j in vids]
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
                .set_footer(text="Gehaald van Danbooru • Credits gaan naar de artiest")
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            return
        try:
            view = ReportContent(ctx, image)
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image, view=view)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(text="Gehaald van Danbooru • Credits gaan naar de artiest")
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
                    text="Gehaald van Danbooru • Credits gaan naar de artiest\nAls je illegale inhoud ziet, gebruik dan /botreport en voeg de link toe bij het rapporteren"
                )
            )
            await ctx.followup.send(embed=embed)

    async def Hentai_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError, type: str
    ):
        if type == "NotFound":
            no_tag = Embed(
                description="De hentai kon niet worden gevonden", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if type == "cooldown":
            cooldown = Embed(
                description=f"WOAH! Rustig aan! Geef me even een pauze!\nProbeer het opnieuw over `{round(error.retry_after, 2)} seconden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)
