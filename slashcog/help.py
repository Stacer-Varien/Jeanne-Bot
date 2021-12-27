from discord import Embed
from discord.ext.commands import Cog
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.cog_ext import cog_slash as jeanne_slash
from discord_slash.model import ButtonStyle


class help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="See how you can use the bot's command")
    async def help(self, ctx):
        buttons = [
            create_button(
                style=ButtonStyle.URL,
                label="Jeanne Wiki",
                url="https://github.com/ZaneRE544/Jeanne-Bot/wiki/JeanneBot-Wiki#welcome-to-the-jeanne-bot-wiki"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="Support Server",
                url="https://discord.gg/VVxGUmqQhF"
            ),
        ]

        action_row = create_actionrow(*buttons)

        help = Embed(
            description="Click on one of the buttons to open the documentation or get help on the support server")

        await ctx.send(embed=help, components=[action_row])

def setup(bot):
    bot.add_cog(help(bot))
