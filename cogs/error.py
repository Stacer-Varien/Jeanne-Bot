from discord import *
from discord.app_commands import *
from discord.ext.commands import Bot, Cog, Context, NotOwner


class errors(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.tree.on_error = self.on_app_command_error

    @Cog.listener()
    async def on_app_command_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, MissingPermissions):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed=embed)
        elif isinstance(error, CommandInvokeError):
            with open('cmd-invoke-errors.txt', 'a') as f:
                f.writelines(f"{ctx.user.id}-{error}\n\n")
        elif isinstance(error, BotMissingPermissions):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed=embed)
        elif isinstance(error, NoPrivateMessage):
            embed = Embed(description=error, color=Color.red())
            await ctx.followup.send(embed=embed)
        elif isinstance(error, CommandOnCooldown):
            pass

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            pass
        elif isinstance(error, NotOwner):
            pass


async def setup(bot: Bot):
    await bot.add_cog(errors(bot))
