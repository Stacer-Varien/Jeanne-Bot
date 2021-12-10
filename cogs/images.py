import random, requests, glob
from discord import Embed, File
from discord.ext import commands


class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kitsune(self, ctx):
        kistune_api = requests.get("https://nekos.life/api/v2/img/fox_girl").json()
        kitsune = Embed(color=0xFFC0CB)
        kitsune.set_footer(text="Fetched from nekos.life")
        kitsune.set_image(url=kistune_api["url"])
        await ctx.send(embed=kitsune)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wallpaper(self, ctx):
        file_path_type = ["./Images/Wallpaper/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        wallpaper = Embed(color=0xFFC0CB)
        wallpaper.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=wallpaper)


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def saber(self, ctx):
        file_path_type = ["./Images/Saber/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        saber = Embed(color=0xFFC0CB)
        saber.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=saber)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jeanne(self, ctx):
        file_path_type = ["./Images/Jeanne/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        jeanne = Embed(color=0xFFC0CB)
        jeanne.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=jeanne)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def neko(self, ctx):
        file_path_type = ["./Images/Neko/*.jpg"]
        images = glob.glob(random.choice(file_path_type))
        random_image = random.choice(images)
        file = File(random_image)
        neko = Embed(color=0xFFC0CB)
        neko.set_footer(text="Powered by JeanneBot")
        await ctx.send(file=file, embed=neko)



def setup(bot):
    bot.add_cog(images(bot))
