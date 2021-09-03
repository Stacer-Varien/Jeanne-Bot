import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='re!', intents=intents)

bot.remove_command('help')

bot.load_extension("cogs.moderation")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.manage")
bot.load_extension("cogs.info")
bot.load_extension("cogs.owner")


@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    print('Connected to {} servers'.format(len(bot.guilds)))

load_dotenv()
TOKEN = os.getenv("token")
bot.run(TOKEN)
