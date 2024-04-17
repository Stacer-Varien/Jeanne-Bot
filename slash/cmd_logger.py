import csv
from typing import Union
from discord import Interaction, app_commands as Jeanne
from discord.ext.commands import Bot, Cog
from datetime import datetime


class CommandLog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_app_command_completion(
        self, ctx: Interaction, command: Union[Jeanne.Command, Jeanne.ContextMenu]
    ):
        fields = ["Date and Time", "User", "Command Used", "Command Usage"]
        command_dict = [
            {
                "Date and Time": datetime.now(),
                "User": f"{ctx.user} | {ctx.user.id}",
                "Command Used": command.qualified_name,
                "Command Usage": str(ctx.data),
            }
        ]
        with open("commandlog.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerows(command_dict)


async def setup(bot: Bot):
    await bot.add_cog(CommandLog(bot))
