from discord import (
    Forbidden, HTTPException, Interaction,
    NotFound, TextChannel, app_commands as Jeanne
)
from discord.ext.commands import Cog, Bot, GroupCog
from assets.dictionary import dictionary
from functions import (
    check_botbanned_app_command, check_disabled_app_command, is_suspended
)
from py_expression_eval import Parser
from typing import Literal, Optional
from humanfriendly import InvalidTimespan
from discord.app_commands import locale_str as T
import languages.en.utilities as en
import languages.fr.utilities as fr

class EmbedGroup(GroupCog, name="embed"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("generate_name"),
        description=T("generate_desc"),
        extras={"member_perms": "Administrator"},
    )
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.describe(
        channel=T("generate_channel_parm_desc"),
        jsonscript=T("generate_jsonscript_parm_desc"),
    )
    @Jeanne.rename(
        channel=T("generate_channel_parm_name"),
        jsonscript=T("generate_jsonscript_parm_name"),
    )
    async def generate(
        self, ctx: Interaction, channel: TextChannel, jsonscript: str):
        if ctx.locale.value=="en-GB" or ctx.locale.value=="en-US":
            await en.EmbedGroup(self.bot).generate(ctx, channel, jsonscript)
        elif ctx.locale.value=="fr":
            await fr.EmbedGroup(self.bot).generate(ctx, channel, jsonscript)

    @Jeanne.command(
        name=T("edit_name"),
        description=T("edit_desc"),
        extras={"member_perms": "Administrator"},
    )
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.describe(
        channel=T("edit_channel_parm_desc"),
        messageid=T("edit_messageid_parm_desc"),
        jsonscript=T("edit_jsonscript_parm_desc"),
    )
    @Jeanne.rename(
        channel=T("edit_channel_parm_name"),
        messageid=T("edit_messageid_parm_name"),
        jsonscript=T("edit_jsonscript_parm_name"),
    )
    async def edit(
        self, ctx: Interaction, channel: TextChannel, messageid: str, jsonscript: str):
        await ctx.response.defer()
        if ctx.locale.value=="en-GB" or ctx.locale.value=="en-US":
            await en.EmbedGroup(self.bot).edit(ctx, channel, messageid, jsonscript)
        elif ctx.locale.value=="fr":
            await fr.EmbedGroup(self.bot).edit(ctx, channel, messageid, jsonscript)

    @edit.error
    async def edit_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(error.original, (Forbidden, NotFound, HTTPException)):
            if ctx.locale.value=="en-GB" or ctx.locale.value=="en-US":
                await en.EmbedGroup(self.bot).edit_error(ctx, error)
            elif ctx.locale.value=="fr":
                await fr.EmbedGroup(self.bot).edit_error(ctx, error)


