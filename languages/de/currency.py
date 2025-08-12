from random import choice, randint, shuffle
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Member,
    app_commands as Jeanne,
    Interaction,
    ui,
)
from datetime import datetime, timedelta
from discord.ext.commands import Bot
from assets.blackjack_game import BlackjackView
from assets.components import Dice_Buttons, Guess_Buttons, Heads_or_Tails
from functions import (
    BetaTest,
    Currency,
)
from config import TOPGG
from topgg import DBLClient


class vote_button(ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="Top.gg",
                url="https://top.gg/bot/831993597166747679/vote",
            )
        )


class Guess_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    async def free(self, ctx: Interaction):
        view = Guess_Buttons(ctx.user)
        await ctx.response.defer()
        await ctx.followup.send(
            embed=Embed(
                description="Raad mijn nummer door op een van de onderstaande knoppen te klikken",
                color=Color.random(),
            ),
            view=view,
        )
        answer = randint(1, 10)
        await view.wait()
        if view.value == answer:
            await Currency(ctx.user).add_qp(20)
            correct = Embed(
                description="JA! JE HEBT HET GOED GERADEN!\nJe hebt 20 <:quantumpiece:1161010445205905418> ontvangen!",
                color=Color.random(),
            )
            
            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(round((20 * 1.25), 2))
                    correct.add_field(
                        name="Beta Gebruiker Bonus",
                        value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.edit_original_response(embed=correct, view=None)
            return
        wrong = Embed(description=f"Fout antwoord. Het was {answer}", color=Color.red())
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.edit_original_response(embed=wrong, view=None)


    async def bet(
        self,
        ctx: Interaction,
        bet: int,
    ):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Je saldo is te laag!\nZet minder dan {balance} <:quantumpiece:1161010445205905418> in"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Helaas heb je 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Guess_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Raad mijn nummer door op een van de onderstaande knoppen te klikken",
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        answer = randint(1, 10)
        if view.value == answer:
            await Currency(ctx.user).add_qp(bet)
            correct = Embed(
                description=f"JA! JE HEBT HET GOED GERADEN!\nJe hebt {bet} <:quantumpiece:1161010445205905418> ontvangen!",
                color=Color.random(),
            )
            
            
            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                    correct.add_field(
                        name="Beta Gebruiker Bonus",
                        value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.followup.send(embed=correct, view=view)
            return
        await Currency(ctx.user).remove_qp(bet)
        wrong = Embed(
            description=f"Fout antwoord. Het was {answer}\nHelaas moet ik {bet} <:quantumpiece:1161010445205905418> van je afnemen...",
            color=Color.red(),
        )
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.followup.send(embed=wrong)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"Je hebt je gratis kans al gebruikt\nProbeer het opnieuw na <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Rustig aan!\nProbeer het opnieuw na `{round(error.retry_after, 2)} seconden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Dice_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        view = Dice_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Wat denk je dat de dobbelsteen zal gooien?",
                color=Color.random(),
            ),
            view=view,
        )

        await view.wait()

        rolled = randint(1, 6)
        if view.value == rolled:
            await Currency(ctx.user).add_qp(20)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="YAY! Je hebt het goed!\nEr is 20 <:quantumpiece:1161010445205905418> toegevoegd",
                value=f"De dobbelsteen gooide: **{rolled}**\nJij gokte: **{view.value}**!",
                inline=False,
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        embed = Embed(description=f"Oh nee. Het werd een **{rolled}**", color=Color.red())
        await ctx.edit_original_response(embed=embed, view=None)


    async def bet(
        self,
        ctx: Interaction,
        bet: int
    ):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Je saldo is te laag!\nZet minder dan {balance} <:quantumpiece:1161010445205905418> in"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Helaas heb je 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Dice_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Wat denk je dat de dobbelsteen zal gooien?",
                color=Color.random(),
            ),
            view=view,
        )

        await view.wait()

        rolled = randint(1, 6)
        if view.value == rolled:
            await Currency(ctx.user).add_qp(bet)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! Je hebt het goed!\nEr is {bet} <:quantumpiece:1161010445205905418> toegevoegd",
                value=f"De dobbelsteen gooide: **{rolled}**\nJij gokte: **{view.value}**!",
                inline=False,
            )
            
            

            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                    embed.add_field(
                        name="Beta Gebruiker Bonus",
                        value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        await Currency(ctx.user).remove_qp(bet)
        embed = Embed(color=Color.red())
        embed = Embed(description=f"Oh nee. Het werd een **{rolled}**", color=Color.red())
        await ctx.edit_original_response(embed=embed, view=None)


    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"Je hebt je gratis kans al gebruikt\nProbeer het opnieuw na <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Rustig aan!\nProbeer het opnieuw na `{round(error.retry_after, 2)} seconden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Flip_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        view = Heads_or_Tails(ctx, ctx.user)
        ask = Embed(description="Heads or Tails?", color=Color.random())
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.user).add_qp(20)
            embed = Embed(
                description="YAY! Je hebt het goed!\n20 <:quantumpiece:1161010445205905418> is toegevoegd",
                color=Color.random(),
            )
            
            await Currency(ctx.user).add_qp(round((20 * 1.25), 2))

            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(round((20 * 1.25), 2))
                    embed.add_field(
                        name="Beta Gebruiker Bonus",
                        value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh nee, het was {}".format(jeannes_pick),
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Sorry maar je deed er te lang over. Het was {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)


    async def bet(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Je saldo is te laag!\nZet minder dan {balance} <:quantumpiece:1161010445205905418> in"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Helaas heb je 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Heads_or_Tails(ctx, ctx.user)
        ask = Embed(description="Heads or Tails?")
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.user).add_qp(bet)
            embed = Embed(
                description="YAY! Je hebt het goed!\n{} <:quantumpiece:1161010445205905418> is toegevoegd".format(
                    bet
                )
            )
            
            

            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                    embed.add_field(
                        name="Beta Gebruiker Bonus",
                        value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            await Currency(ctx.user).remove_qp(int(bet))
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh nee, het was {}\nHet spijt me, maar ik moet {} <:quantumpiece:1161010445205905418> van je afnemen".format(
                    jeannes_pick, bet
                ),
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Sorry maar je deed er te lang over. Het was {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"Je hebt je gratis kans al gebruikt\nProbeer het opnieuw na <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Rustig aan!\nProbeer het opnieuw na `{round(error.retry_after, 2)} seconden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Blackjack_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        def create_deck() -> list[tuple[str, str]]:
            return [(rank, suit) for suit in suits for rank in ranks]

        def deal_card(deck: list[tuple[str, str]]):
            return deck.pop(randint(0, len(deck) - 1))

        deck = create_deck()
        shuffle(deck)

        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]

        view = BlackjackView(self.bot, ctx, deck, player_hand, dealer_hand)
        await ctx.followup.send(embed=view.embed, view=view)

        await view.wait()

        if view.value is None:
            timeout = Embed(
                description="Sorry maar je deed er te lang over. Probeer het opnieuw",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)

    async def bet(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Je saldo is te laag!\nZet minder dan {balance} <:quantumpiece:1161010445205905418> in"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Helaas heb je 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        def create_deck() -> list[tuple[str, str]]:
            return [(rank, suit) for suit in suits for rank in ranks]

        def deal_card(deck: list[tuple[str, str]]):
            return deck.pop(randint(0, len(deck) - 1))

        deck = create_deck()
        shuffle(deck)

        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]

        view = BlackjackView(self.bot, ctx, deck, player_hand, dealer_hand, bet)
        await ctx.followup.send(embed=view.embed, view=view)

        await view.wait()

        if view.value is None:
            timeout = Embed(
                description="Sorry maar je deed er te lang over. Probeer het opnieuw",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
            description=f"Je hebt je gratis kans al gebruikt\nProbeer het opnieuw na <t:{reset_hour}:R>",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        cooldown = Embed(
            description=f"WOAH! Rustig aan!\nProbeer het opnieuw na `{round(error.retry_after, 2)} seconden`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)


class currency():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def balance_callback_error(self, ctx: Interaction, error: Exception):
            cooldown = Embed(
                description=f"WOAH! Rustig aan! Waarom blijf je zo snel controleren?\nProbeer het opnieuw na `{round(error.retry_after, 2)} seconden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def get_balance(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        bal = Currency(member).get_balance
        balance = Embed(
            description=f"{'Je' if (member == ctx.user) else member} heeft {bal} <:quantumpiece:1161010445205905418>",
            color=Color.blue(),
        )
        balance.add_field(
            name="Als je meer wilt <:quantumpiece:1161010445205905418>:",
            value="[Stem op mij in TopGG](https://top.gg/bot/831993597166747679/vote)",
            inline=True,
        )
        await ctx.followup.send(embed=balance)

    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        bank = Currency(ctx.user)
        tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())
        if bank.check_daily:
            await bank.give_daily()
            daily = Embed(
                title="Daily",
                description=f"**{ctx.user}**, je hebt je dagelijkse beloning opgeëist.",
                color=Color.random(),
            )
            check_beta = await BetaTest(self.bot).check(ctx.user)
            is_weekend = datetime.today().weekday() >= 5
            rewards_text = "Beloningen (weekend):" if is_weekend else "Beloningen:"
            rewards_value = (
                "Je hebt 200 <:quantumpiece:1161010445205905418> ontvangen"
                if is_weekend
                else "Je hebt 100 <:quantumpiece:1161010445205905418> ontvangen"
            )
            bonus_text = "Beta Bonus (weekend)" if is_weekend else "Beta Bonus"
            bonus_value = (
                "50 <:quantumpiece:1161010445205905418>"
                if is_weekend
                else "25 <:quantumpiece:1161010445205905418>"
            )
            daily.add_field(
                name=rewards_text,
                value=rewards_value,
            )
            if check_beta:
                await bank.add_qp(50 if is_weekend else 25)
                daily.add_field(
                    name=bonus_text,
                    value=bonus_value,
                )
            daily.add_field(
                name="Saldo",
                value=f"{bank.get_balance} <:quantumpiece:1161010445205905418>",
            )
            daily.add_field(name="Volgende Daily:", value=f"<t:{tomorrow}:f>")
            await ctx.followup.send(embed=daily)
        else:
            cooldown = Embed(
                description=f"Je hebt je dagelijkse beloning al opgeëist.\nJe volgende claim is <t:{bank.check_daily}:R>",
                color=Color.red(),
            )
            await ctx.followup.send(embed=cooldown)

    async def balance_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
            cooldown = Embed(
                description=f"WOAH! Rustig aan! Waarom blijf je zo snel controleren?\nProbeer het opnieuw na `{round(error.retry_after, 2)} seconden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def vote(self, ctx: Interaction):
        embed = Embed(
            color=Color.random(),
            description="Je kunt op mij stemmen door op een van de onderstaande knoppen te klikken om de volgende voordelen te krijgen:",
        )
        topgg_perks = """
- 100 QP
- 5XP keer hun wereldwijde niveau
- - Beloningen zijn dubbel in het weekend
"""
        embed.add_field(name="Stemvoordelen", value=topgg_perks, inline=True)
        await ctx.response.send_message(
            embed=embed,
            view=vote_button(),
        )
