from datetime import timedelta, datetime
from discord import (
    Attachment,
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    Message,
    TextChannel,
    app_commands as Jeanne,
    ui,
)
from aiohttp import ClientSession
from discord.ext.commands import Cog, Bot, GroupCog
from assets.components import ReportModal
from assets.dictionary import dictionary
from functions import Botban, Reminder
from config import WEATHER
from discord.ui import View
from py_expression_eval import Parser
from typing import Optional
from json import loads
from requests import get
from enum import Enum
from humanfriendly import parse_timespan, InvalidTimespan

bot_invite_url = "https://discord.com/oauth2/authorize?client_id=831993597166747679&scope=bot%20applications.commands&permissions=467480734774"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

orleans = "https://discord.gg/jh7jkuk2pp"


class Languages(Enum):
    English = "en"
    Spanish = "es"
    French = "fr"
    Japanese = "jp"


class invite_button(View):
    def __init__(self):
        super().__init__()

        self.add_item(
            ui.Button(style=ButtonStyle.url, label="Bot Invite", url=bot_invite_url)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.url, label="Top.gg", url=topgg_invite)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.url, label="DiscordBots", url=discordbots_url)
        )
        self.add_item(ui.Button(style=ButtonStyle.url, label="Orleans", url=orleans))


class Weather_Group(GroupCog, name="weather"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Get weather information on a city")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.describe(city="Add a city")
    async def city(self, ctx: Interaction, city: str):
        if Botban(ctx.user).check_botbanned_user():
            return

        await ctx.response.defer()

        emoji_map = {
            "globe": "🌍",
            "newspaper": "📰",
            "min_tempe": "🌡️",
            "max_tempe": "🔥",
            "feels_like": "🤚",
            "humidity": "💧",
            "visibility": "👁️",
            "clouds": "☁️",
            "wind_dir": "➡️",
            "guste": "💨",
        }

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER}&units=metric"
        async with ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    weather_data = await r.json()

                    main_data = weather_data["main"]
                    weather = weather_data["weather"][0]
                    sys_data = weather_data["sys"]
                    wind = weather_data["wind"]

                    embed = Embed(
                        title=f"{emoji_map['globe']} Weather details of {city} {emoji_map['globe']}",
                        description=f"{emoji_map['globe']} Country: {sys_data['country']}",
                        color=Color.random(),
                    )
                    embed.add_field(
                        name=f"{emoji_map['newspaper']} Description",
                        value=weather["description"],
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['min_tempe']} Minimum Temperature",
                        value=f"{main_data['temp_min']}°C",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['max_tempe']} Maximum Temperature",
                        value=f"{main_data['temp_max']}°C",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['feels_like']} Feels Like",
                        value=f"{main_data['feels_like']}°C",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['humidity']} Humidity",
                        value=f"{main_data['humidity']}",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['visibility']} Visibility",
                        value=f"{weather_data['visibility']}m",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['clouds']} Clouds",
                        value=f"{weather_data['clouds']['all']}%",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['wind_dir']} Wind Direction",
                        value=f"{wind['deg']}°",
                        inline=True,
                    )
                    embed.add_field(
                        name=f"{emoji_map['guste']} Wind Gust",
                        value=f"{wind['speed']}m/s",
                        inline=True,
                    )

                    await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Get weather information on a city but with a ZIP code and Country code"
    )
    @Jeanne.describe(zip_code="Add a ZIP code", country_code="Add a country code")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def zipcode(self, ctx: Interaction, zip_code: str, country_code: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        emoji_map = {
            "newspaper": "📰",
            "min_tempe": "🌡️",
            "max_tempe": "🔥",
            "feels_like": "🤚",
            "humidity": "💧",
            "visibility": "👁️",
            "clouds": "☁️",
            "wind_dir": "➡️",
            "guste": "💨"
        }

        url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={WEATHER}&units=metric"
        async with ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    weather_data = await r.json()

                    main_data = weather_data["main"]
                    weather = weather_data["weather"][0]
                    sys_data = weather_data["sys"]
                    wind = weather_data["wind"]

                    embed = Embed(
                        title=f"⛅ Weather details of {zip_code} ⛅",
                        description=f":earth_africa: Country: {sys_data['country']}",
                        color=Color.random()
                    )
                    embed.add_field(
                        name=f"{emoji_map['newspaper']} Description",
                        value=weather["description"],
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['min_tempe']} Minimum Temperature",
                        value=f"{main_data['temp_min']}°C",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['max_tempe']} Maximum Temperature",
                        value=f"{main_data['temp_max']}°C",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['feels_like']} Feels Like",
                        value=f"{main_data['feels_like']}°C",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['humidity']} Humidity",
                        value=f"{main_data['humidity']}",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['visibility']} Visibility",
                        value=f"{weather_data['visibility']}m",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['clouds']} Clouds",
                        value=f"{weather_data['clouds']['all']}%",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['wind_dir']} Wind Direction",
                        value=f"{wind['deg']}°",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{emoji_map['guste']} Wind Gust",
                        value=f"{wind['speed']}m/s",
                        inline=True
                    )

                    await ctx.followup.send(embed=embed)

    @city.error
    async def city_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            embed = Embed(color=Color.red())
            embed.description = "Woah, slow down! Give the command a rest.\n\nYou can try again after `{} seconds`".format(
                round(error.retry_after)
            )
            await ctx.followup.send(embed=embed)

    @zipcode.error
    async def city_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            embed = Embed(color=Color.red())
            embed.description = "Woah, slow down! Give the command a rest.\n\nYou can try again after `{} seconds`".format(
                round(error.retry_after)
            )
            await ctx.followup.send(embed=embed)


