from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from config import kitsune_nekoslife
from glob import glob
from random import choice
from requests import get

class slashimages(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get a kitsune image")
    async def kitsune(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            kistune_api = get(kitsune_nekoslife).json()
            kitsune = Embed(color=0xFFC0CB)
            kitsune.set_footer(text="Fetched from nekos.life")
            kitsune.set_image(url=kistune_api["url"])
            await interaction.followup.send(embed=kitsune)

    @jeanne_slash(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            file_path_type = ["./Media/Wallpaper/*.jpg"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            wallpaper = Embed(color=0xFFC0CB)
            wallpaper.set_footer(text="Powered by JeanneBot")
            await interaction.followup.send(file=file, embed=wallpaper)

    @jeanne_slash(description="Get a Jeanne d'Arc image")
    async def jeanne(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            file_path_type = ["./Media/Jeanne/*.jpg"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            jeanne = Embed(color=0xFFC0CB)
            jeanne.set_footer(text="Powered by JeanneBot")
            await interaction.followup.send(file=file, embed=jeanne)

    @jeanne_slash(description="Get a Saber image")
    async def saber(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            file_path_type = ["./Media/Saber/*.jpg"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            saber = Embed(color=0xFFC0CB)
            saber.set_footer(text="Powered by JeanneBot")
            await interaction.followup.send(file=file, embed=saber)

    @jeanne_slash(description="Get a neko image")
    async def neko(self, interaction : Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            file_path_type = ["./Media/Neko/*.jpg"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            neko = Embed(color=0xFFC0CB)
            neko.set_footer(text="Powered by JeanneBot")
            await interaction.followup.send(file=file, embed=neko)


def setup(bot):
    bot.add_cog(slashimages(bot))
