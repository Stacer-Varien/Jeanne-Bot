from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from aiohttp import ClientSession
from nextcord.ext.commands import Cog
from config import WEATHER
from py_expression_eval import Parser

parser = Parser()


class slashutilities(Cog):
    def __init__(self, bot):
        self.bot = bot

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
                answer = parser.parse(calculate).evaluate({})
                calculation = Embed(title="Result", color=0x00FFFF)
                calculation.add_field(name=calculate, value=answer)
                await ctx.followup.send(embed=calculation)
            except Exception as e:
                failed = Embed(
                    description=f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command")
                await ctx.followup.send(embed=failed)


def setup(bot):
    bot.add_cog(slashutilities(bot))
