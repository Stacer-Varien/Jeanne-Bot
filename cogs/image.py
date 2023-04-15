from functions import Botban
from discord import Color, Embed, Interaction, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from config import kitsune_nekoslife, neko_purrbot
from requests import get
from assets.images import (
    get_jeanne_pic,
    get_medusa_pic,
    get_saber_pic,
    get_wallpaper_pic,
    safebooru_pic,
)


class images(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Jeanne.command(description="Get a kitsune image")
    async def kitsune(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        kistune_api = get(kitsune_nekoslife).json()
        kitsune = Embed(color=Color.random())
        kitsune.set_footer(
            text="Fetched from nekos.life • Credits must go to the artist"
        )
        kitsune.set_image(url=kistune_api["url"])
        await ctx.followup.send(embed=kitsune)

    @Jeanne.command(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        wallpaper = Embed(color=Color.random())
        wallpaper.set_image(url=get_wallpaper_pic())
        wallpaper.set_footer(
            text="Fetched from Wallpaper_1936 • Credits must go to the artist"
        )
        await ctx.followup.send(embed=wallpaper)

    @Jeanne.command(description="Get a Jeanne d'Arc image")
    async def jeanne(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        jeanne = Embed(color=Color.random())
        jeanne.set_image(url=get_jeanne_pic())
        jeanne.set_footer(
            text="Fetched from Jeanne_1936 • Credits must go to the artist"
        )
        await ctx.followup.send(embed=jeanne)

    @Jeanne.command(description="Get a Saber image")
    async def saber(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        saber = Embed(color=Color.random())
        saber.set_image(url=get_saber_pic())
        saber.set_footer(text="Fetched from Saber_1936 • Credits must go to the artist")
        await ctx.followup.send(embed=saber)

    @Jeanne.command(description="Get a neko image")
    async def neko(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        neko_api = get(neko_purrbot).json()
        neko = Embed(color=Color.random())
        neko.set_image(url=neko_api["link"])
        neko.set_footer(
            text="Fetched from PurrBot.site • Credits must go to the artist"
        )
        await ctx.followup.send(embed=neko)

    @Jeanne.command(description="Get a Medusa (Fate) image")
    async def medusa(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        medusa = Embed(color=Color.random())
        medusa.set_image(url=get_medusa_pic())
        medusa.set_footer(
            text="Fetched from Medusa_1936 • Credits must go to the artist"
        )
        await ctx.followup.send(embed=medusa)

    @Jeanne.command(description="Get an image from Safebooru")
    async def safebooru(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_image(url=safebooru_pic())
        embed.set_footer(text="Fetched from Safebooru • Credits must go to the artist")
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(images(bot))
