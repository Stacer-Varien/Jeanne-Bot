from datetime import datetime
from io import BytesIO
from discord import Color, Embed, File
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
            channel = await self.bot.fetch_channel(1257420940128550942)
            error_message=f"""
```
Command: {ctx.command.qualified_name}
Date and Time: {datetime.now().strftime("%d/%m%Y %H:%M")}
Error:
{"".join(traceback_error)}
```
"""
            if len(error_message)>2000:
                file = BytesIO(error_message.encode("utf-8"))
                file = File(fp=file, filename="prefix_error.txt")

                await channel.send(file=file)
            else:
                await channel.send(error_message)
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
