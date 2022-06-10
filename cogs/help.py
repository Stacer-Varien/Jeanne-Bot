from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View
from config import db


class help_button(View):
    def __init__(self):
        super().__init__()

        wiki_url = 'https://github.com/ZaneRE544/Jeanne-Bot/wiki/JeanneBot-Wiki#welcome-to-the-jeanne-bot-wiki'
        haze_url = 'https://discord.gg/VVxGUmqQhF'

        self.add_item(Button(style=ButtonStyle.url,
                      label="Jeanne Wiki", url=wiki_url))
        self.add_item(Button(style=ButtonStyle.url,
                      label="Support Server", url=haze_url))


class slashhelp(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get help from the wiki or join the support server for further help")
    async def help(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            help = Embed(
                description="Click on one of the buttons to open the documentation or get help on the support server")
            await interaction.followup.send(embed=help, view=help_button())


def setup(bot):
    bot.add_cog(slashhelp(bot))
