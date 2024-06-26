import csv
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from discord import Intents, AllowedMentions
from os import listdir
from config import TOKEN


class Jeanne(AutoShardedBot):
    async def setup_hook(self):
        dirs = ["./events", "./prefix", "./slash"]
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
    command_prefix=when_mentioned_or("J!", "j!", "Jeanne", "jeanne"), intents=intents
)
bot.allowed_mentions = AllowedMentions.all()
bot.case_insensitive = True
bot.strip_after_prefix = True
bot.remove_command("help")


@bot.event
async def on_ready():
    cfields = ["Date and Time", "User", "Command Used", "Command Usage"]
    efields = ["Date", "Command", "Error"]

    with open("commandlog.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cfields)
        writer.writeheader()

    with open("errors.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=efields)
        writer.writeheader()

    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))
    print("Connected to {} servers".format(len(bot.guilds)))
    print("Listening to {} users".format(len(bot.users)))
    print("Listening to {} shards".format(bot.shard_count))


bot.run(TOKEN)
