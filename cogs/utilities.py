<<<<<<< Updated upstream
from config import db
=======
>>>>>>> Stashed changes
from nextcord import *
from nextcord import slash_command as jeanne_slash
from aiohttp import ClientSession
from nextcord.ext.commands import Cog
<<<<<<< Updated upstream
from config import WEATHER
from py_expression_eval import Parser

parser = Parser()

=======
from config import db, WEBHOOK, WEATHER
from nextcord.abc import GuildChannel
from nextcord.ui import Button, View
from assets.errormsgs import admin_perm
from asyncio import TimeoutError
from nextcord.ext.application_checks import *
from py_expression_eval import Parser

bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

haze_url = "https://discord.gg/VVxGUmqQhF"

class invite_button(View):
    def __init__(self):
        super().__init__()

        self.add_item(Button(style=ButtonStyle.url,
                      label="Bot Invite", url=bot_invite_url))
        self.add_item(Button(style=ButtonStyle.url,
                      label="Top.gg", url=topgg_invite))
        self.add_item(Button(style=ButtonStyle.url,
                      label="DiscordBots", url=discordbots_url))
        self.add_item(Button(style=ButtonStyle.url,
                      label="HAZE", url=haze_url))
>>>>>>> Stashed changes

class slashutilities(Cog):
    def __init__(self, bot):
        self.bot = bot
<<<<<<< Updated upstream
=======
        self.parser = Parser()
>>>>>>> Stashed changes

    @jeanne_slash(description="Main weather command")
    async def weather(self, ctx: Interaction):
        pass

    @weather.subcommand(description="Get weather information on a city")
    async def city(self, ctx: Interaction, city=SlashOption(description="Which city are you looking for weather info", required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            urlil = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        tempp = js['main']['temp']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        pres = js['wind']['speed']
                        windir = js['wind']['deg']
                        embed = Embed(
                            title=f'⛅ Weather details of {city} ⛅', description=f':earth_africa: Country: {count}', colour=0x00FFFF)
                        embed.add_field(name=':thermometer: Temperature:',
                                        value=f'{tempp}° Celsius', inline=True)
                        embed.add_field(name=':newspaper: Description:',
                                        value=f'{desc}', inline=True)
                        embed.add_field(name=":droplet: Humidity:",
                                        value=f'{hum}', inline=True)
                        embed.add_field(name=":cloud: Pressure:",
                                        value=f'{pres} Pa', inline=True)
                        embed.add_field(name=":arrow_right: Wind Direction:",
                                        value=f'{windir}° degrees', inline=True)
                        await ctx.followup.send(embed=embed)

    @weather.subcommand(description="Get weather information on a city but with a ZIP code and Country code")
    async def zip_code(self, ctx: Interaction, zip_code=SlashOption(description="Enter the ZIP Code for weather info", required=True), country_code=SlashOption(required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            urlil = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        name = js['name']
                        tempp = js['main']['temp']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        pres = js['wind']['speed']
                        windir = js['wind']['deg']
                        embed = Embed(
                            title=f'⛅ Weather details of {name} ⛅', description=f':earth_africa: Country: {count}', colour=0x00FFFF)
                        embed.add_field(name=':thermometer: Temperature:',
                                        value=f'{tempp}° Celsius', inline=True)
                        embed.add_field(name=':newspaper: Description:',
                                        value=f'{desc}', inline=True)
                        embed.add_field(name=":droplet: Humidity:",
                                        value=f'{hum}', inline=True)
                        embed.add_field(name=":cloud: Pressure:",
                                        value=f'{pres} Pa', inline=True)
                        embed.add_field(name=":arrow_right: Wind Direction:",
                                        value=f'{windir}° degrees', inline=True)
                        await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Do a calculation")
    async def calculator(self, ctx: Interaction, calculate=SlashOption(description="What do you want to calculate?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            try:
<<<<<<< Updated upstream
                answer = parser.parse(calculate).evaluate({})
=======
                answer = self.parser.parse(calculate).evaluate({})
>>>>>>> Stashed changes
                calculation = Embed(title="Result", color=0x00FFFF)
                calculation.add_field(name=calculate, value=answer)
                await ctx.followup.send(embed=calculation)
            except Exception as e:
                failed = Embed(
                    description=f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command")
                await ctx.followup.send(embed=failed)

<<<<<<< Updated upstream
=======
    @jeanne_slash(description="Invite me to your server or join the support server")
    async def invite(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
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

            if ctx.user.id == botbanned:
                pass
        except:
            await ctx.followup.send("Type something!", ephemeral=True)

            def check(m):
                return m.author == ctx.user and m.content

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=300)

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

            if ctx.user.id == botbanned:
                pass
        except:
            ask = Embed(
                description="Type something\nMaxinum characters allowed is 4096")
            await ctx.followup.send(embed=ask)

            def check(m):
                return m.author == ctx.user and m.content

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=300)

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
    async def report(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            await ctx.followup.send("This command has been disabled due to troll reports of users requesting illicit material. Will be up and running after the v3.0 update")

    @jeanne_slash(force_global=False)
    @is_owner()
    async def report_test(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            await ctx.followup.send("Please go to your DMs to report", ephemeral=True)
            asktype = Embed(title="Hi, what are you reporting?")
            await ctx.user.send("What do you want to report?")

            def check(m):
                return m.author == ctx.user and m.content

            msg = await self.bot.wait_for('message', check=check, timeout=300)

            await ctx.user.send("Thank you")

            report = Embed(title="Report", description=msg.content)
            report.set_footer(text=f"Reporter: {ctx.user}\t{ctx.user.id}")
            webhook = SyncWebhook.from_url(WEBHOOK)
            webhook.send(embed=report)

>>>>>>> Stashed changes

def setup(bot):
    bot.add_cog(slashutilities(bot))
