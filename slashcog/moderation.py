import discord, asyncio, re
from discord import Member, Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord.ext.commands import MissingPermissions
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


    @cog_ext.cog_slash(description="Unmute a member")
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
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Warn a member")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx:SlashContext, member: discord.Member, reason=None):
                embed = discord.Embed(title="User was warned", color=0xFF0000)
                embed.add_field(name="Name",
                                value=member,
                                inline=False)
                embed.add_field(name="ID", value=member.id, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_author(name=ctx.message.author,
                                icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)

                await ctx.send(embed=embed)

    @warn.error
    async def warn_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=discord.Embed(title="Warn failed", description="Sorry but you cannot warn this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
                await ctx.send(embed=embed) 


    @cog_ext.cog_slash(description="Ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx:SlashContext, user: Member, reason=None):
        try:
            banmsg = Embed(
                description=f"You are banned from **{ctx.guild.name}** for **{reason}**")
            await user.send(embed=banmsg)
        except:
            pass
        ban = discord.Embed(title="User Banned", color=0xFF0000)
        ban.add_field(name="Name", value=user, inline=True)
        ban.add_field(name="ID", value=user.id, inline=True)
        ban.add_field(name="Responsible Moderator",
                      value=ctx.author, inline=True)
        ban.add_field(name="Reason", value=reason, inline=True)
        ban.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=ban)
        await user.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=discord.Embed(title="Ban failed", description="Sorry but you cannot ban this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Ban Members", inline=False)
                await ctx.send(embed=embed) 
   

    @cog_ext.cog_slash(description="Kick a member out of the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        try:
            kickmsg = Embed(
                description=f"You are kicked from **{ctx.guild.name}** for **{reason}**")
            await member.send(embed=kickmsg)
        except:
            pass
        kick = Embed(title="Member Kicked", color=0xFF0000)
        kick.add_field(name="Name", value=member, inline=True)
        kick.add_field(name="ID", value=member.id, inline=True)
        kick.add_field(name="Responsible Moderator",
                       value=ctx.author, inline=True)
        kick.add_field(name="Reason", value=reason, inline=False)
        kick.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=kick)
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=discord.Embed(title="Kick failed", description="Sorry but you cannot kick this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
                await ctx.send(embed=embed) 

    @cog_ext.cog_slash(description="Creates a mute role")
    @commands.bot_has_permissions(manage_roles=True)
    async def muterole(self, ctx):
        guild = ctx.guild
        await guild.create_role(name="Muted")
        await ctx.send("Mute role created")

        for channel in guild.channels:
            mute_role = get(guild.roles, name="Muted")
            await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)


    @cog_ext.cog_slash(description="Mute a member")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, time: TimeConverter = None, reason=None):
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
        mute.set_thumbnail(url=member.avatar_url)
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
 
    @cog_ext.cog_slash(description="Bulk delete messages")
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
