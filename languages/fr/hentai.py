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
                text="Récupéré depuis {} • Les crédits doivent revenir à l'artiste".format(source)
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
                img
                for img in (image[randint(1, len(image)) - 1] for _ in range(4))
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
                Embed(color=color, url="https://gelbooru.com")
                .set_image(url=img["file_url"])
                .set_footer(
                    text="Récupéré depuis Gelbooru • Les crédits doivent revenir à l'artiste"
                )
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
                .set_footer(
                    text="Récupéré depuis Gelbooru • Les crédits doivent revenir à l'artiste"
                )
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
                    text="Récupéré depuis Gelbooru • Les crédits doivent revenir à l'artiste\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
                )
            )
            await ctx.followup.send(embed=embed)

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
                Embed(color=color, url="https://rule34.xxx")
                .set_image(url=img["file_url"])
                .set_footer(
                    text="Récupéré depuis Rule34 • Les crédits doivent revenir à l'artiste"
                )
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
                .set_footer(
                    text="Récupéré depuis Rule34 • Les crédits doivent revenir à l'artiste"
                )
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
                    text="Récupéré depuis Rule34 • Les crédits doivent revenir à l'artiste\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
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
        if "02" in tag:
            await ctx.followup.send(
                "Ce tag a été mis sur liste noire car il retourne du contenu extrême"
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
                .set_footer(
                    text="Récupéré depuis Yande.re • Les crédits doivent revenir à l'artiste"
                )
                for url in images
            ]
            footer_text = "Récupéré depuis Yande.re • Les crédits doivent revenir à l'artiste"
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
                footer_text += "\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.followup.send(embeds=embeds)
            return
        color = Color.random()
        image = choice(image)["file_url"]
        shortened_url = shorten_url(str(image))
        embed = Embed(color=color, url="https://yande.re")
        embed.set_image(url=image)
        footer_text = "Récupéré depuis Yande.re • Les crédits doivent revenir à l'artiste"
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
            footer_text += "\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
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
            selected_images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            images=[img["file_url"] for img in selected_images]
            shortened_urls = [shorten_url(img["file_url"]) for img in images]
            try:
                shortened_urls = [shorten_url(img["file_url"]) for img in images]
                view = ReportContentPlus(ctx, *shortened_urls)
                color = Color.random()
                embeds = [
                    Embed(color=color, url="https://konachan.com")
                    .set_image(url=str(url))
                    .set_footer(
                        text="Récupéré depuis Konachan • Les crédits doivent revenir à l'artiste"
                    )
                    for url in images
                ]
                footer_text = "Récupéré depuis Konachan • Les crédits doivent revenir à l'artiste"
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
                    .set_image(url=str(url))
                    .set_footer(
                        text="Récupéré depuis Konachan • Les crédits doivent revenir à l'artiste"
                    )
                    for url in images
                ]
                footer_text += "\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
                for embed in embeds:
                    embed.set_footer(text=footer_text)
                await ctx.followup.send(embeds=embeds)
            return
        color = Color.random()
        image= choice(image)["file_url"]
        embed = Embed(color=color, url="https://konachan.com")
        embed.set_image(url=image)
        footer_text = "Récupéré depuis Konachan • Les crédits doivent revenir à l'artiste"
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
            footer_text += "\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
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
            images = [img for img in (image[randint(1, len(image)) - 1] for _ in range(4)) if ".zip" not in img["file_url"]]
            media = [j["file_url"] for j in images if "mp4" in j["file_url"] or "webm" in j["file_url"]]
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
                .set_footer(
                    text="Récupéré depuis Danbooru • Les crédits doivent revenir à l'artiste"
                )
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            return
        try:
            image=choice([img for img in image if ".zip" not in img["file_url"]])["file_url"]
            view = ReportContent(ctx, image)
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image, view=view)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Récupéré depuis Danbooru • Les crédits doivent revenir à l'artiste"
                )
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
            image=choice([img for img in image if ".zip" not in img["file_url"]])["file_url"]
            if str(image).endswith(("mp4", "webm")):
                await ctx.followup.send(image)
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image)
                .set_footer(
                    text="Récupéré depuis Danbooru • Les crédits doivent revenir à l'artiste\nSi vous voyez un contenu illégal, veuillez utiliser /botreport et joindre le lien lors du signalement"
                )
            )
            await ctx.followup.send(embed=embed)

    async def Hentai_error(self, ctx: Interaction, error: Jeanne.AppCommandError, type:str):
        if type =="NotFound":
            no_tag = Embed(
                description="Le hentai n'a pas pu être trouvé", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if type=="cooldown":
            cooldown = Embed(
                description=f"WOAH! Calmez-vous ! Donnez-moi une pause !\nRéessayez après `{round(error.retry_after, 2)} secondes`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)
