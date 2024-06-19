from random import choice, randint, shuffle
from typing import Optional
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Member,
    Message,
    ui,
)
from datetime import datetime, timedelta
from discord.ext.commands import Cog, Bot, Context
import discord.ext.commands as Jeanne
from assets.blackjack_game import BlackjackView
from assets.components import Dice_Buttons, Guess_Buttons, Heads_or_Tails
from functions import (
    BetaTest,
    Currency,
    DBLvoter,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from config import DBL_AUTH


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
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="Discord Bot List",
                url="https://discordbotlist.com/bots/jeanne/upvote",
            )
        )


class CurrencyPrefix(Cog, name="Currency"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dbl = DBLvoter(self.bot, DBL_AUTH)

    @Jeanne.group(
        invoke_without_command=True,
        description="Main Guess command",
    )
    async def guess(self, ctx: Context): ...

    @guess.command(name="free", description="Guess my number and you can win 20 QP")
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def guess_free(self, ctx: Context):
        view = Guess_Buttons(ctx.author)
        m = await ctx.send(
            embed=Embed(
                description="Guess my number by clicking on one of the buttons below",
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        answer = randint(1, 10)
        if view.value == answer:
            await Currency(ctx.author).add_qp(20)
            correct = Embed(
                description="YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 <:quantumpiece:1161010445205905418>!",
                color=Color.random(),
            )
            if await self.dbl.get_user_vote(ctx.author) == True:
                await Currency(ctx.author).add_qp(round((20 * 1.25), 2))
                correct.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((20 * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                )
                if await BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.author).add_qp(round((20 * 1.25), 2))
                    correct.add_field(
                        name="Beta User Bonus",
                        value=f"{round(
                        (20 * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await m.edit(embed=correct, view=None)
            return
        wrong = Embed(description=f"Wrong answer. It was {answer}", color=Color.red())
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await m.edit(embed=wrong, view=None)

    @guess.command(
        name="bet",
        description="Guess my number and you can win with betting",
        usage="[BET]",
    )
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def guess_bet(self, ctx: Context, bet: Jeanne.Range[int, 5]):
        balance = Currency(ctx.author).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.send(embed=zerobal)
            return
        view = Guess_Buttons(ctx.author)
        m = await ctx.send(
            embed=Embed(
                description="Guess my number by clicking on one of the buttons below",
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        answer = randint(1, 10)
        if view.value == answer:
            await Currency(ctx.author).add_qp(bet)
            correct = Embed(
                description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {bet} <:quantumpiece:1161010445205905418>!",
                color=Color.random(),
            )
            if await self.dbl.get_user_vote(ctx.author) == True:
                await Currency(ctx.author).add_qp(round((bet * 1.25), 2))
                correct.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((bet * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                )
                if await BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.author).add_qp(round((bet * 1.25), 2))
                    correct.add_field(
                        name="Beta User Bonus",
                        value=f"{round(
                        (bet * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await m.edit(embed=correct, view=None)
            return
        await Currency(ctx.author).remove_qp(bet)
        wrong = Embed(
            description=f"Wrong answer. It was {answer}\nAfraid I have to take {bet} <:quantumpiece:1161010445205905418> from you...",
            color=Color.red(),
        )
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await m.edit(embed=wrong, view=None)

    @guess_free.error
    async def guess_free_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @guess_bet.error
    async def guess_bet_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @Jeanne.group(
        invoke_without_command=True,
        description="Main Dice command",
    )
    async def dice(self, ctx: Context): ...

    @dice.command(
        name="free", description="Roll a dice for free 20 QP", usage="[DIGIT]"
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    async def dice_free(self, ctx: Context):
        view = Dice_Buttons(ctx.author)
        m = await ctx.send(
            embed=Embed(
                description="What do you think the dice will roll?",
                color=Color.random(),
            ),
            view=view,
        )

        await view.wait()

        rolled = randint(1, 6)
        if view.value == rolled:
            await Currency(ctx.author).add_qp(20)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! You got it!\n20 <:quantumpiece:1161010445205905418> has been added",
                value=f"Dice rolled: **{rolled}**\nYou guessed: **{view.value}**!",
                inline=False,
            )
            if await self.dbl.get_user_vote(ctx.author) == True:
                await Currency(ctx.author).add_qp(round((20 * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((20 * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                )
                if await BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.author).add_qp(round((20 * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round(
                        (20 * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                    )
            await m.edit(embed=embed, view=None)
            return
        embed = Embed(description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
        await m.edit(embed=embed, view=None)

    @dice.command(
        name="bet", description="Roll a dice with betting", usage="[BET] [DIGIT]"
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    async def dice_bet(
        self,
        ctx: Context,
        bet: Jeanne.Range[int, 5],
    ):
        balance = Currency(ctx.author).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.send(embed=zerobal)
            return
        view = Dice_Buttons(ctx.author)
        m = await ctx.send(
            embed=Embed(
                description="What do you think the dice will roll?",
                color=Color.random(),
            ),
            view=view,
        )

        await view.wait()

        rolled = randint(1, 6)
        if view.value == rolled:
            await Currency(ctx.author).add_qp(bet)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! You got it!\n{bet} <:quantumpiece:1161010445205905418> has been added",
                value=f"Dice rolled: **{rolled}**\nYou guessed: **{view.value}**!",
                inline=False,
            )
            if await self.dbl.get_user_vote(ctx.author) == True:
                await Currency(ctx.author).add_qp(round((bet * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round(
                    (bet * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                )
                if await BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.author).add_qp(round((bet * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round((bet * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                    )
            await m.edit(embed=embed, view=None)
            return
        await Currency(ctx.author).remove_qp(bet)
        embed = Embed(color=Color.red())
        embed = Embed(description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
        await m.edit(embed=embed, view=None)

    @dice_free.error
    async def dice_free_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @dice_bet.error
    async def dice_bet_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @Jeanne.group(
        invoke_without_command=True,
        description="Main Flip command",
    )
    async def flip(self, ctx: Context): ...

    @flip.command(name="free", description="Flip a coin and earn 20 QP for free")
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def flip_free(self, ctx: Context):
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        view = Heads_or_Tails(ctx.author)
        ask = Embed(description="Heads or Tails?", color=Color.random())
        m: Message = await ctx.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.author).add_qp(20)
            embed = Embed(
                description="YAY! You got it!\n20 <:quantumpiece:1161010445205905418> has been added",
                color=Color.random(),
            )
            if await self.dbl.get_user_vote(ctx.author) == True:
                await Currency(ctx.author).add_qp(round((20 * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((20 * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                )
                if await BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.author).add_qp(round((20 * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round(
                        (20 * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                    )
            await m.edit(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh no, it was {}".format(jeannes_pick),
                color=Color.red(),
            )
            await m.edit(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Sorry but you took too long. It was {jeannes_pick}",
            color=Color.red(),
        )
        await m.edit(embed=timeout, view=None)

    @flip.command(
        name="bet", description="Flip a coin and earn with betting", usage="[BET]"
    )
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def flip_bet(self, ctx: Context, bet: Jeanne.Range[int, 5]):
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        balance = Currency(ctx.author).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.send(embed=zerobal)
            return
        view = Heads_or_Tails(ctx.author)
        ask = Embed(description="Heads or Tails?")
        m: Message = await ctx.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.author).add_qp(bet)
            embed = Embed(
                description="YAY! You got it!\n{} <:quantumpiece:1161010445205905418> has been added".format(
                    bet
                )
            )
            if await self.dbl.get_user_vote(ctx.author) == True:
                await Currency(ctx.author).add_qp(round((bet * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((bet * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                )
                if await BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.author).add_qp(round((bet * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round((bet * 1.25), 2)} <:quantumpiece:1161010445205905418>",
                    )
            await m.edit(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            await Currency(ctx.author).remove_qp(int(bet))
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh no, it was {}\nI'm afraid that I have to take {} <:quantumpiece:1161010445205905418> from you".format(
                    jeannes_pick, bet
                ),
                color=Color.red(),
            )
            await m.edit(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Sorry but you took too long. It was {jeannes_pick}",
            color=Color.red(),
        )
        await m.edit(embed=timeout, view=None)

    @flip_free.error
    async def flip_free_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @flip_bet.error
    async def flip_bet_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @Jeanne.group(
        aliases=["bj"],
        invoke_without_command=True,
        description="Main blackjack command",
    )
    async def blackjack(self, ctx: Context): ...

    @blackjack.command(
        name="free", description="Play a game of blackjack and earn 20 QP for free"
    )
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def bj_free(self, ctx: Context):
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

        view = BlackjackView(ctx, self.bot, deck, player_hand, dealer_hand, None)
        m = await ctx.send(embed=view.embed, view=view)

        await view.wait()

        if view.value == None:
            timeout = Embed(
                description=f"Sorry but you took too long. Please try again",
                color=Color.red(),
            )
            await m.edit(embed=timeout, view=None)

    @blackjack.command(name="bet", description="Play a game of blackjack and earn 20 QP for free")
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def bj_bet(self, ctx: Context, bet: Jeanne.Range[int, 5]):
        balance = Currency(ctx.author).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.send(embed=zerobal)
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

        view = BlackjackView(ctx, self.bot, deck, player_hand, dealer_hand, bet)
        m = await ctx.send(embed=view.embed, view=view)

        await view.wait()

        if view.value == None:
            timeout = Embed(
                description=f"Sorry but you took too long. Please try again",
                color=Color.red(),
            )
            await m.edit(embed=timeout, view=None)

    @bj_free.error
    async def bj_free_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @bj_bet.error
    async def bj_bet_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    async def get_balance(self, ctx: Context, member: Member):
        bal = Currency(member).get_balance
        balance = Embed(
            description=f"{'You have' if (member == ctx.author) else (str(member) + '\thas')} {bal} <:quantumpiece:1161010445205905418>",
            color=Color.blue(),
        )
        balance.add_field(
            name=f"If you want more <:quantumpiece:1161010445205905418>:",
            value="Vote for me by clicking the buttons below",
            inline=True,
        )
        await ctx.send(embed=balance, view=vote_button())

    @Jeanne.command(description="Claim your daily")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def daily(self, ctx: Context):
        bank = Currency(ctx.author)
        tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())
        if bank.check_daily == True:
            await bank.give_daily()
            daily = Embed(
                title="Daily",
                description=f"**{ctx.author}**, you claimed your daily reward.",
                color=Color.random(),
            )
            check_beta = await BetaTest(self.bot).check(ctx.author)
            is_weekend = datetime.today().weekday() >= 5
            rewards_text = "Rewards (weekend):" if is_weekend else "Rewards:"
            rewards_value = (
                "You received 200 <:quantumpiece:1161010445205905418>"
                if is_weekend
                else "You received 100 <:quantumpiece:1161010445205905418>"
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
                name="Balance",
                value=f"{bank.get_balance} <:quantumpiece:1161010445205905418>",
            )
            daily.add_field(name="Next Daily:", value=f"<t:{tomorrow}:f>")
            await ctx.send(embed=daily)
        else:
            cooldown = Embed(
                description=f"You have already claimed your daily.\nYour next claim is <t:{bank.check_daily}:R>",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @Jeanne.command(
        aliases=["bal", "qp"],
        description="Check how much QP you have",
        usage="<MEMBER | MEMBER NAME | MEMBER ID>",
    )
    @Jeanne.cooldown(1, 60, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def balance(self, ctx: Context, member: Optional[Member] = None):
        member = ctx.author if (member == None) else member
        await self.get_balance(ctx, member)

    @balance.error
    async def balance_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @Jeanne.command(description="Vote for me in TopGG or DiscordBotLists, or both!")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def vote(self, ctx: Context):
        embed = Embed(
            color=Color.random(),
            description="You can vote for me by clicking one of the buttons below to get the following perks:",
        )
        topgg_perks = """
- 100 QP
- 5XP times their global level
- - Rewards are double on weekends
- - Beta users receive 25% extra of the nearest 5 
"""
        dbl_perks = """
- 25% QP boost when winning
- 10XP per message on weekdays, 15XP per message on weekends
- - Beta users receive an extra 5XP per message and extra 25% QP boost when winning
"""
        embed.add_field(name="TopGG", value=topgg_perks, inline=True)
        embed.add_field(name="DiscordBotList", value=dbl_perks, inline=True)
        await ctx.send(
            embed=embed,
            view=vote_button(),
        )


async def setup(bot: Bot):
    await bot.add_cog(CurrencyPrefix(bot))
