from os import getenv
from dotenv import load_dotenv
from sqlite3 import connect

load_dotenv()
TOKEN = getenv("token")
WEATHER = getenv("weather_api")
TOPGG = getenv("topgg")
TOPGG_AUTH = getenv("topgg_auth")
WEBHOOK=getenv("report_webhook")
BB_WEBHOOK = getenv("botban_webhook")
IMGUR_ID=getenv("imgur_client_id")
IMGUR_SECRET = getenv("imgur_client_secret")
JEANNE=getenv("jeanne_album")
SABER = getenv("saber_album")
WALLPAPER = getenv("wallpaper_album")
NEKO = getenv("neko_album")
MEDUSA = getenv("medusa_album")
ANIMEME=getenv("animeme_album")

db=connect('database.db')
inv_db=connect('inventory.db')

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

