from asyncio import TimeoutError
from random import *
from discord import *
from datetime import *
from discord.ext.commands import Cog, Bot, GroupCog, cooldown, CommandOnCooldown, BucketType
from assets.buttons import Heads_or_Tails
from assets.needed import *
from db_functions import add_qp, check_botbanned_user, get_balance, get_next_daily, give_daily, remove_qp


current_time = date.today()


class Guess_Group(GroupCog, name="guess"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.command(description="Guess my number and you can win 20 QP")
    @cooldown(1, 3600, type=BucketType.user)
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
    @cooldown(1, 20, type=BucketType.user)
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
    async def free_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.response.send_message(embed=cooldown)

class Dice_Group(GroupCog, name="dice"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

class currencysys(Cog):
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
    @cooldown(1, 30, type=BucketType.user)
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
    async def balance_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)

    @free.error
    async def free_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.send(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)

    @_free.error
    async def _free_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)  # compensate the 1 hour behind
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.send(embed=cooldown)

    @_bet.error
    async def _bet_error(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)

    @hybrid_group(name='flip')
    async def flip(self, ctx:Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="`flip free`\n`flip bet AMOUNT`")
            await ctx.send(embed=embed)


    @flip.command(name='free')
    @cooldown(1, 3600, type=BucketType.user)
    async def _free_(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            jeannes_pick = ['Heads', 'Tails']
            qp = str(self.bot.get_emoji(980772736861343774))
            view=Heads_or_Tails()
            ask=Embed(description="Heads or Tails?")
            m = await ctx.send(embed=ask, view=view)
            await view.wait()

            if view.value == choice(jeannes_pick):
                add_qp(ctx.user.id, 20)

                embed = Embed(
                    description="YAY! You got it!\n20 {} has been added".format(qp))

                await m.edit(embed=embed, view=None)

            elif view.value == None:
                timeout = Embed(
                    description=f"Sorry but you took too long. It was {choice(jeannes_pick)}", color=0xFF0000)
                await m.edit(embed=timeout, view=None)

            else:
                embed = Embed(color=Color.red())
                embed = Embed(
                    description="Oh no, it was {}".format(choice(jeannes_pick)), color=Color.red())
                await m.edit(embed=embed, view=None)

    @flip.command(name='bet')
    @cooldown(1, 20, type=BucketType.user)
    async def _bet_(self, ctx: Interaction, bet:int):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            jeannes_pick = ['Heads', 'Tails']
            balance = get_balance(ctx.user.id)
            if 5 > int(bet):
                bethigher = Embed(
                    description=f'Please bet an amount higher than 5 {qp}')
                await ctx.send(embed=bethigher)

            elif int(balance) < int(bet) :
                betlower = Embed(
                    description=f'Your balance is too low!\nPlease bet lower than {balance} {qp}')
                await ctx.send(embed=betlower)
            elif int(balance) == 0:
                zerobal = Embed(
                    description=f'Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free chance to do `/guess free`, `/flip free` and/or `/dice free`')
                await ctx.send(embed=zerobal)

            elif int(bet) <= int(balance):
                view = Heads_or_Tails()
                ask = Embed(description="Heads or Tails?")
                m=await ctx.send(embed=ask, view=view)
                await view.wait()

                if view.value == choice(jeannes_pick):
                    add_qp(ctx.user.id, int(bet))

                    embed = Embed(
                        description="YAY! You got it!\n{} {} has been added".format(int(bet), qp))

                    await m.edit(embed=embed, view=None)

                elif view.value==None:
                    timeout = Embed(
                        description=f"Sorry but you took too long. It was {choice(jeannes_pick)}", color=0xFF0000)
                    await m.edit(embed=timeout, view=None)

                else:
                    remove_qp(ctx.user.id, int(bet))
                    embed = Embed(color=Color.red())
                    embed = Embed(
                        description="Oh no, it was {}\nI'm afraid that I have to take {}{} from you".format(choice(jeannes_pick), int(bet), qp), color=Color.red())
                    await m.edit(embed=embed, view=None)


    @_free_.error
    async def _freeerror(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
            reset_hour = round(reset_hour_time.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{reset_hour}:R>", color=0xff0000)
            await ctx.send(embed=cooldown)

    @_bet_.error
    async def _beterror(self, ctx: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.followup.send(embed=cooldown)


async def setup(bot:Bot):
    await bot.add_cog(currencysys(bot))
