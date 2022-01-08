from time import time
from asyncio import sleep
from datetime import timedelta
from sys import version_info as py_version
from nextcord.ext.commands import BucketType, command as jeanne, Cog, cooldown
from nextcord import Member, Embed, __version__ as nextcord_version


format = "%d %b %Y | %H:%M:%S"
start_time = time()


class info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne(aliases=['uinfo', 'minfo'])
    @cooldown(1, 5, BucketType.user)
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
        userinfo.set_thumbnail(url=member.display_avatar)
        await ctx.send(embed=userinfo)

    @jeanne(aliases=['sinfo', 'guild', 'ginfo'])
    @cooldown(1, 5, BucketType.user)
    async def serverinfo(self, ctx):
        guild=ctx.guild
        emojis = [str(x) for x in guild.emojis]
        features = [str(x) for x in guild.features]
        true_member_count = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])

        if guild.premium_subscription_count < 2:
            boostlevel = "Level 0"
        elif guild.premium_tier_1:
            boostlevel = "Level 1"
        elif guild.premium_tier_2:
            boostlevel = "Level 2"
        elif guild.premium_tier_3:
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

        if guild.icon==None:
            pass
        else:
            embed.set_thumbnail(url=guild.icon)

        if guild.splash==None:
            pass
        else:
            embed.set_image(url=guild.splash)
        await ctx.send(embed=embed)

    @jeanne(aliases=['serverbanner', 'gbanner', 'sbanner'])
    @cooldown(1, 5, BucketType.user)
    async def guildbanner(self, ctx):
        guild = ctx.guild
        banner = guild.banner

        if guild.premium_subscription_count < 2 or guild.premium_tier_1:
            nobanner = Embed(description="Server is not boosted at level 2")
            await ctx.send(embed=nobanner)
        else:
            embed = Embed(colour=0x00B0ff)
            embed.set_footer(text=f"{guild.name}'s banner")
            embed.set_image(url=banner)
            await ctx.send(embed=embed)

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx):
        _1st_start_time = time()
        test = Embed(description="Testing Ping...", colour=0x236ce1)
        message = await ctx.send(embed=test)
        _1st_end_time = time()

        _2nd_start_time = time()
        await sleep(0.5)
        _2nd_end_time = time()

        ping = Embed(color=0x236ce1)
        ping.add_field(
            name="**>** Bot Latency", value=f'{round(self.bot.latency * 1000)}ms', inline=False)
        ping.add_field(
            name="**>** 1st API Latency", value=f'{round((_1st_end_time - _1st_start_time) * 1000)}ms', inline=False)
        ping.add_field(
            name="**>** 2nd API Latency", value=f'{round((_2nd_end_time - _2nd_start_time) * 1000)}ms', inline=False)
        await message.edit(content="Ping results", embed=ping)

    @jeanne()
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
            name="Version", value=f"**>** **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n**>** **nextcord.py Version:** {nextcord_version}", inline=True)
        embed.add_field(name="Count",
                        value=f"**>** **Server Count:** {len(ctx.bot.guilds)} servers\n**>** **User Count:** {len(set(ctx.bot.get_all_members()))}", inline=True)
        # this is an empty field
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(name="Ping",
                        value=f"**>** **Bot Latency:** {round(ctx.bot.latency * 1000)}ms", inline=True)
        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = str(timedelta(seconds=difference))
        embed.add_field(
            name="Uptime", value=f"{uptime} hours")
        embed.set_thumbnail(
            url=self.bot.user.display_avatar)
        await ctx.send(embed=embed)

    @jeanne(aliases=['av','pfp'])
    async def avatar(self, ctx, *, member: Member = None):
        if member==None:
            member=ctx.author

        avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)
        avatar.set_image(url=member.display_avatar)
        await ctx.send(embed=avatar)

    @jeanne(aliases=['gav', 'gpfp', 'gavatar'])
    async def guildavatar(self, ctx, *, member: Member = None):

        if member == None:
            member = ctx.author

        guild_avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)
        try: 
            guild_avatar.set_image(url=member.guild_avatar)
            await ctx.send(embed=guild_avatar)
        except:
            guild_avatar.set_image(url=member.display_avatar)
            guild_avatar.set_footer(text="Member has no server avatar. Passed normal avatar instead")
            await ctx.send(embed=guild_avatar)

    @jeanne(aliases=['mbanner','banner','memberbanner'])
    async def member_banner(self, ctx,*, member:Member=None):
        if member==None:
            member=ctx.author

        member_id=member.id
        user= await self.bot.fetch_user(member_id)

        try: 
            mbanner = Embed(title=f"{user}'s Banner", color=0x236ce1)
            mbanner.set_image(url=user.banner)
            await ctx.send(embed=mbanner)
        except:
            mbanner = Embed(description="Member has no banner", color=0x236ce1)
            await ctx.send(embed=mbanner)
        


def setup(bot):
    bot.add_cog(info(bot))


