from discord import (
    Forbidden, HTTPException, Interaction,
    NotFound, TextChannel, app_commands as Jeanne
)
from discord.ext.commands import Cog, Bot, GroupCog
from assets.dictionary import dictionary
from functions import (
    check_botbanned_app_command, check_disabled_app_command, is_suspended, AutoCompleteChoices
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
        extras={
            "en": {
                "name": "generate",
                "description": "Generates an embed message. Use [Discohook](https://discohook.app) for JSON generation.",
                "member_perms": "Administrator",
                "parameters": [
                    {
                        "name": "channel",
                        "description": "Which channel?",
                        "required": True,
                    },
                    {
                        "name": "jsonscript",
                        "description": "Insert JSON script",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "générer",
                "description": "Génère un message embed. Utilisez [Discohook](https://discohook.app) pour générer le JSON.",
                "member_perms": "Administrateur",
                "parameters": [
                    {
                        "name": "canal",
                        "description": "Quel canal ?",
                        "required": True,
                    },
                    {
                        "name": "jsonscript",
                        "description": "Insérer un script JSON",
                        "required": True,
                    },
                ],
            },
        },
    )
    @Jeanne.checks.has_permissions(administrator=True)
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.describe(
        channel=T("channel_parm_desc"),
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
        extras={
            "en": {
                "name": "edit",
                "description": "Edits an embed message. Use [Discohook](https://discohook.app) for JSON generation.",
                "member_perms": "Administrator",
                "parameters": [
                    {
                        "name": "channel",
                        "description": "Which channel?",
                        "required": True,
                    },
                    {
                        "name": "messageid",
                        "description": "Message ID of the embed",
                        "required": True,
                    },
                    {
                        "name": "jsonscript",
                        "description": "Insert JSON script",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "éditer",
                "description": "Édite un message embed. Utilisez [Discohook](https://discohook.app) pour générer le JSON.",
                "member_perms": "Administrateur",
                "parameters": [
                    {
                        "name": "canal",
                        "description": "Quel canal ?",
                        "required": True,
                    },
                    {
                        "name": "idmessage",
                        "description": "ID du message de l'embed",
                        "required": True,
                    },
                    {
                        "name": "jsonscript",
                        "description": "Insérer un script JSON",
                        "required": True,
                    },
                ],
            },
        },
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
        channel=T("channel_parm_name"),
        messageid=T("message_id_parm_name"),
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


class ReminderCog(GroupCog, name=T("reminder")):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("reminder_add_name"),
        description=T("reminder_add_desc"),
        extras={
            "en": {
                "name": "add",
                "description": "Add a reminder",
                "parameters": [
                    {
                        "name": "reason",
                        "description": "Reason for the reminder",
                        "required": True,
                    },
                    {
                        "name": "time",
                        "description": "Time (e.g., 1h, 30m)",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "ajouter",
                "description": "Ajouter un rappel",
                "parameters": [
                    {
                        "name": "raison",
                        "description": "Raison du rappel",
                        "required": True,
                    },
                    {
                        "name": "temps",
                        "description": "Temps (ex : 1h, 30m)",
                        "required": True,
                    },
                ],
            },
        },
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
        extras={
            "en": {
                "name": "list",
                "description": "List all the reminders you have",
            },
            "fr": {
                "name": "liste",
                "description": "Liste tous les rappels que vous avez",
            },
        },
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
        extras={
            "en": {
                "name": "cancel",
                "description": "Cancel a reminder",
                "parameters": [
                    {
                        "name": "reminderid",
                        "description": "Reminder ID",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "annuler",
                "description": "Annuler un rappel",
                "parameters": [
                    {
                        "name": "idrappel",
                        "description": "ID du rappel",
                        "required": True,
                    }
                ],
            },
        },
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
        extras={
            "en": {
                "name": "weather",
                "description": "Get weather information on a city",
                "parameters": [
                    {
                        "name": "city",
                        "description": "Add a city",
                        "required": True,
                    },
                    {
                        "name": "units",
                        "description": "Metric or Imperial? (Default is metric)",
                        "required": False,
                    },
                    {
                        "name": "three_day",
                        "description": "Show 3 day forecast?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "météo",
                "description": "Obtenez des informations météorologiques sur une ville",
                "parameters": [
                    {
                        "name": "ville",
                        "description": "Ajouter une ville",
                        "required": True,
                    },
                    {
                        "name": "unités",
                        "description": "Métrique ou Impérial ? (Par défaut : métrique)",
                        "required": False,
                    },
                    {
                        "name": "trois_jours",
                        "description": "Afficher les prévisions sur 3 jours ?",
                        "required": False,
                    },
                ],
            }
        },
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).weather(ctx, city, units, three_day)
        elif ctx.locale.value == "fr":
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
        extras={
            "en": {
                "name": "calculator",
                "description": "Do a calculation",
                "parameters": [
                    {
                        "name": "calculation",
                        "description": "Add a calculation",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "calculatrice",
                "description": "Effectuer un calcul",
                "parameters": [
                    {
                        "name": "calcul",
                        "description": "Ajouter un calcul",
                        "required": True,
                    },
                ],
            },
        },
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
        extras={
            "en": {
                "name": "invite",
                "description": "Invite me to your server or join the support server",
            },
            "fr": {
                "name": "inviter",
                "description": "Invitez-moi sur votre serveur ou rejoignez le serveur de support",
            },
        },
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
        extras={
            "en": {
                "name": "botreport",
                "description": "Submit a bot report if you found something wrong",
            },
            "fr": {
                "name": "rapportbot",
                "description": "Soumettez un rapport sur le bot si vous avez trouvé un problème",
            },
        },
    )
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.describe(report_type=T("botreport_type_parm_desc"))
    @Jeanne.rename(report_type=T("botreport_type_parm_name"))
    @Jeanne.autocomplete(report_type=AutoCompleteChoices.report_types)
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def botreport(self, ctx: Interaction, report_type:str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).botreport(ctx, report_type)
        elif ctx.locale.value == "fr":
            await fr.Utilities(self.bot).botreport(ctx, report_type)

    @Jeanne.command(
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

    @Jeanne.command(
        name=T("confess_name"),
        description=T("confess_desc"),
        extras={
            "en": {
                "name": "confess",
                "description": "Confess something anonymously or not",
                "parameters": [
                    {
                        "name": "confession",
                        "description": "What do you want to confess?",
                        "required": True,
                    },
                    {
                        "name": "anonymous",
                        "description": "Do you want to confess anonymously?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "confesser",
                "description": "Confessez quelque chose de manière anonyme ou non",
                "parameters": [
                    {
                        "name": "confession",
                        "description": "Que voulez-vous confesser ?",
                        "required": True,
                    },
                    {
                        "name": "anonyme",
                        "description": "Voulez-vous confesser anonymement ?",
                        "required": False,
                    },
                ],
            },
        },
    )
    @Jeanne.describe(confession=T("confession_parm_desc"), anonymous=T("anonymous_parm_desc"))
    @Jeanne.rename(confession=T("confession_parm_name"), anonymous=T("anonymous_parm_name"))
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def confess(self, ctx:Interaction, confession: Jeanne.Range[str, 1, 4096], anonymous: Optional[bool] = False):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).confession(ctx, confession, anonymous)
        elif ctx.locale.value == "fr":
            await fr.Utilities(self.bot).confession(ctx, confession, anonymous)

    @Jeanne.command(
        name=T("reportconfession_name"),
        description=T("reportconfession_desc"),
        extras={
            "en": {
                "name": "report-confession",
                "description": "Report a confession",
                "parameters": [
                    {
                        "name": "confession_id",
                        "description": "ID of the confession to report",
                        "required": True,
                    },
                    {
                        "name": "reason",
                        "description": "Reason for reporting the confession",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "rapport-confession",
                "description": "Signaler une confession",
                "parameters": [
                    {
                        "name": "id_confession",
                        "description": "ID de la confession à signaler",
                        "required": True,
                    },
                    {
                        "name": "raison",
                        "description": "Raison du signalement de la confession",
                        "required": True,
                    },
                ],
            },
        },
    )
    @Jeanne.describe(
        confession_id=T("reportconfession_id_parm_desc"),
        reason=T("reportconfession_rsn_parm_desc"),
    )
    @Jeanne.rename(
        confession_id=T("reportconfession_id_parm_name"), reason=T("reason_param_name")
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.autocomplete(confession_id=AutoCompleteChoices.confessions)
    async def reportconfession(self, ctx: Interaction, confession_id: int, reason: Jeanne.Range[str, 1, 512]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Utilities(self.bot).reportconfession(ctx, confession_id, reason)
        elif ctx.locale.value == "fr":
            await fr.Utilities(self.bot).reportconfession(
                ctx, confession_id, reason
            )

async def setup(bot: Bot):
    await bot.add_cog(EmbedGroup(bot))
    await bot.add_cog(SlashUtilities(bot))
    await bot.add_cog(ReminderCog(bot))
