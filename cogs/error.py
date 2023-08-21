from datetime import datetime
from discord import Color, Embed, Interaction
from discord import app_commands as Jeanne
from discord.ext.commands import Bot, Cog, Context, NotOwner, CommandNotFound
import traceback


class ErrorsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.tree.on_error=self.on_app_command_error

    @Cog.listener()
    async def on_app_command_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):

        if isinstance(error, Jeanne.errors.MissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.followup.send(embed=embed)
        elif isinstance(error, Jeanne.errors.CommandInvokeError):
            traceback_error = traceback.format_exception(
                error, error, error.__traceback__
            )
            with open("errors.txt", "a") as f:
                f.writelines(f"{datetime.now()} --- {''.join(traceback_error)}")
        elif isinstance(error, Jeanne.errors.BotMissingPermissions):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.followup.send(embed=embed)
        elif isinstance(error, Jeanne.errors.NoPrivateMessage):
            embed = Embed(description=str(error), color=Color.red())
            await ctx.followup.send(embed=embed)
        elif isinstance(error, Jeanne.errors.CommandOnCooldown):
            pass

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            return
        if isinstance(error, NotOwner):
            return


async def setup(bot: Bot):
    await bot.add_cog(ErrorsCog(bot))
