from discord.ext.commands import Cog, Bot, Context
from discord import *
from discord.ext.commands.errors import *

class errors(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx:Context, error):
        if isinstance(error, CommandInvokeError):
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, NSFWChannelRequired):
            await ctx.send(embed=embed)
        elif isinstance(error, NotOwner):
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, MissingPermissions):
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, UserNotFound):
            embed = Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, UserInputError):
            embed = Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)

async def setup(bot:Bot):
    await bot.add_cog(errors(bot))