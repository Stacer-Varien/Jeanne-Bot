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
    command_prefix=when_mentioned_or("J!", "j!", "Jeanne", "jeanne"),
    intents=intents,
    allowed_mentions=AllowedMentions.all(),
    case_insensitive=True,
    strip_after_prefix=True,
    chunk_guilds_at_startup=False,
)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))
    print("Connected to {} servers".format(len(bot.guilds)))
    print("Listening to {} shards".format(bot.shard_count))
    for guild in bot.guilds:
        try:
            print(f"Chunking guild: {guild.name} ({guild.id})...")
            await asyncio.wait_for(guild.chunk(), timeout=60.0)
            print(f"Successfully chunked {guild.name}.")
        except asyncio.TimeoutError:
            print(f"Chunking timed out for {guild.name}.")
        except Exception as e:
            print(f"An error occurred while chunking {guild.name}: {e}")
    print("Listening to {} users".format(len(bot.users)))


bot.run(TOKEN)
