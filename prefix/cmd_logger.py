from discord.ext.commands import Bot, Cog, Context
from datetime import datetime


class CommandLog(Cog, name="cmdlogger"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        logged = f"Date and Time = {datetime.now()}\nUser = {ctx.author} | {ctx.author.id}\nCommand used = {ctx.command.qualified_name}\n\n"
        with open("commandlog.txt", "a") as f:
            f.writelines(logged)


async def setup(bot: Bot):
    await bot.add_cog(CommandLog(bot))
