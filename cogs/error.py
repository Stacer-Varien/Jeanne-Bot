from datetime import datetime
import traceback
from discord import Color, Embed, Interaction, InteractionResponseType
from discord import app_commands as Jeanne
from discord.ext.commands import Bot, Cog
import pandas as pd
import languages.en.error as en
import languages.fr.error as fr
import languages.de.error as de
from functions import get_command_locale


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

    @staticmethod
    def _error_response_already_sent(ctx: Interaction) -> bool:
        return ctx.response.type in (
            InteractionResponseType.channel_message,
            InteractionResponseType.message_update,
        )

    @staticmethod
    async def _send_error(ctx: Interaction, embed: Embed) -> None:
        if ctx.response.is_done():
            await ctx.followup.send(embed=embed)
        else:
            await ctx.response.send_message(embed=embed)

    @Cog.listener()
    async def on_app_command_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        try:
            existing_file = "errors.xlsx"
            error_traceback = "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
            command_name = ctx.command.qualified_name if ctx.command else "unknown"
            df_new = pd.DataFrame(
                {
                    "Date": [f"{datetime.now()}"],
                    "Command": [command_name],
                    "Error": [error_traceback],
                }
            )
            df_existing = pd.read_excel(existing_file)
            pd.concat([df_existing, df_new], ignore_index=True).to_excel(
                existing_file, index=False
            )
        except Exception as logging_error:
            print(f"Unable to write command error log: {logging_error}")

        # Command-specific handlers run before this global handler.
        if self._error_response_already_sent(ctx):
            return

        if isinstance(error, Jeanne.MissingPermissions):
            if get_command_locale(ctx) not in ("fr", "de"):
                await en.Errors.handle_missing_permissions(self, ctx, error)
                return
            if get_command_locale(ctx) == "fr":
                await fr.Errors.handle_missing_permissions(self, ctx, error)
                return
            if get_command_locale(ctx) == "de":
                await de.Errors.handle_missing_permissions(self, ctx, error)
                return
            return
        if isinstance(error, Jeanne.BotMissingPermissions):
            if get_command_locale(ctx) not in ("fr", "de"):
                await en.Errors.handle_bot_missing_permissions(self, ctx, error)
                return
            if get_command_locale(ctx) == "fr":
                await fr.Errors.handle_bot_missing_permissions(self, ctx, error)
                return
            if get_command_locale(ctx) == "de":
                await de.Errors.handle_bot_missing_permissions(self, ctx, error)
                return
            return
        if isinstance(error, Jeanne.NoPrivateMessage):
            embed = Embed(description=str(error), color=Color.red())
            await self._send_error(ctx, embed)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, RuntimeError
        ):
            if ctx.command.qualified_name == "help command":
                return
            embed = Embed(description=str(error), color=Color.red())
            await self._send_error(ctx, embed)
            return
        if isinstance(error, Jeanne.CommandOnCooldown):
            retry_after = round(error.retry_after, 2)
            messages = {
                "fr": f"Cette commande est en cooldown. Réessayez dans `{retry_after}` secondes.",
                "de": f"Dieser Befehl hat eine Abklingzeit. Versuche es in `{retry_after}` Sekunden erneut.",
            }
            embed = Embed(
                description=messages.get(
                    get_command_locale(ctx),
                    f"This command is on cooldown. Try again in `{retry_after}` seconds.",
                ),
                color=Color.red(),
            )
            await self._send_error(ctx, embed)


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
