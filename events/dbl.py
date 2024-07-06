import aiohttp
from functions import BetaTest, Botban, Currency, Levelling
from config import DB_AUTH, TOPGG, TOPGG_AUTH
from topgg import DBLClient, WebhookManager
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import datetime


class DBL(Cog, name="DBL"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(
            bot=self.bot, token=TOPGG, autopost=True, post_shard_count=True
        )
        self.topgg_webhook = WebhookManager(self.bot).dbl_webhook(
            route="/dblwebhook", auth_key=TOPGG_AUTH
        )
        self.topgg_webhook.run(5000)
        self.update_stats.start()

    @tasks.loop(minutes=30, reconnect=True)
    async def update_stats(self):
        try:
            servers = len(self.bot.guilds)
            dbheaders = {
                "Content-Type": "application/json",
                "Authorization": DB_AUTH,
            }
            async with aiohttp.ClientSession(headers=dbheaders) as session:
                await session.post(
                    " https://discord.bots.gg/api/v1/bots/831993597166747679/stats",
                    json={"guildCount": servers, "shardCount": self.bot.shard_count},
                )

            await self.topggpy.post_guild_count(
                guild_count=servers, shard_count=self.bot.shard_count
            )
            print(
                f"Posted server count ({servers}) at {datetime.now().strftime('%H:%M')}"
            )
            print(
                f"Posted shard count ({self.bot.shard_count}) at {datetime.now().strftime('%H:%M')}"
            )
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    @update_stats.before_loop
    async def before_update_stats(self):
        await self.bot.wait_until_ready()

    @Cog.listener()
    async def on_dbl_vote(self, data: dict):
        if data["type"] == "upvote":
            voter_id = int(data["user"])
            voter = await self.bot.fetch_user(voter_id)
            if Botban(voter).check_botbanned_user:
                return
            credits = 100 if await self.topggpy.get_weekend_status() else 50
            xp = (
                (10 * Levelling(voter).get_user_level)
                if await self.topggpy.get_weekend_status()
                else (5 * Levelling(voter).get_user_level)
            )
            if await BetaTest(self.bot).check(voter):
                credits = round(credits * 1.25)
                await Levelling(voter).add_xp((5 * round(xp / 5)))
            await Currency(voter).add_qp(credits)
            await Levelling(voter).add_xp(xp)


async def setup(bot: Bot):
    await bot.add_cog(DBL(bot))
