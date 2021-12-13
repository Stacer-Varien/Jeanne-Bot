import discord, sys, os
from discord import Embed, Activity, ActivityType
from discord.ext import commands
from discord import User, Guild

def restart_bot():
  os.execv(sys.executable, ['python'] + sys.argv)

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"
class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fuser'])
    @commands.is_owner()
    async def finduser(self, ctx, user:User):
        if user.bot == True:
            botr = ":o:"
        else:
            botr = ":x:"

        fuser = Embed(title="User Found", color=0xccff33)
        fuser.add_field(name="User Information",
                           value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}\n**>** **Creation Date:** {user.created_at.strftime(format)}\n**>** **Mutuals:** {len(user.mutual_guilds)}\n**>** **Is Bot?:** {botr}",
                           inline=True)
        fuser.set_image(url=user.avatar_url)
        await ctx.send(embed=fuser)

    

    @commands.command(aliases=['fserver'])
    @commands.is_owner()
    async def findserver(self, ctx, *, guild: Guild):
        fserver = Embed(color=0x00B0ff)
        fserver.set_author(name="Server Found")
        fserver.add_field(name="General Information",
                        value=f"**>** **Name:** {guild.name}\n**>** **ID:** {guild.id}\n**>** **Creation Date:** {guild.created_at.strftime(format)}\n**>** **Member Count:** {len(guild.members)}\n**>** **Verification:** {guild.verification_level}\n**>** **Roles:** {len(guild.roles)}", inline=True)
        fserver.add_field(
            name="Owner", value=f"**>** **Name:**{guild.owner}\n**>** **ID:** {guild.owner.id}", inline=True)
        fserver.add_field(name="_ _", value="_ _", inline=False)
        fserver.add_field(name="**>** **Server Features**",
                        value=guild.features, inline=False)
        fserver.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=fserver)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def mutuals(self, ctx, *, user: User):
        embed = Embed(title="Mutual Servers",
                              color=0xF7FF00)
        embed.add_field(name="Name", value=user, inline=True)
        embed.add_field(name="Mutuals", value=len(
            user.mutual_guilds), inline=True)
        embed.add_field(name="Servers", value=user.mutual_guilds, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['bm'])
    @commands.is_owner()
    async def botmutuals(self, ctx):
        mutuals = [str(x) for x in ctx.bot.guilds]
        embed = Embed(color=0xF7FF00)
        embed.add_field(name="Mutuals", value=len(ctx.bot.guilds), inline=True)
        if len(mutuals) > 1024:
            mutuals = mutuals[:1024]
        embed.add_field(name="Servers", value="[ ]".join(
            mutuals), inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def activity(self, ctx, activitytype, *, activity):

        if activitytype=="listen":
            await ctx.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
            await ctx.send(f"Bot's activity changed to `listening to {activity}`")
        elif activitytype=="play":
            await ctx.bot.change_presence(activity=discord.Game(name=activity))
            await ctx.send(f"Bot's activity changed to `playing {activity}`")

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        await ctx.send(f"YAY! NEW UPDATE!")
        restart_bot()              

def setup(bot):
    bot.add_cog(owner(bot))
