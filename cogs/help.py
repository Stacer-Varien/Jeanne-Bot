from discord import (
    Interaction,
    app_commands as Jeanne,
)
from discord.ext.commands import GroupCog, Bot
from functions import AutoCompleteChoices, check_botbanned_app_command, is_suspended
import languages.en.help as en
import languages.fr.help as fr
from discord.app_commands import locale_str as T


class HelpGroup(GroupCog, name=T("help_group_name")):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(name=T("command_name"),description=T("command_desc"))
    @Jeanne.autocomplete(command=AutoCompleteChoices.command_choices)
    @Jeanne.rename(command=T("command_parm_name"))
    @Jeanne.describe(command=T("command_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def command(self, ctx: Interaction, command: Jeanne.Range[str, 3]):
        if ctx.locale.value=="en-GB" or ctx.locale.value == "en-US":
            await en.HelpGroup(self.bot).command(ctx, command)
        elif ctx.locale.value == "fr":
            await fr.HelpGroup(self.bot).command(ctx, command)

    @command.error
    async def command_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.HelpGroup(self.bot).command_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.HelpGroup(self.bot).command_error(ctx, error)

    @Jeanne.command(name=T("support_name"), description=T("support_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def support(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.HelpGroup(self.bot).support(ctx)
        elif ctx.locale.value == "fr":
            await fr.HelpGroup(self.bot).support(ctx)

async def setup(bot: Bot):
    await bot.add_cog(HelpGroup(bot))
