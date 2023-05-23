from random import choice, randint
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Message,
    app_commands as Jeanne,
    Interaction,
    ui,
)
from datetime import date, datetime, timedelta
from discord.ext.commands import Cog, Bot, GroupCog
from assets.components import Heads_or_Tails
from functions import Botban, Currency

current_time = date.today()
class Guess_Group(GroupCog, name="guess"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Guess my number and you can win 20 QP")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.describe(number="Guess her number (between 1 and 10)")
    async def free(self, ctx: Interaction, number: int):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        qp = str(self.bot.get_emoji(980772736861343774))

        answer = randint(1, 10)

        if int(number) == answer:
            Currency(ctx.user).add_qp(20)

            correct = Embed(
                description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 {qp}!",
                color=Color.random(),
            )
            correct.set_image(url="https://i.imgur.com/ICndRZg.gifv")
            await ctx.followup.send(embed=correct)
        else:
            wrong = Embed(
                description=f"Wrong answer. It was {answer}", color=Color.red()
            )
            wrong.set_image(url="https://i.imgur.com/faD48C3.jpg")
            await ctx.followup.send(embed=wrong)

    @Jeanne.command(description="Guess my number and you can win 20 QP with betting")
    @Jeanne.describe(
        bet="How much are you betting?", number="Guess her number (between 1 and 10)"
    )
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(self, ctx: Interaction, bet: str, number: int):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        qp = str(self.bot.get_emoji(980772736861343774))
        balance = Currency(ctx.user).get_balance()
        if int(bet) < 5:
            bethigher = Embed(description=f"Please bet an amount higher than 5 {qp}")
            await ctx.followup.send(embed=bethigher)

        elif int(bet) > int(balance):
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} {qp}"
            )
            await ctx.followup.send(embed=betlower)
        elif int(balance) == 0:
            zerobal = Embed(
                description=f"Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free`, `/flip free` and/or `/dice free`"
            )
            await ctx.followup.send(embed=zerobal)
        else:
            answer = randint(1, 10)

            if int(number) == answer:
                Currency(ctx.user).add_qp(int(bet))
                correct = Embed(
                    description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {int(bet)} {qp}!",
                    color=Color.random(),
                )
                correct.set_image(url="https://i.imgur.com/ICndRZg.gifv")
            else:
                Currency(ctx.user).remove_qp(int(bet))
                wrong = Embed(
                    description=f"Wrong answer. It was {answer}\nAfraid I have to take {int(bet)} {qp} from you...",
                    color=Color.red(),
                )
                wrong.set_image(url="https://i.imgur.com/faD48C3.jpg")
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
        super().__init__()

    @Jeanne.command(description="Roll a dice for free 20 QP")
    @Jeanne.describe(digit="Guess what will roll")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction, digit: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        rolled = randint(1, 6)
        qp = str(self.bot.get_emoji(980772736861343774))
        if int(digit) == rolled:
            Currency(ctx.user).add_qp(20)
            embed = Embed(color=Color.random())
            embed.add_field(
                name=f"YAY! You got it!\n20 {qp} has been added",
                value=f"Dice rolled: **{rolled}**\You guessed: **{digit}**!",
                inline=False,
            )
            await ctx.followup.send(embed=embed)
        else:
            embed = Embed(
                description=f"Oh no. It rolled a **{rolled}**", color=Color.red()
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Roll a dice with betting")
    @Jeanne.describe(bet="How much are you betting?", digit="Guess what will roll")
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(self, ctx: Interaction, bet: str, digit: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        qp = str(self.bot.get_emoji(980772736861343774))
        rolled = randint(1, 6)
        balance = Currency(ctx.user).get_balance()
        if int(bet) < 5:
            bethigher = Embed(description=f"Please bet an amount higher than 5 {qp}")
            await ctx.followup.send(embed=bethigher)

        elif int(bet) > int(balance):
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} {qp}"
            )
            await ctx.followup.send(embed=betlower)
        elif int(balance) == 0:
            zerobal = Embed(
                description=f"Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free` and/or `/dice free`"
            )
            await ctx.followup.send(embed=zerobal)

        else:
            if rolled == int(digit):
                Currency(ctx.user).add_qp(int(bet))
                embed = Embed(color=Color.random())
                embed.add_field(
                    name=f"YAY! You got it!\n20 {qp} has been added",
                    value=f"Dice rolled: **{rolled}**\You guessed: **{digit}**!",
                    inline=False,
                )
                await ctx.followup.send(embed=embed)

            else:
                Currency(ctx.user).remove_qp(int(bet))
                embed = Embed(color=Color.red())
                embed = Embed(
                    description=f"Oh no. It rolled a **{rolled}**", color=Color.red()
                )
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
        super().__init__()

    @Jeanne.command(description="Flip a coin and earn 20 QP for free")
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        qp = str(self.bot.get_emoji(980772736861343774))
        view = Heads_or_Tails(ctx.user)
        ask = Embed(description="Heads or Tails?", color=Color.random())
        await ctx.followup.send(embed=ask, view=view)
        await view.wait()

        if view.value is jeannes_pick:
            Currency(ctx.user).add_qp(20)

            embed = Embed(
                description="YAY! You got it!\n20 {} has been added".format(qp)
            )

            await ctx.edit_original_response(embed=embed, view=None)

        elif view.value == None:
            timeout = Embed(
                description=f"Sorry but you took too long. It was {jeannes_pick}",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=timeout, view=None)

        else:
            embed = Embed(color=Color.red())
            embed = Embed(
                description="Oh no, it was {}".format(jeannes_pick),
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=embed, view=None)

    @Jeanne.command(name="bet", description="Flip a coin and earn with betting")
    @Jeanne.describe(bet="How much are you betting?")
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(self, ctx: Interaction, bet: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        qp = str(self.bot.get_emoji(980772736861343774))
        picks = ["Heads", "Tails"]
        jeannes_pick = choice(picks)
        balance = Currency(ctx.user).get_balance()
        if 5 > int(bet):
            bethigher = Embed(description=f"Please bet an amount higher than 5 {qp}")
            await ctx.followup.send(embed=bethigher)

        elif int(balance) < int(bet):
            betlower = Embed(
                description=f"Your balance is too low!\nPlease bet lower than {balance} {qp}"
            )
            await ctx.followup.send(embed=betlower)
        elif int(balance) == 0:
            zerobal = Embed(
                description=f"Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free`, `/flip free` and/or `/dice free`"
            )
            await ctx.followup.send(embed=zerobal)

        elif int(bet) <= int(balance):
            view = Heads_or_Tails(ctx.user)
            ask = Embed(description="Heads or Tails?")
            await ctx.followup.send(embed=ask, view=view)
            await view.wait()

            if view.value is jeannes_pick:
                Currency(ctx.user).add_qp(int(bet))

                embed = Embed(
                    description="YAY! You got it!\n{} {} has been added".format(
                        int(bet), qp
                    )
                )

                await ctx.edit_original_response(embed=embed, view=None)

            elif view.value == None:
                timeout = Embed(
                    description=f"Sorry but you took too long. It was {jeannes_pick}",
                    color=Color.red(),
                )
                await ctx.edit_original_response(embed=timeout, view=None)

            else:
                Currency(ctx.user).remove_qp(int(bet))
                embed = Embed(color=Color.red())
                embed = Embed(
                    description="Oh no, it was {}\nI'm afraid that I have to take {}{} from you".format(
                        jeannes_pick, int(bet), qp
                    ),
                    color=Color.red(),
                )
                await ctx.edit_original_response(embed=embed, view=None)

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


class currency(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(description="Claim your daily")
    async def daily(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        qp = self.bot.get_emoji(980772736861343774)
        tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())

        if Currency(ctx.user).give_daily() == True:
            balance = Currency(ctx.user).get_balance()

            daily = Embed(
                title="Daily",
                description=f"**{ctx.user}**, you claimed your daily reward.",
                color=Color.random(),
            )

            if datetime.today().weekday() > 5:
                daily.add_field(
                    name="Rewards (weekend):", value=f"You received 200 {qp}"
                )
            else:
                daily.add_field(name="Rewards:", value=f"You received 100 {qp}")
            daily.add_field(name="Balance", value=f"{balance} {qp}")
            daily.add_field(name="Next Daily:", value=f"<t:{tomorrow}:f>")
            await ctx.response.send_message(embed=daily)

        elif Currency(ctx.user).give_daily() == False:
            cooldown = Embed(
                description=f"You have already claimed your daily.\nYour next claim is <t:{Currency(ctx.user).get_next_daily()}:R>",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="Check how much QP you have")
    @Jeanne.checks.cooldown(1, 30, key=lambda i: (i.user.id))
    async def balance(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        qp = str(self.bot.get_emoji(980772736861343774))
        bal = Currency(ctx.user).get_balance()

        balance = Embed(description=f"You have {bal} {qp}", color=Color.blue())
        balance.add_field(
            name=f"If you want more {qp}:",
            value="[Vote for me in TopGG](https://top.gg/bot/831993597166747679/vote)",
            inline=True,
        )
        await ctx.followup.send(embed=balance)

    @balance.error
    async def balance_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="Vote for me in TopGG to get more QP!")
    async def vote(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        await ctx.response.send_message(
            embed=Embed(
                color=Color.random(),
                description="You can vote for me by [clicking here](https://top.gg/bot/831993597166747679/vote) to get more QP!!",
            ),
            view=ui.View().add_item(
                ui.Button(
                    style=ButtonStyle.url,
                    label="Vote Here",
                    url="https://top.gg/bot/831993597166747679/vote",
                )
            ),
        )


async def setup(bot: Bot):
    await bot.add_cog(Guess_Group(bot))
    await bot.add_cog(Dice_Group(bot))
    await bot.add_cog(Flip_Group(bot))
    await bot.add_cog(currency(bot))
