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
TENOR = getenv("tenor")
CLIENTKEY = getenv("client_key")
JEANNE = str(getenv("jeanne_album"))
SABER = str(getenv("saber_album"))
WALLPAPER = str(getenv("wallpaper_album"))
MEDUSA = str(getenv("medusa_album"))
ANIMEME = str(getenv("animeme_album"))
NEKO = str(getenv("neko_album"))
MORGAN = str(getenv("morgan_album"))
KITSUNE = str(getenv("kitsune_album"))
CATBOX_HASH = str(getenv("catbox_hash"))
db = connect("database.db", check_same_thread=False)
hug = f"https://tenor.googleapis.com/v2/search?q=hug%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
slap = f"https://tenor.googleapis.com/v2/search?q=slap%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
smug = f"https://tenor.googleapis.com/v2/search?q=smug%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
poke = f"https://tenor.googleapis.com/v2/search?q=poke%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
pat = f"https://tenor.googleapis.com/v2/search?q=headpat%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
kiss = f"https://tenor.googleapis.com/v2/search?q=kiss%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
tickle = f"https://tenor.googleapis.com/v2/search?q=tickle%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
baka = f"https://tenor.googleapis.com/v2/search?q=baka%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
feed = f"https://tenor.googleapis.com/v2/search?q=feed%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
cry = f"https://tenor.googleapis.com/v2/search?q=cry%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
bite = f"https://tenor.googleapis.com/v2/search?q=bite%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
blush = f"https://tenor.googleapis.com/v2/search?q=blush%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
cuddle = f"https://tenor.googleapis.com/v2/search?q=cuddle%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
dance = f"https://tenor.googleapis.com/v2/search?q=dance%20anime&key={TENOR}&client_key={CLIENTKEY}&limit=3"
