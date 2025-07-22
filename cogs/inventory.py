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


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description=T("country_desc"),
        extras={
            "en": {"name": "country", "description": "Buy a country badge"},
            "fr": {"name": "pays", "description": "Acheter un badge de pays"},
        },
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def country(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Shop_Group(self.bot).country(ctx)
        elif ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).country(ctx)

    @Jeanne.command(
        description=T("backgrounds_desc"),
        extras={
            "en": {
                "name": "backgrounds",
                "description": "Check all the wallpapers available",
            },
            "fr": {
                "name": "fonds d'écran",
                "description": "Vérifiez tous les fonds d'écran disponibles",
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

    @backgrounds.error
    async def backgrounds_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Shop_Group(self.bot).backgrounds_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).backgrounds_error(ctx, error)


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
        },
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.describe(name=T("buycustom_name_desc"), link=T("buycustom_link_desc"))
    @Jeanne.rename(name="name_parm_name", link="link_parm_name")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def buycustom(self, ctx: Interaction, name: str, link: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Background_Group(self.bot).buycustom(ctx, name, link)
        elif ctx.locale.value == "fr":
            await fr.Background_Group(self.bot).buycustom(ctx, name, link)

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

    @Jeanne.command(
        name=T("list_name"),
        description=T("list_desc"),
        extras={
            "en": {"name": "list", "description": "Check which backgrounds you have"},
            "fr": {
                "name": "liste",
                "description": "Vérifiez quels fonds d'écran vous avez",
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


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))
