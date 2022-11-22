import contextlib
from io import StringIO
from discord.ext.commands import Cog, Bot, group, is_owner, guild_only, Context, Greedy, command
from discord import *
from os import execv
from sys import executable, argv
from db_functions import add_botbanned_user, check_botbanned_user
from config import BB_WEBHOOK
from time import time
from typing import Literal, Optional

def restart_bot():
  execv(executable, ['python'] + argv)

class slashowner(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot


    @group(aliases=['act', 'pressence'])
    @is_owner()
    async def activity(self, ctx : Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="`activity play ACTIVITY`\n`activity listen ACTIVITY`\n`activity clear`")
            await ctx.send(embed=embed)

    @activity.command(aliases=['playing'])
    @is_owner()
    async def play(self, ctx: Context, activity:str):
        """Make Jeanne play something as an activity"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await self.bot.change_presence(activity=Game(name=activity))
            await ctx.send(f"Jeanne is now playing `{activity}`")

    @activity.command(aliases=['listening'])
    @is_owner()
    async def listen(self, ctx: Context, activity:str):
        """Make Jeanne listen to something as an activity"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
            await ctx.send(f"Jeanne is now listening to `{activity}`")

    @activity.command(aliases=['remove', 'clean', 'stop'])
    @is_owner()
    async def clear(self, ctx: Context):
        """Clears the bot's activity"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await self.bot.change_presence(activity=None)
            await ctx.send(f"Jeanne's activity has been removed")


    @command(aliases=['fuser'])
    @is_owner()
    async def finduser(self, ctx: Context, user_id:int):
        """Finds a user"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            user = await self.bot.fetch_user(user_id)
            if user.bot == True:
                    botr = ":o:"
            else:
                    botr = ":x:"
            fuser = Embed(title="User Found", color=0xccff33)
            fuser.add_field(name="Name",
                                value=user,
                                inline=True)
            fuser.add_field(name="Creation Date", value="<t:{}:F>".format(round(user.created_at.timestamp())), inline=True)
            fuser.add_field(
                    name="Mutuals", value=len(user.mutual_guilds), inline=True)
            fuser.add_field(
                    name="Bot?", value=botr, inline=True)
            fuser.set_image(url=user.display_avatar)
            if user.banner==None:
                    await ctx.send(embed=fuser)
            else:
                userbanner = Embed(title="User Banner", color=0xccff33)
                userbanner.set_image(url=user.banner)

                e = [fuser, userbanner]
                await ctx.send(embeds=e)

    @command(aliases=['restart', 'refresh'])
    @is_owner()
    async def update(self, ctx:Context):
        """Restart me so I can be updated"""
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await ctx.send(f"YAY! NEW UPDATE!")
            restart_bot()
    
    @command(aliases=['forbid', 'disallow', 'bban', 'bb'])
    @is_owner()
    async def botban(self, ctx: Context, user_id:int, *, reason:str=None):
        """Botban a user from using the bot"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if reason == None:
                await ctx.send("Reason missing for botban", ephemeral=True)
            else:
                user=await self.bot.fetch_user(user_id)
                add_botbanned_user(user_id, reason)                    

                botbanned=Embed(title="User has been botbanned!", description="They will no longer use Jeanne, permanently!")
                botbanned.add_field(name="User",
                                value=user)
                botbanned.add_field(name="ID", value=user.id,
                                inline=True)
                botbanned.add_field(name="Reason of ban",
                                        value=reason,
                                        inline=False)
                botbanned.set_footer(text="Due to this user botbanned, all data except warnings are immediatley deletedfrom the database! They will have no chance of appealing their botban and all the commands executed bythem are now rendered USELESS!")
                botbanned.set_thumbnail(url=user.avatar)
                webhook = SyncWebhook.from_url(BB_WEBHOOK)
                webhook.send(embed=botbanned)

                await ctx.send("User botbanned", ephemeral=True)

    @command(aliases=['eval', 'execute', 'exe', 'exec'])
    @is_owner()
    async def evaluate(self, ctx: Context, raw:Optional[Literal["True", "False"]]):
        """Evaluates a code"""
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            m = await ctx.send("Insert your code.\nType 'cancel' if you don't want to evaluate")

            def check(m:Message):
                return m.author == ctx.author and m.content

            code:Message = await self.bot.wait_for('message', check=check)

            if code.content.startswith("cancel"):
                await m.edit(content="Evaluation aborted")
            elif code.content.startswith("```") and code.content.endswith("```"):
                str_obj = StringIO()
                start_time = time()
                await ctx.typing()
                try:
                    with contextlib.redirect_stdout(str_obj):
                        exec(code.content.strip("`python"))
                except Exception as e:
                    
                    embed = Embed(title="Evaluation failed :negative_squared_cross_mark:\nResults:",
                                description=f"```{e.__class__.__name__}: {e}```", color=0xFF0000)
                    end_time = time()
                    embed.set_footer(
                        text=f"Compiled in {round((end_time - start_time) * 1000)}ms")
                    return await ctx.send(embed=embed)
                if raw == None:
                    embed1 = Embed(title="Evaluation suscessful! :white_check_mark: \nResults:",
                            description=f'```{str_obj.getvalue()}```', color=0x008000)
                    end_time = time()
                    embed1.set_footer(
                        text=f"Compiled in {round((end_time - start_time) * 1000)}ms")
                    await ctx.send(embed=embed1)
                else:
                    await ctx.send(str_obj.getvalue())

    @command()
    @guild_only()
    @is_owner()
    async def sync(self, ctx: Context, guilds: Greedy[Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot:Bot):
    await bot.add_cog(slashowner(bot))
