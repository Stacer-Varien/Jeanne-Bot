from asyncio import TimeoutError
from random import *
from discord import *
from datetime import *
from discord.ext.commands import Cog, Bot, GroupCog
from discord.app_commands import *
from assets.buttons import Heads_or_Tails
from assets.needed import *
from db_functions import add_qp, check_botbanned_user, get_balance, get_next_daily, give_daily, remove_qp

current_time = date.today()

class Guess_Group(GroupCog, name="guess"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.command(description="Guess my number and you can win 20 QP")
    @checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            qp = str(self.bot.get_emoji(980772736861343774))
            guessit = Embed(
                description="I'm thinking of a number between 1 to 10.\nYou have 5 seconds to guess it!", color=0x00FFFF)
            await ctx.followup.send(embed=guessit)

            def is_correct(m: Message):
                return m.author == ctx.user and m.content.isdigit()

            answer = randint(1, 10)

            try:
                guess:Message = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
            except TimeoutError:
                timeout = Embed(
                    description=f"Sorry but you took too long. It was {answer}", color=0xFF0000)
                timeout.set_image(url='https://i.imgur.com/faD48C3.jpg')
                return await ctx.followup.send(embed=timeout)

            if guess.content == answer:
                add_qp(ctx.user.id, 20)

                correct = Embed(
                    description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 {qp}!", color=0x008000)
                correct.set_image(url='https://i.imgur.com/ICndRZg.gifv')
                await ctx.followup.send(embed=correct)
            else:
                wrong = Embed(
                    description=f"Wrong answer. It was {answer}", color=0xFF0000)
                wrong.set_image(url='https://i.imgur.com/faD48C3.jpg')
                await ctx.followup.send(embed=wrong)


    @app_commands.command(description='Guess my number and you can win 20 QP with betting')
    @app_commands.describe(bet="How much are you betting?")
    @checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(self, ctx: Interaction, bet: int):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            qp = str(self.bot.get_emoji(980772736861343774))
            balance = get_balance(ctx.user.id)
            if int(bet) < 5:
                bethigher = Embed(
                    description=f'Please bet an amount higher than 5 {qp}')
                await ctx.followup.send(embed=bethigher)

            elif int(bet) > int(balance):
                betlower = Embed(
                    description=f'Your balance is too low!\nPlease bet lower than {balance} {qp}')
                await ctx.followup.send(embed=betlower)
            elif int(balance) == 0:
                zerobal = Embed(
                    description=f'Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free`, `/flip free` and/or `/dice free`')
                await ctx.followup.send(embed=zerobal)
            else:
                guessit = Embed(
                    description="I'm thinking of a number between 1 to 10.\nYou have 5 seconds to guess it!", color=0x00FFFF)
                await ctx.followup.send(embed=guessit)

                def is_correct(m: Message):
                    return m.author == ctx.user and m.content.isdigit()

                answer = randint(1, 10)

                try:
                    guess:Message = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
                except TimeoutError:
                    timeout = Embed(
                        description=f"Sorry but you took too long. It was {answer}", color=0xFF0000)
                    timeout.set_image(url='https://i.imgur.com/faD48C3.jpg')
                    return await ctx.followup.send(embed=timeout)

                if guess.content == answer:
                    try:
                        add_qp(ctx.user.id, int(bet))
                        correct = Embed(
                            description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {int(bet)} {qp}!", color=0x008000)
                        correct.set_image(
                            url='https://i.imgur.com/ICndRZg.gifv')
                    except:
                        correct = Embed(
                            description="YES!", color=0x008000)
                        correct.set_image(
                            url='https://i.imgur.com/ICndRZg.gifv')
                    await ctx.followup.send(embed=correct)
                else:
                    remove_qp(ctx.user.id, int(bet))
                    wrong = Embed(
                        description=f"Wrong answer. It was {answer}\nAfraid I have to take {int(bet)} {qp} from you...", color=0xFF0000)
                    wrong.set_image(url='https://i.imgur.com/faD48C3.jpg')
                    await ctx.followup.send(embed=wrong)

    @free.error
    async def free_error(self, ctx: Interaction, error:AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error:AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

class Dice_Group(GroupCog, name="dice"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Roll a dice for free 20 QP")
    @app_commands.describe(digit="Guess what will roll")
    @checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction, digit:int):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            rolled = randint(1, 6)
            qp = str(self.bot.get_emoji(980772736861343774))
            if int(digit) == rolled:
                add_qp(ctx.user.id, 20)
                embed = Embed(color=0x0000FF)
                embed.add_field(name=f"YAY! You got it!\n20 {qp} has been added",
                                value=f"Dice rolled: **{rolled}**\You guessed: **{digit}**!", inline=False)
                await ctx.followup.send(embed=embed)
            else:
                embed = Embed(
                    description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="Roll a dice with betting")
    @app_commands.describe(bet="How much are you betting?",digit="Guess what will roll")
    @checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(self, ctx: Interaction, bet:int, digit:int):
        
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            qp = str(self.bot.get_emoji(980772736861343774))
            rolled = randint(1, 6)
            balance = get_balance(ctx.user.id)
            if int(bet) < 5:
                bethigher = Embed(
                    description=f'Please bet an amount higher than 5 {qp}')
                await ctx.followup.send(embed=bethigher)

            elif int(bet) > int(balance):
                betlower = Embed(
                    description=f'Your balance is too low!\nPlease bet lower than {balance} {qp}')
                await ctx.followup.send(embed=betlower)
            elif int(balance) == 0:
                zerobal = Embed(
                    description=f'Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free` and/or `/dice free`')
                await ctx.followup.send(embed=zerobal)

            else:
                if rolled == int(digit):
                    add_qp(ctx.user.id, int(bet))
                    embed = Embed(color=0x0000FF)
                    embed.add_field(name=f"YAY! You got it!\n20 {qp} has been added",
                            value=f"Dice rolled: **{rolled}**\You guessed: **{digit}**!", inline=False)
                    await ctx.followup.send(embed=embed)

                else:
                    remove_qp(ctx.user.id, int(bet))
                    embed = Embed(color=Color.red())
                    embed = Embed(
                        description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
                    await ctx.followup.send(embed=embed)  

    @free.error
    async def free_error(self, ctx: Interaction, error:AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

class Flip_Group(GroupCog, name="flip"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Flip a coin and earn 20 QP for free")
    @checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            jeannes_pick = ['Heads', 'Tails']
            qp = str(self.bot.get_emoji(980772736861343774))
            view = Heads_or_Tails(ctx.user)
            ask = Embed(description="Heads or Tails?")
            await ctx.followup.send(embed=ask, view=view)
            await view.wait()

            if str(view.value) == str(choice(jeannes_pick)):
                add_qp(ctx.user.id, 20)

                embed = Embed(
                    description="YAY! You got it!\n20 {} has been added".format(qp))

                await ctx.edit_original_response(embed=embed, view=None)

            elif view.value == None:
                timeout = Embed(
                    description=f"Sorry but you took too long. It was {choice(jeannes_pick)}", color=0xFF0000)
                await ctx.edit_original_response(embed=timeout, view=None)

            else:
                embed = Embed(color=Color.red())
                embed = Embed(
                    description="Oh no, it was {}".format(choice(jeannes_pick)), color=Color.red())
                await ctx.edit_original_response(embed=embed, view=None)

    @app_commands.command(name='bet', description='Flip a coin and earn with betting')
    @app_commands.describe(bet="How much are you betting?")
    @checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(self, ctx: Interaction, bet:int):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            jeannes_pick = ['Heads', 'Tails']
            balance = get_balance(ctx.user.id)
            if 5 > int(bet):
                bethigher = Embed(
                    description=f'Please bet an amount higher than 5 {qp}')
                await ctx.followup.send(embed=bethigher)

            elif int(balance) < int(bet):
                betlower = Embed(
                    description=f'Your balance is too low!\nPlease bet lower than {balance} {qp}')
                await ctx.followup.send(embed=betlower)
            elif int(balance) == 0:
                zerobal = Embed(
                    description=f'Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free`, `/flip free` and/or `/dice free`')
                await ctx.followup.send(embed=zerobal)

            elif int(bet) <= int(balance):
                view = Heads_or_Tails(ctx.user)
                ask = Embed(description="Heads or Tails?")
                await ctx.followup.send(embed=ask, view=view)
                await view.wait()

                if str(view.value) == str(choice(jeannes_pick)):
                    add_qp(ctx.user.id, int(bet))

                    embed = Embed(
                        description="YAY! You got it!\n{} {} has been added".format(int(bet), qp))

                    await ctx.edit_original_response(embed=embed, view=None)

                elif view.value == None:
                    timeout = Embed(
                        description=f"Sorry but you took too long. It was {choice(jeannes_pick)}", color=0xFF0000)
                    await ctx.edit_original_response(embed=timeout, view=None)

                else:
                    remove_qp(ctx.user.id, int(bet))
                    embed = Embed(color=Color.red())
                    embed = Embed(
                        description="Oh no, it was {}\nI'm afraid that I have to take {}{} from you".format(choice(jeannes_pick), int(bet), qp), color=Color.red())
                    await ctx.edit_original_response(embed=embed, view=None)

    @free.error
    async def free_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{round(error.retry_after, 2)} seconds`", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

class currency(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @app_commands.command(description="Claim your daily")
    async def daily(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            qp = self.bot.get_emoji(980772736861343774)
            tomorrow = round((datetime.now() + timedelta(days=1)).timestamp())

            if give_daily(ctx.user.id) == True:
                balance=get_balance(ctx.user.id)
                

                daily = Embed(
                    title="Daily", description=f"**{ctx.user}**, you claimed your daily reward.", color=ctx.user.color)
                
                if datetime.today().weekday() > 5:
                    daily.add_field(name="Rewards (weekend):",
                                    value=f"You received 200 {qp}")
                else:
                    daily.add_field(name="Rewards:",
                                    value=f"You received 100 {qp}")
                daily.add_field(
                    name='Balance', value=f"{balance} {qp}")
                daily.add_field(name="Next Daily:",
                                value=f"<t:{tomorrow}:f>")
                await ctx.response.send_message(embed=daily)

            elif give_daily(ctx.user.id) == False:
                cooldown = Embed(
                    description=f"You have already claimed your daily.\nYour next claim is <t:{get_next_daily(ctx.user.id)}:R>", color=Color.red())
                await ctx.response.send_message(embed=cooldown)

    @app_commands.command(description="Check how much QP you have")
    @checks.cooldown(1, 30, key=lambda i: (i.user.id))
    async def balance(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            qp = str(self.bot.get_emoji(980772736861343774))
            bal=get_balance(ctx.user.id)

            balance = Embed(
                    description=f"You have {bal} {qp}", color=Color.blue())
            balance.add_field(
                name=f"If you want more {qp}:", value="[Vote for me in TopGG](https://top.gg/bot/831993597166747679/vote)", inline=True)
            await ctx.followup.send(embed=balance)

    @balance.error
    async def balance_error(self, ctx: Interaction, error:AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{round(error.retry_after, 2)} seconds`", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

async def setup(bot:Bot):
    await bot.add_cog(Guess_Group(bot))
    await bot.add_cog(Dice_Group(bot))
    await bot.add_cog(Flip_Group(bot))
    await bot.add_cog(currency(bot))
    