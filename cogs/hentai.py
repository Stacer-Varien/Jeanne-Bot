from json import loads
from nextcord import *
from nextcord import slash_command as jeanne_slash
from glob import glob
from nextcord.ext.commands import Cog
from random import choice
from requests import get
from nextcord.ext.application_checks import *
from config import db




class slashnsfw(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get a random hentai from Jeanne")
    @is_nsfw()
    async def hentai(self, interaction: Interaction):
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
            file_path_type = ["/Media/Hentai/*.*"]
            images = glob(choice(file_path_type))
            random_image = choice(images)
            file = File(random_image)
            hentai = Embed(color=0xFFC0CB)
            hentai.set_footer(text="Powered by JeanneBot")
            await interaction.followup.send(file, embed=hentai)


    @jeanne_slash(description="Get a random hentai from Yande.re")
    @is_nsfw()
    async def yandere(self, interaction: Interaction, tag=SlashOption(description="Add a tag for something specific", required=False)):
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
                try:
                    if tag == None:
                        yandere_api = choice(get(
                            "https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub").json())

                    elif tag == "02":
                        await interaction.followup.send("Tag has been blacklisted due to it returning extreme content and guro")

                    else:
                        yandere_api = choice(get(
                            f"https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub+{tag}").json())

                    yandere = Embed(color=0xFFC0CB)
                    yandere.set_image(url=yandere_api['file_url'])
                    yandere.set_footer(text="Fetched from Yande.re")
                    await interaction.followup.send(embed=yandere)
                except IndexError:
                    pass

    @jeanne_slash(description="Get hentai from Gelbooru")
    @is_nsfw()
    async def gelbooru(self, interaction: Interaction, tag=SlashOption(description="Add a tag for something specific", required=False)):
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
                if tag == None:
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit+-loli+-shota+-cub"

                else:
                    gelbooru_api = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit+-loli+-shota+-cub+{tag}"
                try:
                    response = get(gelbooru_api)
                    json_api_url = loads(response.text)
                    image_url = choice(json_api_url['post'])["file_url"]


                    gelbooru = Embed(color=0xFFC0CB)
                    gelbooru.set_image(url=image_url)
                    gelbooru.set_footer(text="Fetched from Gelbooru")
                    await interaction.followup.send(embed=gelbooru)
                except KeyError:
                    pass

    @jeanne_slash(description="Get a random hentai from Konachan")
    @is_nsfw()
    async def konachan(self, interaction: Interaction, tag=SlashOption(description="Add a tag for something specific", required=False)):
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
                try:
                    if tag == None:
                        konachan_api = choice(get(
                            "https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub").json())

                    else:
                        konachan_api = choice(get(
                            f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub+{tag}").json())

                    konachan = Embed(color=0xFFC0CB)
                    konachan.set_image(url=konachan_api['file_url'])
                    konachan.set_footer(text="Fetched from Konachan")
                    await interaction.followup.send(embed=konachan)
                except IndexError:
                    pass


def setup(bot):
    bot.add_cog(slashnsfw(bot))
