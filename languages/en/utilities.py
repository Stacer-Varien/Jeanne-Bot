from datetime import timedelta, datetime
import re
import aiohttp
from discord import (
    ButtonStyle, Color, Embed, Interaction,
    TextChannel, app_commands as Jeanne, ui
)
from discord.ext.commands import Bot
from reactionmenu import ViewButton, ViewMenu
from assets.components import ReportModal
from functions import (
    Reminder
)
from config import WEATHER
from discord.ui import View
from py_expression_eval import Parser
from typing import Literal, Optional
from json import loads
from humanfriendly import parse_timespan, InvalidTimespan

bot_invite_url = "https://canary.discord.com/oauth2/authorize?client_id=831993597166747679"
topgg_invite = "https://top.gg/bot/831993597166747679"
discordbots_url = "https://discord.bots.gg/bots/831993597166747679"
orleans = "https://discord.gg/jh7jkuk2pp"


class InviteButton(View):
    def __init__(self):
        super().__init__()
        urls = [
            ("Bot Invite", bot_invite_url),
            ("Top.gg", topgg_invite),
            ("DiscordBots", discordbots_url),
            ("Orleans", orleans),
        ]
        for label, url in urls:
            self.add_item(ui.Button(style=ButtonStyle.url, label=label, url=url))


class EmbedGroup():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def generate(
        self, ctx: Interaction, channel: TextChannel, jsonscript: str):
        await ctx.response.defer()
        if not jsonscript:
            await ctx.followup.send(
                embed=Embed(
                    description="Provide either a JSON script or file. Use [Discohook](https://discohook.app/)"
                )
            )
            return
        json_data = loads(jsonscript)
        content = json_data.get("content", None)
        embeds = [Embed.from_dict(i) for i in json_data.get("embeds", [])]

        if len(embeds) > 10:
            await ctx.followup.send(content="Too many embeds! Maximum is 10.", ephemeral=True)
            return

        message = await channel.send(content=content, embeds=embeds or None)
        await ctx.followup.send(content=f"{message.jump_url} sent in {channel.mention}")

    async def edit(
        self, ctx: Interaction, channel: TextChannel, messageid: str, jsonscript: str):
        await ctx.response.defer()
        message = await channel.fetch_message(int(messageid))

        json_data = loads(jsonscript)
        content = json_data.get("content", None)
        embeds = [Embed.from_dict(i) for i in json_data.get("embeds", [])]

        if len(embeds) > 10:
            await ctx.followup.send(content="Too many embeds! Maximum is 10.", ephemeral=True)
            return

        await message.edit(content=content, embeds=embeds or None)
        await ctx.followup.send(content=f"{message.jump_url} edited in {channel.mention}")

    async def edit_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        await ctx.followup.send(embed=Embed(description=str(error), color=Color.red()))


