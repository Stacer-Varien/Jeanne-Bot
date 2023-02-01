from config import TOKEN
from discord.ext.commands import Bot, when_mentioned_or
from discord import *
from os import listdir
from assets.handler import handler
#from discord.gateway import DiscordWebSocket

#class MyDiscordWebSocket(DiscordWebSocket):

#    async def send_as_json(self, data):
#        if data.get('op') == self.IDENTIFY:
#            if data.get('d', {}).get('properties', {}).get('browser') is not None:
#                data['d']['properties']['browser'] = 'Discord Android'
#                data['d']['properties']['device'] = 'Discord Android'
#        await super().send_as_json(data)

#DiscordWebSocket.from_client = MyDiscordWebSocket.from_client


class Jeanne(Bot):
    async def setup_hook(self):
        await self.tree.sync()
        for filename in listdir('./cogs'):
          if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"{filename} loaded")

          else:
            print(f'Unable to load {filename[:-3]}')

intents = Intents().all()
intents.presences = False
intents.voice_states = False
intents.reactions = False
intents.auto_moderation=False

bot = Jeanne(command_prefix=when_mentioned_or('j!', 'J!', 'jeanne ', 'Jeanne'), intents=intents, #the prefix is owner only
             allowed_mentions=AllowedMentions.all(), max_messages=10000)
bot.remove_command('help')

@bot.event
async def on_ready():
  print('Connected to bot: {}'.format(bot.user.name))
  print('Bot ID: {}'.format(bot.user.id))

bot.run(TOKEN, log_handler=handler())
