from discord import Embed, File
from discord.ext.commands import Cog
from discord_slash.cog_ext import cog_slash as jeanne_slash
from glob import glob
from random import choice
from requests import get


class images(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get a kitsune image")
    async def kitsune(self, ctx):
        kistune_api = get("https://nekos.life/api/v2/img/fox_girl").json()
        kitsune = Embed(color=0xFFC0CB)
        kitsune.set_footer(text="Fetched from nekos.life")
        kitsune.set_image(url=kistune_api["url"])
        await ctx.send(embed=kitsune)

    @jeanne_slash(description="Need a wallpaper for your PC?")
    async def wallpaper(self, ctx):
        file_path_type = ["./Media/Wallpaper/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        wallpaper = Embed(color=0xFFC0CB)
        wallpaper.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=wallpaper)

    @jeanne_slash(description="Get a random Jeanne d'Arc image")
    async def jeanne(self, ctx):
        file_path_type = ["./Media/Jeanne/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        jeanne = Embed(color=0xFFC0CB)
        jeanne.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=jeanne)

    @jeanne_slash(description="Get a random Saber image")
    async def saber(self, ctx):
        file_path_type = ["./Media/Saber/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        saber = Embed(color=0xFFC0CB)
        saber.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=saber)

    @jeanne_slash(description="Get a random neko image")
    async def neko(self, ctx):
        file_path_type = ["./Media/Neko/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        neko = Embed(color=0xFFC0CB)
        neko.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=neko)


def setup(bot):
    bot.add_cog(images(bot))
