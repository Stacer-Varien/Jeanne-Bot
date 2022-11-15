from discord import *
from discord.ext.commands import Cog, Bot
from db_functions import check_botbanned_user


class help_button(ui.View):
    def __init__(self):
        super().__init__()

        wiki_url = 'https://jeannebot.nicepage.io/Commands.html'
        haze_url = 'https://discord.gg/VVxGUmqQhF'
        tos_and_policy_url = 'https://jeannebot.nicepage.io/ToS-and-Privacy-Policy.html'

        self.add_item(ui.Button(style=ButtonStyle.link,
                      label="Jeanne Webiste", url=wiki_url))
        self.add_item(ui.Button(style=ButtonStyle.link,
                      label="Support Server", url=haze_url))
        self.add_item(ui.Button(style=ButtonStyle.link,
                      label="ToS and Privacy Policy", url=tos_and_policy_url))


class help(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @app_commands.command(description="Get help from the wiki or join the support server for further help")
    async def help(self, ctx: Interaction):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            view=help_button()
            help = Embed(
                description="Click on one of the buttons to open the documentation or get help on the support server")
            await ctx.response.send_message(embed=help, view=view)


async def setup(bot:Bot):
    await bot.add_cog(help(bot))
