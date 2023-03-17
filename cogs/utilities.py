from discord import Attachment, ButtonStyle, Color, Embed, Interaction, Message, TextChannel, app_commands as Jeanne, ui
from aiohttp import ClientSession
from discord.ext.commands import Cog, Bot, GroupCog
from assets.modals import ReportModal
from db_functions import Botban
from config import WEATHER

from discord.ui import View
from py_expression_eval import Parser
from typing import Optional
from json import loads
from requests import get

bot_invite_url = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1428479601718&scope=bot%20applications.commands"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

haze_url = "https://discord.gg/jh7jkuk2pp"





class invite_button(View):

    def __init__(self):
        super().__init__()

        self.add_item(
            ui.Button(style=ButtonStyle.url,
                      label="Bot Invite",
                      url=bot_invite_url))
        self.add_item(
            ui.Button(style=ButtonStyle.url, label="Top.gg", url=topgg_invite))
        self.add_item(
            ui.Button(style=ButtonStyle.url,
                      label="DiscordBots",
                      url=discordbots_url))
        self.add_item(
            ui.Button(style=ButtonStyle.url, label="Orleans", url=haze_url))


class Weather_Group(GroupCog, name="weather"):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Get weather information on a city")
    @Jeanne.describe(city="Add a city")
    async def city(self, ctx: Interaction, city: str):
            if Botban(ctx.user).check_botbanned_user() == True:
                return
        
            await ctx.response.defer()
            min_tempe = self.bot.get_emoji(1009760796017963119)
            max_tempe = self.bot.get_emoji(1009761541169618964)
            guste = self.bot.get_emoji(1009766251431743569)
            globe = self.bot.get_emoji(1009723165305491498)

            urlil = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        feels_like = js['main']['feels_like']
                        min_temp = js['main']['temp_min']
                        max_temp = js['main']['temp_max']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        visibility = js['visibility']
                        clouds = js['clouds']['all']
                        windir = js['wind']['deg']
                        wind_gust = js['wind']['speed']

                        embed = Embed(title=f'⛅ Weather details of {city} ⛅',
                                      description=f'{globe} Country: {count}',
                                      colour=Color.random())
                        embed.add_field(name=":newspaper: Description",
                                        value=desc,
                                        inline=True)
                        embed.add_field(
                            name=f"{min_tempe} Minimum Temperature",
                            value=f"{min_temp}°C",
                            inline=True)
                        embed.add_field(
                            name=f"{max_tempe} Maximum Temperature",
                            value=f"{max_temp}°C",
                            inline=True)
                        embed.add_field(
                            name=":raised_back_of_hand: Feels Like",
                            value=f"{feels_like}°C",
                            inline=True)
                        embed.add_field(name=":droplet: Humidity",
                                        value=hum,
                                        inline=True)
                        embed.add_field(name=":eye: Visibility",
                                        value=f"{visibility}m",
                                        inline=True)
                        embed.add_field(name=":cloud: Clouds",
                                        value=f"{clouds}%",
                                        inline=True)
                        embed.add_field(name=":arrow_right: Wind Direction",
                                        value=f"{windir}°",
                                        inline=True)
                        embed.add_field(name=f"{guste} Wind Gust",
                                        value=f"{wind_gust}m/s",
                                        inline=True)
                        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description=
        "Get weather information on a city but with a ZIP code and Country code"
    )
    @Jeanne.describe(zip_code="Add a ZIP code",
                     country_code="Add a country code")
    async def zipcode(self, ctx: Interaction, zip_code: str,
                      country_code: str):
            await ctx.response.defer()
            if Botban(ctx.user).check_botbanned_user() == True:
                return
            
            min_tempe = self.bot.get_emoji(1009760796017963119)
            max_tempe = self.bot.get_emoji(1009761541169618964)
            guste = self.bot.get_emoji(1009766251431743569)
            urlil = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={WEATHER}&units=metric'
            async with ClientSession() as session:
                async with session.get(urlil) as r:
                    if r.status == 200:
                        js = await r.json()
                        feels_like = js['main']['feels_like']
                        min_temp = js['main']['temp_min']
                        max_temp = js['main']['temp_max']
                        desc = js['weather'][0]["description"]
                        count = js['sys']['country']
                        hum = js['main']['humidity']
                        visibility = js['visibility']
                        clouds = js['clouds']['all']
                        windir = js['wind']['deg']
                        wind_gust = js['wind']['speed']
                        embed = Embed(
                            title=f'⛅ Weather details of {zip_code} ⛅',
                            description=f':earth_africa: Country: {count}',
                            colour=Color.random())
                        embed.add_field(name=":newspaper: Description",
                                        value=desc,
                                        inline=True)
                        embed.add_field(
                            name=f"{min_tempe} Minimum Temperature",
                            value=f"{min_temp}°C",
                            inline=True)
                        embed.add_field(
                            name=f"{max_tempe} Maximum Temperature",
                            value=f"{max_temp}°C",
                            inline=True)
                        embed.add_field(
                            name=":raised_back_of_hand: Feels Like",
                            value=f"{feels_like}°C",
                            inline=True)
                        embed.add_field(name=":droplet: Humidity",
                                        value=hum,
                                        inline=True)
                        embed.add_field(name=":eye: Visibility",
                                        value=f"{visibility}m",
                                        inline=True)
                        embed.add_field(name=":cloud: Clouds",
                                        value=f"{clouds}%",
                                        inline=True)
                        embed.add_field(name=":arrow_right: Wind Direction",
                                        value=f"{windir}°",
                                        inline=True)
                        embed.add_field(name=f"{guste} Wind Gust",
                                        value=f"{wind_gust}m/s",
                                        inline=True)
                        await ctx.followup.send(embed=embed)