class Embed_Group(GroupCog, name="embed"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description="Generates an embed message. This needs the Discohook.org embed generator"
    )
    @Jeanne.describe(
        channel="Send to which channel?",
        jsonscript="Add a JSON script",
        jsonfile="Add a JSON file",
    )
    @Jeanne.checks.has_permissions(administrator=True)
    async def generate(
        self,
        ctx: Interaction,
        channel: TextChannel,
        jsonscript: Optional[str] = None,
        jsonfile: Optional[Attachment] = None,
    ):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer(ephemeral=True)

        if not jsonscript and not jsonfile:
            embed = Embed(
                description="You are missing the JSON script or JSON file\nPlease use [Discohook](https://discohook.org/)"
            )
            await ctx.followup.send(embed=embed)
        elif jsonscript and jsonfile:
            embed = Embed(
                description="You are using both the JSON script and JSON file\nPlease use one"
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
                embed = Embed.from_dict(json["embeds"][0])
                await channel.send(content=content, embed=embed)
            except:
                await channel.send(content=content)
            await ctx.followup.send(
                content="Embed sent in {}".format(channel.mention), ephemeral=True
            )

    @Jeanne.command(
        description="Edits an embed message. This needs the Discohook.org embed generator"
    )
    @Jeanne.describe(
        channel="Which channel is the embed message in?",
        messageid="What is the message ID?",
        jsonscript="Add a JSON script",
        jsonfile="Add a JSON file",
    )
    @Jeanne.checks.has_permissions(administrator=True)
    async def edit(
        self,
        ctx: Interaction,
        channel: TextChannel,
        messageid: str,
        jsonscript: Optional[str] = None,
        jsonfile: Optional[Attachment] = None,
    ):
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
                        description="You are missing the JSON script or JSON file\nPlease use [Discohooks](https://discohook.org/)"
                    )
                    await ctx.followup.send(embed=embed)
                elif jsonscript and jsonfile:
                    embed = Embed(
                        description="You are using both the JSON script and JSON file\nPlease use one"
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

                        if content == "":
                            content = None
                    except:
                        pass

                    try:
                        embed = Embed.from_dict(json["embeds"][0])
                        await message.edit(content=content, embed=embed)
                    except:
                        await message.edit(content=content)
                    await ctx.followup.send(
                        content="[Message]({}) edited".format(message.jump_url),
                        ephemeral=True,
                    )


class ReminderCog(GroupCog, name="reminder"):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    @Jeanne.command(name="add", description="Add a reminder")
    async def _add(
        self, ctx: Interaction, reason: str, time: str, dm: Optional[bool] = None
    ):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return
        embed = Embed()
        if len(Reminder(ctx.user).get_all_user_reminders()) >= 10:
            embed.description = "You have too many reminders!\nWait for one of them to be due or cancel a reminder"
            embed.color = Color.red()
            ctx.followup.send(embed=embed)
        else:
            embed.title = "Reminder added"
            date = datetime.now() + timedelta(seconds=parse_timespan(time))
            embed.description = f"On <t:{round(date.timestamp())}:F>, I will alert you about your reminder"
            embed.color = Color.random()
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(
                text="Please allow your DMs to be opened in this server (or any other server you are mutual to me) to recieve alerts"
            )
            Reminder(ctx.user)._add(reason, time)
            await ctx.followup.send(embed=embed, ephemeral=True)

    @_add.error
    async def _add_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if InvalidTimespan:
                embed = Embed(
                    title="Invalid time added",
                    description="You have entered the time incorrectly!",
                    color=Color.red(),
                )
                embed.add_field(
                    name="The time units (and abbreviations) supported by this command are:",
                    value="- ms, millisecond, milliseconds\n- s, sec, secs, second, seconds\n- m, min, mins, minute, minutes\n- h, hour, hours\n- d, day, days\n- w, week, weeks\n- y, year, years",
                    inline=False,
                )
                await ctx.followup.send(embed=embed, ephemeral=True)

    @Jeanne.command(name="list", description="List all the reminders you have")
    async def _list(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return        
        reminders = Reminder(ctx.user).get_all_user_reminders()
        embed = Embed()
        embed.description = reminders
        embed.color = Color.random()
        await ctx.followup.send(embed=embed, ephemeral=True)
    
    #@Jeanne.command(name="cancel", description="Cancel a reminder")
    #async def cancel(self, ctx:Interaction, reminder):
    #    await ctx.response.defer()
    #    if Botban(ctx.user).check_botbanned_user():
    #        return
    #    ...


class slashutilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.parser = Parser()

    @Jeanne.command(description="Type something and I will say it")
    @Jeanne.describe(channel="Send to which channel?", message="What should I say?")
    @Jeanne.checks.has_permissions(administrator=True)
    async def say(self, ctx: Interaction, channel: TextChannel, message: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer(ephemeral=True)
        await ctx.followup.send(content="Message sent to {}".format(channel.mention))
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
                description=f"{e}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command"
            )
            await ctx.followup.send(embed=failed)

    @Jeanne.command(description="Invite me to your server or join the support server")
    async def invite(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        invite = Embed(
            title="Invite me!",
            description="Click on one of these buttons to invite me to you server or join my creator's server",
            color=Color.random(),
        )

        await ctx.followup.send(embed=invite, view=invite_button())

    @Jeanne.command(description="Submit a bot report if you found something wrong")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def botreport(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.send_modal(ReportModal())

    @Jeanne.command(description="Check the meaning of a word with this command")
    @Jeanne.describe()
    async def dictionary(
        self, ctx: Interaction, word: str, language: Optional[Languages]
    ):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        await dictionary(ctx, word, language if not None else None)

async def setup(bot: Bot):
    await bot.add_cog(Weather_Group(bot))
    await bot.add_cog(Embed_Group(bot))
    await bot.add_cog(slashutilities(bot))
