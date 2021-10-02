import discord
import asyncio
import re
from discord import User, Member
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord.ext.commands import MissingPermissions


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

    @cog_ext.cog_slash(description="Unban a user")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx:SlashContext, user : User, reason=None):
                await ctx.guild.unban(user)
                embed = discord.Embed(title="User Unbanned", color=0xFF0000)
                embed.add_field(name="Name",
                                value=user,
                                inline=False)
                embed.add_field(name="ID", value=user.id, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_author(name=ctx.message.author,
                                icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)


    @cog_ext.cog_slash(description="Unmute a member")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx:SlashContext, member: Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f"You have unmuted from: - {ctx.guild.name}")
        embed = discord.Embed(
            title="unmute", description=f" unmuted-{member.mention}", colour=discord.Colour.light_gray())
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
    async def ban(self, ctx:SlashContext, member: discord.User, reason=None):
                embed = discord.Embed(title="User Banned", color=0xFF0000)
                embed.add_field(name="Name",
                                value=member,
                                inline=False)
                embed.add_field(name="ID", value=member.id, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_author(name=ctx.message.author,
                                icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
                await ctx.guild.ban(member, reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=discord.Embed(title="Ban failed", description="Sorry but you cannot ban this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Ban Members", inline=False)
                await ctx.send(embed=embed) 
   

    @cog_ext.cog_slash(description="Kick a member out of the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx:SlashContext, member: discord.Member, reason=None):
            embed = discord.Embed(title="User Kicked", color=0xFF0000)
            embed.add_field(name="Name",
                            value=member,
                            inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_author(name=ctx.message.author,
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)

            await ctx.send(embed=embed)
            await ctx.guild.kick(member, reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=discord.Embed(title="Kick failed", description="Sorry but you cannot kick this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
                await ctx.send(embed=embed) 
        


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
        await ctx.send(("Muted {} for {} for {}s" if time else "Muted {} for {}").format(member, reason, time))
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
    async def purge(self, ctx, limit=100, member: discord.Member = None):
        await ctx.message.delete()
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
                embed=discord.Embed(title="Purge failed", description="Sorry but you cannot purge any messages", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Manage Messages", inline=False)
                await ctx.send(embed=embed) 

def setup(bot):
    bot.add_cog(moderation(bot))
