from discord import app_commands as Jeanne
from functions import BetaTest, Botban, Currency
from config import DB_AUTH, TOPGG, TOPGG_AUTH, DBL_AUTH
from topgg import DBLClient, WebhookManager
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import datetime
import aiohttp


class DBL(Cog):
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
        self.check_dbl_votes.start()

    async def post_cmds(self):
        cmds = [
            cmd
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Jeanne.Group) and not cmd.nsfw
        ]
        dictionary = [
            {"name": cmd.qualified_name, "description": cmd.description, "type": 1}
            for cmd in cmds
        ]
        headers = {"Content-Type": "application/json", "Authorization": DBL_AUTH}
        async with aiohttp.ClientSession(headers=headers) as session:
            await session.post(
                "https://discordbotlist.com/api/v1/bots/831993597166747679/commands",
                json=dictionary,
            )

    @tasks.loop(minutes=30, reconnect=True)
    async def update_stats(self):
        try:
            dblheaders = {
                "Content-Type": "application/json",
                "Authorization": DBL_AUTH,
            }

            dbheaders = {
                "Content-Type": "application/json",
                "Authorization": DB_AUTH,
            }

            servers = len(self.bot.guilds)
            async with aiohttp.ClientSession(headers=dblheaders) as session:
                await session.post(
                    "https://discordbotlist.com/api/v1/bots/831993597166747679/stats",
                    json={"guilds": servers, "users": len(self.bot.users)},
                )

            async with aiohttp.ClientSession(headers=dbheaders) as session:
                await session.post(
                    " https://discord.bots.gg/api/v1/bots/831993597166747679/stats",
                    json={"guildCount": servers},
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
        await self.post_cmds()
        await self.bot.wait_until_ready()

    @Cog.listener()
    async def on_dbl_vote(self, data: dict):
        if data["type"] == "test":
            voter_id = int(data["user"])
            voter = await self.bot.fetch_user(voter_id)
            if Botban(voter).check_botbanned_user:
                return
            credits = 100 if await self.topggpy.get_weekend_status() else 50
            if await BetaTest(self.bot).check(voter):
                credits = round(credits * 1.25)
            await Currency(voter).add_qp(credits)
            with open("voterdata.txt", "a") as f:
                f.writelines(f"{data}\n")

    @tasks.loop(minutes=1, reconnect=True)
    async def check_dbl_votes(self):
        dblheaders = {
            "Content-Type": "application/json",
            "Authorization": DBL_AUTH,
        }
        async with aiohttp.ClientSession(headers=dblheaders) as session:
            r=await session.get("https://discordbotlist.com/api/v1/bots/831993597166747679/upvotes")
        print(await r.json())


async def setup(bot: Bot):
    await bot.add_cog(DBL(bot))
