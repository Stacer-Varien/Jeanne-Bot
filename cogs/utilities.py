from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from aiohttp import ClientSession
from nextcord.ext.commands import Cog
from config import WEATHER
from py_expression_eval import Parser

parser=Parser()

class slashutilities(Cog):
    def __init__(self, bot):
        self.bot = bot
               

    @jeanne_slash(description="Get weather information on a city")
    async def weather(self, ctx: Interaction, type=SlashOption(description="City or ZIP Code", choices=["city", "ZIP code"]), place=SlashOption(description="Which place are you looking for weather info", required=True), country_code=SlashOption(description="Required if you are using ZIP code", required=False)):
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
            if type=="city":
                urlil = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={WEATHER}&units=metric'
                async with ClientSession() as session:
                    async with session.get(urlil) as r:
                        if r.status == 200:
                            js = await r.json()
                            tempp = js['main']['temp']
                            desc = js['weather'][0]["description"]
                            count = js['sys']['country']
                            hum = js['main']['humidity']
                            pres = js['wind']['speed']
                            windir=js['wind']['deg']
                            embed = Embed(
                                title=f'⛅ Weather details of {place} ⛅', description=f':earth_africa: Country: {count}', colour=0x00FFFF)
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

            if type=="ZIP code":
                urlil = f'http://api.openweathermap.org/data/2.5/weather?zip={place},{country_code}&appid={WEATHER}&units=metric'
                async with ClientSession() as session:
                    async with session.get(urlil) as r:
                        if r.status == 200:
                            js = await r.json()
                            name=js['name']
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
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
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
