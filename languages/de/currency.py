import asyncio
from random import choice, randint, shuffle
import random
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
from assets.spinwheel import Wheel
from functions import (
    BetaTest,
    Currency,
    ServerSettings,
)


def qp(ctx: Interaction, amount: int) -> str:
    return ServerSettings.format_currency_for(ctx.guild, amount)


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

    async def free(self, ctx: Interaction):
        view = Guess_Buttons(ctx.user)
        await ctx.response.defer()
        await ctx.followup.send(
            embed=Embed(
                description="Rate meine Zahl, indem du auf einen der untenstehenden Buttons klickst",
                color=Color.random(),
            ),
            view=view,
        )
        answer = randint(1, 10)
        await view.wait()
        if view.value == answer:
            await Currency(ctx.user).add_qp(20)
            correct = Embed(
                description=f"JA! DU HAST RICHTIG GERATEN!\nDu hast {qp(ctx, 20)} erhalten!",
                color=Color.random(),
            )
            
            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(Currency.normalize_qp(20 * 1.25))
                    correct.add_field(
                        name="Beta-Benutzer-Bonus",
                        value=qp(ctx, Currency.normalize_qp(20 * 1.25)),
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.edit_original_response(embed=correct, view=None)
            return
        wrong = Embed(description=f"Falsche Antwort. Es war {answer}", color=Color.red())
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
                description=f"Dein Guthaben ist zu niedrig!\nSetze weniger als {qp(ctx, balance)} ein"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Leider hast du {qp(ctx, 0)}."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Guess_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Rate meine Zahl, indem du auf einen der untenstehenden Buttons klickst",
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        answer = randint(1, 10)
        if view.value == answer:
            await Currency(ctx.user).add_qp(bet)
            correct = Embed(
                description=f"JA! DU HAST RICHTIG GERATEN!\nDu hast {qp(ctx, bet)} erhalten!",
                color=Color.random(),
            )
            
            
            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(Currency.normalize_qp(bet * 1.25))
                    correct.add_field(
                        name="Beta-Benutzer-Bonus",
                        value=qp(ctx, Currency.normalize_qp(bet * 1.25)),
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.followup.send(embed=correct, view=view)
            return
        await Currency(ctx.user).remove_qp(bet)
        wrong = Embed(
            description=f"Falsche Antwort. Es war {answer}\nLeider muss ich {qp(ctx, bet)} von dir nehmen...",
            color=Color.red(),
        )
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.followup.send(embed=wrong)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"Du hast deine kostenlose Chance bereits genutzt\nVersuche es erneut in <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Ruhig Blut!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Dice_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        view = Dice_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Was denkst du, wird der Würfel würfeln?",
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
                name=f"YAY! Du hast es richtig!\n{qp(ctx, 20)} wurden hinzugefügt",
                value=f"Der Würfel zeigte: **{rolled}**\nDu hast gewettet auf: **{view.value}**!",
                inline=False,
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        embed = Embed(description=f"Oh nein. Es wurde ein **{rolled}**", color=Color.red())
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
                description=f"Dein Guthaben ist zu niedrig!\nSetze weniger als {qp(ctx, balance)} ein"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Leider hast du {qp(ctx, 0)}."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Dice_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Was denkst du, wird der Würfel würfeln?",
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
                name=f"YAY! Du hast es richtig!\n{qp(ctx, bet)} wurden hinzugefügt",
                value=f"Der Würfel zeigte: **{rolled}**\nDu hast gewettet auf: **{view.value}**!",
                inline=False,
            )
            
            

            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(Currency.normalize_qp(bet * 1.25))
                    embed.add_field(
                        name="Beta-Benutzer-Bonus",
                        value=qp(ctx, Currency.normalize_qp(bet * 1.25)),
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        await Currency(ctx.user).remove_qp(bet)
        embed = Embed(color=Color.red())
        embed = Embed(description=f"Oh nein. Es wurde ein **{rolled}**", color=Color.red())
        await ctx.edit_original_response(embed=embed, view=None)


    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"Du hast deine kostenlose Chance bereits genutzt\nVersuche es erneut in <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Ruhig Blut!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Flip_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

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
                description=f"YAY! Du hast es richtig!\n{qp(ctx, 20)} wurden hinzugefügt",
                color=Color.random(),
            )
            
            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(Currency.normalize_qp(20 * 1.25))
                    embed.add_field(
                        name="Beta-Benutzer-Bonus",
                        value=qp(ctx, Currency.normalize_qp(20 * 1.25)),
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh nein, es war {}".format(jeannes_pick),
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Tut mir leid, du hast zu lange gebraucht. Es war {jeannes_pick}",
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
                description=f"Dein Guthaben ist zu niedrig!\nSetze weniger als {qp(ctx, balance)} ein"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Leider hast du {qp(ctx, 0)}."
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
                description=f"YAY! Du hast es richtig!\n{qp(ctx, bet)} wurden hinzugefügt"
            )
            
            

            if await BetaTest(self.bot).check(ctx.user):
                    await Currency(ctx.user).add_qp(Currency.normalize_qp(bet * 1.25))
                    embed.add_field(
                        name="Beta-Benutzer-Bonus",
                        value=qp(ctx, Currency.normalize_qp(bet * 1.25)),
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            await Currency(ctx.user).remove_qp(int(bet))
            embed = Embed(color=Color.red())
            embed = Embed(
                description=f"Oh nein, es war {jeannes_pick}\nEs tut mir leid, aber ich muss {qp(ctx, bet)} von dir nehmen",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Tut mir leid, du hast zu lange gebraucht. Es war {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"Du hast deine kostenlose Chance bereits genutzt\nVersuche es erneut in <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Ruhig Blut!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
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
                description="Tut mir leid, du hast zu lange gebraucht. Versuche es erneut",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)

    async def bet(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Dein Guthaben ist zu niedrig!\nSetze weniger als {qp(ctx, balance)} ein"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Leider hast du {qp(ctx, 0)}."
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
                description="Tut mir leid, du hast zu lange gebraucht. Versuche es erneut",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
            description=f"Du hast deine kostenlose Chance bereits genutzt\nVersuche es erneut in <t:{reset_hour}:R>",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        cooldown = Embed(
            description=f"WOAH! Ruhig Blut!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)


class currency():
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def qp(ctx: Interaction, amount: int) -> str:
        return qp(ctx, amount)

    async def balance_callback_error(self, ctx: Interaction, error: Exception):
        cooldown = Embed(
                description=f"WOAH! Ruhig Blut! Warum kontrollierst du so oft?\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
        await ctx.response.send_message(embed=cooldown)

    async def get_balance(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        bal = Currency(member).get_balance
        balance = Embed(
            description=f"{'Du' if (member == ctx.user) else member} hat {self.qp(ctx, bal)}",
            color=Color.blue(),
        )
        balance.add_field(
            name=f"Wenn du mehr {ServerSettings(ctx.guild).currency_name} möchtest:",
            value="[Stem op mij in TopGG](https://top.gg/bot/831993597166747679/vote)",
            inline=True,
        )
        await ctx.followup.send(embed=balance)

    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        bank = Currency(ctx.user)
        next_claim = await bank.claim_daily()
        if next_claim is not None:
            daily = Embed(
                title="Daily",
                description=f"**{ctx.user}**, du hast deine tägliche Belohnung eingelöst.",
                color=Color.random(),
            )
            check_beta = await BetaTest(self.bot).check(ctx.user)
            is_weekend = datetime.today().weekday() >= 5
            rewards_text = "Beloningen (weekend):" if is_weekend else "Beloningen:"
            rewards_value = (
                f"Du hast {self.qp(ctx, 200)} erhalten"
                if is_weekend
                else f"Du hast {self.qp(ctx, 100)} erhalten"
            )
            bonus_text = "Beta Bonus (weekend)" if is_weekend else "Beta Bonus"
            bonus_value = (
                self.qp(ctx, 50)
                if is_weekend
                else self.qp(ctx, 25)
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
                value=self.qp(ctx, bank.get_balance),
            )
            daily.add_field(name="Nächster Daily:", value=f"<t:{next_claim}:f>")
            await ctx.followup.send(embed=daily)
        else:
            next_daily = bank.check_daily
            cooldown = Embed(
                description=f"Du hast deine tägliche Belohnung bereits eingelöst.\nDein nächster Anspruch ist in <t:{next_daily}:R>",
                color=Color.red(),
            )
            await ctx.followup.send(embed=cooldown)

    async def balance_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
        cooldown = Embed(
                description=f"WOAH! Ruhig Blut! Warum kontrollierst du so oft?\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
        await ctx.response.send_message(embed=cooldown)

    async def vote(self, ctx: Interaction):
        embed = Embed(
            color=Color.random(),
            description="Du kannst für mich stimmen, indem du auf einen der untenstehenden Buttons klickst, um folgende Vorteile zu erhalten:",
        )
        topgg_perks = """
- 5XP keer hun wereldwijde niveau
- - Beloningen zijn dubbel in het weekend
"""
        topgg_perks = f"- {self.qp(ctx, 100)}\n{topgg_perks}"
        embed.add_field(name="Stimmvorteile", value=topgg_perks, inline=True)
        await ctx.response.send_message(
            embed=embed,
            view=vote_button(),
        )

    async def slots(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            await ctx.followup.send(
                embed=Embed(
                    description=f"Dein Guthaben ist zu niedrig!\nSetze weniger als {self.qp(ctx, balance)} ein",
                    color=Color.red(),
                )
            )
            return

        emojis = (
                ["🍒"] * 60 
                + ["🍋"] * 25
                + ["🍉"] * 10 
                + ["🔔"] * 4 
                + ["⭐"] * 1 
                + ["💎"] * 0 
            )

        def spin_symbol():
            if randint(1, 2000) == 1: 
                return "💎"
            return choice(emojis)

        def spin_grid():
            return [spin_symbol() for _ in range(9)]

        def format_grid(grid):
            return (
                    f"{grid[0]} {grid[1]} {grid[2]}\n"
                    f"{grid[3]} {grid[4]} {grid[5]}  ⬅️\n"
                    f"{grid[6]} {grid[7]} {grid[8]}"
                )

        grid = spin_grid()

        embed.description = f"🎰 **SPIELAUTOMAT**\n{format_grid(grid)}\n\nAm Drehen..."
        await ctx.edit_original_response(embed=embed)

        for _ in range(8):
            await asyncio.sleep(0.95)
            grid = spin_grid()
            embed.color = Color.random()
            embed.description = f"🎰 **SPIELAUTOMAT**\n{format_grid(grid)}\n\nAm Drehen..."
            await ctx.edit_original_response(embed=embed)

        await asyncio.sleep(0.6)
        final_grid = spin_grid()
        middle = final_grid[3:6]  

        payout = 0

        result_text = f"💀 Du hast **{self.qp(ctx, bet)}** verloren."
        await Currency(ctx.user).remove_qp(bet)

        if middle == ["💎", "💎", "💎"]:
            payout = bet * 10
            result_text = f"💎💎💎 **LEGENDÄRER JACKPOT!**\nDu hast **{self.qp(ctx, payout)}** gewonnen!"
        elif middle == ["⭐", "⭐", "⭐"]:
            payout = bet * 5
            result_text = f"⭐ **Dreifache Sterne!**\nDu hast **{self.qp(ctx, payout)}** gewonnen!"
        elif middle == ["🔔", "🔔", "🔔"]:
            payout = bet * 3
            result_text = f"🔔 **Dreifache Glocken!**\nDu hast **{self.qp(ctx, payout)}** gewonnen!"
        elif middle.count("🍉") == 3:
            payout = bet * 2
            result_text = f"🍉 **Dreifache Melonen!**\nDu hast **{self.qp(ctx, payout)}** gewonnen!"
        elif middle.count("🍒") == 3:
            payout = bet
            result_text = "🍒 **Knapp gewonnen.**\nEinsatz zurückerstattet."

        if payout > 0:
            await Currency(ctx.user).add_qp(payout)

        embed.description = (
                f"🎰 **ERGEBNIS**\n" f"{format_grid(final_grid)}\n\n" f"{result_text}"
            )

        await ctx.edit_original_response(embed=embed)

    async def slots_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        cooldown = Embed(
                description=f"WOAH! Ruhig Blut!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
        await ctx.response.send_message(embed=cooldown)

    async def spin(self, ctx: Interaction, bet: int):
        wheel = Wheel()
        negatives = [round(random.uniform(-2.0, -0.5), 1) for _ in range(5)]
        small_positives = [round(random.uniform(0.1, 0.5), 1) for _ in range(2)]
        big_positive = [round(random.uniform(1.5, 2.0), 1)]

        multipliers = negatives + small_positives + big_positive
        random.shuffle(multipliers)

        negative_indexes = [i for i, m in enumerate(multipliers) if m < 0]
        small_positive_indexes = [i for i, m in enumerate(multipliers) if 0 < m <= 0.5]
        big_positive_index = [i for i, m in enumerate(multipliers) if m > 1][0]

        roll = random.random()

        if roll <= 0.80:
            winner_index = random.choice(negative_indexes)
        elif roll <= 0.98:
            winner_index = random.choice(small_positive_indexes)
        else:
            winner_index = big_positive_index

        winner_multiplier = multipliers[winner_index]

        await ctx.response.send_message("🎡 Das Rad dreht sich...")
        message = await ctx.original_response()

        total_spins = randint(20, 28)
        current_index = 0

        for i in range(total_spins):
            wheel_visual = wheel.build_wheel(multipliers, current_index)

            embed = Embed(
                title="🎡 Spinnen...", description=wheel_visual, color=Color.gold()
            )

            await message.edit(embed=embed)
            current_index = (current_index + 1) % 8
            await asyncio.sleep(0.07 + (i / total_spins) * 0.3)

        wheel_visual = wheel.build_wheel(multipliers, winner_index)

        winnings = Currency.normalize_qp(bet * winner_multiplier)

        if winnings > 0:
            won = await Currency(ctx.user).add_qp(winnings)
            result_text = f"🎉 Du hast {self.qp(ctx, won)} gewonnen!"
            color = Color.green()
        elif winnings < 0:
            lost = await Currency(ctx.user).remove_qp(abs(winnings))
            result_text = (
                f"💀 Du hast {self.qp(ctx, lost)} verloren..."
            )
            color = Color.red()
        else:
            result_text = "😐 Du hast das Spiel ausgeglichen!"
            color = Color.blurple()

        final_embed = Embed(
            title="🎯 Radergebnis", description=wheel_visual, color=color
        )
        final_embed.add_field(name="💰 Wette", value=self.qp(ctx, bet))
        final_embed.add_field(name="📈 Multiplikator", value=f"{winner_multiplier}x")
        final_embed.add_field(name="🏆 Ergebnis", value=result_text)

        await message.edit(embed=final_embed)

    async def spin_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        cooldown = Embed(
                description=f"WOAH! Ruhig Blut!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.red(),
            )
        await ctx.response.send_message(embed=cooldown)
