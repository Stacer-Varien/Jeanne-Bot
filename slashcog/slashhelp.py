from nextcord import Embed, ButtonStyle, slash_command as jeanne_slash, Interaction
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View


class slashhelp(Cog):
    def __init__(self, bot):
        self.bot = bot

class help_button(View):
    def __init__(self):
        super().__init__()

        wiki_url='https://github.com/ZaneRE544/Jeanne-Bot/wiki/JeanneBot-Wiki#welcome-to-the-jeanne-bot-wiki'
        haze_url='https://discord.gg/VVxGUmqQhF'
        
        self.add_item(Button(style=ButtonStyle.url, label="Jeanne Wiki", url=wiki_url))
        self.add_item(Button(style=ButtonStyle.url, label="Support Server", url=haze_url))


class help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash()
    async def help(self, interaction : Interaction):
        help=Embed(description="Click on one of the buttons to open the documentation or get help on the support server")

        await interaction.response.send_message(embed=help, view=help_button())

def setup(bot):
    bot.add_cog(slashhelp(bot))
