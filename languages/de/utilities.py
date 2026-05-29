from datetime import timedelta, datetime
from random import randint
import re
import aiohttp
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    TextChannel,
    app_commands as Jeanne,
    ui,
)
from discord.ext.commands import Bot
from reactionmenu import ViewButton, ViewMenu
from assets.components import ReportModal
from functions import Confess, Moderation, Reminder
from config import WEATHER
from discord.ui import View
from py_expression_eval import Parser
from typing import Literal, Optional
from json import loads
from humanfriendly import parse_timespan, InvalidTimespan

bot_invite_url = (
    "https://canary.discord.com/oauth2/authorize?client_id=831993597166747679"
)
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


class EmbedGroup:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def generate(self, ctx: Interaction, channel: TextChannel, jsonscript: str):
        await ctx.response.defer()
        if not jsonscript:
            await ctx.followup.send(
                embed=Embed(
                    description="Gib ein JSON-Skript oder eine Datei an. Verwende [Discohook](https://discohook.app/)"
                )
            )
            return
        json_data = loads(jsonscript)
        content = json_data.get("content", None)
        embeds = [Embed.from_dict(i) for i in json_data.get("embeds", [])]

        if len(embeds) > 10:
            await ctx.followup.send(
                content="Te veel embeds! Maximum is 10.", ephemeral=True
            )
            return

        message = await channel.send(content=content, embeds=embeds or None)
        await ctx.followup.send(content=f"{message.jump_url} verzonden in {channel.mention}")

    async def edit(
        self, ctx: Interaction, channel: TextChannel, messageid: str, jsonscript: str
    ):
        await ctx.response.defer()
        message = await channel.fetch_message(int(messageid))

        json_data = loads(jsonscript)
        content = json_data.get("content", None)
        embeds = [Embed.from_dict(i) for i in json_data.get("embeds", [])]

        if len(embeds) > 10:
            await ctx.followup.send(
                content="Te veel embeds! Maximum is 10.", ephemeral=True
            )
            return

        await message.edit(content=content, embeds=embeds or None)
        await ctx.followup.send(
            content=f"{message.jump_url} bewerkt in {channel.mention}"
        )

    async def edit_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        await ctx.followup.send(embed=Embed(description=str(error), color=Color.red()))


