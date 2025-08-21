from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from discord import Interaction, app_commands as Jeanne
from discord.ext.commands import Bot, GroupCog
from discord.app_commands import locale_str as T
import languages.en.inventory as en
import languages.fr.inventory as fr
import languages.de.inventory as de


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description=T("country_desc"),
        extras={
            "en": {"name": "country", "description": "Buy a country badge"},
            "fr": {"name": "pays", "description": "Acheter un badge de pays"},
            "de": {"name": "land", "description": "Kaufen Sie ein Länderabzeichen"}
        },
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def country(self, ctx: Interaction):
        if ctx.locale.value == "de":
            await de.Shop_Group(self.bot).country(ctx)
            return
        if ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).country(ctx)
            return    
        await en.Shop_Group(self.bot).country(ctx)

    @Jeanne.command(
        description=T("backgrounds_desc"),
        extras={
            "en": {
                "name": "backgrounds",
                "description": "Check all the wallpapers available",
            },
            "fr": {
                "name": "backgrounds",
                "description": "Vérifiez tous les backgrounds disponibles",
            },
            "de": {
                "name": "hintergründe",
                "description": "Überprüfen Sie alle verfügbaren Hintergründe",
            },
        },
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def backgrounds(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Shop_Group(self.bot).backgrounds(ctx)
        elif ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).backgrounds(ctx)
        elif ctx.locale.value == "de":
            await de.Shop_Group(self.bot).backgrounds(ctx)

    @backgrounds.error
    async def backgrounds_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Shop_Group(self.bot).backgrounds_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).backgrounds_error(ctx, error)
        elif ctx.locale.value == "de":
            await de.Shop_Group(self.bot).backgrounds_error(ctx, error)


class Background_Group(GroupCog, name="background"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name="buy-custom",
        description=T("buycustom_desc"),
        extras={
            "en": {
                "name": "buycustom",
                "description": "Buy a custom background pic for your level card",
                "parameters": [
                    {
                        "name": "name",
                        "description": "What will you name it?",
                        "required": True,
                    },
                    {
                        "name": "link",
                        "description": "Add an image link",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "buy-custom",
                "description": "Acheter une image de fond personnalisée pour votre carte de niveau",
                "parameters": [
                    {
                        "name": "nom",
                        "description": "Comment voulez-vous l'appeler?",
                        "required": True,
                    },
                    {
                        "name": "lien",
                        "description": "Ajoutez un lien d'image",
                        "required": True,
                    },
                ],
            },
            "de": {
                "name": "buy-custom",
                "description": "Kaufen Sie ein benutzerdefiniertes Hintergrundbild für Ihre Levelkarte",
                "parameters": [
                    {
                        "name": "name",
                        "description": "Wie möchten Sie es nennen?",
                        "required": True,
                    },
                    {
                        "name": "link",
                        "description": "Fügen Sie einen Bildlink hinzu",
                        "required": True,
                    },
                ],
            },
        },
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.describe(name=T("name_parm_desc"), link=T("link_parm_desc"))
    @Jeanne.rename(name="name_parm_name", link="link_parm_name")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def buycustom(self, ctx: Interaction, name: str, link: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Background_Group(self.bot).buycustom(ctx, name, link)
        elif ctx.locale.value == "fr":
            await fr.Background_Group(self.bot).buycustom(ctx, name, link)
        elif ctx.locale.value == "de":
            await de.Background_Group(self.bot).buycustom(ctx, name, link)

    @buycustom.error
    async def buycustom_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Background_Group(self.bot).buycustom_error(
                ctx,
                error,
                (
                    "cooldown"
                    if isinstance(error, Jeanne.CommandOnCooldown)
                    else "invalid"
                ),
            )
        elif ctx.locale.value == "fr":
            await fr.Background_Group(self.bot).buycustom_error(
                ctx,
                error,
                (
                    "cooldown"
                    if isinstance(error, Jeanne.CommandOnCooldown)
                    else "invalid"
                ),
            )
        elif ctx.locale.value == "de":
            await de.Background_Group(self.bot).buycustom_error(
                ctx,
                error,
                (
                    "cooldown"
                    if isinstance(error, Jeanne.CommandOnCooldown)
                    else "invalid"
                ),
            )

    @Jeanne.command(
        name=T("list_name"),
        description=T("list_desc"),
        extras={
            "en": {"name": "list", "description": "Check which backgrounds you have"},
            "fr": {
                "name": "liste",
                "description": "Vérifiez quels fonds d'écran vous avez",
            },
            "de": {
                "name": "liste",
                "description": "Überprüfen Sie, welche Hintergründe Sie haben",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _list(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Background_Group(self.bot).list(ctx)
        elif ctx.locale.value == "fr":
            await fr.Background_Group(self.bot).list(ctx)
        elif ctx.locale.value == "de":
            await de.Background_Group(self.bot).list(ctx)


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))
