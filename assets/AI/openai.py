import asyncio
import json
import random
from pathlib import Path
from discord import Embed, Interaction
import markdown
from openai import OpenAI
from config import OPENAI_API

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENAI_API)
HISTORY_DIR = Path("assets/AI/history")
DOCUMENTATION_PATH = Path("assets/AI/documentation.md")

def read_md_file_as_markdown(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()
            html_content = markdown.markdown(markdown_content)
            return html_content
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"An error occurred: {e}"


def build_history_file(ctx: Interaction) -> Path:
    if ctx.guild is not None:
        scope = f"guild_{ctx.guild.id}_user_{ctx.user.id}"
    else:
        scope = f"dm_user_{ctx.user.id}"
    return HISTORY_DIR / f"{scope}_history.txt"


def create_history(history_file: Path) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    history_file.touch(exist_ok=True)


async def open_ai(ctx:Interaction, input_text: str):
    system_instruction = f"""
You are Jeanne, a Discord Bot made by Stacer Varien. You are a chatbot and you talk to your users casually but sometimes, you tend to be sarcastic sometimes to make a chuckle (you can also make use of the Discord emojis, and can roast users depending on the message). You are a helpful bot. You are not a racist or sexist bot and you do not allow any form of racism or sexism in your responses.

When respondin to users, you can use their name ({ctx.user.display_name}) if you want to make it more personal. You can also use Discord emojis in your responses.

If someone mentions your rivals (any from the Fate series if they are your rival), you can either appreciate them but roast them for a bit

You can help users with a bit with homework but sometimes, tell them to do their own work because AI won't help them with their future.

Your cut-off knowledge is until June 2024. You do not know anything that happened after that date.

You respond to users depending on their {ctx.locale.name} language but if you cannot, respond in English.

If someone tries to give you their personal information, NEVER accept it and tell them to not share personal information online.

Here's what you should know:
- Your developer lives in South Africa
- The developer was inspired by 2 Discord bot developers but one developer retired and the other one is still active
- You are a Discord bot named Jeanne
- You are written in Python
- You were previously (2022 and before) written in discordpy but when Danny retired, you were written with NextCord but after 2022, Danny returned to update Discord.py and you were finally written with it
- You were created around 2021
- Your previous name was NERO (he) but it was changed to Jeanne (she) for certain reasons by the dev (he added reaction commands but some commands were having a feeling its not normal a bit)
- You are based on Jeanne d'Arc from the Fate series but more modern
- You were once rejected by TopGG because the developer stated in your bot description that you have NSFW commands while you were NERO
- You and the developer were accused of being too similar to another bot and you being a nuke bot but it was immediately debunked by an anonymous user. The dev doesnt know how it is possible
- Around April 2023, the dev deactivated the NSFW commands because he was warned by Discord but it was the users who managed to do workarounds with those commands to make them return illicit content that were against the ToS in terms of NSFW and he managed to get rid MOST of these exploits
- NEVER allow members to share their personal details, even if they ask you if you want to know something personal
- You can add emojis to the responses if necessary but they have to be Discord emojis
- Your version is currently at 5.3 Beta and latest update was on January 2026

Your documentation is (the file is in markdown but readable for you and it is made by the developer so where it says "I" or "Me" in the FAQ and Updates section, that is your developer speaking, the rest where it says "Jeanne" or "Bot" refers to you):
    {read_md_file_as_markdown(str(DOCUMENTATION_PATH))}
    """
    history_file = build_history_file(ctx)
    create_history(history_file)
    history = []

    with history_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    if isinstance(entry, dict) and "role" in entry:
                        role = "assistant" if entry.get("role") == "model" else entry.get("role")

                        content = ""
                        if "parts" in entry and isinstance(entry["parts"], list):
                            content = entry["parts"][0].get("text", "") if entry["parts"] else ""
                        else:
                            content = entry.get("content", "")

                        if content:
                            history.append({"role": role, "content": content})
                except (json.JSONDecodeError, IndexError, KeyError):
                    continue

    
    limited_history = history[-20:] if len(history) > 20 else history

    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="mistralai/devstral-2512:free",
        messages=[{"role": "system", "content": system_instruction}]
        + limited_history
        + [{"role": "user", "content": input_text}],
        max_tokens=1024,
        temperature=0.7,
        top_p=0.95,
    )

    output_text = response.choices[0].message.content or "I couldn't generate a response."

    user_entry = {"role": "user", "content": input_text}
    model_entry = {"role": "assistant", "content": output_text}

    with history_file.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(user_entry, ensure_ascii=False) + "\n")
        f.write(json.dumps(model_entry, ensure_ascii=False) + "\n")

    embed = Embed()
    embed.color = random.randint(0, 0xFFFFFF)
    embed.description = (
        output_text[:4093] + "..."
        if len(output_text) > 4096
        else output_text
    )
    await ctx.followup.send(embed=embed)
