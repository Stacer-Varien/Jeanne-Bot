from discord import (
    Interaction,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot
from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from typing import Optional
import languages.en.hentai as en
import languages.fr.hentai as fr
import languages.de.hentai as de
from discord.app_commands import locale_str as T


class nsfw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        description=T("hentai_desc"),
        nsfw=True,
        extras={
            "nsfw": True,
            "name": "hentai",
            "en": {"description": "Get a random hentai from Jeanne"},
            "fr": {
                "name": "hentai",
                "description": "Obtenez un hentai aléatoire de Jeanne",
            },
            "de":{"name": "hentai", "description": "Holen Sie sich ein zufälliges Hentai von Jeanne"},
        },
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def hentai(
        self,
        ctx: Interaction,
    ) -> None:
        if ctx.locale.value == "fr":
            await fr.nsfw(self.bot).hentai(ctx)
            return
        if ctx.locale.value == "de":
            await de.nsfw(self.bot).hentai(ctx)
            return
        await en.nsfw(self.bot).hentai(ctx)



    @Jeanne.command(
        description=T("yandere_desc"),
        nsfw=True,
        extras={
            "nsfw": True,
            "en": {
                "name": "yandere",
                "description": "Get a random media content from Yandere",
                "parameters": [
                    {"name": "tag", "description": "Add your tags", "required": False},
                    {
                        "name": "plus",
                        "description": "Need more content? (up to 4)",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "yandere",
                "description": "Obtenez un contenu multimédia aléatoire de Yandere",
                "parameters": [
                    {
                        "name": "tag",
                        "description": "Ajoutez vos tags",
                        "required": False,
                    },
                    {
                        "name": "plus",
                        "description": "Besoin de plus de contenu? (jusqu'à 4)",
                        "required": False,
                    },
                ],
            },
            "de": {
                "name": "yandere",
                "description": "Holen Sie sich einen zufälligen Medieninhalt von Yandere",
                "parameters": [
                    {
                        "name": "tag",
                        "description": "Fügen Sie Ihre Tags hinzu",
                        "required": False,
                    },
                    {
                        "name": "plus",
                        "description": "Brauchen Sie mehr Inhalte? (bis zu 4)",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(tag=T("tag_parm_desc"), plus=T("plus_parm_desc"))
    @Jeanne.rename(tag=T("tag_parm_name"), plus=T("plus_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def yandere(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if ctx.locale.value == "fr":
            await fr.nsfw(self.bot).yandere(ctx, tag, plus)
            return
        if ctx.locale.value == "de":
            await de.nsfw(self.bot).yandere(ctx, tag, plus)
            return
        await en.nsfw(self.bot).yandere(ctx, tag, plus)


    @Jeanne.command(
        description=T("konachan_desc"),
        nsfw=True,
        extras={
            "nsfw": True,
            "en": {
                "name": "konachan",
                "description": "Get a random media content from Konachan",
                "parameters": [
                    {"name": "tag", "description": "Add your tags", "required": False},
                    {
                        "name": "plus",
                        "description": "Need more content? (up to 4)",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "konachan",
                "description": "Obtenez un contenu multimédia aléatoire de Konachan",
                "parameters": [
                    {
                        "name": "tag",
                        "description": "Ajoutez vos tags",
                        "required": False,
                    },
                    {
                        "name": "plus",
                        "description": "Besoin de plus de contenu? (jusqu'à 4)",
                        "required": False,
                    },
                ],
            },
            "de": {
                "name": "konachan",
                "description": "Holen Sie sich einen zufälligen Medieninhalt von Konachan",
                "parameters": [
                    {
                        "name": "tag",
                        "description": "Fügen Sie Ihre Tags hinzu",
                        "required": False,
                    },
                    {
                        "name": "plus",
                        "description": "Brauchen Sie mehr Inhalte? (bis zu 4)",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(
        tag=T("tag_parm_desc"),
        plus=T("plus_parm_desc"),
    )
    @Jeanne.rename(
        tag=T("tag_parm_name"),
        plus=T("plus_parm_name"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def konachan(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if ctx.locale.value == "fr":
            await fr.nsfw(self.bot).konachan(ctx, tag, plus)
            return
        if ctx.locale.value == "de":
            await de.nsfw(self.bot).konachan(ctx, tag, plus)
            return
        await en.nsfw(self.bot).konachan(ctx, tag, plus)


    @Jeanne.command(
        description=T("danbooru_desc"),
        nsfw=True,
        extras={
            "nsfw": True,
            "en": {
                "name": "danbooru",
                "description": "Get a random media content from Danbooru",
                "parameters": [
                    {"name": "tag", "description": "Add your tags", "required": False},
                    {
                        "name": "plus",
                        "description": "Need more content? (up to 4)",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "danbooru",
                "description": "Obtenez un contenu multimédia aléatoire de Danbooru",
                "parameters": [
                    {
                        "name": "tag",
                        "description": "Ajoutez vos tags",
                        "required": False,
                    },
                    {
                        "name": "plus",
                        "description": "Besoin de plus de contenu? (jusqu'à 4)",
                        "required": False,
                    },
                ],
            },
            "de": {
                "name": "danbooru",
                "description": "Holen Sie sich einen zufälligen Medieninhalt von Danbooru",
                "parameters": [
                    {
                        "name": "tag",
                        "description": "Fügen Sie Ihre Tags hinzu",
                        "required": False,
                    },
                    {
                        "name": "plus",
                        "description": "Brauchen Sie mehr Inhalte? (bis zu 4)",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(
        tag=T("tag_parm_desc"),
        plus=T("plus_parm_desc"),
    )
    @Jeanne.rename(
        tag=T("tag_parm_name"),
        plus=T("plus_parm_name"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def danbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if ctx.locale.value == "fr":
            await fr.nsfw(self.bot).danbooru(ctx, tag, plus)
            return
        if ctx.locale.value == "de":
            await de.nsfw(self.bot).danbooru(ctx, tag, plus)
            return
        await en.nsfw(self.bot).danbooru(ctx, tag, plus)


    @hentai.error
    @konachan.error
    @yandere.error
    @danbooru.error
    async def Hentai_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            if ctx.locale.value == "fr":
                await fr.nsfw(self.bot).Hentai_error(ctx, error, "NotFound")
                return
            if ctx.locale.value == "de":
                await de.nsfw(self.bot).Hentai_error(ctx, error, "NotFound")
                return
            await en.nsfw(self.bot).Hentai_error(ctx, error, "NotFound")

        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            if ctx.locale.value == "fr":
                await fr.nsfw(self.bot).Hentai_error(ctx, error, "Cooldown")
                return
            if ctx.locale.value == "de":
                await de.nsfw(self.bot).Hentai_error(ctx, error, "Cooldown")
                return
            await en.nsfw(self.bot).Hentai_error(ctx, error, "Cooldown")


async def setup(bot: Bot):
    await bot.add_cog(nsfw(bot))
