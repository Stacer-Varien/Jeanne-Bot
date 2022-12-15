from db_functions import add_qp, check_botbanned_user
from config import TOPGG, TOPGG_AUTH
from topgg import *
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import *

dbl_token = TOPGG

class topgg(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.topggpy = DBLClient(self.bot, dbl_token)
        self.topgg_webhook = WebhookManager(
            self.bot).dbl_webhook("/dblwebhook", TOPGG_AUTH)
        self.topgg_webhook.run(5000)
        self.update_stats.start()

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
        if data["type"] == "upvote":
            voter = await self.bot.fetch_user(data['user'])
            if check_botbanned_user(voter.id) == True:
                pass
            else:
                if await self.topggpy.get_weekend_status() is True:
                    credits = 100
                else:
                    credits = 50

                add_qp(voter.id, credits)
                print(f"Received a vote:\n{data}")

async def setup(bot:Bot):
    await bot.add_cog(topgg(bot))
