from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from config import kitsune_nekoslife
from glob import glob
from random import choice
from requests import get
from assets.media import *



class slashimages(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get a kitsune image")
    async def kitsune(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            kistune_api = get(kitsune_nekoslife).json()
            kitsune = Embed(color=0xFFC0CB)
            kitsune.set_footer(text="Fetched from nekos.life")
            kitsune.set_image(url=kistune_api["url"])
            await ctx.followup.send(embed=kitsune)
            
    @jeanne_slash(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            wallpaper = Embed(color=0xFFC0CB)
            wallpaper.set_image(url=choice(wallpaper1936))
            wallpaper.set_footer(text="Fetched from Wallpaper_1936")
            await ctx.followup.send(embed=wallpaper)
        
    @jeanne_slash(description="Get a Jeanne d'Arc image")
    async def jeanne(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            file_path_type = ["./Media/Jeanne/*.jpg"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            jeanne = Embed(color=0xFFC0CB)
            jeanne.set_footer(text="Powered by JeanneBot")
            await ctx.followup.send(file=file, embed=jeanne)

    @jeanne_slash(description="Get a Saber image")
    async def saber(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            file_path_type = ["./Media/Saber/*.jpg"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            saber = Embed(color=0xFFC0CB)
            saber.set_footer(text="Powered by JeanneBot")
            await ctx.followup.send(file=file, embed=saber)

    @jeanne_slash(description="Get a neko image")
    async def neko(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            neko = Embed(color=0xFFC0CB)
            neko.set_image(url=choice(neko1936))
            neko.set_footer(text="Fetched from Neko_1936")
            await ctx.followup.send(embed=neko)


def setup(bot):
    bot.add_cog(slashimages(bot))
