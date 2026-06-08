import asyncio
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from discord import Intents, AllowedMentions
from os import listdir
from languages.Translator import MyTranslator
from config import TOKEN
from functions import ensure_database_schema


ensure_database_schema()



class Jeanne(AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chunked_guild_ids: set[int] = set()

    async def setup_hook(self):
        for directory in ("events", "cogs"):
            for filename in sorted(listdir(directory)):
                if not filename.endswith(".py"):
                    continue
                await self.load_extension(f"{directory}.{filename[:-3]}")
                print(f"./{directory}.{filename} loaded")
        self.translator = MyTranslator()
        await self.tree.set_translator(self.translator)
        await self.load_extension("jishaku")
        await self.tree.sync()


intents = Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.members = True
intents.message_content = True


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
        if guild.id in bot.chunked_guild_ids:
            continue
        try:
            print(f"Chunking guild: {guild.name} ({guild.id})...")
            await asyncio.wait_for(guild.chunk(), timeout=60.0)
            bot.chunked_guild_ids.add(guild.id)
            print(f"Successfully chunked {guild.name}.")
        except asyncio.TimeoutError:
            print(f"Chunking timed out for {guild.name}.")
        except Exception as e:
            print(f"An error occurred while chunking {guild.name}: {e}")
    print("Listening to {} users".format(len(bot.users)))


bot.run(TOKEN)
