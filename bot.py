import json
import os
import sys
import discord
from discord.ext import commands


format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='re!', intents=intents)
bot.remove_command('help')
bot.load_extension("cogs.nsfw")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.manage")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('with Kawaii'))

    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

#ping
@bot.command()
async def ping(ctx):
    embed = discord.Embed(color=0x236ce1)
    embed.add_field(
        name="Ping", value=f'{round(bot.latency * 1000)}ms', inline=False)
    await ctx.send(embed=embed)
#ping

#info cmds
@bot.command(aliases=['minfo', 'uinfo'], pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def userinfo(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title="{}'s Info".format(member.name),
                          color=0xccff33)
    embed.add_field(name="Name",
                    value=member.name + "#" + member.discriminator,
                    inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Creation Date",
                    value=member.created_at.strftime(format),
                    inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime(format))
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.group(aliases=['sinfo', 'guild', 'ginfo'], pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def serverinfo(ctx):
    emojis = [str(x) for x in ctx.guild.emojis]
    features= [str(x) for x in ctx.guild.features]
    embed = discord.Embed(color=0x00B0ff)
    embed.set_author(name="Server Info")
    embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
    embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
    embed.add_field(name="Owner ID", value=ctx.guild.owner.id, inline=True)
    embed.add_field(name="ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Region", value=ctx.guild.region, inline=True)
    embed.add_field(name="Members", value=len(ctx.guild.members), inline=True)
    embed.add_field(name="Creation Date",
                    value=ctx.guild.created_at.strftime(format),
                    inline=True)
    embed.add_field(name="Verification",
                    value=ctx.guild.verification_level,
                    inline=True)
    embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="Emojis", value=len(emojis), inline=True)    
    embed.add_field(name="Server Features",
                    value=" \n".join(features),
                    inline=False)
    
    if len(emojis) > 20:
            emojis=emojis[:20]
    embed.add_field(name='Emojis (first 20)', value="".join(emojis), inline=False)
    
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command(aliases=['fuser'], pass_context=True)
@commands.is_owner()
async def finduser(ctx, user: discord.User = None):
    embed = discord.Embed(title="User Found", color=0xccff33)
    embed.add_field(name="Name",
                    value=user.name + "#" + user.discriminator,
                    inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Creation Date",
                    value=user.created_at.strftime(format),
                    inline=True)
    embed.add_field(name="Mutuals", value=len(user.mutual_guilds), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)


@bot.command(aliases=['fserver'], pass_context=True)
@commands.is_owner()
async def findserver(ctx: commands.Context, guild: discord.Guild):
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
    embed.add_field(name="Server Features", value=guild.features, inline=True)
    embed.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
@commands.is_owner()
async def mutuals(ctx: commands.Context, user: discord.User):
    embed = discord.Embed(title="Mutual Servers".format(user.name),
                          color=0xF7FF00)
    embed.add_field(name="Name", value=user, inline=True)
    embed.add_field(name="Mutuals", value=len(user.mutual_guilds), inline=True)
    embed.add_field(name="Servers", value=user.mutual_guilds, inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases = ['bm'])
@commands.is_owner()
async def botmutuals(ctx):
    mutuals = [str(x) for x in ctx.bot.guilds]
    embed = discord.Embed(color=0xF7FF00)
    embed.add_field(name="Mutuals", value=len(bot.guilds), inline=True)
    if len(mutuals) > 25:
            mutuals=mutuals[:25]  
    embed.add_field(name="Servers", value=" \n".join(mutuals), inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['av'], pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title="{}'s Avatar".format(member.name),
                          color=0x1A751B)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)
#end of info cmds

#errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            title="Command failed to execute",
            description="Sorry, this command can be used by my creator.",
            color=0xf00000)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.GuildNotFound):
        embed = discord.Embed(
            title="Server not found",
            description="Sorry but I can't find that server. Maybe it's because it does not exist, you didn't give me the ID, the ID is wrong or I am not in that server",
            color=0xf00000)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(
            title="User not found",
            description="Sorry but I can't find that user. Maybe it's because they do not exist, you gave me the incorrect or incompleted ID or they have deleted their account.",
            color=0xf00000)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Command on cooldown",
            description=f"Sorry but this command is on cooldown. Please try again after {error.retry_after: .2f} seconds.",
            color=0xf00000)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(
            title=f"NSFW Not Allowed",
            description="Sorry but it looks like this channel is not NSFW.",
            color=0xf00000)
        await ctx.send(embed=embed)
#end of errors



TOKEN = os.getenv("token")
bot.run(TOKEN)
