from config import TOPGG, db, TOPGG_AUTH
from topgg import DBLClient, WebhookManager
from nextcord.ext import tasks
from nextcord.ext.commands import Cog
from datetime import *

dbl_token = TOPGG


class topgg(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()
        self.topggpy = DBLClient(self.bot, dbl_token)
        self.topgg_webhook = WebhookManager(self.bot).dbl_webhook("/dblwebhook", TOPGG_AUTH)

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.topggpy.post_guild_count()
            print(
                f"Posted server count ({self.topggpy.guild_count}) at {datetime.now().strftime('%H:%M')}")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @Cog.listener()
    async def on_dbl_vote(self, data):
        voter = await self.bot.fetch_user(data['user'])
        cur = db.execute(
            "INSERT OR IGNORE INTO bankData (user_id, amount) VALUES (?,?)", (voter.id, 50))

        if cur.rowcount == 0:
            db.execute(
                f"UPDATE bankData SET amount = amount + 100 WHERE user_id = {voter.id}")
            db.commit()
            print(f"Received a vote:\n{data}")


def setup(bot):
    bot.add_cog(topgg(bot))
