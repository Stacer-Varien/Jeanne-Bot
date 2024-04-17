from discord.ext.commands import Bot, Cog, Context
from datetime import datetime
import csv


class CommandLog(Cog, name="cmdlogger"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        fields = ["Date and Time", "User", "Command Used", "Command Usage"]
        with open("commandlog.csv", "a", newline="") as f:
            command_dict = {
                "Date and Time": datetime.now(),
                "User": f"{ctx.author} | {ctx.author.id}",
                "Command Used": ctx.command.qualified_name,
                "Command Usage": ctx.message.content,
            }

            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(command_dict)


async def setup(bot: Bot):
    await bot.add_cog(CommandLog(bot))
