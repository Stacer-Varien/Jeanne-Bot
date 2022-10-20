from db_functions import check_botbanned_user
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from config import kitsune_nekoslife
from requests import get
from assets.imgur import *

class slashimages(Cog):
    def __init__(self, bot):
        self.bot = bot


    @jeanne_slash(description="Get a kitsune image")
    async def kitsune(self, ctx : Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            kistune_api = get(kitsune_nekoslife).json()
            kitsune = Embed(color=0xFFC0CB)
            kitsune.set_footer(text="Fetched from nekos.life")
            kitsune.set_image(url=kistune_api["url"])
            await ctx.followup.send(embed=kitsune)
            
    @jeanne_slash(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, ctx : Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            wallpaper = Embed(color=0xFFC0CB)
            wallpaper.set_image(url=get_wallpaper_pic())
            wallpaper.set_footer(text="Fetched from Wallpaper_1936")
            await ctx.followup.send(embed=wallpaper)
        
    @jeanne_slash(description="Get a Jeanne d'Arc image")
    async def jeanne(self, ctx : Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            jeanne = Embed(color=0xFFC0CB)
            jeanne.set_image(url=get_jeanne_pic())
            jeanne.set_footer(text="Fetched from Jeanne_1936")
            await ctx.followup.send(embed=jeanne)

    @jeanne_slash(description="Get a Saber image")
    async def saber(self, ctx : Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            saber = Embed(color=0xFFC0CB)
            saber.set_image(url=get_saber_pic())
            saber.set_footer(text="Fetched from Saber_1936")
            await ctx.followup.send(embed=saber)

    @jeanne_slash(description="Get a neko image")
    async def neko(self, ctx : Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            neko = Embed(color=0xFFC0CB)
            neko.set_image(url=get_neko_pic())
            neko.set_footer(text="Fetched from Neko_1936")
            await ctx.followup.send(embed=neko)

    @jeanne_slash(description="Get a Medusa (Fate) image")
    async def medusa(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            medusa = Embed(color=0xFFC0CB)
            medusa.set_image(url=get_medusa_pic())
            medusa.set_footer(text="Fetched from Medusa_1936")
            await ctx.followup.send(embed=medusa)


def setup(bot):
    bot.add_cog(slashimages(bot))
