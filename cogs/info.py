import discord, sys, time
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Member, Embed


format = "%d %b %Y | %H:%M:%S"


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['uinfo', 'minfo'])
    @commands.guild_only()
    @commands.cooldown(1, 5, BucketType.user)
    async def userinfo(self, ctx, *, member: Member = None):
        if member == None:
            member = ctx.author
        hasroles = [
            role.mention for role in member.roles][1:][:: -1]

        if member.bot == True:
            botr = ":o:"
        else:
            botr = ":x:"

        userinfo = Embed(title="{}'s Info".format(member.name),
                         color=0xccff33)
        userinfo.add_field(name="General Information",
                           value=f"**>** **Name:** {member}\n**>** **Nickname:** {member.nick}\n**>** **ID:** {member.id}\n**>** **Creation Date:** {member.created_at.strftime(format)}\n**>** **Is Bot?:** {botr}",
                           inline=True)
        userinfo.add_field(name="Member Information",
                           value=f"**>** **Joined Server:** {member.joined_at.strftime(format)}\n**>** **Number of Roles:** {len(member.roles)}",
                           inline=True)
        userinfo.add_field(name="Roles Held",
                           value=''.join(hasroles[:20]) + '@everyone', inline=False)
        userinfo.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=userinfo)

    @commands.command(aliases=['sinfo', 'guild', 'ginfo'])
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild=ctx.guild
        emojis = [str(x) for x in guild.emojis]
        features = [str(x) for x in guild.features]
        true_member_count = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])

        if guild.premium_subscription_count < 2:
            boostlevel = "Level 0"
        elif guild.premium_subscription_count < 3:
            boostlevel = "Level 1"
        elif guild.premium_subscription_count < 8:
            boostlevel = "Level 2"
        elif guild.premium_subscription_count == 14:
            boostlevel = "Level 3"
        elif guild.premium_subscription_count < 14:
            boostlevel = "Level 3"

        embed = Embed(title="Server's Info", color=0x00B0ff)
        embed.add_field(name="General Information",
                        value=f"**>** **Name:** {guild.name}\n**>** **ID:** {guild.id}\n**>** **Creation Date:** {guild.created_at.strftime(format)}\n**>** **Member Count:** {len(guild.members)}\n**>** **Verification:** {guild.verification_level}\n**>** **Roles:** {len(guild.roles)}\n**>** **Emojis:** {len(emojis)}\n{''.join(emojis[:10])}", inline=True)
        embed.add_field(
            name="Owner", value=f"**>** **Name:** {guild.owner}\n**>** **ID:** {guild.owner.id}", inline=True)
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(name="Boost Status",
                        value=f"**>** **Boosters:** {len(guild.premium_subscribers)}\n**>** **Boosts:** {guild.premium_subscription_count}\n**>** **Boost Level:** {boostlevel}",
                        inline=True)
        embed.add_field(name="Members", value=f"**>** **Humans:** {true_member_count}\n**>** **Bots:** {bots}")
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(name='Features',
                        value=features, inline=False)


        embed.set_thumbnail(url=guild.icon_url)
        embed.set_image(url=guild.splash_url)
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

        ping = Embed(color=0x236ce1)
        ping.add_field(
            name="**>** Bot Latency", value=f'{round(ctx.bot.latency * 1000)}ms', inline=False)
        ping.add_field(
            name="**>** API Latency", value=f'{round((end_time - start_time) * 1000)}ms', inline=False)
        await message.edit(content="Ping results", embed=ping)

    @commands.command()
    async def stats(self, ctx):
        botowner = self.bot.get_user(597829930964877369)
        embed = Embed(title="Bot stats", color=0x236ce1)
        embed.add_field(
            name="General Information", value=f"**>** **Name:** {self.bot.user}\n**>** **ID:** {self.bot.user.id}", inline=False)
        embed.add_field(
            name="Developer", value=f"**>** **Name:** {botowner}\n**>** **ID:** {botowner.id}")
        # this is an empty field
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(
            name="Version", value=f"**>** **Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n**>** **Discord.py Version:** {discord.__version__}", inline=True)
        embed.add_field(name="Count",
                        value=f"**>** **Server Count:** {len(ctx.bot.guilds)} servers\n**>** **User Count:** {len(set(ctx.bot.get_all_members()))}", inline=True)
        # this is an empty field
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(name="Ping",
                        value=f"**>** **Bot Latency:** {round(ctx.bot.latency * 1000)}ms", inline=True)
        embed.add_field(
            name="Uptime", value="[Click Here](https://status.watchbot.app/bot/831993597166747679)\nPowered by [WatchBot](https://watchbot.app/)")
        embed.set_thumbnail(
            url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['av','pfp'])
    async def avatar(self, ctx, *, member: Member = None):
        if member==None:
            member=ctx.author

        avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)
        avatar.set_image(url=member.avatar_url)
        await ctx.send(embed=avatar)

def setup(bot):
    bot.add_cog(info(bot))


