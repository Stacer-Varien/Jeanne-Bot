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


class Guess_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def free(self, ctx: Interaction):
        view = Guess_Buttons(ctx.user)
        await ctx.response.defer()
        await ctx.followup.send(
            embed=Embed(
                description="Devinez mon numéro en cliquant sur l'un des boutons ci-dessous",
                color=Color.random(),
            ),
            view=view,
        )
        answer = randint(1, 10)
        await view.wait()
        if view.value == answer:
            await Currency(ctx.user).add_qp(20)
            correct = Embed(
                description=f"OUI! VOUS AVEZ DEVINEZ CORRECTEMENT!\nVous avez reçu {qp(ctx, 20)}!",
                color=Color.random(),
            )

            if await BetaTest(self.bot).check(ctx.user):
                await Currency(ctx.user).add_qp(Currency.normalize_qp(20 * 1.25))
                correct.add_field(
                    name="Beta User Bonus",
                    value=qp(ctx, Currency.normalize_qp(20 * 1.25)),
                )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.edit_original_response(embed=correct, view=None)
            return
        wrong = Embed(
            description=f"Mauvaise réponse. C'était {answer}", color=Color.red()
        )
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
                description=f"Votre solde est trop bas!\nVeuillez parier moins de {qp(ctx, balance)}"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Malheureusement, vous avez {qp(ctx, 0)}."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Guess_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Devinez mon numéro en cliquant sur l'un des boutons ci-dessous",
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        answer = randint(1, 10)
        if view.value == answer:
            await Currency(ctx.user).add_qp(bet)
            correct = Embed(
                description=f"OUI! VOUS AVEZ DEVINEZ CORRECTEMENT!\n{qp(ctx, bet)} a été ajouté",
                color=Color.random(),
            )
            if await BetaTest(self.bot).check(ctx.user):
                await Currency(ctx.user).add_qp(Currency.normalize_qp(bet * 1.25))
                correct.add_field(
                    name="Beta User Bonus",
                    value=qp(ctx, Currency.normalize_qp(bet * 1.25)),
                )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.followup.send(embed=correct, view=view)
            return
        await Currency(ctx.user).remove_qp(bet)
        wrong = Embed(
            description=f"Mauvaise réponse. C'était {answer}\nJe suis désolé mais je dois vous prendre {qp(ctx, bet)}",
            color=Color.red(),
        )
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.followup.send(embed=wrong)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
            description=f"Vous avez déjà utilisé votre chance gratuite\nEssayez à nouveau après <t:{reset_hour}:R>",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        cooldown = Embed(
            description=f"WOAH! Calmez-vous!\nEssayez à nouveau après `{round(error.retry_after, 2)} secondes`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)


class Dice_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        view = Dice_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Quel numéro pensez-vous que le dé va rouler?",
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
                name=f"YAY! Vous avez eu raison!\n{qp(ctx, 20)} a été ajouté",
                value=f"Le dé a roulé: **{rolled}**\nVous avez deviné: **{view.value}**!",
                inline=False,
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        embed = Embed(
            description=f"Oh non. Il a roulé un **{rolled}**", color=Color.red()
        )
        await ctx.edit_original_response(embed=embed, view=None)

    async def bet(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Votre solde est trop bas!\nVeuillez parier moins de {qp(ctx, balance)}"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Malheureusement, vous avez {qp(ctx, 0)}."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Dice_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Quel numéro pensez-vous que le dé va rouler?",
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
                name=f"YAY! Vous avez eu raison!\n{qp(ctx, bet)} a été ajouté",
                value=f"Le dé a roulé: **{rolled}**\nVous avez deviné: **{view.value}**!",
                inline=False,
            )
            if await BetaTest(self.bot).check(ctx.user):
                await Currency(ctx.user).add_qp(Currency.normalize_qp(bet * 1.25))
                embed.add_field(
                    name="Beta User Bonus",
                    value=qp(ctx, Currency.normalize_qp(bet * 1.25)),
                )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        await Currency(ctx.user).remove_qp(bet)
        embed = Embed(color=Color.red())
        embed = Embed(
            description=f"Oh no. It rolled a **{rolled}**\nJe suis désolé mais je dois vous prendre {qp(ctx, bet)}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=embed, view=None)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
            description=f"Vous avez déjà utilisé votre chance gratuite\nEssayez à nouveau après <t:{reset_hour}:R>",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        cooldown = Embed(
            description=f"WOAH! Calmez-vous!\nEssayez à nouveau après `{round(error.retry_after, 2)} secondes`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)


class Flip_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        picks = ["Pile", "Face"]
        jeannes_pick = choice(picks)
        view = Heads_or_Tails(ctx, ctx.user)
        ask = Embed(description="Pile ou Face ?", color=Color.random())
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.user).add_qp(20)
            embed = Embed(
                description=f"YAY! Vous avez trouvé !\n{qp(ctx, 20)} ont été ajoutés",
                color=Color.random(),
            )

            if await BetaTest(self.bot).check(ctx.user):
                await Currency(ctx.user).add_qp(Currency.normalize_qp(20 * 1.25))
                embed.add_field(
                    name="Bonus Utilisateur Beta",
                    value=qp(ctx, Currency.normalize_qp(20 * 1.25)),
                )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            embed = Embed(
                description=f"Oh non, c'était {jeannes_pick}",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Désolé, mais vous avez mis trop de temps. C'était {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)

    async def bet(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        picks = ["Pile", "Face"]
        jeannes_pick = choice(picks)
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Votre solde est trop bas !\nVeuillez parier moins de {qp(ctx, balance)}"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Malheureusement, vous avez {qp(ctx, 0)}."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Heads_or_Tails(ctx, ctx.user)
        ask = Embed(description="Pile ou Face ?")
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.user).add_qp(bet)
            embed = Embed(
                description=f"YAY! Vous avez trouvé !\n{qp(ctx, bet)} ont été ajoutés"
            )

            if await BetaTest(self.bot).check(ctx.user):
                await Currency(ctx.user).add_qp(Currency.normalize_qp(bet * 1.25))
                embed.add_field(
                    name="Bonus Utilisateur Beta",
                    value=qp(ctx, Currency.normalize_qp(bet * 1.25)),
                )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            await Currency(ctx.user).remove_qp(int(bet))
            embed = Embed(
                description=f"Oh non, c'était {jeannes_pick}\nJe suis désolé mais je dois vous prendre {qp(ctx, bet)}",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Désolé, mais vous avez mis trop de temps. C'était {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)

    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
            description=f"Vous avez déjà utilisé votre chance gratuite\nEssayez à nouveau après <t:{reset_hour}:R>",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        cooldown = Embed(
            description=f"WOAH! Calmez-vous !\nEssayez à nouveau après `{round(error.retry_after, 2)} secondes`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)


class Blackjack_Group:
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
                description="Désolé, mais vous avez pris trop de temps. Veuillez réessayer",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)

    async def bet(self, ctx: Interaction, bet: int):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Votre solde est trop bas!\nVeuillez parier moins de {qp(ctx, balance)}"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description=f"Malheureusement, vous avez {qp(ctx, 0)}."
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
                description="Désolé, mais vous avez pris trop de temps. Veuillez réessayer",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)


class currency:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def qp(ctx: Interaction, amount: int) -> str:
        return qp(ctx, amount)

    async def balance_callback_error(self, ctx: Interaction, error: Exception):
        cooldown = Embed(
            description=f"WOAH! Calmez-vous!\nEssayez à nouveau après `{round(error.retry_after, 2)} secondes`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def get_balance(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        bal = Currency(member).get_balance
        balance = Embed(
            description=f"{'Vous' if (member == ctx.user) else member} avez {self.qp(ctx, bal)}",
            color=Color.blue(),
        )
        balance.add_field(
            name=f"Si vous souhaitez plus de {ServerSettings(ctx.guild).currency_name}:",
            value="[Vote for me in TopGG](https://top.gg/bot/831993597166747679/vote)",
            inline=True,
        )
        await ctx.followup.send(embed=balance)

    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        bank = Currency(ctx.user)
        next_claim = await bank.claim_daily()
        if next_claim is not None:
            daily = Embed(
                title="Quotidien",
                description=f"**{ctx.user}**, vous avez réclamé votre récompense quotidienne.",
                color=Color.random(),
            )
            check_beta = await BetaTest(self.bot).check(ctx.user)
            is_weekend = datetime.today().weekday() >= 5
            rewards_text = "Récompenses (week-end)" if is_weekend else "Récompenses"
            rewards_value = (
                f"Vous avez reçu {self.qp(ctx, 200)}"
                if is_weekend
                else f"Vous avez reçu {self.qp(ctx, 100)}"
            )
            bonus_text = "Bonus Beta (week-end)" if is_weekend else "Bonus Beta"
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
                name="Solde",
                value=self.qp(ctx, bank.get_balance),
            )
            daily.add_field(name="Prochain quotidien :", value=f"<t:{next_claim}:f>")
            await ctx.followup.send(embed=daily)
        else:
            next_daily = bank.check_daily
            cooldown = Embed(
                description=f"Vous avez déjà réclamé votre quotidien.\nVotre prochaine réclamation est <t:{next_daily}:R>",
                color=Color.red(),
            )
            await ctx.followup.send(embed=cooldown)

    async def balance_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
        cooldown = Embed(
            description=f"WOAH! Calmez-vous! Pourquoi vérifier encore si rapidement ?\nRéessayez après `{round(error.retry_after, 2)} secondes`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)

    async def vote(self, ctx: Interaction):
        embed = Embed(
            color=Color.random(),
            description="Vous pouvez voter pour moi en cliquant sur l'un des boutons ci-dessous pour obtenir les avantages suivants :",
        )
        topgg_perks = """
- 5XP multipliés par leur niveau global
- - Les récompenses sont doublées le week-end
"""
        topgg_perks = f"- {self.qp(ctx, 100)}\n{topgg_perks}"
        embed.add_field(name="Avantages du vote", value=topgg_perks, inline=True)
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
                    description=f"Votre solde est trop bas!\nVeuillez parier moins de {self.qp(ctx, balance)}",
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

        embed.description = f"🎰 **MACHINE À SOUS**\n{format_grid(grid)}\n\nLancement..."
        await ctx.edit_original_response(embed=embed)

        for _ in range(8):
            await asyncio.sleep(0.95)
            grid = spin_grid()
            embed.color = Color.random()
            embed.description = f"🎰 **MACHINE À SOUS**\n{format_grid(grid)}\n\nLancement..."
            await ctx.edit_original_response(embed=embed)

        await asyncio.sleep(0.6)
        final_grid = spin_grid()
        middle = final_grid[3:6]  

        payout = 0
        # Translation for loss
        result_text = f"💀 Vous avez perdu **{self.qp(ctx, bet)}**."
        await Currency(ctx.user).remove_qp(bet)

        if middle == ["💎", "💎", "💎"]:
            payout = bet * 10
            result_text = f"💎💎💎 **JACKPOT LÉGENDAIRE !**\nVous avez gagné **{self.qp(ctx, payout)}** !"
        elif middle == ["⭐", "⭐", "⭐"]:
            payout = bet * 5
            result_text = f"⭐ **Triple Étoile !**\nVous avez gagné **{self.qp(ctx, payout)}** !"
        elif middle == ["🔔", "🔔", "🔔"]:
            payout = bet * 3
            result_text = f"🔔 **Triple Cloche !**\nVous avez gagné **{self.qp(ctx, payout)}** !"
        elif middle.count("🍉") == 3:
            payout = bet * 2
            result_text = f"🍉 **Triple Pastèque !**\nVous avez gagné **{self.qp(ctx, payout)}** !"
        elif middle.count("🍒") == 3:
            payout = bet
            result_text = "🍒 **Tout juste.**\nVotre mise vous a été remboursée."

        if payout > 0:
            await Currency(ctx.user).add_qp(payout)

        embed.description = (
                f"🎰 **RÉSULTAT**\n" f"{format_grid(final_grid)}\n\n" f"{result_text}"
            )

        await ctx.edit_original_response(embed=embed)

    async def slots_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        cooldown = Embed(
            description=f"WOAH! Calmez-vous!\nEssayez à nouveau après `{round(error.retry_after, 2)} secondes`",
            color=Color.red(),
        )
        await ctx.response.send_message(embed=cooldown)
    
    async def spin_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            cooldown = Embed(
                description=f"WOAH! Calmez-vous!\nEssayez à nouveau après `{round(error.retry_after, 2)} secondes`",
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

        await ctx.response.send_message("🎡 Faire tourner la roue...")
        message = await ctx.original_response()

        total_spins = randint(20, 28)
        current_index = 0

        for i in range(total_spins):
            wheel_visual = wheel.build_wheel(multipliers, current_index)

            embed = Embed(
                title="🎡 Filage...", description=wheel_visual, color=Color.gold()
            )

            await message.edit(embed=embed)
            current_index = (current_index + 1) % 8
            await asyncio.sleep(0.07 + (i / total_spins) * 0.3)

        wheel_visual = wheel.build_wheel(multipliers, winner_index)

        winnings = Currency.normalize_qp(bet * winner_multiplier)

        if winnings > 0:
            won = await Currency(ctx.user).add_qp(winnings)
            result_text = f"🎉 Vous avez gagné {self.qp(ctx, won)}!"
            color = Color.green()
        elif winnings < 0:
            lost = await Currency(ctx.user).remove_qp(abs(winnings))
            result_text = (
                f"💀 Vous avez perdu {self.qp(ctx, lost)}..."
            )
            color = Color.red()
        else:
            result_text = "😐 Vous êtes à zéro !"
            color = Color.blurple()

        final_embed = Embed(
            title="🎯 Résultat de la roue", description=wheel_visual, color=color
        )
        final_embed.add_field(name="💰 Mise", value=self.qp(ctx, bet))
        final_embed.add_field(name="📈 Multiplicateur", value=f"{winner_multiplier}x")
        final_embed.add_field(name="🏆 Résultat", value=result_text)

        await message.edit(embed=final_embed)
