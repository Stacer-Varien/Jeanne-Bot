import asyncio
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from discord import Intents, AllowedMentions
from os import listdir
from config import TOKEN


class Jeanne(AutoShardedBot):
    async def setup_hook(self):
        for directory in ("events", "cogs"):
            for filename in listdir(f"./{directory}"):
                if filename.endswith(".py"):
                    await self.load_extension(f"{directory}.{filename[:-3]}")
                    print(f"Loaded: {directory}.{filename[:-3]}")
                else:
                    print(f"Skipped: {directory}.{filename}")

        await self.load_extension("jishaku")
        await self.tree.sync()


intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = Jeanne(
    command_prefix=when_mentioned_or("J!", "j!", "Jeanne", "jeanne"),
    intents=intents,
    allowed_mentions=AllowedMentions(everyone=False, users=True, roles=False),
    case_insensitive=True,
    strip_after_prefix=True,
    chunk_guilds_at_startup=False,
)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} servers and {len(bot.users)} users")
    print(f"Listening on {bot.shard_count} shards")

    for guild in bot.guilds:
        for attempt in range(3):  
            try:
                print(f"Chunking guild: {guild.name} ({guild.id})...")
                await asyncio.wait_for(guild.chunk(), timeout=60.0)
                print(f"Successfully chunked {guild.name}.")
                break
            except asyncio.TimeoutError:
                print(f"Timeout while chunking {guild.name}. Retrying...")
                await asyncio.sleep(5)  
            except Exception as e:
                print(f"An error occurred while chunking {guild.name}: {e}")
                break
        else:
            print(f"Failed to chunk {guild.name} after multiple attempts.")
        await asyncio.sleep(1)


bot.run(TOKEN)
