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
        self.topgg_webhook = WebhookManager(self.bot).dbl_webhook("/dblwebhook", "webhook")
        self.topgg_webhook.run(5000)

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.topggpy.post_guild_count()
            print(f"Posted server count ({self.topggpy.guild_count}) at {datetime.now().strftime('%H:%M')}")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @Cog.listener()
    async def on_dbl_vote(self, data):
        if data["type"] == "upvote":
            try:
                voter = await self.bot.fetch_user(data['user'])
                cur=db.execute(f"SELECT * in bankData WHERE user_id = {voter.id}")
                user=cur.fetchone()[0]
                if voter.id == user:
                    db.execute(
                        f"UPDATE bankData SET amount = amount + 25 WHERE user_id = {voter.id}")
                    db.commit()
            except:
                pass
        print(f"Received a vote:\n{data}")


def setup(bot):
    bot.add_cog(topgg(bot))