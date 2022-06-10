import contextlib
from io import StringIO
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as jeanne_slash
from os import execv
from sys import executable, argv
from config import BB_WEBHOOK, db
from nextcord.ext.application_checks import *

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

def restart_bot():
  execv(executable, ['python'] + argv)

class slashowner(Cog):
    def __init__(self, bot):
        self.bot = bot


    @jeanne_slash(description="Changes the bot's play activity")
    @is_owner()
    async def activity(self, ctx : Interaction, activitytype=SlashOption(description="Choose an activity type", choices=['listen', 'play'], required=True), activity=SlashOption(description="What is the new activity")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
                if activitytype=="listen":
                    await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
                    await ctx.followup.send(f"Bot's activity changed to `listening to {activity}`")            
                elif activitytype=="play":
                    await self.bot.change_presence(activity=Game(name=activity))
                    await ctx.followup.send(f"Bot's activity changed to `playing {activity}`")            
             
                

    @jeanne_slash(description="Finds a user")
    @is_owner()
    async def finduser(self, ctx: Interaction, user_id=SlashOption(description="Which user?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
                user = await self.bot.fetch_user(user_id)
                if user.bot == True:
                    botr = ":o:"
                else:
                    botr = ":x:"
                fuser = Embed(title="User Found", color=0xccff33)
                fuser.add_field(name="Name",
                                value=user,
                                inline=True)
                fuser.add_field(name="Creation Date", value=user.created_at.strftime(format), inline=True)
                fuser.add_field(
                    name="Mutuals", value=len(user.mutual_guilds), inline=True)
                fuser.add_field(
                    name="Bot?", value=botr, inline=True)
                fuser.set_image(url=user.display_avatar)
                if user.banner==None:
                    await ctx.followup.send(embed=fuser)
                else:
                    userbanner = Embed(title="User Banner", color=0xccff33)
                    userbanner.set_image(url=user.banner)

                    e = [fuser, userbanner]
                    await ctx.followup.send(embeds=e)
           

    @jeanne_slash(description="Restart me to be updated")
    @is_owner()
    async def update(self, ctx:Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
                await ctx.followup.send(f"YAY! NEW UPDATE!")
                restart_bot()
    
    @jeanne_slash(description="Botban a user from using the bot")
    @is_owner()
    async def botban(self, ctx: Interaction, user_id=SlashOption(description="Which user?"), reason = SlashOption(description="Add a reason")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
                user=await self.bot.fetch_user(user_id)
                cur = db.execute("INSERT OR IGNORE INTO botbannedData (user_id, reason) VALUES (?,?)", (user.id, reason))

                if cur.rowcount==0:
                    db.execute(
                        f"UPDATE botbannedData SET reason = {reason} WHERE user_id = {user.id}")
                db.commit()
                    
                cur1=db.cursor()
                cur2=db.cursor()
                cur3=db.cursor()
                cur1.execute(
                        f"SELECT * FROM serverxpData WHERE user_id = {user.id}")
                result1=cur1.fetchall()
                cur2.execute(f"SELECT * FROM globalxpData WHERE user_id = {user.id}")
                result2=cur2.fetchone()
                cur3.execute(f"SELECT * FROM bankData WHERE user_id = {user.id}")
                result3=cur3.fetchone()

                if result1 == None:
                    pass

                else:
                    cur1.execute(f"DELETE FROM serverxpData WHERE user_id = {user.id}")
                    
                if result2 == None:
                    pass

                else:
                    cur2.execute(
                            f"DELETE FROM globalxpData WHERE user_id = {user.id}")

                if result3 == None:
                    pass

                else:
                    cur3.execute(
                            f"DELETE FROM bankData WHERE user_id = {user.id}")                         

                botbanned=Embed(title="User has been botbanned!", description="They will no longer use Jeanne, permanently!")
                botbanned.add_field(name="User",
                                value=user)
                botbanned.add_field(name="ID", value=user.id,
                                inline=True)
                botbanned.add_field(name="Reason of ban",
                                        value=reason,
                                        inline=False)
                botbanned.set_footer(text="Due to this user botbanned, all data except warnings are immediatley deleted from the database! They will have no chance of appealing their botban.")
                botbanned.set_thumbnail(url=user.avatar)
                webhook = SyncWebhook.from_url(BB_WEBHOOK)
                webhook.send(embed=botbanned)
                db.commit()
                await ctx.followup.send("User botbanned", ephemeral=True)

    @jeanne_slash(description="Evaluates a code")
    @is_owner()
    async def evaluate(self, ctx: Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
                await ctx.followup.send("Insert your code.\nType 'cancel' if you don't want to evaluate")
                def check(m):
                    return m.author == ctx.user and m.content

                code = await self.bot.wait_for('message', check=check)

                if code.content.startswith("cancel"):
                    await ctx.followup.send("Evaluation aborted")
                
                else:
                    str_obj = StringIO()
                    try:
                        with contextlib.redirect_stdout(str_obj):
                            exec(code.content)
                    except Exception as e:
                        embed = Embed(title="Evaluation failed :negative_squared_cross_mark:\nResults:",
                                    description=f"```{e.__class__.__name__}: {e}```", color=0xFF0000)
                        embed.set_footer(
                            text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                        return await ctx.followup.send(embed=embed)
                    embed1 = Embed(title="Evaluation suscessful! :white_check_mark: \nResults:",
                                description=f'```{str_obj.getvalue()}```', color=0x008000)
                    embed1.set_footer(
                            text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                    await ctx.followup.send(embed=embed1)

    @jeanne_slash(description="Makes me leave a server")
    @is_owner()
    async def leave_server(self, ctx: Interaction, server_id=SlashOption(description="What is the server's ID?", required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            guild=await self.bot.fetch_guild(server_id)
            
            try:
                confirm = Embed(title="Is this the server you want me to leave?", description=guild.name)

                if guild.icon == None:
                    pass
                elif guild.icon.is_animated() is True:
                    confirm.set_thumbnail(url=guild.icon.with_size(512))
                else:
                    confirm.set_thumbnail(url=guild.icon)

                confirm.set_footer(text="Type 'yes' to confirm or 'no' to cancel. You have 1 minute")

                confirmation=await ctx.followup.send(embed=confirm)

                def is_correct(m):
                    return m.author == ctx.user and m.content
                try:
                    msg = await self.bot.wait_for("message", check=is_correct, timeout=60.0)

                    if "Yes".lower() in msg.content:
                        confirmed = Embed(
                            description="Successfully left the server")
                        await guild.leave()
                        await confirmation.edit(embed=confirmed)

                    if "No".lower() in msg.content:
                        confirmed = Embed(
                            description="Okay then I'm staying in the server")
                        await confirmation.edit(embed=confirmed)

                except TimeoutError:
                    timeout = Embed(
                        description=f"Timeout", color=0xFF0000)
                    return await ctx.followup.send(embed=timeout)

            except Exception as e:
                await ctx.followup.send(embed=Embed(description=e))                    


def setup(bot):
    bot.add_cog(slashowner(bot))