class ReminderCog(GroupCog, name="reminder"):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("reminder_add_name"),
        description=T("reminder_add_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.describe(
        reason=T("reminder_add_reason_parm_desc"),
        time=T("reminder_add_time_parm_desc"),
    )
    @Jeanne.rename(
        reason=T("reminder_add_reason_parm_name"),
        time=T("reminder_add_time_parm_name"),
    )
    async def add(self, ctx: Interaction, reason: str, time: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.ReminderCog(self.bot).add(ctx, reason, time)
        elif ctx.locale.value == "fr":
            await fr.ReminderCog(self.bot).add(ctx, reason, time)

    @add.error
    async def add_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(error.original, InvalidTimespan):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.ReminderCog(self.bot).add_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.ReminderCog(self.bot).add_error(ctx, error)

    @Jeanne.command(
        name=T("reminder_list_name"),
        description=T("reminder_list_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def _list(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.ReminderCog(self.bot)._list(ctx)
        elif ctx.locale.value == "fr":
            await fr.ReminderCog(self.bot)._list(ctx)

    @Jeanne.command(
        name=T("reminder_cancel_name"),
        description=T("reminder_cancel_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.describe(reminder_id=T("reminder_cancel_rmd_id_parm_desc"))
    @Jeanne.rename(reminder_id=T("reminder_cancel_rmd_id_parm_name"))
    async def cancel(self, ctx: Interaction, reminder_id: int):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.ReminderCog(self.bot).cancel(ctx, reminder_id)
        elif ctx.locale.value == "fr":
            await fr.ReminderCog(self.bot).cancel(ctx, reminder_id)

class SlashUtilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.parser = Parser()

    @Jeanne.command(
        name=T("weather_name"),
        description=T("weather_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.checks.cooldown(3, 14400, key=lambda i: (i.user.id))
    @Jeanne.describe(
        city=T("weather_city_parm_desc"),
        units=T("weather_units_parm_desc"),
        three_day=T("weather_three_day_parm_desc"),
    )
    @Jeanne.rename(
        city=T("weather_city_parm_name"),
        units=T("weather_units_parm_name"),
        three_day=T("weather_three_day_parm_name"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def weather(
        self,
        ctx: Interaction,
        city: Jeanne.Range[str, 1],
        units: Optional[Literal["Metric", "Imperial"]] = None,
        three_day: Optional[bool] = False,
    ):
        if ctx.locale.value=="en-GB" or ctx.locale.value=="en-US":
            await en.Utilities(self.bot).weather(ctx, city, units, three_day)
        elif ctx.locale.value=="fr":
            await fr.Utilities(self.bot).weather(ctx, city, units, three_day)

    @weather.error
    async def weather_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value=="en-GB" or ctx.locale.value=="en-US":
                await en.Utilities(self.bot).weather_error(ctx, error, "cooldown")
            elif ctx.locale.value=="fr":
                await fr.Utilities(self.bot).weather_error(ctx, error, "cooldown")
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (KeyError, TypeError)
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Utilities(self.bot).weather_error(ctx, error, "failed")
            elif ctx.locale.value == "fr":
                await fr.Utilities(self.bot).weather_error(ctx, error, "failed")

    @Jeanne.command(
        name=T("calculator_name"),
        description=T("calculator_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.describe(calculate=T("calculator_calculate_parm_desc"))
    @Jeanne.rename(calculate=T("calculator_calculate_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def calculator(self, ctx: Interaction, calculate: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).calculator(ctx, calculate)
        elif ctx.locale.value == "fr":
            await fr.Utilities(self.bot).calculator(ctx, calculate)

    @calculator.error
    async def calculator_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, OverflowError
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Utilities(self.bot).calculator_error(ctx, error, "overflow")
            elif ctx.locale.value == "fr":
                await fr.Utilities(self.bot).calculator_error(ctx, error, "overflow")
        elif isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, Exception
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Utilities(self.bot).weather_error(ctx, error, "failed")
            elif ctx.locale.value == "fr":
                await fr.Utilities(self.bot).weather_error(ctx, error, "failed")

    @Jeanne.command(
        name=T("invite_name"),
        description=T("invite_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def invite(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).invite(ctx)
        elif ctx.locale.value == "fr":
            await fr.Utilities(self.bot).invite(ctx)

    @Jeanne.command(
        name=T("botreport_name"),
        description=T("botreport_desc"),
    )
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.describe(report_type=T("botreport_type_parm_desc"))
    @Jeanne.rename(report_type=T("botreport_type_parm_name"))
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def botreport(self, ctx: Interaction, report_type: Literal["Fault", "Bug", "ToS Violator", "Exploit", "Translation Error","Other"]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).botreport(ctx, report_type)
        elif ctx.locale.value == "fr":
            await fr.Utilities(self.bot).botreport(ctx, report_type)

    @Jeanne.command(
        name=T("dictionary_name"),
        description=T("dictionary_desc"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.describe(word=T("dictionary_word_parm_desc"))
    @Jeanne.rename(word=T("dictionary_word_parm_name"))
    async def dictionary(
        self,
        ctx: Interaction,
        word: Jeanne.Range[str, 1],
    ):
        await dictionary(ctx, word.lower())


async def setup(bot: Bot):
    await bot.add_cog(EmbedGroup(bot))
    await bot.add_cog(SlashUtilities(bot))
    await bot.add_cog(ReminderCog(bot))
