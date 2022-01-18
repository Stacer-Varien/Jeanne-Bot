from os import listdir
from nextcord import Intents
from nextcord.ext.commands import Bot as Jeanne
from config import TOKEN

intents = Intents().all()
bot = Jeanne(command_prefix="/", intents=intents)
bot.remove_command('help')


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
