from nextcord import Embed, File, slash_command as jeanne_slash, Interaction, SlashOption
from glob import glob
from nextcord.ext.commands import Cog
from random import choice
from requests import get
from assets.needed import illegal_tags, test_server
from assets.errormsgs import no_hentai

class slashnsfw(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @jeanne_slash(description="Get a random hentai from Jeanne", guild_ids=[test_server])
    async def hentai(self, interaction : Interaction):
        file_path_type = ["./Media/Hentai/*.jpg", "./Media/Hentai/*.mp4"]
        images = glob(choice(file_path_type))
        random_image = choice(images)
        file = File(random_image)
        hentai = Embed(color=0xFFC0CB)
        hentai.set_footer(text="Powered by JeanneBot")
        await interaction.response.defer()
        if interaction.channel.is_nsfw():
            await interaction.followup.send(file=file, embed=hentai)
        else:
            await interaction.followup.send(embed=no_hentai)


    @jeanne_slash(description="Get a random hentai from Yande.re")
    async def yandere(self, interaction : Interaction, tag=SlashOption(description="Put a tag but note that some are blacklisted", required=False)):
        if interaction.channel.is_nsfw():
            try:
                if tag == None:
                    yandere_api = choice(get(
                        "https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub").json())

                elif any(word in tag.lower() for word in illegal_tags):
                    blacklisted_tags = Embed(
                        description="This tag is currently blacklisted")
                    await interaction.response.send_message(embed=blacklisted_tags)
                
                elif tag=="02":
                    await interaction.response.send_message("Tag has been blacklisted due to it returning extreme content and guro")

                else:
                    yandere_api = choice(get(
                        "https://yande.re/post.json?limit=100&tags=rating:explicit-loli-shota-cub+" + tag).json())

                yandere = Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api["file_url"])
                yandere.set_footer(text="Fetched from Yande.re")
                await interaction.response.send_message(embed=yandere)
            except IndexError:
                notag = Embed(
                    description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Danbooru tag format or if the tag exists")
                await interaction.response.send_message(embed=notag)
        else:
            await interaction.response.send_message(embed=no_hentai)

    @jeanne_slash(description="Get a random hentai from Danbooru")
    async def danbooru(self, interaction: Interaction, tag=SlashOption(description="Put a tag but note that some are blacklisted", required=False)):
        if interaction.channel.is_nsfw():
            try:
                if tag == None:
                    danbooru_api = choice(get(
                        "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub").json())

                elif any(word in tag for word in illegal_tags):
                    blacklisted_tags = Embed(
                        description="This tag is currently blacklisted")
                    await interaction.response.send_message(embed=blacklisted_tags)
                else:
                    danbooru_api = choice(get(
                        "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub+" + tag).json())

                danbooru = Embed(color=0xFFC0CB)
                danbooru.set_image(url=danbooru_api["file_url"])
                danbooru.set_footer(text="Fetched from Danbooru")
                await interaction.response.send_message(embed=danbooru)
            except IndexError:
                notag = Embed(
                    description=f"{tag} doesn't exist. Please make sure the tag format is the same as the Danbooru tag format or if the tag exists")
                await interaction.response.send_message(embed=notag)
        else:
            await interaction.response.send_message(embed=no_hentai)

    


def setup(bot):
    bot.add_cog(slashnsfw(bot))
