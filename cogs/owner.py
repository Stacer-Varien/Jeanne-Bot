import contextlib
import io
from os import execv
import re
from sys import executable, argv
from nextcord.ext.commands import command as jeanne, Cog, is_owner
from nextcord import User, Guild, Game, Embed, Activity, ActivityType



def restart_bot():
  execv(executable, ['python'] + argv)

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"
class owner(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne(aliases=['fuser'])
    @is_owner()
    async def finduser(self, ctx, user:User):
        if user.bot == True:
            botr = ":o:"
        else:
            botr = ":x:"

        fuser = Embed(title="User Found", color=0xccff33)
        fuser.add_field(name="User Information",
                           value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}\n**>** **Creation Date:** {user.created_at.strftime(format)}\n**>** **Mutuals:** {len(user.mutual_guilds)}\n**>** **Is Bot?:** {botr}",
                           inline=True)
        fuser.set_image(url=user.display_avatar)
        await ctx.send(embed=fuser)

    

    @jeanne(aliases=['fserver'])
    @is_owner()
    async def findserver(self, ctx, *, guild: Guild):
        serverinfo = f"_____\nGeneral Information\nServer Name: {guild.name}\nServer ID: {guild.id}\nCreation Date: {guild.created_at.strftime(format)}\nMember Count: {len(guild.members)}\nVerification: {guild.verification_level}\nRoles: {len(guild.roles)}\nOwner Name:{guild.owner}\nID: {guild.owner.id}\n_______"
        print(serverinfo)
        await ctx.send(f"`Check console log for {guild.name}`", delete_after=10)

    @jeanne(pass_context=True)
    @is_owner()
    async def mutuals(self, ctx, *, user: User):
        mutuals=f"______\nName: {user}\nMutuals: {len(user.mutual_guilds)}\nServers: {user.mutual_guilds}\n______"
        print(mutuals)
        await ctx.send(f"`Check console log for {user.name}'s mutuals`", delete_after=10)

    @jeanne(aliases=['bm'])
    @is_owner()
    async def botmutuals(self, ctx):
        mutuals = [str(x) for x in ctx.bot.guilds]
        botmutuals=f"____\nMutuals: {len(ctx.bot.guilds)}\nServers: {' ,'.join(mutuals)}\n______"
        print(botmutuals)
        await ctx.send("`Check console log for bot's mutuals`", delete_after=10)


    @jeanne()
    @is_owner()
    async def activity(self, ctx, activitytype, *, activity):

        if activitytype=="listen":
            await ctx.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
            await ctx.send(f"Bot's activity changed to `listening to {activity}`")
        elif activitytype=="play":
            await ctx.bot.change_presence(activity=Game(name=activity))
            await ctx.send(f"Bot's activity changed to `playing {activity}`")

    @jeanne()
    @is_owner()
    async def update(self, ctx):
        await ctx.send(f"YAY! NEW UPDATE!")
        restart_bot()      

def setup(bot):
    bot.add_cog(owner(bot))
