import discord, random, requests
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

badtags = ["+loli", "+shota", "+cub", "+scat",
           "+shit", "+vore", "+gore", "+guro"]


class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Get a kitsune image")
    async def kitsune(self, ctx: SlashContext):
        kistune_api = requests.get("https://nekos.life/api/v2/img/fox_girl").json()
        kitsune = Embed(color=0xFFC0CB)
        kitsune.set_footer(text="Fetched from nekos.life")
        kitsune.set_image(url=kistune_api["url"])
        await ctx.send(embed=kitsune)

    @cog_ext.cog_slash(description="Need a wallpaper for your PC?")
    async def wallpaper(self, ctx: SlashContext):
        wallpaper_api = requests.get(
            "https://nekos.life/api/v2/img/wallpaper").json()
        wallpaper = Embed(color=0xFFC0CB)
        wallpaper.set_footer(text="Fetched from nekos.life")
        wallpaper.set_image(url=wallpaper_api["url"])
        await ctx.send(embed=wallpaper)

    @cog_ext.cog_slash(description="Get a random Jeanne d'Arc image")
    async def jeanne(self, ctx: SlashContext):
        jeanne_api_yandere = random.choice(requests.get(
            "https://yande.re/post.json?tags=rating:safe+jeanne_d'arc").json())

        jeanne_gelbooru_api = random.choice(requests.get(
            "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:safe +jeanne_d'arc_(fate)").json())

        jeanne_images=[jeanne_api_yandere, jeanne_gelbooru_api]   

        jeanne = discord.Embed(color=0xFFC0CB)
        jeanne.set_image(url=random.choice(jeanne_images)["file_url"])
        jeanne.set_footer(text="Jeanne d'Arc")
        await ctx.send(embed=jeanne)

    @cog_ext.cog_slash(description="Get a random Saber image")
    async def saber(self, ctx: SlashContext):
        saber_api_yandere = random.choice(requests.get(
            "https://yande.re/post.json?tags=rating:safe+saber").json())

        saber_gelbooru_api = random.choice(requests.get(
            "https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:safe +saber").json())

        saber_images = [saber_api_yandere, saber_gelbooru_api]

        saber = discord.Embed(color=0xFFC0CB)
        saber.set_image(url=random.choice(saber_images)["file_url"])
        saber.set_footer(text="Saber")
        await ctx.send(embed=saber)



def setup(bot):
    bot.add_cog(images(bot))
