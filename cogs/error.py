import csv
from datetime import datetime
from io import BytesIO
from discord import Color, Embed, File, Interaction
from discord import app_commands as Jeanne
from discord.ext.commands import Bot, Cog
import traceback


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
        if isinstance(error, Jeanne.MissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.response.send_message(embed=embed)
        elif isinstance(error, Jeanne.BotMissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.response.send_message(embed=embed)
        elif isinstance(error, Jeanne.NoPrivateMessage):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.response.send_message(embed=embed)
        elif isinstance(error, Jeanne.CommandInvokeError) and isinstance(error.original, RuntimeError):
            if ctx.command.qualified_name=="help command":
                return
            embed = Embed(description=str(error), color=Color.red())
            await ctx.response.send_message(embed=embed)
        elif isinstance(error, Jeanne.CommandOnCooldown):
            pass


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
