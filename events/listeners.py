import json
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from discord import AllowedMentions, DMChannel, Embed, Message, TextChannel
from discord.ext.commands import Bot, Cog
from functions import BetaTest, DevPunishment, Levelling
from asyncio import Lock, sleep
from pathlib import Path

# Path to the cooldowns JSON file
COOLDOWNS_FILE = Path("lvlcooldowns.json")

# In-memory cache for cooldowns
cooldowns = defaultdict(lambda: {"global": {"next_time": datetime.min}, "servers": {}})

# Load cooldowns from the JSON file
def load_cooldowns():
    if COOLDOWNS_FILE.exists():
        with open(COOLDOWNS_FILE, "r") as file:
            data = json.load(file)
            for user_id, user_data in data.items():
                cooldowns[int(user_id)] = {
                    "global": {
                        "next_time": datetime.fromisoformat(user_data["global"]["next_time"])
                    },
                    "servers": {
                        int(server_id): {
                            "next_time": datetime.fromisoformat(server_data["next_time"])
                        }
                        for server_id, server_data in user_data["servers"].items()
                    },
                }

# Save cooldowns to the JSON file
def save_cooldowns():
    with open(COOLDOWNS_FILE, "w") as file:
        json.dump(
            {
                user_id: {
                    "global": {"next_time": data["global"]["next_time"].isoformat()},
                    "servers": {
                        server_id: {"next_time": server_data["next_time"].isoformat()}
                        for server_id, server_data in data["servers"].items()
                    },
                }
                for user_id, data in cooldowns.items()
            },
            file,
            indent=4,
        )


load_cooldowns()

class listenersCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot or isinstance(message.channel, DMChannel):
            return

        if DevPunishment(message.author).check_botbanned_user:
            return

        user_id = message.author.id
        server_id = message.guild.id
        now_time = datetime.now()


        if user_id not in cooldowns:
            cooldowns[user_id] = {
                "global": {"next_time": datetime.min},
                "servers": {},
            }

        user_cooldowns = cooldowns[user_id]


        if server_id not in user_cooldowns["servers"]:
            user_cooldowns["servers"][server_id] = {"next_time": datetime.min}


        if now_time >= user_cooldowns["global"]["next_time"]:
            if now_time >= user_cooldowns["servers"][server_id]["next_time"]:
                try:
                    level_instance = Levelling(message.author, message.guild)
                    if level_instance.check_xpblacklist_channel(message.channel) is None:
                        weekend_check = now_time.isoweekday() >= 6
                        xp = 15 if weekend_check else 10
                        await level_instance.add_xp(xp)
                        user_cooldowns["global"]["next_time"] = now_time + timedelta(minutes=2)
                        user_cooldowns["servers"][server_id]["next_time"] = now_time + timedelta(minutes=2)

                        save_cooldowns()
                except Exception as e:
                    print(f"Error in on_message: {e}")

    async def send_level_message(
        self, channel: Optional[TextChannel], content: str, embed: Optional[Embed]
    ):
        if channel is not None:
            await channel.send(content=content, embed=embed)


async def cleanup_cooldowns():
    while True:
        now_time = datetime.now()
        expired_users = []

        for user_id, data in list(cooldowns.items()):
            if now_time >= data["global"]["next_time"]:
                data["global"]["next_time"] = datetime.min

            expired_servers = [
                server_id
                for server_id, server_data in data["servers"].items()
                if now_time >= server_data["next_time"]
            ]
            for server_id in expired_servers:
                del data["servers"][server_id]

            if data["global"]["next_time"] == datetime.min and not data["servers"]:
                expired_users.append(user_id)

        for user_id in expired_users:
            del cooldowns[user_id]

        save_cooldowns()

        await sleep(120)


async def setup(bot: Bot):
    await bot.add_cog(listenersCog(bot))
    bot.loop.create_task(cleanup_cooldowns())
