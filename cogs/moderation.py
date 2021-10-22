import discord, asyncio, re
from discord import User, Member, Embed
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands.errors import MemberNotFound
from discord.utils import get


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user : User, *, reason=None):
                await ctx.guild.unban(user)
                embed = Embed(title="User Unbanned", color=0xFF0000)
                embed.add_field(name="Name",
                                value=user,
                                inline=True)
                embed.add_field(name="ID", value=user.id, inline=True)
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.add_field(name="Responsible Moderator",
                                value=ctx.author, inline=True)
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: Member):
        mutedRole = get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        embed = Embed(
            title="Member Unmute", color=0xFF0000)
        embed.add_field(name="Name",
                        value=member,
                        inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Responsible Moderator",
                        value=ctx.author, inline=True)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['w'])
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: Member, reason=None):
        warn = Embed(title="Member Warned", color=0xFF0000)
        warn.add_field(name="Name", value=member, inline=True)
        warn.add_field(name="ID", value=member.id, inline=True)
        warn.add_field(name="Reason", value=reason, inline=True)
        warn.add_field(name="Responsible Moderator",
                      value=ctx.author, inline=True)
        warn.set_image(url=member.avatar_url)
        await ctx.send(embed=warn)

    @warn.error
    async def warn_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=Embed(title="Warn failed", description="Sorry but you cannot warn this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
                await ctx.send(embed=embed)
             elif isinstance(error, MemberNotFound):
                embed = discord.Embed(
                    Title="Warn failed", color=0xff0000)
                embed.add_field(
                    name="Reason", value="Member is not in this server or invalid user ID has been given", inline=False)
                await ctx.send(embed=embed)


    @commands.command(pass_context=True, aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: User, *, reason=None):
        banmsg = Embed(description=f"You are banned from **{ctx.guild.name}** for **{reason}**")
        try:
            await user.send(embed=banmsg) #if the member's DMs is opened before banning
        except Forbidden: #if member's DMs are closed
            pass    #will now ban the member
        ban = discord.Embed(title="User Banned", color=0xFF0000)
        ban.add_field(name="Name", value=user, inline=True)
        ban.add_field(name="ID", value=user.id, inline=True)
        ban.add_field(name="Reason", value=reason, inline=True)
        ban.add_field(name="Responsible Moderator", value=ctx.author, inline=True)
        ban.set_image(url=user.avatar_url)
        await ctx.send(embed=ban)
        await ctx.guild.ban(user, reason=reason)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed=Embed(title="Ban failed", description="Sorry but you cannot ban this user", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Ban Members", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):
            embed = Embed(
                title="Ban failed", description="Invalid user ID given.", color=0xff0000)
            await ctx.send(embed=embed)
            
   

    @commands.command(pass_context=True, aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        kickmsg = Embed(
            description=f"You are kicked from **{ctx.guild.name}** for **{reason}**")
        try:
            # if the member's DMs is opened
            await member.send(embed=kickmsg)
        except Forbidden:  # if member's DMs are closed
            pass  # will now kick the member
        kick = Embed(title="Member Kicked", color=0xFF0000)
        kick.add_field(name="Name", value=member, inline=True)
        kick.add_field(name="ID", value=member.id, inline=True)
        kick.add_field(name="Reason", value=reason, inline=True)
        kick.add_field(name="Responsible Moderator",
                      value=ctx.author, inline=True)
        kick.set_image(url=member.avatar_url)
        await ctx.send(embed=kick)
        await ctx.guild.kick(member, reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed=Embed(title="Kick failed", description="Sorry but you cannot kick this user", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):             
            embed = Embed(
                title="Kick failed", description="Member is not in this server", color=0xff0000)
            await ctx.send(embed=embed)    
        


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: Member, time: TimeConverter = None, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        mute = Embed(title="Member Muted", color=0xff0000)
        mute.add_field(name="Name", value=member, inline=True)
        mute.add_field(name="ID", value=member.id, inline=True)
        mute.add_field(name="Reason", value=reason, inline=True)
        mute.add_field(name="Duration", value=time, inline=True)
        mute.add_field(name="Responsible Moderator",
                       value=ctx.author, inline=True)
        mute.set_image(url=member.avatar_url)
        await ctx.send(embed=mute)
        if time:
            await asyncio.sleep(time)
            await member.remove_roles(role)
        
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed=discord.Embed(title="Mute failed", description="Sorry but you cannot mute this user", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
            await ctx.send(embed=embed)     
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Mute failed", description="Member is not in this server", color=0xff0000)
            await ctx.send(embed=embed)
 
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, member: Member = None, *, limit=100):
        msg = []
        try:
            limit = int(limit)
        except:
            return await ctx.send("Please pass in an integer as limit")
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)
        await self.bot.process_commands(m)

    @purge.error
    async def purge_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=discord.Embed(title="Purge failed", description="Sorry but you cannot purge messages", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Manage Messages", inline=False)
                await ctx.send(embed=embed) 

def setup(bot):
    bot.add_cog(moderation(bot))
