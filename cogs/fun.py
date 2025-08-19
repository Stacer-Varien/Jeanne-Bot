from discord import Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from assets.images import get_animeme_pic
from typing import Optional
import languages.en.fun as en
import languages.fr.fun as fr
import languages.de.fun as de
from discord.app_commands import locale_str as T

# de = dutch and translate to dutch
class fun(Cog, name="FunSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name="8ball",
        description=T("8ball_desc"),
        extras={
            "en": {
                "name": "8ball",
                "description": "Ask 8 ball anything and you will get your answer",
                "parameters": [
                    {
                        "name": "question",
                        "description": "The question you want to ask the 8ball",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "8ball",
                "description": "Demandez à 8 ball n'importe quoi et vous obtiendrez votre réponse",
                "parameters": [
                    {
                        "name": "question",
                        "description": "Ajoutez votre question",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "8ball",
                "description": "Fragen Sie 8 Ball alles und Sie erhalten Ihre Antwort",
                "parameters": [
                    {
                        "name": "question",
                        "description": "Die Frage, die Sie 8 Ball stellen möchten",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(question=T("question_parm_desc"))
    @Jeanne.rename(question=T("question_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _8ball(self, ctx: Interaction, question: str):
        if ctx.locale.value == "fr":
            await fr.fun(self.bot)._8ball(ctx, question) 
            return
        if ctx.locale.value == "de":
            await de.fun(self.bot)._8ball(ctx, question)      
        await en.fun(self.bot)._8ball(ctx, question)

    @Jeanne.command(
        name=T("reverse_name"),
        description=T("reverse_desc"),
        extras={
            "en": {
                "name": "reverse",
                "description": "Say something and I will say it in reversed text",
                "parameters": [
                    {
                        "name": "text",
                        "description": "The text you want to reverse",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "inverse",
                "description": "Dites quelque chose et je le dirai dans un texte inversé",
                "parameters": [
                    {
                        "name": "texte",
                        "description": "Qu'est-ce que vous inversez?",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "inverse",
                "description": "Sagen Sie etwas und ich werde es in umgekehrtem Text sagen",
                "parameters": [
                    {
                        "name": "text",
                        "description": "Was möchten Sie umkehren?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(text=T("text_parm_desc"))
    @Jeanne.rename(text=T("text_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def reverse(self, ctx: Interaction, text: str):
        if ctx.locale.value == "fr":
            await fr.fun(self.bot).reverse(ctx, text)
            return
        if ctx.locale.value == "de":
            await de.fun(self.bot).reverse(ctx, text)
            return
        await en.fun(self.bot).reverse(ctx, text)

    @Jeanne.command(
        description=T("animeme_desc"),
        extras={
            "en": {"name": "animeme", "description": "Get a random animeme"},
            "fr": {
                "name": "animeme",
                "description": "Obtenez un animeme aléatoire",
            },
            "de": {
                "name": "animeme",
                "description": "Holen Sie sich ein zufälliges Animeme",
            }
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def animeme(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_animeme_pic(ctx)
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(
        name=T("combine_name"),
        description=T("combine_desc"),
        extras={
            "en": {
                "name": "combine",
                "description": "Combine 2 words to get 2 combined words",
                "parameters": [
                    {
                        "name": "first_word",
                        "description": "Add first word",
                        "required": True,
                    },
                    {
                        "name": "second_word",
                        "description": "Add second word",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "combiner",
                "description": "Combinez deux mots en un seul",
                "parameters": [
                    {
                        "name": "premier_mot",
                        "description": "Le premier mot à combiner",
                        "required": True,
                    },
                    {
                        "name": "deuxième_mot",
                        "description": "Le deuxième mot à combiner",
                        "required": True,
                    },
                ],
            },
            "de": {
                "name": "kombinieren",
                "description": "Kombinieren Sie zwei Wörter zu einem",
                "parameters": [
                    {
                        "name": "erstes_wort",
                        "description": "Das erste Wort zum Kombinieren",
                        "required": True,
                    },
                    {
                        "name": "zweites_wort",
                        "description": "Das zweite Wort zum Kombinieren",
                        "required": True,
                    },
                ],
            },
        },
    )
    @Jeanne.describe(
        first_word=T("first_word_parm_desc"), second_word=T("second_word_parm_desc")
    )
    @Jeanne.rename(
        first_word=T("first_word_parm_name"), second_word=T("second_word_parm_name")
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def combine(self, ctx: Interaction, first_word: str, second_word: str):
        if ctx.locale.value == "fr":
            await fr.fun(self.bot).combine(ctx, first_word, second_word)
            return
        if ctx.locale.value == "de":
            await de.fun(self.bot).combine(ctx, first_word, second_word)
            return
        await en.fun(self.bot).combine(ctx, first_word, second_word)

    @Jeanne.command(
        name=T("choose_name"),
        description=T("choose_desc"),
        extras={
            "en": {
                "name": "choose",
                "description": "Give me a lot of choices and I will pick one for you",
                "parameters": [
                    {
                        "name": "choices",
                        "description": "Add your choices here. Separate them with ','",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "choisir",
                "description": "Donnez-moi beaucoup de choix et je choisirai l'un d'entre eux pour vous",
                "parameters": [
                    {
                        "name": "choix",
                        "description": "Ajoutez vos choix ici. Séparez-les par ','",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "wählen",
                "description": "Geben Sie mir viele Optionen und ich wähle eine für Sie aus",
                "parameters": [
                    {
                        "name": "auswahl",
                        "description": "Fügen Sie hier Ihre Auswahl hinzu. Trennen Sie sie mit ','",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(choices=T("choices_parm_desc"))
    @Jeanne.rename(choices=T("choices_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def choose(self, ctx: Interaction, choices: str):
        if ctx.locale.value == "fr":
            await fr.fun(self.bot).choose(ctx, choices)
            return
        if ctx.locale.value == "de":
            await de.fun(self.bot).choose(ctx, choices)
            return
        await en.fun(self.bot).choose(ctx, choices)

    @Jeanne.command(
        description=T("simprate_desc"),
        extras={
            "en": {
                "name": "simprate",
                "description": "Get a random simp rate for you or someone else",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "simprate",
                "description": "Obtenez un taux de simp aléatoire pour vous ou quelqu'un d'autre",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre?",
                        "required": False,
                    }
                ],
            },
            "de": {
                "name": "simprate",
                "description": "Holen Sie sich eine zufällige Simp-Bewertung für Sie oder jemand anderen",
                "parameters": [
                    {
                        "name": "mitglied",
                        "description": "Welches Mitglied?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        if ctx.locale.value == "fr":
            await fr.fun(self.bot).simprate(ctx, member)
            return
        if ctx.locale.value == "de":
            await de.fun(self.bot).simprate(ctx, member)
            return
        await en.fun(self.bot).simprate(ctx, member)

    @Jeanne.command(
        description=T("gayrate_desc"),
        extras={
            "en": {
                "name": "gayrate",
                "description": "Rate how gay you or a member is",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "gayrate",
                "description": "Obtenez un taux de gay aléatoire pour vous ou quelqu'un d'autre",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Quel membre?",
                        "required": False,
                    }
                ],
            },
            "de": {
                "name": "gayrate",
                "description": "Holen Sie sich eine zufällige Gay-Bewertung für Sie oder jemand anderen",
                "parameters": [
                    {
                        "name": "mitglied",
                        "description": "Welches Mitglied?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def gayrate(self, ctx: Interaction, member: Optional[Member] = None):
        if ctx.locale.value == "fr":
            await fr.fun(self.bot).gayrate(ctx, member)
            return
        if ctx.locale.value == "de":
            await de.fun(self.bot).gayrate(ctx, member)
            return
        await en.fun(self.bot).gayrate(ctx, member)


async def setup(bot: Bot):
    await bot.add_cog(fun(bot))
