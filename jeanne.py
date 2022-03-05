from os import listdir
from nextcord import *
from nextcord.ext.commands import Bot as Jeanne
from config import TOKEN, db

intents = Intents(guilds=True, members=True, messages=True,
                  typing=True, presences=True)
bot = Jeanne(command_prefix='/', intents=intents)
bot.remove_command('help')

for filename in listdir('./slashcog'):
  if filename.endswith('.py'):
    bot.load_extension(f'slashcog.{filename[:-3]}')
    print(f"Slash {filename} loaded")

  else:
    print(f'Unable to load {filename[:-3]}')


@bot.event
async def on_ready():
  await bot.change_presence(activity=Game(name="Playing with Saber"))
  print('Connected to bot: {}'.format(bot.user.name))
  print('Bot ID: {}'.format(bot.user.id))

bot.run(TOKEN)
