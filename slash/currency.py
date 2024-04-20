from random import choice, randint
from typing import Optional
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
from discord.ext.commands import Cog, Bot, GroupCog
from assets.components import Guess_Buttons, Heads_or_Tails
from config import DBL_AUTH
from functions import (
    BetaTest,
    Currency,
    DBLvoter,
    check_botbanned_app_command,
    check_disabled_app_command,
)


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
                label="Discord Bot List (Beta)",
                url="https://discordbotlist.com/bots/jeanne/upvote",
            )
        )


class Guess_Group(GroupCog, name="guess"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dbl = DBLvoter(self.bot, DBL_AUTH)
        super().__init__()

    @Jeanne.command(description="Guess my number and you can win 20 QP")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def free(self, ctx: Interaction):
        view = Guess_Buttons(ctx.user)
        await ctx.response.defer()
        await ctx.followup.send(
            embed=Embed(
                description="Guess my number by clicking on one of the buttons below",
                color=Color.random(),
            ),
            view=view,
        )
        answer = randint(1, 10)
        await view.wait()
        if view.value == answer:
            await Currency(ctx.user).add_qp(20)
            correct = Embed(
                description="YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 <:quantumpiece:1161010445205905418>!",
                color=Color.random(),
            )
            if self.dbl.get_user_vote(ctx.user) == True:
                await Currency(ctx.user).add_qp(round((20 * 1.25), 2))
                correct.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                )
                if BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.user).add_qp(round((20 * 1.25), 2))
                    correct.add_field(
                        name="Beta User Bonus",
                        value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.edit_original_response(embed=correct, view=None)
            return
        wrong = Embed(description=f"Wrong answer. It was {answer}", color=Color.red())
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.edit_original_response(embed=wrong, view=None)

    @Jeanne.command(description="Guess my number and you can win with betting")
    @Jeanne.describe(bet="How much are you betting?")
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def bet(
        self,
        ctx: Interaction,
        bet: Jeanne.Range[int, 5],
    ):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Guess_Buttons(ctx.user)
        await ctx.followup.send(
            embed=Embed(
                description="Guess my number by clicking on one of the buttons below",
                color=Color.random(),
            ),
            view=view,
        )
        await view.wait()
        answer = randint(1, 10)
        if view.value == answer:
            await Currency(ctx.user).add_qp(bet)
            correct = Embed(
                description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {bet} <:quantumpiece:1161010445205905418>!",
                color=Color.random(),
            )
            if self.dbl.get_user_vote(ctx.user) == True:
                await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                correct.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                )
                if BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                    correct.add_field(
                        name="Beta User Bonus",
                        value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            correct.set_image(url="https://files.catbox.moe/phqnb1.gif")
            await ctx.followup.send(embed=wrong, view=view)
            return
        await Currency(ctx.user).remove_qp(bet)
        wrong = Embed(
            description=f"Wrong answer. It was {answer}\nAfraid I have to take {bet} <:quantumpiece:1161010445205905418> from you...",
            color=Color.red(),
        )
        wrong.set_image(url="https://files.catbox.moe/mbk0nm.jpg")
        await ctx.followup.send(embed=wrong)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Dice_Group(GroupCog, name="dice"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dbl = DBLvoter(self.bot, DBL_AUTH)
        super().__init__()

    @Jeanne.command(description="Roll a dice for free 20 QP")
    @Jeanne.describe(digit="Guess what will roll")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction, digit: Jeanne.Range[int, 1, 6]):
        await ctx.response.defer()
        rolled = randint(1, 6)
        if digit == rolled:
            await Currency(ctx.user).add_qp(20)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! You got it!\n20 <:quantumpiece:1161010445205905418> has been added",
                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**!",
                inline=False,
            )
            await ctx.followup.send(embed=embed)
            return
        embed = Embed(description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Roll a dice with betting")
    @Jeanne.describe(bet="How much are you betting?", digit="Guess what will roll")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(
        self,
        ctx: Interaction,
        bet: Jeanne.Range[int, 5],
        digit: Jeanne.Range[int, 1, 6],
    ):
        await ctx.response.defer()
        rolled = randint(1, 6)
        balance = Currency(ctx.user).get_balance
        if bet > balance:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        if rolled == digit:
            await Currency(ctx.user).add_qp(bet)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! You got it!\n{bet} <:quantumpiece:1161010445205905418> has been added",
                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**!",
                inline=False,
            )
            if self.dbl.get_user_vote(ctx.user) == True:
                await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                )
                if BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            await ctx.followup.send(embed=embed)
            return
        await Currency(ctx.user).remove_qp(bet)
        embed = Embed(color=Color.red())
        embed = Embed(description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
        await ctx.followup.send(embed=embed)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class Flip_Group(GroupCog, name="flip"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dbl = DBLvoter(self.bot, DBL_AUTH)
        super().__init__()

    @Jeanne.command(description="Flip a coin and earn 20 QP for free")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        view = Heads_or_Tails(ctx.user)
        ask = Embed(description="Heads or Tails?", color=Color.random())
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.user).add_qp(20)
            embed = Embed(
                description="YAY! You got it!\n20 <:quantumpiece:1161010445205905418> has been added",
                color=Color.random(),
            )
            if self.dbl.get_user_vote(ctx.user) == True:
                await Currency(ctx.user).add_qp(round((20 * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                )
                if BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.user).add_qp(round((20 * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh no, it was {}".format(jeannes_pick),
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Sorry but you took too long. It was {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)

    @Jeanne.command(name="bet", description="Flip a coin and earn with betting")
    @Jeanne.describe(bet="How much are you betting?")
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def bet(self, ctx: Interaction, bet: Jeanne.Range[int, 5]):
        await ctx.response.defer()
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        balance = Currency(ctx.user).get_balance
        if balance < bet:
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:1161010445205905418>"
            )
            await ctx.followup.send(embed=betlower)
            return
        if balance == 0:
            zerobal = Embed(
                description="Unfortunately, you have 0 <:quantumpiece:1161010445205905418>."
            )
            await ctx.followup.send(embed=zerobal)
            return
        view = Heads_or_Tails(ctx.user)
        ask = Embed(description="Heads or Tails?")
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()
        if view.value == jeannes_pick:
            await Currency(ctx.user).add_qp(bet)
            embed = Embed(
                description="YAY! You got it!\n{} <:quantumpiece:1161010445205905418> has been added".format(
                    bet
                )
            )
            if self.dbl.get_user_vote(ctx.user) == True:
                await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                embed.add_field(
                    name="DiscordBotList Bonus",
                    value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                )
                if BetaTest(self.bot).check(ctx.user) == True:
                    await Currency(ctx.user).add_qp(round((bet * 1.25), 2))
                    embed.add_field(
                        name="Beta User Bonus",
                        value=f"{round((bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                    )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        if view.value != jeannes_pick:
            await Currency(ctx.user).remove_qp(int(bet))
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh no, it was {}\nI'm afraid that I have to take {} <:quantumpiece:1161010445205905418> from you".format(
                    jeannes_pick, bet
                ),
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)
            return
        timeout = Embed(
            description=f"Sorry but you took too long. It was {jeannes_pick}",
            color=Color.red(),
        )
        await ctx.edit_original_response(embed=timeout, view=None)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


class currency(Cog, name="CurrencySlash"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.balance_context = Jeanne.ContextMenu(
            name="Balance", callback=self.balance_callback
        )
        self.bot.tree.add_command(self.balance_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.balance_context.name, type=self.balance_context.type
        )
        self.balance_callback_error = self.balance_context.error(
            self.balance_callback_error
        )

    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def balance_callback(self, ctx: Interaction, member: Member):
        await self.get_balance(ctx, member)

    async def balance_callback_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    async def get_balance(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        bal = Currency(member).get_balance
        balance = Embed(
            description=f"{'You' if (member == ctx.user) else member} have {bal} <:quantumpiece:1161010445205905418>",
            color=Color.blue(),
        )
        balance.add_field(
            name=f"If you want more <:quantumpiece:1161010445205905418>:",
            value="[Vote for me in TopGG](https://top.gg/bot/831993597166747679/vote)",
            inline=True,
        )
        await ctx.followup.send(embed=balance)

    @Jeanne.command(description="Claim your daily")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        bank = Currency(ctx.user)
        tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())
        if bank.check_daily == True:
            await bank.give_daily()
            daily = Embed(
                title="Daily",
                description=f"**{ctx.user}**, you claimed your daily reward.",
                color=Color.random(),
            )
            check_beta = await BetaTest(self.bot).check(ctx.user)
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
            await ctx.followup.send(embed=daily)
        else:
            cooldown = Embed(
                description=f"You have already claimed your daily.\nYour next claim is <t:{bank.check_daily}:R>",
                color=Color.red(),
            )
            await ctx.followup.send(embed=cooldown)

    @Jeanne.command(description="Check how much QP you have")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def balance(self, ctx: Interaction, member: Optional[Member] = None):
        member = ctx.user if (member == None) else member
        await self.get_balance(ctx, member)

    @balance.error
    async def balance_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="Vote for me in TopGG to get more QP!")
    async def vote(self, ctx: Interaction):
        await ctx.response.send_message(
            embed=Embed(
                color=Color.random(),
                description="You can vote for me by clicking one of the buttons below to get more QP!!",
            ),
            view=vote_button(),
        )


async def setup(bot: Bot):
    await bot.add_cog(Guess_Group(bot))
    await bot.add_cog(Dice_Group(bot))
    await bot.add_cog(Flip_Group(bot))
    await bot.add_cog(currency(bot))
