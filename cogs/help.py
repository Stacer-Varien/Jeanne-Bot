from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.ui import *
from config import db
from assets.needed import test_server
from assets.help_menu.help import *


class slashhelp(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Get help from the wiki or join the support server for further help")
    async def help(self, ctx : Interaction, help_module=SlashOption(choices=['Fun', 'Hentai', 'Image', 'Info', 'Level', 'Management', 'Misc', 'Moderation', 'Owner', 'Reaction', 'Utilities', 'Welcomer'], required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            if help_module==None:
                help=Embed(description="Click on the drop menu below for more help on the dropmenu")
                await ctx.followup.send(embed=help, view=helpview())

def setup(bot):
    bot.add_cog(slashhelp(bot))
