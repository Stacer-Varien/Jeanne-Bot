from nextcord import *
from nextcord.ext.commands import Cog
from nextcord.ext.application_checks.errors import *
from assets.errormsgs import *
from nextcord.ext.commands.errors import CommandNotFound
from cooldowns import *


class errormsgs(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_application_command_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationNSFWChannelRequired):
            await ctx.response.defer()
            await ctx.followup.send(embed=no_hentai)

        elif isinstance(error, ApplicationNotOwner):
            await ctx.response.defer()
            await ctx.followup.send(embed=owner_only)

def setup(bot):
    bot.add_cog(errormsgs(bot))
