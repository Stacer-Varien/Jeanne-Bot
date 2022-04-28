from config import TOPGG
from topgg import *
from nextcord.ext import tasks
from nextcord.ext.commands import Cog
from datetime import *

dbl_token = TOPGG


class topgg(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()
        self.topggpy = DBLClient(self.bot, dbl_token)

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.topggpy.post_guild_count()
            print(f"Posted server count ({self.topggpy.guild_count}) at {datetime.now().strftime('%H:%M')}")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

def setup(bot):
    bot.add_cog(topgg(bot))