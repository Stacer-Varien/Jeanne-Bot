import discord
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Invite me to your server or join my creator's servers")
    async def invite(self, ctx:SlashContext):
        buttons = [
            create_button(
                style=ButtonStyle.URL,
                label="Bot Invite",
                url="https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="Top.gg",
                url="https://top.gg/bot/831993597166747679"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="DiscordBots",
                url="https://discord.bots.gg/bots/831993597166747679"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="HAZE Server",
                url="https://discord.gg/VVxGUmqQhF"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="Jeanne Support Server",
                url="https://discord.gg/Xn3EvGcMrF"
            ),]

        action_row=create_actionrow(*buttons)

        embed = Embed(
            title="Invite me!",
            description="Click on one of these buttons to invite me to you server or join my creator's servers",
            color=0x00bfff)

        await ctx.send(embed=embed, components=[action_row])

    @cog_ext.cog_slash(description="Type a message and I will say it but it will be in plain text")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx:SlashContext, text):
        await ctx.send(text)

    @cog_ext.cog_slash(description="Type a message and I will say it but it will be in embed")
    @commands.has_permissions(administrator=True)
    async def sayembed(self, ctx:SlashContext, text):
        say = discord.Embed(description=f"{text}", color=0xADD8E6)
        await ctx.send(embed=say)


def setup(bot):
    bot.add_cog(misc(bot))
