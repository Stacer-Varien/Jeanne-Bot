from json import dump
from requests import post
from functions import Botban, Currency
from config import TOPGG, TOPGG_AUTH
from topgg import DBLClient, WebhookManager
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import datetime


class TopGG(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG, autopost=True)
        self.topgg_webhook = WebhookManager(self.bot).dbl_webhook(
            route="/dblwebhook", auth_key=TOPGG_AUTH
        )
        self.topgg_webhook.run(5000)
        self.update_stats.start()

    @tasks.loop(minutes=30, reconnect=True)
    async def update_stats(self):
        try:
            print(
                f"Posted server count ({len(self.bot.guilds)}) at {datetime.now().strftime('%H:%M')}"
            )
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @update_stats.before_loop
    async def before_update_stats(self):
        print('waiting...')
        await self.bot.wait_until_ready()       

    @Cog.listener()
    async def on_dbl_vote(self, data: dict):
        if data["type"] == "upvote":
            voter = await self.bot.fetch_user(int(data["user"]))
            if Botban(voter).check_botbanned_user:
                return

            if await self.topggpy.get_weekend_status() == True:
                credits = 100
            else:
                credits = 50

            await Currency(voter).add_qp(credits)
            with open("voterdata.json", "w") as f:
                dump(data, f)


async def setup(bot: Bot):
    await bot.add_cog(TopGG(bot))
