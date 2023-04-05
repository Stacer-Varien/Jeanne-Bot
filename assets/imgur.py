from random import choice
import requests
from config import ANIMEME, JEANNE, MEDUSA, SABER, IMGUR_ID, WALLPAPER
from json import loads

def get_saber_pic():
    url = f"https://api.imgur.com/3/album/{SABER}/images"
    payload = {}
    files = {}
    headers = {'Authorization': f'Client-ID {IMGUR_ID}'}
    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    json=loads(response.text)
    pick_link=choice(json['data'])['link']
    return pick_link


def get_jeanne_pic():
    url = f"https://api.imgur.com/3/album/{JEANNE}/images"
    payload = {}
    files = {}
    headers = {'Authorization': f'Client-ID {IMGUR_ID}'}
    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json['data'])['link']
    return pick_link


def get_wallpaper_pic():
    url = f"https://api.imgur.com/3/album/{WALLPAPER}/images"
    payload = {}
    files = {}
    headers = {'Authorization': f'Client-ID {IMGUR_ID}'}
    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json['data'])['link']
    return pick_link


def get_medusa_pic():
    url = f"https://api.imgur.com/3/album/{MEDUSA}/images"
    payload = {}
    files = {}
    headers = {'Authorization': f'Client-ID {IMGUR_ID}'}
    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json['data'])['link']
    return pick_link


#def get_neko_pic():
#    url = f"https://api.imgur.com/3/album/{NEKO}/images"
#    payload = {}
#    files = {}
#    headers = {'Authorization': f'Client-ID {IMGUR_ID}'}
#    response = requests.request(
#        "GET", url, headers=headers, data=payload, files=files)
#    json = loads(response.text)
#    pick_link = choice(json['data'])['link']
#    return pick_link


def get_animeme_pic():
    url = f"https://api.imgur.com/3/album/{ANIMEME}/images"
    payload = {}
    files = {}
    headers = {'Authorization': f'Client-ID {IMGUR_ID}'}
    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json['data'])['link']
    return pick_link
