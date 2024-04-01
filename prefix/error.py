from datetime import datetime
from discord import Color, Embed
from discord.ext import commands as Jeanne
from discord.ext.commands import Bot, Cog, Context, NotOwner, CommandNotFound
import traceback


class ErrorsCog(Cog, name="Errors"):
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
            with open("errors.txt", "a") as f:
                f.writelines(
                    f"Date = {datetime.now()}\nComamnd = {ctx.command.qualified_name}\nError:\n{''.join(traceback_error)}\n"
                )
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
