"""Everything such as APIs and tokens for the bot, commands and functions to run on"""

from os import getenv
from dotenv import load_dotenv
from sqlite3 import connect


load_dotenv()
TOKEN = getenv("token")
WEATHER = getenv("weather_api")
TOPGG = getenv("topgg")
TOPGG_AUTH = getenv("topgg_auth")
WEBHOOK = getenv("report_webhook")
BB_WEBHOOK = getenv("botban_webhook")
TENOR=getenv("tenor")
CLIENTKEY = getenv("client_key")
JEANNE = str(getenv("jeanne_album"))
SABER = str(getenv("saber_album"))
WALLPAPER = str(getenv("wallpaper_album"))
MEDUSA = str(getenv("medusa_album"))
ANIMEME = str(getenv("animeme_album"))
NEKO = str(getenv("neko_album"))
MORGAN = str(getenv("morgan_album"))
CATBOX_HASH=str(getenv("catbox_hash"))

db = connect("database.db", check_same_thread=False)

kitsune = "https://nekos.life/api/v2/img/fox_girl"
hug = "https://nekos.life/api/v2/img/hug"
slap = "https://nekos.life/api/v2/img/slap"
smug = "https://nekos.life/api/v2/img/smug"
poke = "https://api.otakugifs.xyz/gif?reaction=poke&format=gif"
pat = "https://nekos.life/api/v2/img/pat"
kiss = "https://api.otakugifs.xyz/gif?reaction=kiss&format=gif"
tickle = "https://nekos.life/api/v2/img/tickle"
baka = f"https://tenor.googleapis.com/v2/search?q=baka%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
feed = "https://nekos.life/api/v2/img/feed"
cry = "https://purrbot.site/api/img/sfw/cry/gif"
bite = "https://purrbot.site/api/img/sfw/bite/gif"
blush = "https://purrbot.site/api/img/sfw/blush/gif"
cuddle = "https://purrbot.site/api/img/sfw/cuddle/gif"
dance = "https://purrbot.site/api/img/sfw/dance/gif"
