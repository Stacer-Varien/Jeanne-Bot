from glob import glob
from requests import get
from random import choice
from nextcord import Embed, File
from nextcord.ext.commands import command as jeanne, Cog, cooldown, BucketType
from config import kitsune_nekoslife

class images(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def neko(self, ctx):
        file_path_type = ["./Media/Neko/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        neko = Embed(color=0xFFC0CB)
        neko.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=neko)

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def kitsune(self, ctx):
        kistune_api = get(kitsune_nekoslife).json()
        kitsune = Embed(color=0xFFC0CB)
        kitsune.set_footer(text="Fetched from nekos.life")
        kitsune.set_image(url=kistune_api["url"])
        await ctx.send(embed=kitsune)

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def wallpaper(self, ctx):
        file_path_type = ["./Media/Wallpaper/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        wallpaper = Embed(color=0xFFC0CB)
        wallpaper.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=wallpaper)


    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def saber(self, ctx):
        file_path_type = ["./Media/Saber/*.jpg", "./Media/Saber/*.png"]
        images = glob.glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        saber = Embed(color=0xFFC0CB)
        saber.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=saber)

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def jeanne(self, ctx):
        jeanne_folder = ["./Media/Jeanne/*.jpg"]
        jeanne_images = glob(choice(jeanne_folder))
        random_image = choice(jeanne_images)
        jeanne_pic = File(random_image)        
        jeanne = Embed(color=0xFFC0CB)
        jeanne.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=jeanne_pic, embed=jeanne)

def setup(bot):
    bot.add_cog(images(bot))