class Embed_Group(GroupCog, name="embed"):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description=
        "Generates an embed message. This needs the Discohooks.org embed generator"
    )
    @Jeanne.describe(channel="Send to which channel?",
                     jsonscript="Add a JSON script",
                     jsonfile="Add a JSON file")
    @Jeanne.checks.has_permissions(administrator=True)
    async def generate(self,
                       ctx: Interaction,
                       channel: TextChannel,
                       jsonscript: Optional[str] = None,
                       jsonfile: Optional[Attachment] = None):
            if Botban(ctx.user).check_botbanned_user() == True:
                return
            
            await ctx.response.defer(ephemeral=True)

            if not jsonscript and not jsonfile:
                embed = Embed(
                    description=
                    "You are missing the JSON script or JSON file\nPlease use [Discohook](https://discohook.org/)"
                )
                await ctx.followup.send(embed=embed)
            elif jsonscript and jsonfile:
                embed = Embed(
                    description=
                    "You are using both the JSON script and JSON file\nPlease use one"
                )
                await ctx.followup.send(embed=embed)
            else:
                if jsonscript and not jsonfile:
                    json = loads(jsonscript)

                elif jsonfile and not jsonscript:
                    json_file = jsonfile.url
                    json_request = get(json_file)
                    json_content = json_request.content
                    json = loads(json_content)

                try:
                    content = json["content"]
                except:
                    pass

                try:
                    embed = Embed.from_dict(json['embeds'][0])
                    await channel.send(content=content, embed=embed)
                except:
                    await channel.send(content=content)
                await ctx.followup.send(content="Sent", ephemeral=True)

    @Jeanne.command(
        description=
        "Edits an embed message. This needs the Discohook.org embed generator")
    @Jeanne.describe(channel="Which channel is the embed message in?",
                     messageid="What is the message ID?",
                     jsonscript="Add a JSON script",
                     jsonfile="Add a JSON file")
    @Jeanne.checks.has_permissions(administrator=True)
    async def edit(self,
                   ctx: Interaction,
                   channel: TextChannel,
                   messageid: str,
                   jsonscript: Optional[str] = None,
                   jsonfile: Optional[Attachment] = None):
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        else:
            await ctx.response.defer(ephemeral=True)

            try:
                message: Message = await channel.fetch_message(int(messageid))
            except Exception as e:
                embed = Embed(description=e)
                await ctx.followup.send(embed=embed)
            else:
                if not jsonscript and not jsonfile:
                    embed = Embed(
                        description=
                        "You are missing the JSON script or JSON file\nPlease use [Discohooks](https://discohook.org/)"
                    )
                    await ctx.followup.send(embed=embed)
                elif jsonscript and jsonfile:
                    embed = Embed(
                        description=
                        "You are using both the JSON script and JSON file\nPlease use one"
                    )
                    await ctx.followup.send(embed=embed)
                else:
                    if jsonscript and not jsonfile:
                        json = loads(jsonscript)

                    elif jsonfile and not jsonscript:
                        json_file = jsonfile.url
                        json_request = get(json_file)
                        json_content = json_request.content
                        json = loads(json_content)

                    try:
                        content = json["content"]

                        if content == '':
                            content = None
                    except:
                        pass

                    try:
                        embed = Embed.from_dict(json['embeds'][0])
                        await message.edit(content=content, embed=embed)
                    except:
                        await message.edit(content=content)
                    await ctx.followup.send(content="Message edited",
                                            ephemeral=True)


class slashutilities(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.parser = Parser()

    @Jeanne.command(description="Type something and I will say it")
    @Jeanne.describe(channel="Send to which channel?",
                     message="What should I say?")
    @Jeanne.checks.has_permissions(administrator=True)
    async def say(self, ctx: Interaction, channel: TextChannel, message: str):
            if Botban(ctx.user).check_botbanned_user() == True:
                return
        
            await ctx.response.defer(ephemeral=True)
            await ctx.followup.send(content="Sent")
            await channel.send(message)

    @Jeanne.command(description="Do a calculation")
    @Jeanne.describe(calculate="Add a calculation")
    async def calculator(self, ctx: Interaction, calculate: str):
            await ctx.response.defer()
            if Botban(ctx.user).check_botbanned_user() == True:
                return
        
            try:
                answer = self.parser.parse(calculate).evaluate({})
                calculation = Embed(title="Result", color=Color.random())
                calculation.add_field(name=f"`{calculate}`", value=answer)
                await ctx.followup.send(embed=calculation)
            except Exception as e:
                failed = Embed(
                    description=
                    f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command"
                )
                await ctx.followup.send(embed=failed)

    @Jeanne.command(
        description="Invite me to your server or join the support server")
    async def invite(self, ctx: Interaction):
            await ctx.response.defer()
            if Botban(ctx.user).check_botbanned_user() == True:
                return
        
            invite = Embed(
                title="Invite me!",
                description=
                "Click on one of these buttons to invite me to you server or join my creator's server",
                color=Color.random())

            await ctx.followup.send(embed=invite, view=invite_button())

    @Jeanne.command(
        description="Submit a bot report if you found something wrong")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def botreport(self, ctx: Interaction):
            if Botban(ctx.user).check_botbanned_user() == True:
                return
        
            await ctx.response.send_modal(ReportModal())


async def setup(bot: Bot):
    await bot.add_cog(Weather_Group(bot))
    await bot.add_cog(Embed_Group(bot))
    await bot.add_cog(slashutilities(bot))
