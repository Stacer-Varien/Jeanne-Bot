from asyncio import TimeoutError
from random import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from datetime import *
from nextcord.ext.commands import Cog
from assets.needed import *
from cooldowns import *
from assets.db_functions import add_qp, check_botbanned_user, get_balance, give_daily, remove_qp

current_time = date.today()


class currencysys(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Claim your daily")
    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            qp = self.bot.get_emoji(980772736861343774)
            current_time = date.today()
            tomorrow = (current_time + timedelta(days=1))

            if give_daily(ctx.user.id) == True:
                balance=get_balance(ctx.user.id)

                daily = Embed(
                    title="Daily", description=f"**{ctx.user}**, you claimed your daily reward.", color=ctx.user.color)
                daily.add_field(name="Rewards:",
                                value=f"You received 100 {qp}")
                daily.add_field(
                    name='Balance', value=f"{balance} {qp}")
                daily.add_field(name="Next Daily:",
                                value=tomorrow)
                await ctx.send(embed=daily)

            elif give_daily(ctx.user.id) == False:
                cooldown = Embed(
                    description=f"You have already claimed your daily.\nYour next claim is on `{tomorrow}`", color=Color.red())
                await ctx.followup.send(embed=cooldown)

    @jeanne_slash(description="Main guess command")
    async def guess(self, ctx: Interaction):
        pass

    @guess.subcommand(description="Guess my number and you can win 20 QP")
    @cooldown(1, 3600, bucket=SlashBucket.author)
    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            guessit = Embed(
                description="I'm thinking of a number between 1 to 10.\nYou have 5 seconds to guess it!", color=0x00FFFF)
            await ctx.followup.send(embed=guessit)

            def is_correct(m):
                return m.author == ctx.user and m.content.isdigit()

            answer = randint(1, 10)

            try:
                guess = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
            except TimeoutError:
                timeout = Embed(
                    description=f"Sorry but you took too long. It was {answer}", color=0xFF0000)
                timeout.set_thumbnail(url=wrong_answer_or_timeout)
                return await ctx.followup.send(embed=timeout)

            if int(guess.content) == answer:
                add_qp(ctx.user.id, 20)

                correct = Embed(
                    description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 {qp}!", color=0x008000).set_image(url=correct_answer)
                await ctx.followup.send(embed=correct)
            else:
                wrong = Embed(
                    description=f"Wrong answer. It was {answer}", color=0xFF0000)
                wrong.set_thumbnail(url=wrong_answer_or_timeout)
                await ctx.followup.send(embed=wrong)

    @guess.subcommand(description="Guess my number and you can win 20 QP with betting")
    @cooldown(1, 15, bucket=SlashBucket.author)
    async def bet(self, ctx: Interaction, bet=SlashOption(description="How much are you betting?", required=True)):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            balance=get_balance(ctx.user.id)
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

                def is_correct(m):
                    return m.author == ctx.user and m.content.isdigit()

                answer = randint(1, 10)

                try:
                    guess = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
                except TimeoutError:
                    timeout = Embed(
                        description=f"Sorry but you took too long. It was {answer}", color=0xFF0000)
                    timeout.set_thumbnail(url=wrong_answer_or_timeout)
                    return await ctx.followup.send(embed=timeout)

                if int(guess.content) == answer:
                    try:
                        add_qp(ctx.user.id, int(bet))
                        correct = Embed(
                            description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {int(bet)} {qp}!", color=0x008000)
                    except:
                        correct = Embed(
                            description="YES!", color=0x008000)
                    correct.set_image(url=correct_answer)
                    await ctx.followup.send(embed=correct)
                else:
                    remove_qp(ctx.user.id, int(bet))
                    wrong = Embed(
                        description=f"Wrong answer. It was {answer}\nAfraid I have to take {int(bet)} {qp} from you...", color=0xFF0000)
                    wrong.set_thumbnail(url=wrong_answer_or_timeout)
                    await ctx.followup.send(embed=wrong)

    @jeanne_slash(description="Main dice command")
    async def dice(self, ctx: Interaction):
        pass

    @dice.subcommand(name='free', description="Roll a dice for free 20 QP")
    @cooldown(1, 3600, bucket=SlashBucket.author)
    async def _free(self, ctx: Interaction, digit=SlashOption(description="What number are you guessing?", required=True)):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            rolled = randint(1, 6)

            if rolled == int(digit):
                add_qp(ctx.user.id, 20)

                embed = Embed(color=0x0000FF)
                embed.add_field(name=f"YAY! You got it!\n20 {qp} has been added",
                                value=f"Rolled: **{rolled}**\nResult: **{digit}**!", inline=False)
                await ctx.followup.send(embed=embed)

            else:
                embed = Embed(
                    description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
                await ctx.followup.send(embed=embed)

    @dice.subcommand(name='bet', description="Roll a dice with betting")
    @cooldown(1, 15, bucket=SlashBucket.author)
    async def _bet(self, ctx: Interaction, bet=SlashOption(description='How much are you betting?', required=True), digit=SlashOption(description="What number are you guessing?", required=True)):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
         try:
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

            if rolled == int(digit):
                add_qp(ctx.user.id, int(bet))
                embed = Embed(color=0x0000FF)
                embed.add_field(name=f"YAY! You got it!\n20 {qp} has been added",
                                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**", inline=False)
                await ctx.followup.send(embed=embed)

            else:
                remove_qp(ctx.user.id, int(bet))
                embed = Embed(color=Color.red())
                embed = Embed(
                    description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
                await ctx.followup.send(embed=embed)
         except:
             await ctx.followup.send("Please run /daily")

    @jeanne_slash(description='Check how much QP you have')
    @cooldown(1, 30, bucket=SlashBucket.author)
    async def balance(self, ctx: Interaction):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            bal=get_balance(ctx.user.id)

            balance = Embed(
                    description=f"You have {bal} {qp}", color=Color.blue())
            balance.add_field(
                name=f"If you want more {qp}:", value="[Vote for me in TopGG](https://top.gg/bot/831993597166747679/vote)", inline=True)
            await ctx.followup.send(embed=balance)

    @balance.error
    async def balance_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down! Why keep checking again quickly?\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)

    @free.error
    async def free_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_hour = error.resets_at.strftime('%H:%M')
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after {reset_hour}", color=0xff0000)
            await ctx.send(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)

    @_free.error
    async def _free_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_hour = round(error.resets_at.timestamp())
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after <t:{str(reset_hour)}:t>", color=0xff0000)
            await ctx.send(embed=cooldown)

    @_bet.error
    async def _bet_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)

    @jeanne_slash(description="Main coinflip command")
    async def flip(self, ctx: Interaction):
        pass

    @flip.subcommand(name='free', description="Flip a coin and earn 20 QP for free")
    @cooldown(1, 3600, bucket=SlashBucket.author)
    async def _free_(self, ctx: Interaction, pick=SlashOption(choices=['heads', 'tails'])):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            qp = str(self.bot.get_emoji(980772736861343774))
            jeannes_pick = ['heads', 'tails']

            if pick == choice(jeannes_pick):
                add_qp(ctx.user.id, 20)

                embed = Embed(
                    description="YAY! You got it!\n20 {} has been added".format(qp))

                await ctx.followup.send(embed=embed)

            else:
                embed = Embed(color=Color.red())
                embed = Embed(
                    description="Oh no, it was {}".format(choice(jeannes_pick)), color=Color.red())
                await ctx.followup.send(embed=embed)

    @flip.subcommand(name='bet', description='Flip a coin and earn with betting')
    @cooldown(1, 15, bucket=SlashBucket.author)
    async def _bet_(self, ctx: Interaction, bet=SlashOption(required=True), pick=SlashOption(choices=['heads', 'tails'])):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            try:
                qp = str(self.bot.get_emoji(980772736861343774))
                jeannes_pick = ['heads', 'tails']
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
                        description=f'Unfortunately, you have 0 {qp}.\nPlease do a daily and/or wait for a free     chance to do `/guess free` and/or `/dice free`')
                    await ctx.followup.send(embed=zerobal)

                else:
                    if pick == choice(jeannes_pick):
                        add_qp(ctx.user.id, int(bet))

                        embed = Embed(
                            description="YAY! You got it!\n{} {} has been added".format(int(bet), qp))

                        await ctx.followup.send(embed=embed)

                    else:
                        remove_qp(ctx.user.id, int(bet))
                        embed = Embed(color=Color.red())
                        embed = Embed(
                            description="Oh no, it was {}".format(choice(jeannes_pick)), color=Color.red())
                        await ctx.followup.send(embed=embed)
            except:
                await ctx.followup.send('Please run `/daily')

    @_free_.error
    async def _freeerror(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_hour = error.resets_at.strftime('%H:%M')
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after {reset_hour}", color=0xff0000)
            await ctx.send(embed=cooldown)

    @_bet_.error
    async def _beterror(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.send(embed=cooldown)


def setup(bot):
    bot.add_cog(currencysys(bot))
