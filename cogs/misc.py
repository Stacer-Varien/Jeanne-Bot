from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.abc import GuildChannel
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View
from assets.errormsgs import admin_perm
from asyncio import TimeoutError
from nextcord.ext.application_checks import *

bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

haze_url = "https://discord.gg/VVxGUmqQhF"


class invite_button(View):
    def __init__(self):
        super().__init__()

        self.add_item(Button(style=ButtonStyle.url, label="Bot Invite", url=bot_invite_url))
        self.add_item(Button(style=ButtonStyle.url, label="Top.gg", url=topgg_invite))
        self.add_item(Button(style=ButtonStyle.url, label="DiscordBots", url=discordbots_url))
        self.add_item(Button(style=ButtonStyle.url, label="HAZE", url=haze_url))

class slashmisc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Invite me to your server or join the support server")
    async def invite(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            invite = Embed(
                title="Invite me!",
                description="Click on one of these buttons to invite me to you server or join my creator's server",
                color=0x00bfff)

            await ctx.followup.send(embed=invite, view=invite_button())

    @jeanne_slash(description="Main say command")
    async def say(self, ctx: Interaction):
        pass


    @say.subcommand(description="Type something and I will say it in plain text")
    @has_permissions(administrator=True)
    async def plain(self, ctx: Interaction, channel: GuildChannel = SlashOption(description="Which channel should I send the message?", channel_types=[ChannelType.text, ChannelType.news])):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            await ctx.followup.send("Type something!", ephemeral=True)

            def check(m):
                return m.author == ctx.user and m.content

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=10)

                await ctx.followup.send("Sent", ephemeral=True)
                await msg.delete()
                await channel.send(msg.content)
            except TimeoutError:
                timeout = Embed(
                    description=f"Guess you have nothing to say", color=0xFF0000)
                await ctx.followup.send(embed=timeout, ephemeral=True)

    @say.subcommand(description="Type something and I will say it in embed")
    @has_permissions(administrator=True)
    async def embed(self, ctx: Interaction, channel: GuildChannel = SlashOption(description="Which channel should I send the message?", channel_types=[ChannelType.text, ChannelType.news])):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            ask = Embed(description="Type something\nMaxinum characters allowed is 4096")
            await ctx.followup.send(embed=ask)

            def check(m):
                return m.author == ctx.user and m.content

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=180)

                await ctx.followup.send("Sent", ephemeral=True)

                embed_text = Embed(description=msg.content, color=0x4169E1)
                await msg.delete()
                await channel.send(embed=embed_text)
            except TimeoutError:
                timeout = Embed(
                    description=f"Guess you have nothing to say", color=0xFF0000)
                await ctx.followup.send(embed=timeout, ephemeral=True)


    @plain.error
    async def say_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=admin_perm)

    @embed.error
    async def say_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=admin_perm)


    @jeanne_slash()
    async def report(self, ctx : Interaction):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:        
            await ctx.followup.send("Please [click here](https://forms.gle/DvGiJWXjbZWK3iy88) to submit your report.\nPlease note that I will not be collecting any of your personal information.", ephemeral=True)

def setup(bot):
    bot.add_cog(slashmisc(bot))
