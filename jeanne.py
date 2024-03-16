from discord.ext.commands import Bot, when_mentioned_or
from discord import Intents, AllowedMentions
from os import listdir
from config import TOKEN


class Jeanne(Bot):
    async def setup_hook(self):
        for filename in listdir("./slash_cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"slash_cogs.{filename[:-3]}")
                print(f"{filename} loaded")
            else:
                print(f"Unable to load {filename[:-3]}")
        for filename in listdir("./prefix_cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"prefix_cogs.{filename[:-3]}")
                print(f"{filename} loaded")
            else:
                print(f"Unable to load {filename[:-3]}")
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
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))


bot.run(TOKEN)
