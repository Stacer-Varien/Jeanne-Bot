from discord import Color, Embed, Interaction
import requests
from typing import Optional

async def dictionary(ctx:Interaction, word:str, language:Optional[str]):
    if language == None:
        language='en'
    
    embed=Embed()
    response=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}")
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

        part_of_speech = []
        definitions = []
        examples = []

        for i in data[0]["meanings"]:
            part_of_speech.append(i["partOfSpeech"])
            for j in i["definitions"]:
                definitions.append(j["definition"])
                examples.append(j.get("example", None))

        items_per_page = 2
        total_pages = (len(part_of_speech) + items_per_page - 1) // items_per_page

        for page_num in range(1, total_pages + 1):
            start_index = (page_num - 1) * items_per_page
            end_index = start_index + items_per_page

            page_part_of_speech = part_of_speech[start_index:end_index]
            page_definitions = definitions[start_index:end_index]
            page_examples = examples[start_index:end_index]

            embed = Embed(
                title=f"Page {page_num}/{total_pages}",
                color=Color.blurple()
            )

            for part, definition, example in zip(page_part_of_speech, page_definitions, page_examples):
                embed.add_field(name="Part of Speech", value=part, inline=False)
                embed.add_field(name="Definition", value=definition, inline=False)
                if example:
                    embed.add_field(name="Example", value=example, inline=False)

            embed.set_footer(text="Fetched from dictionaryapi.dev")
            await ctx.edit_original_response(content=None, embed=embed)

        # Remove the return statement from the loop
