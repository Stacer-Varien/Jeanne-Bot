from random import choice
import requests
from config import ANIMEME, JEANNE, MEDUSA, SABER, IMGUR_ID, WALLPAPER
from json import loads
import lxml.etree as ET

def get_saber_pic():
    url = f"https://api.imgur.com/3/album/{SABER}/images"
    payload = {}
    files = {}
    headers = {"Authorization": f"Client-ID {IMGUR_ID}"}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json["data"])["link"]
    return pick_link


def get_jeanne_pic():
    url = f"https://api.imgur.com/3/album/{JEANNE}/images"
    payload = {}
    files = {}
    headers = {"Authorization": f"Client-ID {IMGUR_ID}"}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json["data"])["link"]
    return pick_link


def get_wallpaper_pic():
    url = f"https://api.imgur.com/3/album/{WALLPAPER}/images"
    payload = {}
    files = {}
    headers = {"Authorization": f"Client-ID {IMGUR_ID}"}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json["data"])["link"]
    return pick_link


def get_medusa_pic():
    url = f"https://api.imgur.com/3/album/{MEDUSA}/images"
    payload = {}
    files = {}
    headers = {"Authorization": f"Client-ID {IMGUR_ID}"}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json["data"])["link"]
    return pick_link


def get_animeme_pic():
    url = f"https://api.imgur.com/3/album/{ANIMEME}/images"
    payload = {}
    files = {}
    headers = {"Authorization": f"Client-ID {IMGUR_ID}"}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json = loads(response.text)
    pick_link = choice(json["data"])["link"]
    return pick_link

def safebooru_pic():
    response = requests.get(
        "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=100&tags=-rating:questionable+-animated+score:>=10"
    ).text.encode("utf-8")
    parser = ET.XMLParser(recover=True)
    tree = ET.ElementTree(ET.fromstring(response, parser=parser))
    root = tree.getroot()
    image= choice(root).attrib["file_url"]
    return image
