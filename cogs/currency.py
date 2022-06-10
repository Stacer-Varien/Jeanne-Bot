from asyncio import TimeoutError
from random import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from datetime import *
from nextcord.ext.commands import Cog
from assets.needed import *
from config import db
from cooldowns import *


class currencysys(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Claim your daily")
    @cooldown(1, 10, bucket=SlashBucket.author)
    async def daily(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            current_time = datetime.now()
            tomorrow = (current_time + timedelta(days=1))

            cur = db.execute("INSERT OR IGNORE INTO bankData (user_id, amount) VALUES (?,?)", (ctx.user.id, 100))

            if cur.rowcount==0:
                db.execute(
                f"UPDATE bankData SET amount = amount + 100 WHERE user_id = {ctx.user.id}")

            db.commit()
            daily = Embed(
                title="Daily", description=f"**{ctx.user}**, you claimed your daily reward.", color=ctx.user.color)
            daily.add_field(name="Rewards:",
                                value=f"You received 100 <:quantumpiece:980772736861343774>")
            daily.add_field(name="Next Daily:",
                            value=tomorrow.strftime('%Y-%m-%d %H:%M'))
            await ctx.send(embed=daily)


    @daily.error
    async def daily_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_date = error.resets_at
            await ctx.response.defer()
            cooldown = Embed(
                description=f"You have already claimed your daily.\nYour next claim is on `{reset_date.strftime('%Y-%m-%d %H:%M')}`", color=Color.red())
            await ctx.followup.send(embed=cooldown)

    @jeanne_slash(description="Main guess command")
    async def guess(self, ctx: Interaction):
        pass

    @guess.subcommand(description="Guess my number and you can win 20 QP")
    @cooldown(1, 3600, bucket=SlashBucket.author)
    async def free(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
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
                    cur = db.execute("INSERT OR IGNORE INTO bankData (user_id, amount) VALUES (?,?)", (ctx.user.id, 20))

                    if cur.rowcount == 0:
                        db.execute(f"UPDATE bankData SET amount = amount + 20 WHERE user_id = {ctx.user.id}")

                    db.commit()

                    correct = Embed(
                        description="YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 <:quantumpiece:980772736861343774>!", color=0x008000)
                    ctx.followup.send(embed=correct)
            else:
                wrong = Embed(
                    description=f"Wrong answer. It was {answer}", color=0xFF0000)
                wrong.set_thumbnail(url=wrong_answer_or_timeout)
                await ctx.followup.send(embed=wrong)

    @guess.subcommand(description="Guess my number and you can win 20 QP with betting")
    @cooldown(1, 30, bucket=SlashBucket.author)
    async def bet(self, ctx: Interaction, bet=SlashOption(description="How much are you betting?", required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            balance = db.execute(
                f"SELECT amount FROM bankData WHERE user_id = {ctx.user.id}").fetchone()[0]
            if int(bet) < 5:
                bethigher = Embed(
                    description='Please bet an amount higher than 5 <:quantumpiece:980772736861343774>')
                await ctx.followup.send(embed=bethigher)
            
            elif int(bet) > int(balance):
                betlower = Embed(
                    description=f'Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:980772736861343774>')
                await ctx.followup.send(embed=betlower)
            elif int(balance) == 0:
                zerobal = Embed(
                    description=f'Unfortunately, you have 0 <:quantumpiece:980772736861343774>.\nPlease do a daily and/or wait for a free chance to do `/guess free` and/or `/dice free`')
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
                        db.execute(
                            f"UPDATE bankData SET amount = amount + {int(bet)} WHERE user_id = {ctx.user.id}")
                        db.commit()
                        correct = Embed(
                            description=f"YES! YOU GUESSED IT CORRECTLY!\nYou have been given {int(bet)} <:quantumpiece:980772736861343774>!", color=0x008000)
                    except:
                        correct = Embed(
                            description="YES!", color=0x008000)
                    correct.set_image(url=correct_answer)
                    await ctx.followup.send(embed=correct)
                else:
                    db.execute(f"UPDATE bankData SET amount = amount - {int(bet)} WHERE user_id = {ctx.user.id}")
                    db.commit()
                    wrong = Embed(
                        description=f"Wrong answer. It was {answer}", color=0xFF0000)
                    wrong.set_thumbnail(url=wrong_answer_or_timeout)
                    await ctx.followup.send(embed=wrong)

    @jeanne_slash(description="Main dice command")
    async def dice(self, ctx: Interaction):
        pass

    @dice.subcommand(name='free', description="Roll a dice for free 20 QP")
    @cooldown(1, 3600, bucket=SlashBucket.author)
    async def _free(self, ctx: Interaction, digit=SlashOption(description="What number are you guessing?",required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            rolled = randint(1, 6)

            if rolled==int(digit):
                cur = db.execute(
                      "INSERT OR IGNORE INTO bankData (user_id, amount) VALUES (?,?)", (ctx.user.id, 20))

                if cur.rowcount == 0:
                    db.execute(
                            f"UPDATE bankData SET amount = amount + 20 WHERE user_id = {ctx.user.id}")
                db.commit()

                embed = Embed(color=0x0000FF)
                embed.add_field(name="YAY! You got it!\n20 <:quantumpiece:980772736861343774> has been added",
                            value=f"Rolled: **{rolled}**\nResult: **{digit}**!", inline=False)
                await ctx.followup.send(embed=embed)            

            else:
                embed = Embed(color=Color.red())
                embed.add_field(name="Oh no!",
                                value=f"Rolled: **{rolled}**\nResult: **{digit}**!", inline=False)
                await ctx.followup.send(embed=embed)

    @dice.subcommand(name='bet', description="Roll a dice with betting")
    @cooldown(1, 30, bucket=SlashBucket.author)
    async def _bet(self, ctx: Interaction, bet=SlashOption(description='How much are you betting?', required=True), digit=SlashOption(description="What number are you guessing?", required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
         try:
            rolled = randint(1, 6)
            balance = db.execute(
                f"SELECT amount FROM bankData WHERE user_id = {ctx.user.id}").fetchone()[0]
            if int(bet) < 5:
                bethigher = Embed(
                    description='Please bet an amount higher than 5 <:quantumpiece:980772736861343774>')
                await ctx.followup.send(embed=bethigher)

            elif int(bet) > int(balance):
                betlower = Embed(
                    description=f'Your balance is too low!\nPlease bet lower than {balance} <:quantumpiece:980772736861343774>')
                await ctx.followup.send(embed=betlower)
            elif int(balance) == 0:
                zerobal = Embed(
                    description=f'Unfortunately, you have 0 <:quantumpiece:980772736861343774>.\nPlease do a daily and/or wait for a free chance to do `/guess free` and/or `/dice free`')
                await ctx.followup.send(embed=zerobal)

            if rolled == int(digit):
                db.execute(
                    f"UPDATE bankData SET amount = amount + {int(bet)} WHERE user_id = {ctx.user.id}")
                db.commit()
                embed = Embed(color=0x0000FF)
                embed.add_field(name="YAY! You got it!\n20 <:quantumpiece:980772736861343774> has been added",
                                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**", inline=False)
                await ctx.followup.send(embed=embed)

            else:
                db.execute(
                    f"UPDATE bankData SET amount = amount - {int(bet)} WHERE user_id = {ctx.user.id}")
                db.commit()
                embed = Embed(color=Color.red())
                embed.add_field(name="Oh no!",
                                value=f"Dice rolled: **{rolled}**\nYou guessed: **{digit}**", inline=False)
                await ctx.followup.send(embed=embed)
         except:
             await ctx.followup.send("Please run /daily")

    @jeanne_slash(description='Check how much QP you have')
    @cooldown(1, 60, bucket=SlashBucket.author)
    async def balance(self, ctx:Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            cur=db.execute(f"SELECT amount FROM bankData WHERE user_id = {ctx.user.id}")
            data=cur.fetchone()
            if data == None:
                notthere = Embed(
                    description="You are not in the database\nPlease do `/daily`", color=Color.red())
                await ctx.followup.send(embed=notthere)
            else:
                amount = data[0]
                balance = Embed(
                description=f"You have {amount} <:quantumpiece:980772736861343774>", color=Color.blue())
                await ctx.followup.send(embed=balance)



    @free.error
    async def free_error(self, ctx:Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_hour = error.resets_at.strftime('%H:%M')
            cooldown = Embed(description=f"You have already used your free chance\nTry again after {reset_hour}", color=0xff0000)
            await ctx.followup.send(embed=cooldown)

    @bet.error
    async def bet_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.followup.send(embed=cooldown)

    @_free.error
    async def _free_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_hour = error.resets_at.strftime('%H:%M')
            cooldown = Embed(
                description=f"You have already used your free chance\nTry again after {reset_hour}", color=0xff0000)
            await ctx.followup.send(embed=cooldown)

    @_bet.error
    async def _bet_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            cooldown = Embed(
                description=f"WOAH! Calm down!\nTry again after `{error.retry_after} seconds`", color=0xff0000)
            await ctx.followup.send(embed=cooldown)

def setup(bot):
    bot.add_cog(currencysys(bot))
