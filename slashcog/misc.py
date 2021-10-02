import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Invite me to your server or join my creator's servers")
    async def invite(self, ctx:SlashContext):
        embed = discord.Embed(
            title="Invite me!",
            description="Click on one of these URLs to invite me to you server or join my creator's servers",
            color=0x00bfff)
        embed.add_field(name="Bot Invite",
                        value="[Click here](https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands)",
                        inline=True)
        embed.add_field(name="Top.gg",
                        value="[Click here](https://top.gg/bot/831993597166747679)",
                        inline=True)
        embed.add_field(name="DiscordBots",
                    value="[Click here](https://discord.bots.gg/bots/831993597166747679)", inline=True)
        embed.add_field(name="DiscordBotList",
                        value="[Click here](https://discordbotlist.com/bots/Jeanne-3694)", inline=True)
        embed.add_field(name="HAZE server",
                        value="[Click here](https://discord.gg/VVxGUmqQhF)", inline=True)
        embed.add_field(name="Jeanne Support Server",
                        value="[Click here](https://discord.gg/Xn3EvGcMrF)", inline=True)
        await ctx.send(embed=embed)

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
