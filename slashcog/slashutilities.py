from nextcord import Embed, Interaction, slash_command as jeanne_slash
from aiohttp import ClientSession
from nextcord.ext.commands import Cog
from config import WEATHER

class slashutilities(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get weather information on a city")
    async def weather(self, interaction : Interaction, city):
        city = city
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
                    await interaction.response.send_message.send(embed=embed)


def setup(bot):
    bot.add_cog(slashutilities(bot))
