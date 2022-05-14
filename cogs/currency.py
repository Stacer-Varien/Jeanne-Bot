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

    @jeanne_slash(description="Register to use the currency system")
    async def register(self, ctx: Interaction):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            try:
                user_query = db.execute(
                f"SELECT * FROM bankData WHERE user_id = {ctx.user.id}")
                user_data=user_query.fetchone()
                user=user_data[0]
                if user == ctx.user.id:
                    already = Embed(description="You are already registered")
                    await ctx.send(embed=already)
            except:
                regis = Embed(
                description="Before you can use this system, please read this.", color=Color.red())
                regis.add_field(name="Selfbotting", value="Selfbotting for intends of farming currency is prohibited. This also includes autotypers, macros or anything that enables automation of commands.Not only this violates the rules but also violates Discord's ToS", inline=False)
                regis.add_field(name="Use of alt accounts", value="There is no limits to the use of alt accounts. However, if you are caught using alts to bypass botbans or farming currency (implemented in the future) and asking to transfer to your alt frequently (such as 'I lost my account password' stories), you will be botbanned.", inline=False)
                regis.add_field(name="Giving and taking credits",
                            value="No one can take or recieve credits from another member other than **me** or **Jeanne**.", inline=False)
                regis.add_field(
                name="Reward", value="After registering, you will get 100 credits free. This is for saying 'thank you'.", inline=False)
                regis.set_footer(
                text="After reading the above, type 'accept' to be registered to the database or 'cancel' to decline it.")
                await ctx.followup.send(embed=regis, ephemeral=True)

                def check(m):
                    return m.author == ctx.user

                try:
                    confirmation = await self.bot.wait_for("message", check=check, timeout=30.0)

                    if confirmation.content == 'accept':
                        db.execute("INSERT OR IGNORE INTO bankData (user_id, amount) VALUES (?,?)", (
                        ctx.user.id, 100))

                        db.commit()

                        await confirmation.delete()
                        await ctx.followup.send("Thank you for registering to the currency system.\nYou have recieved 100 credits free!", ephemeral=True)


                    elif confirmation.content == "cancel":
                        await confirmation.delete()
                        await ctx.followup.send("Oh... ok...\n*__From the dev__*", ephemeral=True)

                except TimeoutError:
                    await ctx.followup.send("Oh... ok...\n*__From the dev__*", ephemeral=True)

    @jeanne_slash(description="Claim your daily", guild_ids=[test_server])
    @cooldown(1, 86400, bucket=SlashBucket.author)
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

            db.execute(
                f"UPDATE bankData SET amount = amount + 100 WHERE user_id = {ctx.user.id}")
            db.commit()

            daily = Embed(
                title="Daily", description=f"**{ctx.user}**, you claimed your daily reward.", color=ctx.user.color)
            daily.add_field(name="Rewards:",
                            value=f"You received **100 credits**")
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

    @guess.subcommand(description="Guess my number and you can win 20 credits")
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
                try:
                    db.execute(f"UPDATE bankData SET amount = amount + 10 WHERE user_id = {ctx.user.id}")
                    db.commit()
                    correct = Embed(description="YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 credits", color=0x008000)
                except:
                    correct = Embed(
                        description="YES!", color=0x008000)
                correct.set_image(url=correct_answer)
                await ctx.followup.send(embed=correct)
            else:
                wrong = Embed(
                    description=f"Wrong answer. It was {answer}", color=0xFF0000)
                wrong.set_thumbnail(url=wrong_answer_or_timeout)
                await ctx.followup.send(embed=wrong)

    @free.error
    async def free_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            reset_date = error.resets_at.strftime('%H:%M')
            await ctx.response.defer()
            cooldown = Embed(
                description=f"You have already guessed the correct number\nYou can try again after `{reset_date}`\n\nIf you want, you can bet with your cash which has a lower cooldown by using the `/guess bet` command", color=Color.red())
            await ctx.followup.send(embed=cooldown)

    @guess.subcommand(description="Guess my number and you can win 20 credits")
    @cooldown(1, 30, bucket=SlashBucket.author)
    async def bet(self, ctx: Interaction, bet=SlashOption(required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            if int(bet) < 5:
                bethigher=Embed(description='Please bet an amount higher than 5')
                await ctx.followup.send(embed=bethigher)
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

                if int(guess.content) == 4:
                    try:
                        db.execute(
                            f"UPDATE bankData SET amount = amount + 10 WHERE user_id = {ctx.user.id}")
                        db.commit()
                        correct = Embed(
                            description="YES! YOU GUESSED IT CORRECTLY!\nYou have been given 20 credits", color=0x008000)
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

    @bet.error
    async def bet_error(self, ctx: Interaction, error):
        if isinstance(error, CallableOnCooldown):
            await ctx.response.defer()
            cooldown = Embed(
                description=f"Calm down. Please wait for a bit\nYou can try again after `{error.retry_after} seconds`", color=Color.red())
            await ctx.followup.send(embed=cooldown)

def setup(bot):
    bot.add_cog(currencysys(bot))
