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
from discord.app_commands import locale_str as T


class nsfw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name=T("hentai_name"),
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.nsfw(self.bot).nsfw(ctx)
        elif ctx.locale.value == "fr":
            await fr.nsfw(self.bot).nsfw(ctx)

    @Jeanne.command(
        description=T("gelbooru_desc"),
        nsfw=True,
        extras={
            "nsfw": True,
            "en": {
                "name": "gelbooru",
                "description": "Get a random media content from Gelbooru",
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
                "name": "gelbooru",
                "description": "Obtenez un contenu multimédia aléatoire de Gelbooru",
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
        },
    )
    @Jeanne.checks.cooldown(1, 5, key=lambda i: (i.user.id))
    @Jeanne.describe(tag=T("tag_parm_desc"), plus=T("plus_parm_desc"))
    @Jeanne.rename(tag=T("tag_parm_name"), plus=T("plus_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def gelbooru(
        self,
        ctx: Interaction,
        tag: Optional[str] = None,
        plus: Optional[bool] = None,
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.nsfw(self.bot).gelbooru(ctx, tag, plus)
        elif ctx.locale.value == "fr":
            await fr.nsfw(self.bot).gelbooru(ctx, tag, plus)

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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.nsfw(self.bot).yandere(ctx, tag, plus)
        elif ctx.locale.value == "fr":
            await fr.nsfw(self.bot).yandere(ctx, tag, plus)

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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.nsfw(self.bot).konachan(ctx, tag, plus)
        elif ctx.locale.value == "fr":
            await fr.nsfw(self.bot).konachan(ctx, tag, plus)

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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.nsfw(self.bot).danbooru(ctx, tag, plus)
        elif ctx.locale.value == "fr":
            await fr.nsfw(self.bot).danbooru(ctx, tag, plus)

    @hentai.error
    @gelbooru.error
    @konachan.error
    @yandere.error
    @danbooru.error
    async def Hentai_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, KeyError, TypeError)
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.nsfw(self.bot).Hentai_error(ctx, error, "NotFound ")
            elif ctx.locale.value == "fr":
                await fr.nsfw(self.bot).Hentai_error(ctx, error, "NotFound")
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.nsfw(self.bot).Hentai_error(ctx, error, "Cooldown")
            elif ctx.locale.value == "fr":
                await fr.nsfw(self.bot).Hentai_error(ctx, error, "Cooldown")


async def setup(bot: Bot):
    await bot.add_cog(nsfw(bot))
