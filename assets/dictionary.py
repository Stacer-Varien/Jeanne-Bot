from discord import Color, Embed
import requests
from typing import Optional

def dictionary(word:str, language:Optional[str]):
    if language == None:
        language='en'
    
    embed=Embed()
    response=requests.get("https://api.dictionaryapi.dev/api/v2/entries/{}/{}".format(language, word))
    data=response.json()

    if response.status_code == 404:
        embed.color=Color.red()
        embed.title=data['title']
        embed.description="Sorry, definitions for the word you were looking for could not be found."
        return embed
    
    elif response.status_code == 429:
        embed.color=Color.red()
        embed.title=data['title']
        embed.description="Unfortunately, the dictionary API is being rate limited.\nPlease wait for a few minutes."
        return embed
    elif response.status_code != 200:
        embed.color=Color.red()
        embed.title=data['title']
        embed.description="It seems the dictionary API is facing problems.\nPlease wait for a few minutes."
        return embed
    else:
        embed.color=Color.random()
        embed.title=data[0]['word']
        for i in data[0]['meanings']:
            ...

        embed.description=""
        embed.add_field(name="Phonetic", value=data[0]['phonetic'])


