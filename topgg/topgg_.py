from db_functions import add_voter
from config import TOPGG
from topgg import TopGGClient
from nextcord.ext.commands import Cog, Bot
from nextcord.ext import tasks
from datetime import *
from nextcord import *


class topgg(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topgg = TopGGClient(TOPGG, 831993597166747679)
        self.update_guild_count.start()
        self.check_votes.start()

    @tasks.loop(minutes=30, reconnect=True)
    async def update_guild_count(self):
        try:
            self.topgg.post_server_count(len(self.bot.guilds))
            print("{} servers on {}".format(
                len(self.bot.guilds), datetime.now()))
            
        except Exception as e:
            print(e)

    @tasks.loop(seconds=10, reconnect=True)
    async def check_votes(self):
        voters=self.topgg.fetch_bot_votes()
        for a in voters:
            add_voter(a['id'])
        

def setup(bot: Bot):
    bot.add_cog(topgg(bot))
