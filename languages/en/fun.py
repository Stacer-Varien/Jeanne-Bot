from random import choice, randint
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from functions import (
    DevPunishment,
)
from typing import Optional


class fun():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _8ball(self, ctx: Interaction, question: str):
        await ctx.response.defer()
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes – definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "Why ask me? Just do it!",
            "Why ask me? Just don't do it!",
            "Yeah... no",
            "Yeah... whatever",
            "Yeah... I don't know",
            "Yes? No? I don't know!",
            "Absolutely not, and I'm offended you asked.",
            "Sure, if the stars align and pigs fly.",
            "Only on Tuesdays.",
            "The answer lies within... your fridge.",
            "Ask your cat.",
            "Try again after coffee.",
            "404 answer not found.",
            "You're not ready for that truth.",
            "Do you really want to know?",
            "Hmm... my magic circuits are glitching.",
            "I'm just a ball, not a therapist.",
            "Let me think... nope.",
            "Yes. But also no.",
            "If I told you, I'd have to vanish in a puff of smoke.",
        ]

        embed = Embed(color=Color.random())
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=choice(answers), inline=False)
        await ctx.followup.send(embed=embed)

    async def reverse(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        if any(word in text for word in ["riffak", "reggin", "aggin"]):
            await DevPunishment(ctx.user).add_botbanned_user(
                "Using the reversed version of a common racial slur"
            )
            return
        embed = Embed(description=text[::-1], color=Color.random()).set_footer(
            text=f"Author: {ctx.user} | {ctx.user.id}"
        )
        await ctx.followup.send(embed=embed)

    async def combine(self, ctx: Interaction, first_word: str, second_word: str):
        await ctx.response.defer()
        combine1 = (
            first_word[: len(first_word) // 2] + second_word[len(second_word) // 2 :]
        )
        combine2 = (
            first_word[len(first_word) // 2 :] + second_word[: len(second_word) // 2]
        )
        embed = Embed(
            description=f"**1st combined word**: {combine1}\n**2nd combined word**: {combine2}",
            color=Color.random(),
        ).set_author(name=f"{first_word} + {second_word}")
        await ctx.followup.send(embed=embed)

    async def choose(self, ctx: Interaction, choices: str):
        await ctx.response.defer()
        embed = Embed(
            description=f"I chose **{choice(choices.split(','))}**",
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)

    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member or ctx.user
        embed = Embed(
            description=f"{member}'s simp rate is {perc}%", color=Color.random()
        )
        if perc >= 75:
            embed.set_image(url="https://i.imgur.com/W4u4Igk.jpg")
        elif perc >= 50:
            embed.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")
        await ctx.followup.send(embed=embed)

    async def gayrate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member or ctx.user
        embed = Embed(
            description=f"{member}'s gay rate is {perc}%", color=Color.random()
        )
        if perc >= 75:
            embed.set_image(url="https://i.imgur.com/itOD0Da.png?1")
        elif perc >= 50:
            embed.set_image(url="https://i.imgur.com/tYAbWCl.jpg")
        await ctx.followup.send(embed=embed)

    async def roast(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        member=member if member else ctx.user
        ROASTS = [
            "has the confidence of someone who has never been wrong — despite overwhelming evidence",
            "types 'lol' with a completely straight face",
            "could trip over a cordless phone",
            "is the human equivalent of a loading screen",
            "brings a spoon to a knife fight",
            "would get lost in a one-way hallway",
            "has main character energy but NPC dialogue",
            "radiates 'I didn’t read the instructions' vibes",
            "is proof that autopilot mode exists in humans",
            "has the reaction time of Internet Explorer",
            "would argue with a stop sign and still lose",
            "has the personality of unseasoned chicken",
            "thinks 'gaslight' is a brand of stove",
            "couldn’t pour water out of a boot with instructions on the heel",
            "looks like they clap when the plane lands",
            "has WiFi thoughts but dial-up execution",
            "is the reason group projects are stressful",
            "runs on vibes and zero critical thinking",
            "has the emotional range of a teaspoon",
            "would press the elevator button twice like it helps",
            "has big 'trust me bro' energy",
            "is the final boss of bad decisions",
            "types paragraphs just to say nothing",
            "has the situational awareness of a potato",
            "would forget their own birthday",
            "is built like a placeholder character",
            "thinks cereal is a soup and defends it",
            "has the ambition but not the skillset",
            "is allergic to common sense",
            "would get ratioed in real life",
            "has the vibe of a muted microphone",
            "could mess up a one-button task",
            "is running on 2% battery and bad choices",
            "has the confidence of a man who cannot be humbled",
            "is proof that evolution takes breaks",
            "brings nothing to the table and still eats",
            "has the energy of a forgotten side quest",
            "would lose a staring contest with a wall",
            "has the brain buffering icon permanently on",
            "thinks 'BRB' is a long-term commitment",
            "is the human version of a typo",
            "couldn’t find water in the ocean",
            "has the charisma of a damp sock",
            "is on speaking terms with bad decisions",
            "has the attention span of a goldfish on TikTok",
            "would get banned from single-player mode",
            "is somehow always wrong with confidence",
            "has the vibes of a cracked screen protector",
            "looks like they say 'you too' when the waiter says enjoy your meal",
            "is built like a patch note nobody asked for",
            "would misspell their own name",
            "has big 'I peaked in the tutorial' energy",
            "exists purely to lower the average",
            "has the emotional intelligence of a toaster",
            "would argue with Google Maps",
            "is a walking plot hole",
            "has the energy of a dead group chat",
            "is the reason 'are you sure?' buttons exist",
        ]
        embed = Embed(color=Color.random())
        if member:
            roast = f"{member} is the type of person who {choice(ROASTS)}"
        else:
            roast = f"You are the type of person who {choice(ROASTS)}"
        embed.description = roast
        await ctx.followup.send(embed=embed)

    async def mock(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        mocked = "".join(
            letter.upper() if randint(0, 1) else letter.lower() for letter in text
        )
        embed = Embed(
            title="🗣️ Mock Generator",
            description=mocked,
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)
