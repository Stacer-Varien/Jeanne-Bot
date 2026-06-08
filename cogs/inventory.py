from functions import (
    Currency,
    Inventory,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from assets.components import Confirmation
from discord import Attachment, Color, Embed, Interaction, app_commands as Jeanne
from discord.ext.commands import Bot, GroupCog
from discord.app_commands import locale_str as T
from typing import Optional
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
        if ctx.locale.value not in ("fr", "de"):
            await en.Shop_Group(self.bot).backgrounds(ctx)
        elif ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).backgrounds(ctx)
        elif ctx.locale.value == "de":
            await de.Shop_Group(self.bot).backgrounds(ctx)

    @backgrounds.error
    async def backgrounds_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value not in ("fr", "de"):
            await en.Shop_Group(self.bot).backgrounds_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.Shop_Group(self.bot).backgrounds_error(ctx, error)
        elif ctx.locale.value == "de":
            await de.Shop_Group(self.bot).backgrounds_error(ctx, error)

    @Jeanne.command(
        name="animated-profile",
        description="Permanently unlock animated profile cards for 10,000 QP",
        extras={
            "en": {
                "name": "animated-profile",
                "description": "Permanently unlock animated profile cards for 10,000 QP",
            },
            "fr": {
                "name": "profil-animé",
                "description": "Débloquez définitivement les cartes de profil animées pour 10 000 QP",
            },
            "de": {
                "name": "animiertes-profil",
                "description": "Schalte animierte Profilkarten dauerhaft für 10.000 QP frei",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def animated_profile(self, ctx: Interaction):
        inventory = Inventory(ctx.user)
        locale = ctx.locale.value
        if inventory.animated_profile_unlocked:
            messages = {
                "fr": "Vous avez déjà débloqué les cartes de profil animées.",
                "de": "Du hast animierte Profilkarten bereits freigeschaltet.",
            }
            await ctx.response.send_message(
                messages.get(locale, "You have already unlocked animated profile cards.")
            )
            return
        if Currency(ctx.user).get_balance < 10000:
            messages = {
                "fr": "Vous avez besoin de 10 000 QP pour débloquer les cartes de profil animées.",
                "de": "Du benötigst 10.000 QP, um animierte Profilkarten freizuschalten.",
            }
            await ctx.response.send_message(
                messages.get(
                    locale,
                    "You need 10,000 QP to unlock animated profile cards.",
                )
            )
            return

        descriptions = {
            "fr": "Débloquer définitivement les cartes de profil animées pour **10 000 QP** ?",
            "de": "Animierte Profilkarten dauerhaft für **10.000 QP** freischalten?",
        }
        view = Confirmation(ctx, ctx.user)
        await ctx.response.send_message(
            embed=Embed(
                description=descriptions.get(
                    locale,
                    "Permanently unlock animated profile cards for **10,000 QP**?",
                ),
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        if not view.value:
            await ctx.edit_original_response(
                embed=Embed(description="Cancelled", color=Color.red()), view=None
            )
            return

        unlocked = await inventory.unlock_animated_profile()
        messages = {
            "fr": "Les cartes de profil animées sont maintenant débloquées.",
            "de": "Animierte Profilkarten sind jetzt freigeschaltet.",
        }
        description = messages.get(
            locale, "Animated profile cards are now unlocked."
        )
        if not unlocked:
            description = "Your balance changed before the purchase could complete."
        await ctx.edit_original_response(
            embed=Embed(description=description, color=Color.random()), view=None
        )


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
                    {"name": "link", "description": "Add an image link", "required": False},
                    {"name": "image", "description": "Upload an image or GIF", "required": False},
                ],
            },
            "fr": {
                "name": "buy-custom",
                "description": "Acheter une image de fond personnalisée pour votre carte de niveau",
                "parameters": [
                    {
                        "name": "nom",
                        "description": "Comment voulez-vous l'appeler?",
                        "required": False,
                    },
                    {"name": "image", "description": "Téléversez une image ou un GIF", "required": False},
                    {
                        "name": "lien",
                        "description": "Ajoutez un lien d'image",
                        "required": False,
                    },
                    {"name": "image", "description": "Lade ein Bild oder GIF hoch", "required": False},
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
    @Jeanne.describe(
        name=T("name_parm_desc"),
        link=T("link_parm_desc"),
        image="Upload an image or GIF",
    )
    @Jeanne.rename(name=T("name_parm_name"), link=T("link_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def buycustom(
        self,
        ctx: Interaction,
        name: str,
        link: Optional[str] = None,
        image: Optional[Attachment] = None,
    ):
        if image and image.size > ctx.filesize_limit:
            await ctx.response.send_message(
                f"The uploaded file must be below {ctx.filesize_limit // (1024 * 1024)} MB."
            )
            return
        source_url = image.url if image else link
        if not source_url:
            await ctx.response.send_message("Add an image link or upload an image/GIF.")
            return
        if ctx.locale.value not in ("fr", "de"):
            await en.Background_Group(self.bot).buycustom(ctx, name, source_url)
        elif ctx.locale.value == "fr":
            await fr.Background_Group(self.bot).buycustom(ctx, name, source_url)
        elif ctx.locale.value == "de":
            await de.Background_Group(self.bot).buycustom(ctx, name, source_url)

    @buycustom.error
    async def buycustom_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value not in ("fr", "de"):
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
        if ctx.locale.value not in ("fr", "de"):
            await en.Background_Group(self.bot).list(ctx)
        elif ctx.locale.value == "fr":
            await fr.Background_Group(self.bot).list(ctx)
        elif ctx.locale.value == "de":
            await de.Background_Group(self.bot).list(ctx)


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))
