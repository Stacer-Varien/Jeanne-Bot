from json import dumps, loads
from functions import Botban, Currency
from config import TOPGG, TOPGG_AUTH
from topgg import DBLClient, WebhookManager
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import datetime


class topgg(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(self.bot, TOPGG)
        self.topgg_webhook = WebhookManager(self.bot).dbl_webhook(
            "/dblwebhook", TOPGG_AUTH
        )
        self.topgg_webhook.run(5000)
        self.update_stats.start()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        try:
            print(
                f"Posted server count ({self.topggpy.guild_count}) at {datetime.now().strftime('%H:%M')}"
            )
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @Cog.listener()
    async def on_dbl_vote(self, data: dict):
        if data["type"] == "upvote":
            voter = await self.bot.fetch_user(data["user"])
            if Botban(voter).check_botbanned_user() == True:
                return

            if await self.topggpy.get_weekend_status() == True:
                credits = 100
            else:
                credits = 50

            Currency().add_qp(credits)
            print(f"Received a vote:\n{data}")
            with open("voter_data.json", "r") as f:
                json_dict = "".join(f.readlines())
            dict = loads(json_dict)

            data.update(dict)
            dumps(data)


async def setup(bot: Bot):
    await bot.add_cog(topgg(bot))
