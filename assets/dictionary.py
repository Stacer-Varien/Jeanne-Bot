from discord import Color, Embed, Interaction
import requests
from reactionmenu import ViewMenu, ViewButton


async def dictionary(ctx: Interaction, word: str):

    embed = Embed()
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    data = response.json()

    if response.status_code == 404:
        embed.color = Color.red()
        embed.title = data["title"]
        embed.description = (
            "Sorry, definitions for the word you were looking for could not be found."
        )
        await ctx.response.send_message(embed=embed)
        return

    if response.status_code == 429:
        embed.color = Color.red()
        embed.title = data["title"]
        embed.description = "Unfortunately, the dictionary API is being rate limited.\nPlease wait for a few minutes."
        await ctx.response.send_message(embed=embed)
        return

    if response.status_code != 200:
        embed.color = Color.red()
        embed.title = data["title"]
        embed.description = "It seems the dictionary API is facing problems.\nPlease wait for a few minutes."
        await ctx.response.send_message(embed=embed)
        return

    menu = ViewMenu(
        ctx,
        menu_type=ViewMenu.TypeEmbed,
        disable_items_on_timeout=True,
        style="Page $/& | Fetched from dictionaryapi.dev",
    )
    embed.color = Color.random()
    embed.title = f"Word: {data[0]['word']}"

    for i in data[0]["meanings"]:
        partOfSpeech = i["partOfSpeech"]
        for j in i["definitions"]:
            definition = j["definition"]
            try:
                example = j["example"]
            except Exception:
                pass

            page_embed = Embed(color=embed.color, title=embed.title)
            page_embed.add_field(
                name="Part of Speech", value=partOfSpeech, inline=False
            )
            page_embed.add_field(name="Definition", value=definition, inline=False)
            try:
                page_embed.add_field(name="Example", value=example, inline=False)
            except Exception:
                pass

            menu.add_page(embed=page_embed)

    menu.add_button(ViewButton.go_to_first_page())
    menu.add_button(ViewButton.back())
    menu.add_button(ViewButton.next())
    menu.add_button(ViewButton.go_to_last_page())

    await menu.start()
