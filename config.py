"""Everything such as APIs and tokens for the bot, commands and functions to run on"""

from os import getenv, environ
from dotenv import load_dotenv
from sqlite3 import connect

load_dotenv()
TOKEN = getenv("token")
WEATHER = getenv("weather_api")
TOPGG = getenv("topgg")
TOPGG_AUTH = getenv("topgg_auth")
DB_AUTH = getenv("db_auth")
WEBHOOK = getenv("report_webhook")
BB_WEBHOOK = getenv("botban_webhook")
JEANNE = str(getenv("jeanne_album"))
SABER = str(getenv("saber_album"))
WALLPAPER = str(getenv("wallpaper_album"))
MEDUSA = str(getenv("medusa_album"))
ANIMEME = str(getenv("animeme_album"))
NEKO = str(getenv("neko_album"))
MORGAN = str(getenv("morgan_album"))
KITSUNE = str(getenv("kitsune_album"))
CATBOX_HASH = str(getenv("catbox_hash"))
BADGES = str(getenv("badges_album"))
STATUS_WEBHOOK=str(getenv("status"))

GELBOORU_API=environ["GELBOORU_API_KEY"]
GELBOORU_USER=environ["GELBOORU_USER_ID"]
RULE34_API=environ["RULE34_API_KEY"]
RULE34_USER=environ["RULE34_USER_ID"]

db = connect("database.db", autocommit=True)
