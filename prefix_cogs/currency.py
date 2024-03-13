from random import choice, randint
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
from assets.components import Heads_or_Tails
from functions import (
    BetaTest,
    Currency,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
    is_beta_prefix,
)


class CurrencyCog(Cog, name="Currency"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.group(
        invoke_without_command=True,
        description="Main Guess command for `guess flip` and `guess bet`",
    )
    async def guess(self, ctx: Context): ...

    @guess.command(name="free", description="Guess my number and you can win 20 QP")
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
    async def guess_free(self, ctx: Context, number: Jeanne.Range[int, 1, 10]):

        answer = randint(1, 10)

        if number == answer:
            await Currency(ctx.author).add_qp(20)

            correct = Embed(
                description="YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 <:quantumpiece:1161010445205905418>!",
                color=Color.random(),
            )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.send(embed=correct)
            return

        wrong = Embed(description=f"Wrong answer. It was {answer}", color=Color.red())
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.send(embed=wrong)

    @guess.command(name="bet", description="Guess my number and you can win 20 QP with betting")
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
    async def guess_bet(
        self,
        ctx: Context,
        bet: Jeanne.Range[int, 5],
        number: Jeanne.Range[int, 1, 10],
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

        answer = randint(1, 10)

        if number == answer:
            await Currency(ctx.author).add_qp(bet)
            correct = Embed(
                description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {bet} <:quantumpiece:1161010445205905418>!",
                color=Color.random(),
            )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            return

        Currency(ctx.author).remove_qp(bet)
        wrong = Embed(
            description=f"Wrong answer. It was {answer}\nAfraid I have to take {bet} <:quantumpiece:1161010445205905418> from you...",
            color=Color.red(),
        )
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.send(embed=wrong)

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
        description="Main Dice command for `dice free` and `dice bet`",
    )
    async def dice(self, ctx: Context): ...

    @dice.command(name="free",description="Roll a dice for free 20 QP")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    async def dice_free(self, ctx: Context, digit: Jeanne.Range[int, 1, 6]):

        rolled = randint(1, 6)
        if digit == rolled:
            await Currency(ctx.author).add_qp(20)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! You got it!\n20 <:quantumpiece:1161010445205905418> has been added",
                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**!",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
        await ctx.send(embed=embed)

    @dice.command(name="bet", description="Roll a dice with betting")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    async def dice_bet(
        self,
        ctx: Context,
        bet: Jeanne.Range[int, 5],
        digit: Jeanne.Range[int, 1, 6],
    ):

        rolled = randint(1, 6)
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

        if rolled == digit:
            await Currency(ctx.author).add_qp(bet)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="YAY! You got it!\n20 <:quantumpiece:1161010445205905418> has been added",
                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**!",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        await Currency(ctx.author).remove_qp(bet)
        embed = Embed(color=Color.red())
        embed = Embed(description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
        await ctx.send(embed=embed)

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
        description="Main Flip command for `flip free` and `flip bet`",
    )
    async def flip(self, ctx: Context): ...

    @flip.command(name="free",description="Flip a coin and earn 20 QP for free")
    @Jeanne.cooldown(1, 3600, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
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

    @flip.command(name="bet", description="Flip a coin and earn with betting")
    @Jeanne.cooldown(1, 20, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
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

    async def get_balance(self, ctx: Context, member: Member):
        bal = Currency(member).get_balance

        balance = Embed(
            description=f"{'You' if (member == ctx.author) else member} have {bal} <:quantumpiece:1161010445205905418>",
            color=Color.blue(),
        )
        balance.add_field(
            name=f"If you want more <:quantumpiece:1161010445205905418>:",
            value="[Vote for me in TopGG](https://top.gg/bot/831993597166747679/vote)",
            inline=True,
        )
        await ctx.send(embed=balance)

    @Jeanne.command(description="Claim your daily")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
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

    @Jeanne.command(description="Check how much QP you have")
    @Jeanne.cooldown(1, 60, type=Jeanne.BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
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

    @Jeanne.command(description="Vote for me in TopGG to get more QP!")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(is_beta_prefix)
    async def vote(self, ctx: Context):

        await ctx.send(
            embed=Embed(
                color=Color.random(),
                description="You can vote for me by clicking on the button below to get more QP!!",
            ),
            view=ui.View().add_item(
                ui.Button(
                    style=ButtonStyle.url,
                    label="Top.gg",
                    url="https://top.gg/bot/831993597166747679/vote",
                )
            ),
        )


async def setup(bot: Bot):
    await bot.add_cog(CurrencyCog(bot))
