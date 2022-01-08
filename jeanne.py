from os import listdir
from nextcord import Intents
from nextcord.ext.commands import Bot as Jeanne
from config import TOKEN, aliases

intents = Intents().all()
bot = Jeanne(case_insensitive=True, command_prefix=aliases, intents=intents)
bot.remove_command('help')


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
    print(f'Unable to load {filename[:-3]}')

@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

bot.run(TOKEN)
