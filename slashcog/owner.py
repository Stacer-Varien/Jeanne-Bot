import discord
from discord import Embed, Activity, ActivityType
from discord.ext import commands
from discord_slash import cog_ext

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"
class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(description="See where which servers Jeanne is in (CREATOR ONLY)")
    @commands.is_owner()
    async def botmutuals(self, ctx):
        mutuals = [str(x) for x in self.bot.guilds]
        embed = Embed(color=0xF7FF00)
        embed.add_field(name="Mutuals", value=len(self.bot.guilds), inline=True)
        if len(mutuals) > 1024:
            mutuals = mutuals[:1024]
        embed.add_field(name="Servers", value=" ,".join(
            mutuals), inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Changes the bot's play activity")
    @commands.is_owner()
    async def activity(self, ctx, activitytype, activity):

        if activitytype=="listen":
            await ctx.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
            await ctx.send(f"Bot's activity changed to `listening to {activity}`")
        elif activitytype=="play":
            await ctx.bot.change_presence(activity=discord.Game(name=activity))
            await ctx.send(f"Bot's activity changed to `playing with {activity}`")

    @cog_ext.cog_slash(description="Finds a user")
    @commands.is_owner()
    async def finduser(self, ctx, user_id):

        user = await self.bot.fetch_user(user_id)

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

def setup(bot):
    bot.add_cog(owner(bot))
