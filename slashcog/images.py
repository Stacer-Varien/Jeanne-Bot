import random
import requests
import glob
from discord import Embed, File
from discord.ext import commands
from discord_slash import cog_ext


class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Get a kitsune image")
    async def kitsune(self, ctx):
        kistune_api = requests.get("https://nekos.life/api/v2/img/fox_girl").json()
        kitsune = Embed(color=0xFFC0CB)
        kitsune.set_footer(text="Fetched from nekos.life")
        kitsune.set_image(url=kistune_api["url"])
        await ctx.send(embed=kitsune)

    @cog_ext.cog_slash(description="Need a wallpaper for your PC?")
    async def wallpaper(self, ctx):
        file_path_type = ["./Images/Wallpaper/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        wallpaper = Embed(color=0xFFC0CB)
        wallpaper.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=wallpaper)

    @cog_ext.cog_slash(description="Get a random Jeanne d'Arc image")
    async def jeanne(self, ctx):
        file_path_type = ["./Images/Jeanne/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        jeanne = Embed(color=0xFFC0CB)
        jeanne.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=jeanne)

    @cog_ext.cog_slash(description="Get a random Saber image")
    async def saber(self, ctx):
        file_path_type = ["./Images/Saber/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        saber = Embed(color=0xFFC0CB)
        saber.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=saber)


def setup(bot):
    bot.add_cog(images(bot))
