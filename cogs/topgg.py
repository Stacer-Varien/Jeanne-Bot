from config import TOPGG, db
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
        self.topgg_webhook = WebhookManager(self.bot).dbl_webhook("/dblwebhook", 'password')
        self.topgg_webhook.run(5000)

    @tasks.loop(minutes=30)
    async def update_stats(self):
        try:
            await self.topggpy.post_guild_count()
            print(
                f"Posted server count ({self.topggpy.guild_count}) at {datetime.now().strftime('%H:%M')}")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @Cog.listener()
    async def on_dbl_vote(self, data):        
        if data["type"] == "test":
            return self.bot.dispatch("dbl_test", data)

        print(f"Received a vote:\n{data}")

    @Cog.listener()
    async def on_dbl_test(data):
        print(f"Received a test vote:\n{data}")


def setup(bot):
    bot.add_cog(topgg(bot))