class ReminderCog:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def add(self, ctx: Interaction, reason: str, time: str):
        await ctx.response.defer(ephemeral=True)
        user_reminders = Reminder(ctx.user).get_all_user_reminders

        if user_reminders and len(user_reminders) >= 10:
            await ctx.followup.send(
                embed=Embed(
                    description="Zu viele Erinnerungen! Lösche eine oder warte, bis eine abläuft.",
                    color=Color.red(),
                ),
                ephemeral=True,
            )
            return

        try:
            reminder_time = parse_timespan(time)
            if reminder_time < 60:
                raise InvalidTimespan
        except InvalidTimespan:
            await ctx.followup.send(
                embed=Embed(
                    description="Ungültige Zeit! Verwende eine Dauer von mehr als 1 Minute.",
                    color=Color.red(),
                ),
                ephemeral=True,
            )
            return

        date = datetime.now() + timedelta(seconds=reminder_time)
        await Reminder(ctx.user).add(reason, round(date.timestamp()))
        embed = Embed(
            title="Erinnerung hinzugefügt",
            description=f"Ich werde dich um <t:{round(date.timestamp())}:F> daran erinnern.",
            color=Color.random(),
        )
        embed.add_field(name="Grund", value=reason, inline=False)
        embed.set_footer(text="Stelle sicher, dass deine DMs geöffnet sind, um Benachrichtigungen zu erhalten.")
        await ctx.followup.send(embed=embed, ephemeral=True)

    async def add_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(
            error.original, InvalidTimespan
        ):
            embed = Embed(
                title="Ungültige Zeit",
                description="Ondersteunde tijdseenheden: ms, s, m, h, d, w, j.",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed, ephemeral=True)

    async def _list(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        embed = Embed()
        reminders = Reminder(ctx.user).get_all_user_reminders
        if reminders is None:
            embed.description = "Keine Erinnerungen"
        else:
            for i in reminders:
                ids = i[1]
                reminder = i[3]
                time = f"<t:{i[2]}:F>"

                embed.add_field(
                    name=f"ID: {ids}",
                    value=f"*Herinnering:* {reminder}\n*Tijd:* {time}",
                    inline=True,
                )
        embed.color = Color.random()
        await ctx.followup.send(embed=embed, ephemeral=True)

    async def cancel(self, ctx: Interaction, reminder_id: int):
        await ctx.response.defer(ephemeral=True)
        reminder = Reminder(ctx.user)
        embed = Embed()
        if not await reminder.remove(reminder_id):
            embed.color = Color.red()
            embed.description = "Du hast keine Erinnerung mit dieser ID"
            await ctx.followup.send(embed=embed, ephemeral=True)
            return
        embed.color = Color.random()
        embed.description = "Herinnering `{}` is verwijderd".format(reminder_id)
        await reminder.remove(reminder_id)
        await ctx.followup.send(embed=embed, ephemeral=True)


class Utilities:
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
        days = 1 if not three_day else 3
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
            title=f"{emoji_map['globe']} Weerbericht van {location['name']}, {location['region']}/{location['country']}",
            color=Color.random(),
        )
        day1.description = (
            f"{emoji_map['newspaper']} Conditie: {forecast['condition']['text']}"
        )
        day1.add_field(
            name=f"{emoji_map['min_tempe']} Minimumtemperatuur",
            value=min_temp,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['max_tempe']} Maximumtemperatuur",
            value=max_temp,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['clouds']} Wolken",
            value=f"{current['cloud']}%",
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['humidity']} Vochtigheid",
            value=f"{current['humidity']}%",
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['wind_dir']} Windrichting",
            value=f"{current['wind_degree']}°/{current['wind_dir']}",
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['guste']} Windstoot",
            value=gust,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['visibility']} Zicht",
            value=visibility,
            inline=True,
        )
        day1.add_field(
            name=f"{emoji_map['rain_chance']} Kans op regen",
            value=f"{forecast['daily_chance_of_rain']}%",
            inline=True,
        )
        day1.set_footer(text="Abgerufen von weatherapi.com")
        if three_day:
            menu = ViewMenu(
                ctx,
                menu_type=ViewMenu.TypeEmbed,
                disable_items_on_timeout=True,
                show_page_director=False,
            )
            forecastday2 = weather_data["forecast"]["forecastday"][1]
            forecastday3 = weather_data["forecast"]["forecastday"][2]
            day2 = Embed(
                title=f"{emoji_map['globe']} Weerbericht van {location['name']}, {location['region']}/{location['country']} voor {forecastday2['date']}",
                color=Color.random(),
            )
            day3 = Embed(
                title=f"{emoji_map['globe']} Weerbericht van {location['name']}, {location['region']}/{location['country']} voor {forecastday3['date']}",
                color=Color.random(),
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

            day2.description = f"{emoji_map['newspaper']} Conditie: {forecastday2['day']['condition']['text']}"
            day2.add_field(
                name=f"{emoji_map['min_tempe']} Minimumtemperatuur",
                value=min_temp2,
                inline=False,
            )
            day2.add_field(
                name=f"{emoji_map['max_tempe']} Maximumtemperatuur",
                value=max_temp2,
                inline=False,
            )
            day2.add_field(
                name=f"{emoji_map['guste']} Maximale wind",
                value=maxwind2,
                inline=False,
            )
            day2.add_field(
                name=f"{emoji_map['rain_chance']} Kans op regen",
                value=f"{forecastday2['day']['daily_chance_of_rain']}%",
                inline=False,
            )
            day2.set_footer(text="Abgerufen von weatherapi.com")

            day3.description = f"{emoji_map['newspaper']} Conditie: {forecastday3['day']['condition']['text']}"
            day3.add_field(
                name=f"{emoji_map['min_tempe']} Minimumtemperatuur",
                value=min_temp3,
                inline=False,
            )
            day3.add_field(
                name=f"{emoji_map['max_tempe']} Maximumtemperatuur",
                value=max_temp3,
                inline=False,
            )
            day3.add_field(
                name=f"{emoji_map['guste']} Maximale wind",
                value=maxwind3,
                inline=False,
            )
            day3.add_field(
                name=f"{emoji_map['rain_chance']} Kans op regen",
                value=f"{forecastday3['day']['daily_chance_of_rain']}%",
                inline=False,
            )
            day3.set_footer(text="Abgerufen von weatherapi.com")

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

    async def weather_error(
        self,
        ctx: Interaction,
        error: Jeanne.AppCommandError,
        error_type: Literal["cooldown", "failed"],
    ):
        if error_type == "cooldown":
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"WOAH! Du hast das Wetter bereits überprüft.\nVersuche es erneut in <t:{reset_hour}:R>",
                color=0xFF0000,
            )
            await ctx.response.send_message(embed=cooldown)
            return
        if error_type == "failed":
            no_city = Embed(
                description="Konnte keine Wetterinformationen für diese Stadt abrufen\nHinweis: Postleitzahlen werden für diesen Befehl nur für Kanada, die USA und das Vereinigte Königreich unterstützt.",
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
        calculation = Embed(title="Resultaat", color=Color.random())
        calculation.add_field(name=f"`{calculate}`", value=answer)
        await ctx.followup.send(embed=calculation)

    async def calculator_error(
        self,
        ctx: Interaction,
        error: Jeanne.AppCommandError,
        error_type: Literal["overflow", "failed"],
    ):
        if error_type == "overflow":
            failed = Embed(description=str(error))
            await ctx.followup.send(embed=failed)
            return
        if error_type == "failed":
            failed = Embed(
                description=f"{error}\nSiehe [Python Operators](https://www.geeksforgeeks.org/python-operators/?ref=lbp), wenn du nicht weißt, wie du den Befehl verwenden sollst"
            )
            await ctx.followup.send(embed=failed)

    async def invite(self, ctx: Interaction):
        await ctx.response.defer()
        invite = Embed(
            title="Nodig mij uit!",
            description="Klicke auf einen dieser Buttons, um mich auf deinen Server einzuladen oder dem Server meines Erstellers beizutreten",
            color=Color.random(),
        )
        await ctx.followup.send(embed=invite, view=InviteButton())

    async def botreport(self, ctx: Interaction, report_type: str):
        await ctx.response.send_modal(ReportModal(ctx, report_type))

    async def confession(
        self,
        ctx: Interaction,
        confession: Jeanne.Range[str, 1],
        anonymous: Optional[bool] = False,
    ):
        channel = Confess(ctx.guild).get_confession_channel
        if not channel:
            await ctx.response.send_message(
                embed=Embed(
                    description="Beichtkanal ist nicht eingerichtet. Bitte kontaktiere den Serveradministrator.",
                    color=Color.red(),
                ),
                ephemeral=True,
            )
            return

        confession_id = randint(1, 999999)
        embed = Embed(color=Color.random())

        if anonymous:
            embed.title = "Anonyme Beichte"
        else:
            embed.title = f"Beichte von {ctx.user.name}"

        embed.description = confession
        embed.set_footer(
            text=f"Beicht-ID: {confession_id}\nWenn diese Beichte unangemessen ist, melde sie bitte den Moderatoren mit der Beicht-ID über `/reportconfession`. Wenn die Beichte sehr schwerwiegend ist, melde sie bitte dem Entwickler mit `/botreport` und füge die Beicht-ID hinzu."
        )
        await Confess(ctx.guild).add_confession(ctx.user, confession_id, confession)
        await channel.send(embed=embed)
        await ctx.response.send_message(
            embed=Embed(
                description=f"Dein Geständnis wurde an {channel.mention} mit der ID {confession_id} gesendet",
                color=Color.green(),
            ),
            ephemeral=True,
        )

    async def reportconfession(
        self, ctx: Interaction, confession_id: int, reason: Optional[str] = None
    ):
        confession = await Confess(ctx.guild).get_confession(confession_id)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.response.send_message(
                embed=Embed(
                    description="Moderations-Logkanal ist nicht eingerichtet. Bitte kontaktiere die Serveradministratoren.",
                    color=Color.red(),
                ),
                ephemeral=True,
            )
            return
        if confession is None:
            await ctx.response.send_message(
                embed=Embed(
                    description="Keine Beichte mit dieser ID gefunden.", color=Color.red()
                ),
                ephemeral=True,
            )
            return
        embed = Embed()
        embed.title = "Beichte melden"
        embed.add_field(name="Beicht-ID", value=confession_id, inline=False)
        embed.add_field(name="Grund", value=reason, inline=False)

        await modlog.send(embed=embed)
        await ctx.response.send_message(
            embed=Embed(
                description=f"Beichte mit ID: {confession_id} wurde den Moderatoren gemeldet.",
                color=Color.green(),
            ),
            ephemeral=True,
        )
    

