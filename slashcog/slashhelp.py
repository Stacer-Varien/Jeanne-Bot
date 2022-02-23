from sqlite3 import connect
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View


db = connect("database.db")

class help_button(View):
    def __init__(self):
        super().__init__()

        wiki_url='https://github.com/ZaneRE544/Jeanne-Bot/wiki/JeanneBot-Wiki#welcome-to-the-jeanne-bot-wiki'
        haze_url='https://discord.gg/VVxGUmqQhF'
        
        self.add_item(Button(style=ButtonStyle.url, label="Jeanne Wiki", url=wiki_url))
        self.add_item(Button(style=ButtonStyle.url, label="Support Server", url=haze_url))


class slashhelp(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get help from the wiki or join the support server for further help")
    async def help(self, interaction : Interaction):
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]
            reason=botbanned_data[1]

            botbanned_user=await self.bot.fetch_user(botbanned)
            if interaction.user.id==botbanned_user.id:
                await interaction.response.send_message(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            help=Embed(description="Click on one of the buttons to open the documentation or get help on the support server")
            await interaction.response.send_message(embed=help, view=help_button())

def setup(bot):
    bot.add_cog(slashhelp(bot))
