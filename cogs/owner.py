import discord
from discord.ext import commands
from discord import Member, User, Guild, Role

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"
class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fuser'], pass_context=True)
    @commands.is_owner()
    async def finduser(self, ctx, user: User = None):
        embed = discord.Embed(title="User Found", color=0xccff33)
        embed.add_field(name="Name",
                        value=user,
                        inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Creation Date",
                        value=user.created_at.strftime(format),
                        inline=True)
        embed.add_field(name="Mutuals", value=len(
            user.mutual_guilds), inline=True)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['fserver'], pass_context=True)
    @commands.is_owner()
    async def findserver(self, ctx: commands.Context, guild: Guild):
        embed = discord.Embed(color=0x00B0ff)
        embed.set_author(name="Server Found")
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Owner ID", value=guild.owner.id, inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Region", value=guild.region, inline=True)
        embed.add_field(name="Members", value=len(guild.members), inline=True)
        embed.add_field(name="Creation Date",
                        value=guild.created_at.strftime(format),
                        inline=True)
        embed.add_field(name="Verification",
                        value=guild.verification_level,
                        inline=True)
        embed.add_field(name="Server Features",
                        value=guild.features, inline=True)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def mutuals(self, ctx, user: User):
        embed = discord.Embed(title="Mutual Servers".format(user.name),
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
        embed = discord.Embed(color=0xF7FF00)
        embed.add_field(name="Mutuals", value=len(ctx.bot.guilds), inline=True)
        if len(mutuals) > 25:
            mutuals = mutuals[:25]
        embed.add_field(name="Servers", value=" \n".join(
            mutuals), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(owner(bot))
