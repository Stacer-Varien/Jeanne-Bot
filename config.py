"""Everything such as APIs and tokens for the bot, commands and functions to run on"""

from os import getenv
from dotenv import load_dotenv
from sqlite3 import connect
from random import choice

load_dotenv()
TOKEN = getenv("token")
WEATHER = getenv("weather_api")
TOPGG = getenv("topgg")
TOPGG_AUTH = getenv("topgg_auth")
WEBHOOK = getenv("report_webhook")
BB_WEBHOOK = getenv("botban_webhook")

JEANNE = str(getenv("jeanne_album"))
SABER = str(getenv("saber_album"))
WALLPAPER = str(getenv("wallpaper_album"))
MEDUSA = str(getenv("medusa_album"))
ANIMEME = str(getenv("animeme_album"))
NEKO = str(getenv("neko_album"))
MORGAN = str(getenv("morgan_album"))
CATBOX_HASH=str(getenv("catbox_hash"))

db = connect("database.db", check_same_thread=False)

kitsune_nekoslife = "https://nekos.life/api/v2/img/fox_girl"
hug_nekoslife = "https://nekos.life/api/v2/img/hug"
slap_nekoslife = "https://nekos.life/api/v2/img/slap"
smug_nekoslife = "https://nekos.life/api/v2/img/smug"
poke_nekosfun = "http://api.nekos.fun:8080/api/poke"
pat_nekoslife = "https://nekos.life/api/v2/img/pat"
kiss_nekosfun = "http://api.nekos.fun:8080/api/kiss"
tickle_nekoslife = "https://nekos.life/api/v2/img/tickle"
baka_nekosfun = "http://api.nekos.fun:8080/api/baka"
feed_nekoslife = "https://nekos.life/api/v2/img/feed"
cry_purrbot = "https://purrbot.site/api/img/sfw/cry/gif"
bite_purrbot = "https://purrbot.site/api/img/sfw/bite/gif"
blush_purrbot = "https://purrbot.site/api/img/sfw/blush/gif"
cuddle_purrbot = "https://purrbot.site/api/img/sfw/cuddle/gif"
dance_purrbot = "https://purrbot.site/api/img/sfw/dance/gif"
