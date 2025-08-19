from datetime import datetime
import traceback
from discord import Color, Embed, Interaction
from discord import app_commands as Jeanne
from discord.ext.commands import Bot, Cog
import pandas as pd
import languages.en.error as en
import languages.fr.error as fr
import languages.de.error as de


class ErrorsCog(Cog, name="ErrorsSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    @Cog.listener()
    async def on_app_command_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        existing_file = "errors.xlsx"
        error_traceback = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        new_data = {
            "Date": [f"{datetime.now()}"],
            "Command": [f"{ctx.command.qualified_name}"],
            "Error": [{f"{error_traceback}"}],
        }
        df_new = pd.DataFrame(new_data)
        df_existing = pd.read_excel(existing_file)
        df_combined = df_existing._append(df_new, ignore_index=True)
        df_combined.to_excel(existing_file, index=False)

        if isinstance(error, Jeanne.MissingPermissions):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Errors.handle_missing_permissions(self, ctx, error)
                return
            if ctx.locale.value == "fr":
                await fr.Errors.handle_missing_permissions(self, ctx, error)
                return
            if ctx.locale.value == "de":
                await de.Errors.handle_missing_permissions(self, ctx, error)
                return
            return
        if isinstance(error, Jeanne.BotMissingPermissions):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Errors.handle_bot_missing_permissions(self, ctx, error)
                return
            if ctx.locale.value == "fr":
                await fr.Errors.handle_bot_missing_permissions(self, ctx, error)
                return
            if ctx.locale.value == "de":
                await de.Errors.handle_bot_missing_permissions(self, ctx, error)
                return
            return
        if isinstance(error, Jeanne.NoPrivateMessage):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.response.send_message(embed=embed)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, RuntimeError
        ):
            if ctx.command.qualified_name == "help command":
                return
            embed = Embed(description=str(error), color=Color.red())
            await ctx.response.send_message(embed=embed)
            return
        if isinstance(error, Jeanne.CommandOnCooldown):
            pass


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
