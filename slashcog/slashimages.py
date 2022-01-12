from nextcord import Embed, File, Interaction, slash_command as jeanne_slash
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
        kistune_api = get(kitsune_nekoslife).json()
        kitsune = Embed(color=0xFFC0CB)
        kitsune.set_footer(text="Fetched from nekos.life")
        kitsune.set_image(url=kistune_api["url"])
        await interaction.response.send_message(embed=kitsune)

    @jeanne_slash(description="Need a wallpaper for your PC?")
    async def wallpaper(self, interaction : Interaction):
        file_path_type = ["./Media/Wallpaper/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        wallpaper = Embed(color=0xFFC0CB)
        wallpaper.set_footer(text="Powered by JeanneBot")
        await interaction.response.defer()
        await interaction.followup.send(file=file, embed=wallpaper)

    @jeanne_slash(description="Get a random Jeanne d'Arc image")
    async def jeanne(self, interaction : Interaction):
        file_path_type = ["./Media/Jeanne/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        jeanne = Embed(color=0xFFC0CB)
        jeanne.set_footer(text="Powered by JeanneBot")
        await interaction.response.defer()
        await interaction.followup.send(file=file, embed=jeanne)

    @jeanne_slash(description="Get a random Saber image")
    async def saber(self, interaction : Interaction):
        file_path_type = ["./Media/Saber/*.jpg", "./Media/Saber/*.png"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        saber = Embed(color=0xFFC0CB)
        saber.set_footer(text="Powered by JeanneBot")
        await interaction.response.defer()
        await interaction.followup.send(file=file, embed=saber)

    @jeanne_slash(description="Get a random neko image")
    async def neko(self, interaction : Interaction):
        file_path_type = ["./Media/Neko/*.jpg"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        neko = Embed(color=0xFFC0CB)
        neko.set_footer(text="Powered by JeanneBot")
        await interaction.response.defer()
        await interaction.followup.send(file=file, embed=neko)


def setup(bot):
    bot.add_cog(slashimages(bot))
