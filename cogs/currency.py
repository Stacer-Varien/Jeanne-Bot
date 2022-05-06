from asyncio import TimeoutError
from random import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from datetime import *
from nextcord.ext.commands import Cog
from assets.needed import *
from config import db


class currencysys(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Register to use the currency system", guild_ids=[test_server])
    async def register(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            regis=Embed(description="Before you can use this system, please read this.", color=Color.red())
            regis.add_field(name="Selfbotting", value="Selfbotting for intends of farming currency is prohibited. This also includes autotypers, macros or anything that enables automation of commands.Not only this violates the rules but also violates Discord's ToS")
            regis.add_field(name="Use of alt accounts", value="There is no limits to the use of alt accounts. However, if you are caught using alts to bypass botbans or farming currency (implemented in the future) and asking to transfer to your alt frequently (such as 'I lost my account password' stories), you will be botbanned.")
            regis.add_field(name="Giving and taking credits", value="No one can take or recieve credits from another member other than **me** or **Jeanne**.")
            regis.add_field(name="Reward", value="After registering, you will get 100 credits free. This is for saying 'thank you'.")
            regis.set_footer(text="After reading the above, type 'accept' to be registered to the database or 'cancel' to decline it.")
            await ctx.followup.send(embed=regis, ephemeral=True)

            def check(m):
                return m.author == ctx.user


            try:
                confirmation = await self.bot.wait_for("message", check=check, timeout=30.0)

                if confirmation.content == 'accept':
                    db.execute("INSERT OR IGNORE INTO bankData (user_id, amount) VALUES (?,?)", (
                        ctx.user.id, 100))

                    db.commit()

                    await ctx.followup.send("Thank you for registering to the currency system.\nYou have recieved 100 credits free!", ephemeral=True)

                elif confirmation.content == "cancel":
                    await ctx.followup.send("Oh... ok...\n*__From the dev__*", ephemeral=True)

            except TimeoutError:
                await ctx.followup.send("Oh... ok...\n*__From the dev__*", ephemeral=True)

    @jeanne_slash(description="Claim your daily", guild_ids=[test_server])
    async def daily(self, ctx:Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            try:
                claimed_date=date.today()
                next_date=claimed_date + timedelta(days=1)
                credits_claimed=100
                record = db.execute(f"SELECT * WHERE user_id = {ctx.user.id}")
                if claimed_date is not record.fetchone()[2]:
                        already_claimed = Embed(
                            description=f"You have already claimed your daily credits.\nYour next claim is on {next_date.strftime('%Y-%m-%d')}")
                        await ctx.followup.send(embed=already_claimed)
            
                elif record.fetchone()[2] == "None":
                        db.execute(
                            f"UPDATE bankData SET amount = amount + {credits_claimed}, claimed = {claimed_date} AND next_claim_date = {next_date} WHERE user_id = {ctx.user.id}")

                        claimed = Embed(
                            title="Daily Claimed!", description=f"Thanks for claiming your 100 credits. Now you have {record.fetchone()[1]} credits\nYour next claim is on {record.fetchone()[3]}", color=Color.green())
                
                        await ctx.followup.send(embed=claimed)
                    
                elif claimed_date==record.fetchone()[2]:
                        db.execute(
                            f"UPDATE bankData SET amount = amount + {credits_claimed}, claimed = {claimed_date} AND next_claim_date = {next_date} WHERE user_id = {ctx.user.id}")

                        claimed = Embed(
                            title="Daily Claimed!", description=f"Thanks for claiming your 100 credits. Now you have {record.fetchone()[1]} credits\nYour next claim is on {record.fetchone()[3]}", color=Color.green())

                        await ctx.followup.send(embed=claimed)
                
                db.commit()
            
            except:
                notthere=Embed(description="You are not registered in the currency system.\nPlease run '/register'")
                await ctx.followup.send(embed=notthere)

        


def setup(bot):
    bot.add_cog(currencysys(bot))
