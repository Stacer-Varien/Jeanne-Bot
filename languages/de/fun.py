from random import choice, randint
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from functions import (
    DevPunishment,
)
from typing import Optional


class fun:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _8ball(self, ctx: Interaction, question: str):
        await ctx.response.defer()
        answers = [
            "Es ist sicher.",
            "Es ist definitiv so.",
            "Ohne Zweifel.",
            "Ja – auf jeden Fall.",
            "Darauf kannst du vertrauen.",
            "So wie ich es sehe, ja.",
            "Wahrscheinlich.",
            "Die Aussichten sind gut.",
            "Ja.",
            "Die Zeichen stehen auf Ja.",
            "Antwort ist vage, versuche es erneut.",
            "Frag später noch einmal.",
            "Besser, ich sage es dir jetzt nicht.",
            "Kann jetzt nicht vorhersagen.",
            "Konzentriere dich und frage erneut.",
            "Rechne nicht damit.",
            "Meine Antwort ist nein.",
            "Meine Quellen sagen nein.",
            "Die Aussichten sind nicht so gut.",
            "Sehr zweifelhaft.",
            "Warum fragst du mich? Mach es einfach!",
            "Warum fragst du mich? Tu es einfach nicht!",
            "Ja... nein",
            "Ja... was auch immer",
            "Ja... ich weiß es nicht",
            "Ja? Nein? Ich weiß es nicht!",
            "Absolut nicht, und ich bin beleidigt, dass du es fragst.",
            "Natürlich, wenn die Sterne richtig stehen und Schweine fliegen können.",
            "Nur dienstags.",
            "Die Antwort liegt... in deinem Kühlschrank.",
            "Frag deine Katze.",
            "404 Antwort nicht gefunden.",
            "Du bist noch nicht bereit für diese Wahrheit.",
            "Willst du es wirklich wissen?",
            "Hmm... meine magischen Schaltkreise stottern.",
            "Ich bin nur eine Kugel, kein Therapeut.",
            "Lass mich nachdenken... nein.",
            "Ja. Aber auch nein.",
            "Wenn ich es dir erzähle, muss ich in einer Rauchwolke verschwinden.",
        ]

        embed = Embed(color=Color.random())
        embed.add_field(name="Frage:", value=question, inline=False)
        embed.add_field(name="Antwort:", value=choice(answers), inline=False)
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
            description=f"**1. kombiniertes Wort**: {combine1}\n**2. kombiniertes Wort**: {combine2}",
            color=Color.random(),
        ).set_author(name=f"{first_word} + {second_word}")
        await ctx.followup.send(embed=embed)

    async def choose(self, ctx: Interaction, choices: str):
        await ctx.response.defer()
        embed = Embed(
            description=f"Ich wähle **{choice(choices.split(','))}**",
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)

    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        perc = randint(0, 100)
        member = member or ctx.user
        embed = Embed(
            description=f"Der Simp-Prozentsatz von {member} ist {perc}%",
            color=Color.random(),
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
            description=f"Der Gay-Prozentsatz von {member} ist {perc}%",
            color=Color.random(),
        )
        if perc >= 75:
            embed.set_image(url="https://i.imgur.com/itOD0Da.png?1")
        elif perc >= 50:
            embed.set_image(url="https://i.imgur.com/tYAbWCl.jpg")
        await ctx.followup.send(embed=embed)

    async def roast(self, ctx: Interaction, member: Optional[Member] = None):
        await ctx.response.defer()
        member = member if member else ctx.user
        ROASTS = [
            "hat das Selbstvertrauen von jemandem, der noch nie falsch lag — trotz erdrückender Beweise",
            "schreibt „lol“ mit komplett leerem Gesichtsausdruck",
            "könnte über ein kabelloses Telefon stolpern",
            "ist das menschliche Äquivalent eines Ladebildschirms",
            "bringt einen Löffel zu einem Messerfight mit",
            "würde sich in einem Einbahnflur verlaufen",
            "hat Main-Character-Energie, aber NPC-Dialoge",
            "verströmt starke „Ich habe die Anleitung nicht gelesen“-Vibes",
            "ist der Beweis, dass Autopilot-Modus bei Menschen existiert",
            "hat die Reaktionszeit von Internet Explorer",
            "würde mit einem Stoppschild diskutieren und trotzdem verlieren",
            "hat die Persönlichkeit von ungewürztem Hähnchen",
            "denkt, „Gaslighting“ sei eine Herdmarke",
            "könnte kein Wasser aus einem Stiefel schütten, selbst wenn die Anleitung auf der Sohle steht",
            "sieht aus, als würde man klatschen, wenn das Flugzeug landet",
            "hat Gedanken mit WLAN, aber Umsetzung mit Modem",
            "ist der Grund, warum Gruppenarbeiten stressig sind",
            "lebt von Vibes und null kritischem Denken",
            "hat die emotionale Bandbreite eines Teelöffels",
            "drückt den Aufzugknopf zweimal, als würde das helfen",
            "hat große „Vertrau mir, Bruder“-Energie",
            "ist der Endboss schlechter Entscheidungen",
            "schreibt ganze Absätze, um absolut nichts zu sagen",
            "hat die Situationswahrnehmung einer Kartoffel",
            "würde den eigenen Geburtstag vergessen",
            "sieht aus wie ein Platzhalter-Charakter",
            "denkt, Müsli sei eine Suppe und verteidigt diese Meinung",
            "hat den Ehrgeiz, aber nicht die Fähigkeiten",
            "ist allergisch gegen gesunden Menschenverstand",
            "würde im echten Leben geratioed werden",
            "hat die Ausstrahlung eines stummgeschalteten Mikrofons",
            "könnte eine Aufgabe mit nur einem Knopf versauen",
            "läuft mit 2 % Akku und schlechten Entscheidungen",
            "hat das Selbstvertrauen von jemandem, der nicht zu beschämen ist",
            "ist der Beweis, dass die Evolution manchmal Pausen macht",
            "bringt nichts an den Tisch und isst trotzdem mit",
            "hat die Energie einer vergessenen Nebenquest",
            "würde einen Starrwettbewerb gegen eine Wand verlieren",
            "hat dauerhaft das Lade-Symbol im Gehirn",
            "denkt, „BRB“ sei eine langfristige Verpflichtung",
            "ist die menschliche Version eines Tippfehlers",
            "würde im Ozean kein Wasser finden",
            "hat das Charisma einer feuchten Socke",
            "steht auf gutem Fuß mit schlechten Entscheidungen",
            "hat die Aufmerksamkeitsspanne eines Goldfischs auf TikTok",
            "würde aus dem Singleplayer-Modus gebannt werden",
            "liegt irgendwie immer falsch — mit Selbstvertrauen",
            "hat die Vibes einer gesprungenen Displayschutzfolie",
            "sieht aus, als würde man „dir auch“ sagen, wenn der Kellner „Guten Appetit“ wünscht",
            "ist gebaut wie ein Patchnote, den niemand wollte",
            "würde den eigenen Namen falsch schreiben",
            "hat große „Ich hatte meinen Höhepunkt im Tutorial“-Energie",
            "existiert nur, um den Durchschnitt zu senken",
            "hat die emotionale Intelligenz eines Toasters",
            "würde mit Google Maps streiten",
            "ist ein wandelndes Plotloch",
            "hat die Energie eines toten Gruppen-Chats",
            "ist der Grund, warum „Bist du sicher?“-Buttons existieren",
        ]
        embed = Embed(color=Color.random())
        if member:
            roast = f"{member} ist die Art von Person, die {choice(ROASTS)}"
        else:
            roast = f"Du bist die Art von Person, die {choice(ROASTS)}"
        embed.description = roast
        await ctx.followup.send(embed=embed)

    async def mock(self, ctx: Interaction, text: str):
        await ctx.response.defer()
        mocked = "".join(
            letter.upper() if randint(0, 1) else letter.lower() for letter in text
        )
        embed = Embed(
            title="🗣️ Spott-Generator",
            description=mocked,
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)
