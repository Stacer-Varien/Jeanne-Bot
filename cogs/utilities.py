from json import load
from secrets import choice
from nextcord import *
from nextcord import slash_command as jeanne_slash
from aiohttp import ClientSession
from nextcord.ext.commands import Cog
from pkg_resources import require
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


class Cancel(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = False
        self.stop()

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

class slashutilities(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parser = Parser()

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
                answer = self.parser.parse(calculate).evaluate({})
                calculation = Embed(title="Result", color=0x00FFFF)
                calculation.add_field(name=calculate, value=answer)
                await ctx.followup.send(embed=calculation)
            except Exception as e:
                failed = Embed(
                    description=f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command")
                await ctx.followup.send(embed=failed)

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
                await msg.delete()
                embed_text=Embed(description=msg.content, color=Color.blue())
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
    async def bot_report(self, ctx: Interaction, type=SlashOption(choices=['bug', 'fault', 'exploit', 'violator'])):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            if type=='bug':
                report_type="Bug"
            elif type == 'fault':
                report_type = "Fault"
            elif type == 'exploit':
                report_type = "Exploit"
            elif type == 'violator':
                report_type = "Violator"

            await ctx.user.send("What do you want to report?")

            await ctx.followup.send("Please go to your DMs to report", ephemeral=True)


            def check(m):
                return m.author == ctx.user and m.content
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=300)

                report = Embed(title=f"{report_type} Report",
                           description=msg.content, color=Color.blurple())
                report.set_footer(text=f"Reporter: {ctx.user}\t{ctx.user.id}")

                webhook = SyncWebhook.from_url(WEBHOOK)
                webhook.send(embed=report)

                await ctx.user.send("Thank you for your report. I will look into it. Unfortunately, you have to wait for the outcome if it was successful or not.")
                
            except Exception as e:
                print(e)

    @jeanne_slash(description="Report a member in your server")
    async def report(self, ctx:Interaction, member:Member=SlashOption(description="Who are you reporting?", required=True), anonymous=SlashOption(description=("What to have your name hidden while reporting?"), choices=['True', 'False'], required=False)):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            report_channel = db.execute(
                "SELECT channel_id FROM reportData WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
            if report_channel == None:
                await ctx.followup.send("The server doesn't have a report channel set")
            else:
                try:
                    await ctx.user.send("Why are you reporting this member?\nYou have 5 minutes to type it out and please use media links instead of actual files", view=Cancel())

                    if Cancel().value is False:
                        await ctx.user.send("Report cancelled")
                
                    else:
                        await ctx.followup.send("Please go to your DMs to report. Please remember that it is private and only authorised personal can view your report", ephemeral=True)

                        def check(m):
                            return m.author == ctx.user and m.content
                        try:
                            msg = await self.bot.wait_for('message', check=check, timeout=300)

                            report_channel_id = report_channel[0]
                            channel = self.bot.get_channel(report_channel_id) 

                            await ctx.user.send("Thank you for reporting the member.\nFor security purposes, your report was logged to the bot developer's PC.")

                            db.execute("INSERT OR IGNORE INTO report_data (user_id, message)", (ctx.user.id, msg.content))
                            db.commit()
                            report=Embed(title='Member reported', color=Color.brand_red())
                            report.add_field(name="Reported Member", value=(member + '\n' + member.id), inline=False)
                            report.add_field(name='Reason', value=msg.content, inline=False)

                            if anonymous == 'True':
                                report.set_footer(text="Made by an anonymous member of {}".format(ctx.guild.name))

                            if anonymous == 'False':
                                report.set_footer(text="Made by {} of {}".format((ctx.user + '\n' + ctx.user.id), ctx.guild.name))

                            await channel.send(embed=report)         
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)

   # @jeanne_slash(description="Creates an invite")
   # @has_permissions(create_instant_invite=True)
   # async def create_invite(self, ctx:Interaction, reason = SlashOption(description="What is the reason for the invite?", required=True), )

def setup(bot):
    bot.add_cog(slashutilities(bot))
