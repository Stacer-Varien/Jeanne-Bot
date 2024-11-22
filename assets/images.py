from random import choice
from discord import Color, Embed, File
import requests
from config import ANIMEME, JEANNE, KITSUNE, MEDUSA, MORGAN, SABER, WALLPAPER, NEKO
import lxml.etree as ET
from os import listdir, path


def get_saber_pic() -> tuple[File, Embed]:
    folder_path = SABER
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]
    random_image = choice(image_files)
    file = File(path.join(folder_path, random_image), random_image)
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Saber_1936 • Credits must go to the artist")

    return file, embed


def get_jeanne_pic() -> tuple[Embed, File]:
    folder_path = JEANNE
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]

    random_image = choice(image_files)
    File(path.join(folder_path, random_image), filename="image.png")
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Jeanne_1936 • Credits must go to the artist")
    file = File(path.join(folder_path, random_image), random_image)
    return embed, file


def get_wallpaper_pic() -> tuple[Embed, File]:
    folder_path = WALLPAPER
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]
    random_image = choice(image_files)
    file = File(path.join(folder_path, random_image), random_image)
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Wallpaper_1936 • Credits must go to the artist")

    return embed, file


def get_medusa_pic() -> tuple[Embed, File]:
    folder_path = MEDUSA
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]
    random_image = choice(image_files)
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Medusa_1936 • Credits must go to the artist")
    file = File(path.join(folder_path, random_image), random_image)
    return embed, file


def get_animeme_pic() -> tuple[Embed, File]:
    folder_path = ANIMEME
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", "..gif"))
    ]
    random_image = choice(image_files)
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Animeme_1936 • Credits must go to the artist")
    file = File(path.join(folder_path, random_image), random_image)
    return embed, file


def get_neko_pic() -> tuple[Embed, File]:
    folder_path = NEKO
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]

    random_image = choice(image_files)
    File(path.join(folder_path, random_image), filename="image.png")
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Neko_1936 • Credits must go to the artist")
    file = File(path.join(folder_path, random_image), random_image)
    return embed, file


def get_morgan_pic() -> tuple[Embed, File]:
    folder_path = MORGAN
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]

    random_image = choice(image_files)
    File(path.join(folder_path, random_image), filename="image.png")
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(
        text="Fetched from Morgan_le_Fay_1936 • Credits must go to the artist"
    )
    file = File(path.join(folder_path, random_image), random_image)
    return embed, file


def get_kistune_pic() -> tuple[Embed, File]:
    folder_path = KITSUNE
    files = listdir(folder_path)

    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]

    random_image = choice(image_files)
    File(path.join(folder_path, random_image), filename="image.png")
    embed = Embed(color=Color.random())
    embed.set_image(url=f"attachment://{random_image}")
    embed.set_footer(text="Fetched from Kitsune_1936 • Credits must go to the artist")
    file = File(path.join(folder_path, random_image), random_image)
    return embed, file


def safebooru_pic() -> str:
    response = requests.get(
        "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=100&tags=-rating:questionable+-animated+score:>=10"
    ).text.encode("utf-8")
    parser = ET.XMLParser(recover=True)
    tree = ET.ElementTree(ET.fromstring(response, parser=parser))
    root = tree.getroot()
    image = choice(root).attrib["file_url"]
    return str(image)
