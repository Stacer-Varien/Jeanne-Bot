import discord, time, sys
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord import Member


format = "%a, %d %b %Y | %H:%M:%S"
start_time = time.time()

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="See the bot's status from development to now")
    async def stats(self, ctx:SlashContext):
        embed = discord.Embed(title="Bot stats", color=0x236ce1)
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
        embed.add_field(name="License",
                        value='[MIT License](https://github.com/ZaneRE544/JeanneBot/blob/main/LICENSE)', inline=True)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/831993597166747679/763c0da36ae6dec08433a01c58cf7e60.webp?size=1024")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="See the information of a member or yourself")
    async def userinfo(self, ctx: SlashContext, member: Member = None):
        if member == None:
                member=ctx.author
        hasroles = [
            role.mention for role in member.roles][1:][:: -1]
        embed = discord.Embed(title="{}'s Info".format(member.name),
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
                        value=" ".join(hasroles), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get information about this server")
    async def serverinfo(self, ctx: SlashContext):
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
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Features", value=features, inline=False)
        embed.add_field(name="Emojis", value=len(emojis), inline=True)
        if len(emojis) > 10:
            emojis = emojis[:10]
        elif len(emojis) == 0:
            emojis = "None"
        embed.add_field(name='Emojis (first 10)',
                        value="".join(emojis), inline=False)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.splash_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Check how fast I respond to a command")
    async def ping(self, ctx: SlashContext):
        embed = discord.Embed(color=0x236ce1)
        embed.add_field(
            name="Ping", value=f'{round(ctx.bot.latency * 1000)}ms', inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))
