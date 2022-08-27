from nextcord.ext.commands import Cog
from nextcord import *
from nextcord.ext.application_checks import ApplicationNSFWChannelRequired, ApplicationMissingPermissions, ApplicationNotOwner, ApplicationBotMissingPermissions
from nextcord.ext.commands.errors import UserNotFound

class errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_application_command_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationInvokeError):
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, ApplicationNSFWChannelRequired):
            await ctx.response.defer()
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, ApplicationNotOwner):
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, ApplicationMissingPermissions):
            embed=Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)

        elif isinstance(error, ApplicationBotMissingPermissions):
            embed = Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)

        elif isinstance(error, UserNotFound):
            embed = Embed(description=error, color=Color.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(errors(bot))