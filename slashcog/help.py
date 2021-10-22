import discord
from discord import Embed
from discord.ext import commands
from discord_slash.context import SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash import cog_ext
from discord_slash.model import ButtonStyle


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="See how you can use the bot's command")
    async def help(self, ctx: SlashContext):
        buttons1 = [
            create_button(
                style=ButtonStyle.blue,
                label="Fun",
                custom_id="Fun"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Info",
                custom_id="Info"
            ),
            create_button(
                style=ButtonStyle.green,
                label="Creater Only (OWNER ONLY)",
                custom_id="owner"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Misc",
                custom_id="misc"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Moderation",
                custom_id="mod"
            ),]
    
        buttons2=[    
            create_button(
                style=ButtonStyle.blue,
                label="Management",
                custom_id="manage"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Reactions",
                custom_id="reactions"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Images",
                custom_id="image"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Hentai (NSFW CHANNEL REQUIRED)",
                custom_id="nsfw"
            ),
        ]
        
        action_row = create_actionrow(*buttons1)
        action_row2 = create_actionrow(*buttons2)

        await ctx.send("Click on one of the buttons to get help on a command module\nYou will see the full commands and use of them", components=[action_row])
        await ctx.send("_ _", components=[action_row2])

def setup(bot):
    bot.add_cog(help(bot))
