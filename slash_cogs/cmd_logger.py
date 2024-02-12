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
        logged = f"Date and Time = {datetime.now()}\nUser = {ctx.user} | {ctx.user.id}\nCommand used = {command.qualified_name}\n\n"
        with open("commandlog.txt", "a") as f:
            f.writelines(logged)


async def setup(bot: Bot):
    await bot.add_cog(CommandLog(bot))
