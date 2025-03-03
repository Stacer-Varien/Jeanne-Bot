from typing import Union
from discord import Interaction, app_commands as Jeanne
from discord.ext.commands import Bot, Cog
from datetime import datetime
import pandas as pd


class CommandLog(Cog, name="CommandLogSlash"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_app_command_completion(
        self, ctx: Interaction, command: Union[Jeanne.Command, Jeanne.ContextMenu]
    ):
        fields = ["Date and Time", "User", "Command Used", "Command Usage"]
        command_dict = {
            "Date and Time": datetime.now(),
            "User": f"{ctx.user} | {ctx.user.id}",
            "Command Used": command.qualified_name,
            "Command Usage": str(ctx.data),
        }

        existing_file = "commands.xlsx"
        new_data = {
            "Date and Time": [str(datetime.now())],
            "Username": [ctx.user],
            "User ID": [str(ctx.user.id)],
            "Command Used": [command.qualified_name],
            "Command Usage": [str(ctx.data)],
        }
        df_new = pd.DataFrame(new_data)
        df_existing = pd.read_excel(existing_file)
        df_combined = df_existing._append(df_new, ignore_index=True)
        df_combined.to_excel(existing_file, index=False)


async def setup(bot: Bot):
    await bot.add_cog(CommandLog(bot))
