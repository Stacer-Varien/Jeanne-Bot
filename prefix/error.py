from datetime import datetime
from discord import Color, Embed
from discord.ext import commands as Jeanne
from discord.ext.commands import Bot, Cog, Context, NotOwner, CommandNotFound
import traceback
import csv


class ErrorsCog(Cog, name="ErrorsPrefix"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.MissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, Jeanne.BotMissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, Jeanne.errors.CommandInvokeError):
            traceback_error = traceback.format_exception(
                error, error, error.__traceback__
            )
            fields = ["Date", "Command", "Error"]
            with open("errors.csv", "a", newline="") as f:
                traceback_dict = {
                    "Date": datetime.now(),
                    "Command": ctx.command.qualified_name,
                    "Error": "".join(traceback_error),
                }
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writerow(traceback_dict)
        elif isinstance(error, Jeanne.errors.NoPrivateMessage):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, Jeanne.CommandOnCooldown):
            pass
        elif isinstance(error, CommandNotFound):
            pass
        elif isinstance(error, NotOwner):
            pass


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
