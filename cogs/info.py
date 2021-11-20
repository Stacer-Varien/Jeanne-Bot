import discord
import sys
import time
from discord.ext import commands
from discord import Member, Embed
from discord.ext.commands.errors import MemberNotFound

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['uinfo', 'minfo'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, *, member: Member = None):
        if member == None:
            member = ctx.author
        hasroles = [
            role.mention for role in member.roles][1:][:: -1]
        embed = Embed(title="{}'s Info".format(member.name),
                      color=0xccff33)
        embed.add_field(name="Name",
                        value=member,
                        inline=True)
        embed.add_field(name="Nickname",
                        value=member.nick,
                        inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Creation Date",
                        value=member.created_at.strftime(format),
                        inline=True)
        embed.add_field(
            name="Joined", value=member.joined_at.strftime(format), inline=True)
        embed.add_field(name="Number of Roles",
                        value=len(member.roles), inline=True)
        if len(hasroles) > 20:
            hasroles = hasroles[:20]
        embed.add_field(name="Roles",
                        value=" ".join(hasroles) + " @everyone", inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Command failed", description="This person is not in this server", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo', 'guild', 'ginfo'], pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        emojis = [str(x) for x in ctx.guild.emojis]
        features = [str(x) for x in ctx.guild.features]
        embed = discord.Embed(color=0x00B0ff)
        embed.set_author(name="Server Info")
        embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        embed.add_field(name="Owner ID", value=ctx.guild.owner.id, inline=True)
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.add_field(name="Members", value=len(
            ctx.guild.members), inline=True)
        embed.add_field(name="Creation Date",
                        value=ctx.guild.created_at.strftime(format),
                        inline=True)
        embed.add_field(name="Verification",
                        value=ctx.guild.verification_level,
                        inline=True)
        embed.add_field(name="Boosts",
                        value=ctx.guild.premium_subscription_count,
                        inline=True)

        if ctx.guild.premium_subscription_count < 2:
            boostlevel = "Level 0"
        elif ctx.guild.premium_subscription_count < 3:
            boostlevel="Level 1"
        elif ctx.guild.premium_subscription_count < 8:
            boostlevel = "Level 2"
        elif ctx.guild.premium_subscription_count==14:
            boostlevel = "Level 3"
        elif ctx.guild.premium_subscription_count <14:
            boostlevel = "Level 3"
            
        embed.add_field(name="Boost Level",
                        value=boostlevel,
                        inline=True)
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Emojis", value=len(emojis), inline=True)
        if len(emojis) > 10:
            emojis = emojis[:10]
        elif len(emojis) == 0:
            emojis = "None"
        embed.add_field(name='Emojis (first 10)',
                        value="".join(emojis), inline=False)
        embed.add_field(name="Features", value=features, inline=False)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.splash_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['serverbanner', 'gbanner', 'sbanner'])
    async def guildbanner(self, ctx):
        guild = ctx.guild
        banner = guild.banner_url

        if guild.premium_subscription_count < 7:
            nobanner = Embed(description="Server is not boosted at level 2")
            await ctx.send(embed=nobanner)

        else:

            embed = Embed(colour=0x00B0ff)
            embed.set_footer(text=f"{guild.name}'s banner")
            embed.set_image(url=banner)
            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):

        start_time = time.time()
        test = Embed(description="Testing Ping...", colour=0x236ce1)
        message = await ctx.send(embed=test)
        end_time = time.time()

        embed = Embed(color=0x236ce1)
        embed.add_field(
            name="Ping Latency", value=f'{round(ctx.bot.latency * 1000)}ms', inline=False)
        embed.add_field(
            name="API Latency", value=f'{round((end_time - start_time) * 1000)}ms', inline=False)
        await message.edit(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        embed = Embed(title="Bot stats", color=0x236ce1)
        embed.add_field(
            name="Name", value="<@!831993597166747679>", inline=True)
        embed.add_field(name="Bot ID", value="831993597166747679", inline=True)
        embed.add_field(name="Bot Owner",
                        value="<@!597829930964877369>", inline=True)
        embed.add_field(name="Python Version",
                        value=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", inline=True)
        embed.add_field(name="Discord.py Version",
                        value=f"{discord.__version__}", inline=True)
        embed.add_field(name="Server Count",
                        value=f"{len(ctx.bot.guilds)} servers", inline=True)
        embed.add_field(name="User Count",
                        value=f"{len(set(ctx.bot.get_all_members()))}", inline=True)
        embed.add_field(name="Ping Latency",
                        value=f'{round(ctx.bot.latency * 1000)}ms', inline=True)
        embed.add_field(
            name="Uptime", value="[Click Here](https://status.watchbot.app/bot/831993597166747679)\nPowered by [WatchBot](https://watchbot.app/)")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/831993597166747679/763c0da36ae6dec08433a01c58cf7e60.webp?size=1024")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
