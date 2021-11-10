import discord, os
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand

intents = discord.Intents().all()
aliases = ['j!', 'J!', 'jeanne ', 'Jeanne ']
bot = commands.Bot(command_prefix=aliases, intents=intents)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

#prefixed cog commands
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.manage")
bot.load_extension("cogs.info")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.reactions")
bot.load_extension("cogs.nsfw")
bot.load_extension("cogs.images")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.errormsgs")

#slash cog commands
bot.load_extension("slashcog.info")
bot.load_extension("slashcog.help")
bot.load_extension("slashcog.fun")
bot.load_extension("slashcog.manage")
bot.load_extension("slashcog.misc")
bot.load_extension("slashcog.moderation")
bot.load_extension("slashcog.owner")
bot.load_extension("slashcog.reactions")
bot.load_extension("slashcog.nsfw")
bot.load_extension("slashcog.images")
bot.load_extension("slashcog.utilities")
bot.load_extension("slashcog.errormsgs")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="j!help or /help"))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

load_dotenv()
TOKEN = os.getenv("token")
bot.run(TOKEN, bot=True)
