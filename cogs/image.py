from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from discord import Color, Embed, Interaction, app_commands as Jeanne
from discord.ext.commands import GroupCog, Bot
from assets.images import (
    get_jeanne_pic,
    get_kistune_pic,
    get_medusa_pic,
    get_morgan_pic,
    get_neko_pic,
    get_saber_pic,
    get_wallpaper_pic,
    safebooru_pic,
)
from discord.app_commands import locale_str as T


class images(GroupCog, name="image"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description=T("kitsune_desc"),
        extras={
            "en": {"name": "kitsune", "description": "Get a random kitsune image"},
            "fr": {
                "name": "kitsune",
                "description": "Obtenez une image de kitsune aléatoire",
            },
            "de": {
                "name": "kitsune",
                "description": "Holen Sie sich ein zufälliges Kitsune-Bild",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def kitsune(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_kistune_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("wallpaper_desc"),
        extras={
            "en": {
                "name": "wallpaper",
                "description": "Get a random wallpaper for your PC or phone",
            },
            "fr": {
                "name": "wallpaper",
                "description": "Obtenez un fond d'écran aléatoire pour votre PC ou téléphone",
            },
            "de": {
                "name": "wallpaper",
                "description": "Holen Sie sich ein zufälliges Wallpaper für Ihren PC oder Ihr Telefon",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def wallpaper(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_wallpaper_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("jeanne_desc"),
        extras={
            "en": {
                "name": "jeanne",
                "description": "Get a random image of Jeanne d'Arc",
            },
            "fr": {
                "name": "jeanne",
                "description": "Obtenez une image aléatoire de Jeanne d'Arc",
            },
            "de": {
                "name": "jeanne",
                "description": "Holen Sie sich ein zufälliges Bild von Jeanne d'Arc",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def jeanne(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_jeanne_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("saber_desc"),
        extras={
            "en": {"name": "saber", "description": "Get a random Saber image"},
            "fr": {
                "name": "saber",
                "description": "Obtenez une image aléatoire de Saber",
            },
            "de": {
                "name": "saber",
                "description": "Holen Sie sich ein zufälliges Saber-Bild",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def saber(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_saber_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("neko_desc"),
        extras={
            "en": {"name": "neko", "description": "Get a random Neko image"},
            "fr": {
                "name": "neko",
                "description": "Obtenez une image aléatoire de Neko",
            },
            "de": {
                "name": "neko",
                "description": "Holen Sie sich ein zufälliges Neko-Bild",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def neko(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_neko_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("morgan_desc"),
        extras={
            "en": {
                "name": "morgan",
                "description": "Get a random image of Morgan Le Fay",
            },
            "fr": {
                "name": "morgan",
                "description": "Obtenez une image aléatoire de Morgan Le Fay",
            },
            "de": {
                "name": "morgan",
                "description": "Holen Sie sich ein zufälliges Bild von Morgan Le Fay",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def morgan(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_morgan_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("medusa_desc"),
        extras={
            "en": {"name": "medusa", "description": "Get a random Medusa image"},
            "fr": {
                "name": "medusa",
                "description": "Obtenez une image aléatoire de Medusa",
            },
            "de": {
                "name": "medusa",
                "description": "Holen Sie sich ein zufälliges Bild von Medusa",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def medusa(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_medusa_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        description=T("safebooru_desc"),
        extras={
            "en": {
                "name": "safebooru",
                "description": "Get a random image from Safebooru",
            },
            "fr": {
                "name": "safebooru",
                "description": "Obtenez une image aléatoire de Safebooru",
            },
            "de": {
                "name": "safebooru",
                "description": "Holen Sie sich ein zufälliges Bild von Safebooru",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def safebooru(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_image(url=safebooru_pic())
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            embed.set_footer(
                text="Fetched from Safebooru • Credits must go to the artist"
            )
            return
        if ctx.locale.value=="de":
            embed.set_footer(
                text="Von Safebooru abgerufen • Die Credits müssen an den Künstler gehen"
            )
            return
        if ctx.locale.value == "fr":
            embed.set_footer(
                text="Récupéré depuis Safebooru • Les crédits doivent aller à l'artiste"
            )
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(images(bot))
