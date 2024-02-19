from functions import Botban, Command
from discord import Color, Embed, Interaction, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from config import kitsune_nekoslife
from requests import get
from assets.images import (
    get_jeanne_pic,
    get_medusa_pic,
    get_morgan_pic,
    get_neko_pic,
    get_saber_pic,
    get_wallpaper_pic,
    safebooru_pic,
)


class images(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Jeanne.command(description="Get a kitsune image")
    async def kitsune(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return

        if Command(ctx.guild).check_disabled(self.kitsune.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        kistune_api = get(kitsune_nekoslife).json()
        kitsune = Embed(color=Color.random())
        kitsune.set_footer(
            text="Fetched from nekos.life • Credits must go to the artist"
        )
        kitsune.set_image(url=kistune_api["url"])
        await ctx.followup.send(embed=kitsune)

    @Jeanne.command(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.wallpaper.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed, file = get_wallpaper_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get a Jeanne d'Arc image")
    async def jeanne(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.jeanne.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed, file = get_jeanne_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get a Saber image")
    async def saber(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.saber.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed, file = get_saber_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get a neko image")
    async def neko(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.neko.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        embed, file = get_neko_pic()
        await ctx.followup.send(file=file, embed=embed)

    @Jeanne.command(description="Get a Morgan le Fay (Fate) image")
    async def morgan(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return

        if Command(ctx.guild).check_disabled(self.morgan.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        embed, file = get_morgan_pic()
        await ctx.followup.send(file=file, embed=embed)

    @Jeanne.command(description="Get a Medusa (Fate) image")
    async def medusa(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.medusa.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed, file = get_medusa_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(description="Get an image from Safebooru")
    async def safebooru(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.safebooru.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_image(url=safebooru_pic())
        embed.set_footer(text="Fetched from Safebooru • Credits must go to the artist")
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(images(bot))
