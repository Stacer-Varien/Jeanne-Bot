import asyncio
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from discord import Intents, AllowedMentions
from os import listdir
from config import TOKEN


class Jeanne(AutoShardedBot):
    async def setup_hook(self):
        dirs = ["./events", "./cogs"]
        for i in dirs:
            for filename in listdir(i):
                if filename.endswith(".py"):
                    await self.load_extension(f"{i[2:]}.{filename[:-3]}")
                    print(f"{i}.{filename} loaded")
                else:
                    print(f"Unable to load {i}.{filename[:-3]}")

        await self.load_extension("jishaku")
        await self.tree.sync()


intents = Intents.all()
intents.presences = False
intents.voice_states = False
intents.auto_moderation = False

bot = Jeanne(
    command_prefix=when_mentioned_or("J!", "j!", "Jeanne", "jeanne"), intents=intents,shard_connect_timeout=60
)
bot.allowed_mentions = AllowedMentions.all()
bot.case_insensitive = True
bot.strip_after_prefix = True
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))
    print("Connected to {} servers".format(len(bot.guilds)))
    print("Listening to {} users".format(len(bot.users)))
    print("Listening to {} shards".format(bot.shard_count))



@bot.event
async def on_shard_connect(shard_id):
    while bot.is_ws_ratelimited():
        print(f"Shard {shard_id} is rate-limited. Retrying in 60 seconds...")
        await asyncio.sleep(60)
    print(f"Shard {shard_id} connected successfully.")


@bot.event
async def on_shard_resumed(shard_id):
    print(f"Shard {shard_id} resumed!")


@bot.event
async def on_shard_disconnect(shard_id):
    if bot.is_ws_ratelimited():
        print(f"Shard {shard_id} is rate-limited, delaying reconnection...")
        await asyncio.sleep(60)  # Wait for 60 seconds before reconnecting
    else:
        print(f"Shard {shard_id} disconnected!")


bot.run(TOKEN)
