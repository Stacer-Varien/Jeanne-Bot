from datetime import timedelta, datetime
import re
from discord import (
    Attachment,
    ButtonStyle,
    Color,
    Embed,
    Forbidden,
    Interaction,
    Message,
    NotFound,
    TextChannel,
    app_commands as Jeanne,
    ui,
)
from discord.ext.commands import Cog, Bot, GroupCog
from discord.ext import tasks
from assets.components import ReportModal
from assets.dictionary import dictionary
from functions import Botban, Command, Reminder
from config import WEATHER
from discord.ui import View
from py_expression_eval import Parser
from typing import Literal, Optional
from json import loads
from requests import get
from enum import Enum
from humanfriendly import parse_timespan, InvalidTimespan
from tabulate import tabulate

bot_invite_url = "https://discord.com/oauth2/authorize?client_id=831993597166747679&scope=bot%20applications.commands&permissions=467480734774"

topgg_invite = "https://top.gg/bot/831993597166747679"

discordbots_url = "https://discord.bots.gg/bots/831993597166747679"

orleans = "https://discord.gg/jh7jkuk2pp"


class Languages(Enum):
    English = "en"
    Spanish = "es"
    French = "fr"
    Japanese = "jp"
    Hindi = "hi"
    Dutch = "nl"
    German = "de"


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
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.generate.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.response.defer()

        if not (jsonscript or jsonfile):
            embed = Embed(
                description="You are missing the JSON script or JSON file\nPlease use [Discohook](https://discohook.org/)"
            )
            await ctx.followup.send(embed=embed)
            return
        if jsonscript and jsonfile:
            embed = Embed(
                description="You are using both the JSON script and JSON file\nPlease use one"
            )
            await ctx.followup.send(embed=embed)
            return

        json: dict = (
            loads(jsonscript) if jsonscript else loads(get(jsonfile.url).content)
        )

        try:
            content = json.get("content", None)
        except:
            pass

        try:
            embeds = [Embed.from_dict(i) for i in json.get("embeds", [])]
            if len(embeds) > 10:
                await ctx.followup.send(
                    content="Too many embeds! 10 is the maximum limit",
                    ephemeral=True,
                )
                return
            m = await channel.send(content=content, embeds=embeds)
        except:
            m = await channel.send(content=content)
        await ctx.followup.send(
            content="{} sent in {}".format(m.jump_url, channel.mention)
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
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.edit.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.response.defer()

        try:
            message: Message = await channel.fetch_message(int(messageid))
        except Exception as e:
            embed = Embed(description=e)
            await ctx.followup.send(embed=embed)
            return

        if not (jsonscript or jsonfile):
            embed = Embed(
                description="You are missing the JSON script or JSON file\nPlease use [Discohook](https://discohook.org/)"
            )
            await ctx.followup.send(embed=embed)
            return
        if jsonscript and jsonfile:
            embed = Embed(
                description="You are using both the JSON script and JSON file\nPlease use one"
            )
            await ctx.followup.send(embed=embed)
            return

        json: dict = (
            loads(jsonscript) if jsonscript else loads(get(jsonfile.url).content)
        )

        try:
            content = json.get("content", None)
        except:
            pass

        try:
            embeds = [Embed.from_dict(i) for i in json.get("embeds", [])]
            if len(embeds) > 10:
                await ctx.followup.send(
                    content="Too many embeds! 10 is the maximum limit",
                    ephemeral=True,
                )
                return
            await message.edit(content=content, embeds=embeds)
        except:
            await message.edit(content=content)
        await ctx.followup.send(
            content="{} edited in {}".format(message.jump_url, channel.jump_url)
        )

    @edit.error
    async def edit_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (Forbidden, NotFound)
        ):
            if Command(ctx.guild).check_disabled(self.edit.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            embed = Embed(
                description=error,
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)


class ReminderCog(GroupCog, name="reminder"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_reminders.start()
        super().__init__()

    @tasks.loop(seconds=60, reconnect=True)
    async def check_reminders(self):
        data = Reminder().get_all_reminders
        if data == None:
            return
        for reminder in data:
            if int(round(datetime.now().timestamp())) > int(reminder[2]):
                member = await self.bot.fetch_user(reminder[0])
                id = reminder[1]
                reason = reminder[3]
                try:
                    embed = Embed(title="Reminder ended", color=Color.random())
                    embed.add_field(name="Reminder", value=reason, inline=False)
                    await member.send(embed=embed)
                except:
                    pass
                await Reminder(member).remove(id)
            else:
                continue

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    @Jeanne.command(description="Add a reminder")
    @Jeanne.describe(
        reason="Reason for the reminder",
        time="Time that you want to be reminded at? (1h, 30m, etc)",
    )
    async def add(self, ctx: Interaction, reason: str, time: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        await ctx.response.defer(ephemeral=True)
        embed = Embed()
        user_reminders = Reminder(ctx.user).get_all_user_reminders

        try:
            if len(user_reminders) >= 10:
                embed.description = (
                    "You have too many reminders! Wait for one to be due or cancel one."
                )
                embed.color = Color.red()
                await ctx.followup.send(embed=embed)
                return
        except:
            if parse_timespan(time) < parse_timespan("1 minute"):
                embed.color = Color.red()
                embed.description = "Please add a time more than 1 minute."
                await ctx.followup.send(embed=embed, ephemeral=True)
                return

            date = datetime.now() + timedelta(seconds=parse_timespan(time))
            embed.title = "Reminder added"
            embed.description = f"On <t:{round(date.timestamp())}:F>, I will alert you about your reminder."
            embed.color = Color.random()
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(
                text="Please allow your DMs to be opened in this server (or any other server you are mutual to me) to receive alerts."
            )
            await Reminder(ctx.user).add(reason, round(date.timestamp()))
            await ctx.followup.send(embed=embed, ephemeral=True)

    @add.error
    async def add_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(
            error.original, InvalidTimespan
        ):
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
        if Botban(ctx.user).check_botbanned_user:
            return

        await ctx.response.defer(ephemeral=True)
        reminders = Reminder(ctx.user).get_all_user_reminders
        try:
            reminds = []
            for i in reminders:
                ids = i[1]
                reminder = i[3]
                time = f"<t:{i[2]}:F>"
                reminds.append([str(ids), str(reminder), str(time)])
            col_names = ["ID", "Reminders", "Time"]
            embed = Embed()
            embed.description = tabulate(reminds, headers=col_names, tablefmt="pretty")
        except:
            embed.description = "No reminders"
        embed.color = Color.random()
        await ctx.followup.send(embed=embed, ephemeral=True)

    @Jeanne.command(name="cancel", description="Cancel a reminder")
    async def cancel(self, ctx: Interaction, reminder_id: int):
        if Botban(ctx.user).check_botbanned_user:
            return
        await ctx.response.defer(ephemeral=True)
        reminder = Reminder(ctx.user)
        embed = Embed()
        if await reminder.remove(reminder_id) == False:
            embed.color = Color.red()
            embed.description = "You don't have a reminder with that ID"
            await ctx.followup.send(embed=embed, ephemeral=True)
            return

        embed.color = Color.random()
        embed.description = "Reminder `{}` has been removed".format(reminder_id)
        reminder.remove(reminder_id)
        await ctx.followup.send(embed=embed, ephemeral=True)


class slashutilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.parser = Parser()

    @Jeanne.command(description="Get weather information on a city")
    @Jeanne.checks.cooldown(3, 14400, key=lambda i: (i.user.id))
    @Jeanne.describe(city="Add a city", units="Metric or Imperial? (Default is metric)")
    async def weather(
        self,
        ctx: Interaction,
        city: Jeanne.Range[str, 1],
        units: Optional[Literal["Metric", "Imperial"]] = None,
    ):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.weather.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.response.defer()
        emoji_map = {
            "globe": "🌍",
            "newspaper": "📰",
            "min_tempe": "🌡️",
            "max_tempe": "🔥",
            "feels_like": "🤚",
            "humidity": "💧",
            "clouds": "☁️",
            "visibility": "👁️",
            "wind_dir": "➡️",
            "guste": "💨",
            "rain_chance": "💦",
        }

        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER}&q={city.lower()}&days=1&aqi=no&alerts=no"

        weather_data = get(url).json()

        location = weather_data["location"]

        current = weather_data["current"]
        forecast = weather_data["forecast"]["forecastday"][0]["day"]

        if units == "Imperial":
            min_temp = f"{forecast['mintemp_f']}°F"
            max_temp = f"{forecast['maxtemp_f']}°F"
            feels_like = f"{current['feelslike_f']}°F"
            gust = f"{current['gust_mph']}mph"
            visibility = f"{current['vis_miles']}mi"
        else:
            min_temp = f"{forecast['mintemp_c']}°C"
            max_temp = f"{forecast['maxtemp_c']}°C"
            feels_like = f"{current['feelslike_c']}°C"
            gust = f"{current['gust_kph']}km/h"
            visibility = f"{current['vis_km']}km"

        embed = Embed(
            title=f"{emoji_map['globe']} Weather details of {location['name']}, {location['region']}/{location['country']}",
            color=Color.random(),
        )
        embed.description = (
            f"{emoji_map['newspaper']} Condition: {forecast['condition']['text']}"
        )
        embed.add_field(
            name=f"{emoji_map['min_tempe']} Minimum Temperature",
            value=min_temp,
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['max_tempe']} Maximum Temperature",
            value=max_temp,
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['feels_like']} Feels Like",
            value=feels_like,
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['clouds']} Clouds",
            value=f"{current['cloud']}%",
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['humidity']} Humidity",
            value=f"{current['humidity']}%",
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['wind_dir']} Wind Direction",
            value=f"{current['wind_degree']}°/{current['wind_dir']}",
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['guste']} Wind Gust",
            value=gust,
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['visibility']} Visibility",
            value=visibility,
            inline=True,
        )
        embed.add_field(
            name=f"{emoji_map['rain_chance']} Chance of Rain",
            value=f"{forecast['daily_chance_of_rain']}%",
            inline=True,
        )
        embed.set_footer(text="Fetched from weatherapi.com")
        await ctx.followup.send(embed=embed)

    @weather.error
    async def weather_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.weather.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"WOAH! You have already checked the weather.\nTry again after <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)
            return

        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (KeyError, TypeError)
        ):
            if isinstance(error, Jeanne.CommandOnCooldown):
                if Command(ctx.guild).check_disabled(self.weather.qualified_name):
                    await ctx.followup.send(
                        "This command is disabled by the server's managers",
                        ephemeral=True,
                    )
                    return
            no_city = Embed(
                description="Failed to get weather information on this city\nPlease note that ZIP/postal codes are only supported for Canada, the US, and the UK for this command.",
                color=Color.red(),
            )
            await ctx.followup.send(embed=no_city)

    @Jeanne.command(description="Type something and I will say it")
    @Jeanne.describe(channel="Send to which channel?", message="What should I say?")
    @Jeanne.checks.has_permissions(administrator=True)
    async def say(self, ctx: Interaction, channel: TextChannel, message: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.say.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer(ephemeral=True)
        await ctx.followup.send(content="Message sent to {}".format(channel.mention))
        await channel.send(message)

    @Jeanne.command(description="Do a calculation")
    @Jeanne.describe(calculate="Add a calculation")
    async def calculator(self, ctx: Interaction, calculate: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.calculator.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.response.defer()

        numeric_parts = re.findall(r'\d+\.\d+|\d+', calculate)
        check = ''.join([str(float(part)) if part.isdigit() else part for part in re.split(r'(\d+\.\d+|\d+)', calculate)])
        self.parser.parse(check).evaluate({})

        answer = self.parser.parse(calculate).evaluate({})

        calculation = Embed(title="Result", color=Color.random())
        calculation.add_field(name=f"`{calculate}`", value=answer)
        await ctx.followup.send(embed=calculation)

    @calculator.error
    async def calculator_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, OverflowError
        ):
            failed = Embed(description=str(error))
            await ctx.followup.send(embed=failed)
        elif isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, Exception
        ):
            failed = Embed(
                description=f"{error}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command"
            )
            await ctx.followup.send(embed=failed)

    @Jeanne.command(description="Invite me to your server or join the support server")
    async def invite(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user:
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
        if Botban(ctx.user).check_botbanned_user:
            return

        await ctx.response.send_modal(ReportModal())

    @Jeanne.command(description="Check the meaning of a word")
    @Jeanne.describe()
    async def dictionary(
        self,
        ctx: Interaction,
        word: Jeanne.Range[str, 1],
        language: Optional[Languages] = None,
    ):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.dictionary.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        lang = language.value if language else None
        await dictionary(ctx, word.lower(), lang)


async def setup(bot: Bot):
    await bot.add_cog(Embed_Group(bot))
    await bot.add_cog(slashutilities(bot))
    await bot.add_cog(ReminderCog(bot))