class ReminderCog():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def add(self, ctx: Interaction, reason: str, time: str):
        await ctx.response.defer(ephemeral=True)
        user_reminders = Reminder(ctx.user).get_all_user_reminders

        if user_reminders and len(user_reminders) >= 10:
            await ctx.followup.send(embed=Embed(description="Too many reminders! Cancel one or wait for one to expire.", color=Color.red()), ephemeral=True)
            return

        try:
            reminder_time = parse_timespan(time)
            if reminder_time < 60:
                raise InvalidTimespan
        except InvalidTimespan:
            await ctx.followup.send(embed=Embed(description="Invalid time! Use a duration greater than 1 minute.", color=Color.red()), ephemeral=True)
            return

        date = datetime.now() + timedelta(seconds=reminder_time)
        await Reminder(ctx.user).add(reason, round(date.timestamp()))
        embed = Embed(
            title="Reminder added",
            description=f"On <t:{round(date.timestamp())}:F>, I will remind you.",
            color=Color.random(),
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text="Ensure your DMs are open to receive alerts.")
        await ctx.followup.send(embed=embed, ephemeral=True)

    async def add_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(error.original, InvalidTimespan):
            embed = Embed(
                title="Invalid time",
                description="Supported time units: ms, s, m, h, d, w, y.",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed, ephemeral=True)

    async def _list(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        embed = Embed()
        reminders = Reminder(ctx.user).get_all_user_reminders
        if reminders == None:
            embed.description = "No reminders"
        else:
            for i in reminders:
                ids = i[1]
                reminder = i[3]
                time = f"<t:{i[2]}:F>"

                embed.add_field(
                    name=f"ID: {ids}",
                    value=f"*Reminder:* {reminder}\n*Time:* {time}",
                    inline=True,
                )
        embed.color = Color.random()
        await ctx.followup.send(embed=embed, ephemeral=True)

    async def cancel(self, ctx: Interaction, reminder_id: int):
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
        await reminder.remove(reminder_id)
        await ctx.followup.send(embed=embed, ephemeral=True)


class Utilities():
    def __init__(self, bot: Bot):
        self.bot = bot
        self.parser = Parser()

    async def weather(
        self,
        ctx: Interaction,
        city: Jeanne.Range[str, 1],
        units: Optional[Literal["Metric", "Imperial"]] = None,
        three_day: Optional[bool] = False,
    ):
        await ctx.response.defer()
        emoji_map = {
            "globe": "🌍",
            "newspaper": "📰",
            "min_tempe": "🌡️",
            "max_tempe": "🔥",
            "humidity": "💧",
            "clouds": "☁️",
            "visibility": "👁️",
            "wind_dir": "➡️",
            "guste": "💨",
            "rain_chance": "💦",
        }
        days = 1 if three_day == False else 3
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER}&q={city.lower()}&days={days}&aqi=no&alerts=no"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                weather_data = await resp.json()

        location = weather_data["location"]
        current = weather_data["current"]
        forecast = weather_data["forecast"]["forecastday"][0]["day"]
        if units == "Imperial":
            min_temp = f"{forecast['mintemp_f']}°F"
            max_temp = f"{forecast['maxtemp_f']}°F"
            gust = f"{current['gust_mph']}mph"
            visibility = f"{current['vis_miles']}mi"
        else:
            min_temp = f"{forecast['mintemp_c']}°C"
            max_temp = f"{forecast['maxtemp_c']}°C"
            gust = f"{current['gust_kph']}km/h"
            visibility = f"{current['vis_km']}km"
        day1 = Embed(
            title=f"{emoji_map['globe']} Weather details of {location['name']}, {location['region']}/{location['country']}",
            color=Color.random(),
        )
        day1.description = (
            f"{emoji_map['newspaper']} Condition: {forecast['condition']['text']}"
        )
        day1.add_field(
            name=f"{emoji_map['min_tempe']} Minimum Temperature",
            value=min_temp,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['max_tempe']} Maximum Temperature",
            value=max_temp,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['clouds']} Clouds",
            value=f"{current['cloud']}%",
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['humidity']} Humidity",
            value=f"{current['humidity']}%",
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['wind_dir']} Wind Direction",
            value=f"{current['wind_degree']}°/{current['wind_dir']}",
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['guste']} Wind Gust",
            value=gust,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['visibility']} Visibility",
            value=visibility,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['rain_chance']} Chance of Rain",
            value=f"{forecast['daily_chance_of_rain']}%",
            inline=True,
        )
        day1.set_footer(text="Fetched from weatherapi.com")
        if three_day == True:
            menu = ViewMenu(
                ctx,
                menu_type=ViewMenu.TypeEmbed,
                disable_items_on_timeout=True,
                show_page_director=False,
            )
            forecastday2 = weather_data["forecast"]["forecastday"][1]
            forecastday3 = weather_data["forecast"]["forecastday"][2]
            day2 = Embed(
                title=f"{emoji_map['globe']} Weather details of {location['name']}, {location['region']}/{location['country']} for {forecastday2['date']}", color=Color.random()
            )
            day3 = Embed(title=f"{emoji_map['globe']} Weather details of {location['name']}, {location['region']}/{location['country']} for {forecastday3['date']}", color=Color.random()
            )

            if units == "Imperial":
                min_temp2 = f"{forecastday2['day']['mintemp_f']}°F"
                max_temp2 = f"{forecastday2['day']['maxtemp_f']}°F"
                maxwind2 = f"{forecastday2['day']['maxwind_mph']}mph"
                min_temp3 = f"{forecastday3['day']['mintemp_f']}°F"
                max_temp3 = f"{forecastday3['day']['maxtemp_f']}°F"
                maxwind3 = f"{forecastday3['day']['maxwind_mph']}mph"
            else:
                min_temp2 = f"{forecastday2['day']['mintemp_c']}°C"
                max_temp2 = f"{forecastday2['day']['maxtemp_c']}°C"
                maxwind2 = f"{forecastday2['day']['maxwind_kph']}km/h"
                min_temp3 = f"{forecastday3['day']['mintemp_c']}°C"
                max_temp3 = f"{forecastday3['day']['maxtemp_c']}°C"
                maxwind3 = f"{forecastday3['day']['maxwind_kph']}km/h"

            day2.description = f"{emoji_map['newspaper']} Condition: {forecastday2['day']['condition']['text']}"
            day2.add_field(
                name=f"{emoji_map['min_tempe']} Minimum Temperature",
                value=min_temp2,
                inline=False,
            )
            day2.add_field(
                name=f"{emoji_map['max_tempe']} Maximum Temperature",
                value=max_temp2,
                inline=False,
            )
            day2.add_field(
                name=f"{emoji_map['guste']} Maximum Wind",
                value=maxwind2,
                inline=False,
            )
            day2.add_field(
                name=f"{emoji_map['rain_chance']} Chance of Rain",
                value=f"{forecastday2['day']['daily_chance_of_rain']}%",
                inline=False,
            )
            day2.set_footer(text="Fetched from weatherapi.com")

            day3.description = f"{emoji_map['newspaper']} Condition: {forecastday3['day']['condition']['text']}"
            day3.add_field(
                name=f"{emoji_map['min_tempe']} Minimum Temperature",
                value=min_temp3,
                inline=False,
            )
            day3.add_field(
                name=f"{emoji_map['max_tempe']} Maximum Temperature",
                value=max_temp3,
                inline=False,
            )
            day3.add_field(
                name=f"{emoji_map['guste']} Maximum Wind",
                value=maxwind3,
                inline=False,
            )
            day3.add_field(
                name=f"{emoji_map['rain_chance']} Chance of Rain",
                value=f"{forecastday3['day']['daily_chance_of_rain']}%",
                inline=False,
            )
            day3.set_footer(text="Fetched from weatherapi.com")

            menu.add_page(day1)
            menu.add_page(day2)
            menu.add_page(day3)
            menu.add_button(ViewButton.go_to_first_page())
            menu.add_button(ViewButton.back())
            menu.add_button(ViewButton.next())
            menu.add_button(ViewButton.go_to_last_page())
            await menu.start()
            return
        await ctx.followup.send(embed=day1)

    async def weather_error(self, ctx: Interaction, error: Jeanne.AppCommandError, error_type:Literal["cooldown", "failed"]):
        if error_type=="cooldown":
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"WOAH! You have already checked the weather.\nTry again after <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)
            return
        if error_type=="failed":
            no_city = Embed(
                description="Failed to get weather information on this city\nPlease note that ZIP/postal codes are only supported for Canada, the US, and the UK for this command.",
                color=Color.red(),
            )
            await ctx.followup.send(embed=no_city)

    async def calculator(self, ctx: Interaction, calculate: str):
        await ctx.response.defer()
        check = "".join(
            [
                str(float(part)) if part.isdigit() else part
                for part in re.split(r"(\d+\.\d+|\d+)", calculate)
            ]
        )
        self.parser.parse(check).evaluate({})
        answer = self.parser.parse(calculate).evaluate({})
        calculation = Embed(title="Result", color=Color.random())
        calculation.add_field(name=f"`{calculate}`", value=answer)
        await ctx.followup.send(embed=calculation)

    async def calculator_error(self, ctx: Interaction, error: Jeanne.AppCommandError, error_type:Literal["overflow", "failed"]):
        if error_type=="overflow":
            failed = Embed(description=str(error))
            await ctx.followup.send(embed=failed)
            return
        if error_type=="failed":
            failed = Embed(
                description=f"{error}\nPlease refer to [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp) if you don't know how to use the command"
            )
            await ctx.followup.send(embed=failed)

    async def invite(self, ctx: Interaction):
        await ctx.response.defer()
        invite = Embed(
            title="Invite me!",
            description="Click on one of these buttons to invite me to you server or join my creator's server",
            color=Color.random(),
        )
        await ctx.followup.send(embed=invite, view=InviteButton())

    async def botreport(self, ctx: Interaction, report_type: str):
        await ctx.response.send_modal(ReportModal(report_type))
