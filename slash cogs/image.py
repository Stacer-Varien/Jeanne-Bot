from db_functions import check_botbanned_user
from discord import *
from discord.ext.commands import Cog, hybrid_command, Bot, Context
from config import kitsune_nekoslife
from requests import get
from assets.imgur import *

class slashimages(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot


    @hybrid_command(description="Get a kitsune image", aliases=['foxgirl'])
    async def kitsune(self, ctx : Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            kistune_api = get(kitsune_nekoslife).json()
            kitsune = Embed(color=0xFFC0CB)
            kitsune.set_footer(text="Fetched from nekos.life")
            kitsune.set_image(url=kistune_api["url"])
            await ctx.send(embed=kitsune)
            
    @hybrid_command(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, ctx : Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            wallpaper = Embed(color=0xFFC0CB)
            wallpaper.set_image(url=get_wallpaper_pic())
            wallpaper.set_footer(text="Fetched from Wallpaper_1936")
            await ctx.send(embed=wallpaper)
        
    @hybrid_command(description="Get a Jeanne d'Arc image")
    async def jeanne(self, ctx : Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            jeanne = Embed(color=0xFFC0CB)
            jeanne.set_image(url=get_jeanne_pic())
            jeanne.set_footer(text="Fetched from Jeanne_1936")
            await ctx.send(embed=jeanne)

    @hybrid_command(description="Get a Saber image")
    async def saber(self, ctx : Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            saber = Embed(color=0xFFC0CB)
            saber.set_image(url=get_saber_pic())
            saber.set_footer(text="Fetched from Saber_1936")
            await ctx.send(embed=saber)

    @hybrid_command(description="Get a neko image", aliases=['catgirl'])
    async def neko(self, ctx : Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            neko = Embed(color=0xFFC0CB)
            neko.set_image(url=get_neko_pic())
            neko.set_footer(text="Fetched from Neko_1936")
            await ctx.send(embed=neko)

    @hybrid_command(description="Get a Medusa (Fate) image")
    async def medusa(self, ctx: Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            medusa = Embed(color=0xFFC0CB)
            medusa.set_image(url=get_medusa_pic())
            medusa.set_footer(text="Fetched from Medusa_1936")
            await ctx.send(embed=medusa)


async def setup(bot:Bot):
    await bot.add_cog(slashimages(bot))
