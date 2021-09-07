import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents().all()
aliases = ['re!', 'Re!', 'nero ', 'Nero ', '<@!831993597166747679> ']
bot = commands.Bot(command_prefix=aliases, intents=intents)

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
    print(f'Used by {len(set(bot.get_all_members()))} members')

load_dotenv()
TOKEN = os.getenv("token")
bot.run(TOKEN)
