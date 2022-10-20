
from os import listdir
from assets.handler import handler
handler()
from nextcord import *
from nextcord.ext.commands import Bot as Jeanne
from config import TOKEN
#from nextcord.gateway import DiscordWebSocket

#class MyDiscordWebSocket(DiscordWebSocket):

#    async def send_as_json(self, data):
#        if data.get('op') == self.IDENTIFY:
#            if data.get('d', {}).get('properties', {}).get('browser') is not None:
#                data['d']['properties']['browser'] = 'Discord Android'
#                data['d']['properties']['device'] = 'Discord Android'
#        await super().send_as_json(data)

#DiscordWebSocket.from_client = MyDiscordWebSocket.from_client

intents = Intents().all()
intents.presences = False
intents.webhooks = False
intents.voice_states = False
intents.reactions = False
intents.scheduled_events = False

bot = Jeanne(intents=intents,
             allowed_mentions=AllowedMentions.all())
bot.remove_command('help')

for filename in listdir('./slash cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'slash cogs.{filename[:-3]}')
    print(f"{filename} loaded")

  else:
    print(f'Unable to load {filename[:-3]}')

#bot.load_extension('topgg.topgg_')

@bot.event
async def on_ready():
  
  print('Connected to bot: {}'.format(bot.user.name))
  print('Bot ID: {}'.format(bot.user.id))

bot.run(TOKEN)


