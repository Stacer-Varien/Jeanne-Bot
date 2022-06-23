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
