from os import listdir, getenv
from discord import Activity, ActivityType, Intents
from dotenv import load_dotenv
from discord.ext.commands import Bot as Jeanne
from discord_slash import SlashCommand

intents = Intents().all()
aliases = ['j!', 'J!', 'jeanne ', 'Jeanne ']
bot = Jeanne(command_prefix=aliases, intents=intents)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

#prefixed cog commands
for filename in listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
    print(f"{filename} loaded")
    
  else:
    print(f'Unable to load {filename[:-3]}')

#slash cog commands
for filename in listdir('./slashcog'):
  if filename.endswith('.py'):
    bot.load_extension(f'slashcog.{filename[:-3]}')
    print(f"Slash {filename} loaded")
    
  else:
    print(f'Unable to load slash {filename[:-3]}')

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name="Santa Lily singing"))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

load_dotenv()
TOKEN = getenv("token")
bot.run(TOKEN, bot=True)
