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
    check_botbanned_app_command,
    check_disabled_app_command,
)
from typing import Optional
from assets.components import ReportContent, ReportContentPlus


class nsfw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        description="Get a random hentai from Jeanne",
        nsfw=True,
        extras={"nsfw": True},
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def hentai(
        self,
        ctx: Interaction,
    ) -> None:
        await ctx.response.defer()
        hentai, shortlink, source = await Hentai().hentai()
        is_mp4 = hentai.endswith("mp4")
        if is_mp4:
            view = ReportContent(shortlink)
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
        view = ReportContent(shortlink)
        await ctx.followup.send(embed=embed, view=view)
        await view.wait()
        if view.value == None:
            try:
                await ctx.edit_original_response(view=None)
            except (NotFound, HTTPException):
                return

    @hentai.error
    async def hentai_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Give me a breather!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(
        description="Get a random media content from Gelbooru",
        nsfw=True,
        extras={"nsfw": True},
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(
        tag="Add your tag",
        plus="Need more content? (up to 4)",
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def gelbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = await Hentai().gelbooru(tag)

        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            try:
                view = ReportContentPlus(*[img[1] for img in images])
                vids = [i[0] for i in images if "mp4" in i[1]]
                media = [j[0] for j in vids]
            except:
                view = ReportContentPlus(*[img[1] for img in images])
                vids = [i[0] for i in images if "mp4" in i[0]]
                media = [j[0] for j in vids]

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
                .set_image(url=img[0])
                .set_footer(text="Fetched from Gelbooru • Credits must go to the artist")
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return

        try:
            image=choice(image)
            view = ReportContent(image[1])
            if str(image[0]).endswith("mp4"):
                await ctx.followup.send(image[0], view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(text="Fetched from Gelbooru • Credits must go to the artist")
            )
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except:
            if str(image[0]).endswith("mp4"):
                await ctx.followup.send(image[0])
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(
                    text="Fetched from Gelbooru • Credits must go to the artist\nIf you see illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.followup.send(embed=embed)

    @gelbooru.error
    async def gelbooru_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Give me a breather!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(
        description="Get a random hentai from Yande.re",
        nsfw=True,
        extras={"nsfw": True},
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(
        tag="Add your tag",
        plus="Need more content? (up to 4)",
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def yandere(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        if tag == "02":
            await ctx.followup.send(
                "Tag has been blacklisted due to it returning extreme content"
            )
            return
        image = await Hentai().yandere(tag)

        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            view = ReportContentPlus(*[img[1] for img in images])

            color = Color.random()
            embeds = [
                Embed(color=color, url="https://yande.re")
                .set_image(url=img[0])
                .set_footer(
                    text="Fetched from Yandere • Credits must go to the artist"
                )
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return

        try:
            image = choice(image)
            view = ReportContent(image[1])

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(
                    text="Fetched from Yandere • Credits must go to the artist"
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
        except:
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(
                    text="Fetched from Yandere • Credits must go to the artist\nIf you see illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.followup.send(embed=embed)

    @yandere.error
    async def yandere_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Give me a breather!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(
        description="Get a random hentai from Konachan",
        nsfw=True,
        extras={"nsfw": True},
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(
        tag="Add your tag",
        plus="Need more content (up to 4)",
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def konachan(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = await Hentai().konachan(tag)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            view = ReportContentPlus(*[img[1] for img in images])

            color = Color.random()
            embeds = [
                Embed(color=color, url="https://konachan.com")
                .set_image(url=img[0])
                .set_footer(
                    text="Fetched from Konachan • Credits must go to the artist"
                )
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return

        try:
            image = choice(image)
            view = ReportContent(image[1])

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(text="Fetched from Konachan • Credits must go to the artist")
            )
            await ctx.followup.send(embed=embed, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return
        except:
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(
                    text="Fetched from Konachan • Credits must go to the artist\nIf you see illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.followup.send(embed=embed)

    @konachan.error
    async def konachan_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Give me a breather!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(
        description="Get a random media content from Danbooru",
        nsfw=True,
        extras={"nsfw": True},
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(
        tag="Add your tag (up to 2 tags)",
        plus="Need more content? (up to 4)",
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def danbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        image = await Hentai().danbooru(tag)
        if plus:
            images = [image[randint(1, len(image)) - 1] for _ in range(4)]
            try:
                view = ReportContentPlus(*[img[1] for img in images])
                vids = [i[0] for i in images if "mp4" in i[1]]
                media = [j[0] for j in vids]
            except:
                view = ReportContentPlus(*[img[1] for img in images])
                vids = [i[0] for i in images if "mp4" in i[0]]
                media = [j[0] for j in vids]

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
                Embed(color=color, url="https://danbooru.domain.us")
                .set_image(url=img[0])
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist"
                )
                for img in images
            ]
            await ctx.followup.send(embeds=embeds, view=view)
            await view.wait()
            if view.value is None:
                try:
                    await ctx.edit_original_response(view=None)
                except (NotFound, HTTPException):
                    return
            return

        try:
            image = choice(image)
            view = ReportContent(image[1])
            if str(image[0]).endswith("mp4"):
                await ctx.followup.send(image[0], view=view)
                await view.wait()
                if view.value is None:
                    try:
                        await ctx.edit_original_response(view=None)
                    except (NotFound, HTTPException):
                        return
                return

            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist"
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
        except:
            if str(image[0]).endswith("mp4"):
                await ctx.followup.send(image[0])
                return
            embed = (
                Embed(color=Color.purple())
                .set_image(url=image[0])
                .set_footer(
                    text="Fetched from Danbooru • Credits must go to the artist\nIf you see illegal content, please use /botreport and attach the link when reporting"
                )
            )
            await ctx.followup.send(embed=embed)

    @danbooru.error
    async def danbooru_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            no_tag = Embed(
                description="The hentai could not be found", color=Color.red()
            )
            await ctx.followup.send(embed=no_tag)
            return
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Give me a breather!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

async def setup(bot: Bot):
    await bot.add_cog(nsfw(bot))
