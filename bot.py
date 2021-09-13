import os
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands.converter import clean_content
from discord.ext.commands.errors import CommandInvokeError, MissingPermissions
from discord_slash import SlashCommand, SlashContext
import random
import time
import datetime
import sys
from discord.app import Option
import aiohttp

intents = discord.Intents().all()
aliases = ['re!', 'Re!', 'nero ', 'Nero ']
bot = commands.Bot(command_prefix=aliases, intents=intents)
slash = SlashCommand(bot, override_type=True)

bot.remove_command('help')

bot.load_extension("cogs.moderation")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.manage")
bot.load_extension("cogs.info")
bot.load_extension("cogs.owner")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('DiscordBots'))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

@bot.slash_command(description="See the bot's status from development to now")
async def stats(ctx):
    embed = discord.Embed(title="Bot stats", color=0x236ce1)
    embed.add_field(name="Name", value="Nero#3694", inline=True)
    embed.add_field(name="Bot ID", value="831993597166747679", inline=True)
    embed.add_field(name="Bot Owner",
                    value="<@!597829930964877369>", inline=True)
    embed.add_field(name="Python Version",
                    value=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", inline=False)
    embed.add_field(name="Discord.py Version",
                    value=f"{discord.__version__} (PyCord)", inline=True)
    embed.add_field(name="Server Count",
                    value=f"{len(ctx.bot.guilds)} servers", inline=True)
    embed.add_field(name="User Count",
                    value=f"{len(set(ctx.bot.get_all_members()))}", inline=True)
    embed.add_field(name="Ping Latency",
                    value=f'{round(ctx.bot.latency * 1000)}ms', inline=True)
    embed.add_field(name="License",
                    value='[MIT License](https://github.com/ZaneRE544/NeroBot/blob/main/LICENSE)', inline=True)
    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = str(datetime.timedelta(seconds=difference))
    embed.add_field(name="Uptime", value=f"{uptime} hours", inline=True)
    embed.set_footer(text="The Discord PY version is different than the usuall `re!stats` because you have used a slash command")
    await ctx.send(embed=embed)

@bot.slash_command(name="8ball", description="Ask 8 ball anything and you will get your awnser")
async def _8ball(ctx, question):
    responses = [
        'It is certain.', 'It is decidedly so.', 'Without a doubt.',
        'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
        'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
        'Reply hazy, try again.', 'Ask again later.',
        'Better not tell you now.', 'Cannot predict now.',
        'Concentrate and ask again.', 'Dont count on it.', 'My reply is no.',
        'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
    ]
    embed = discord.Embed(color=0x0000FF)
    embed.add_field(name="Question:", value=f'{question}', inline=False)
    embed.add_field(
        name="Answer:", value=f'{random.choice(responses)}', inline=False)
    await ctx.send(embed=embed)

@bot.slash_command(description="See the information of a member or yourself")
async def userinfo(ctx, member: Member):
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
        embed.add_field(name="Number of Roles",
                        value=len(member.roles), inline=False)
        if len(hasroles) > 20:
            hasroles = hasroles[:20]
        embed.add_field(name="Roles",
                        value=" ".join(hasroles), inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Creation Date",
                        value=member.created_at.strftime(format),
                        inline=False)
        embed.add_field(
            name="Joined", value=member.joined_at.strftime(format), inline=False)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

@bot.slash_command(description="Get some animemes")
async def animeme(ctx):
    animeme_subreddits = [
        'https://www.reddit.com/r/Animemes/new.json?sort=hot', 'https://www.reddit.com/r/animememes/new.json?sort=hot', 'https://www.reddit.com/r/goodanimemes/new.json?sort=hot']
    embed = discord.Embed(colour=0x0000FF)
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'{random.choice(animeme_subreddits)}') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children']
                            [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.slash_command(description="Type two words to get one combined word")
async def combine(ctx, name1: Option(str, "Enter 1st word"), name2: Option(str, "Enter 2nd word"),):
    name1letters = name1[:round(len(name1) / 2)]
    name2letters = name2[round(len(name2) / 2):]
    ship = "".join([name1letters, name2letters])
    emb = (discord.Embed(color=0x36393e, description=f"{ship}"))
    emb.set_author(name=f"{name1} + {name2}")
    await ctx.send(embed=emb)

@bot.slash_command(description="Invite me to a server or join these servers")
async def invite(ctx):
    embed = discord.Embed(
        title="Invite me!",
        description="Click on one of these URLs to invite me to you server or join my creator's servers",
        color=0x00bfff)
    embed.add_field(name="Bot Invite",
                    value="[Click here](https://discord.com/oauth2/authorize?client_id=831993597166747679&scope=bot&permissions=469888182)",
                    inline=True)
    embed.add_field(name="Top.gg",
                    value="[Click here](https://top.gg/bot/831993597166747679)",
                    inline=True)
    embed.add_field(name="DiscordBots",
                    value="[Click here](https://discord.bots.gg/bots/831993597166747679)", inline=True)
    embed.add_field(name="DiscordBotList",
                    value="[Click here](https://discordbotlist.com/bots/nero-3694)", inline=True)
    embed.add_field(name="HAZE server",
                    value="[Click here](https://discord.gg/VVxGUmqQhF)", inline=True)
    embed.add_field(name="NERO Support Server",
                    value="[Click here](https://discord.gg/Xn3EvGcMrF)", inline=True)
    await ctx.send(embed=embed)

@bot.slash_command(description="Get information about this server")
async def serverinfo(ctx):
        emojis = [str(x) for x in ctx.guild.emojis]
        features =[str(x) for x in ctx.guild.features]
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
        embed.add_field(name="Emojis", value=len(emojis), inline=True)
        embed.add_field(name="Server Features",
                        value=" \n".join(features) if len(features) > 0 else "None",
                        inline=False)

        if len(emojis) > 10:
            emojis = emojis[:10]
        embed.add_field(name='Emojis (first 10)',
                        value="".join(emojis), inline=False)

        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

@bot.slash_command(description="Flip a coin")
async def flip(ctx):
    await ctx.send(embed=discord.Embed(color=0x0000FF,
                                       description=f"`{random.choice(['Heads', 'Tails'])}`"))

@bot.slash_command(description="Show the help menu")
async def help(ctx):
    embed = discord.Embed(title="Help Commands",
                          description="Here are some commands to help you.",
                          color=0x236ce1)
    embed.add_field(name="Fun",
                    value="8 Ball (8b, 8ball)\nHentai (h) **NSFW**\nRoll Dice (rd, dice)\nCombine\nAnimeme (meme, animememe)\nFlip (coinflip, headsortails, piece)",
                    inline=True)
    embed.add_field(
        name="Info",
        value="User Info (uinfo, minfo, guild, guildinfo)\nServer Info (sinfo)\nAvavtar (av)Ping\nStats",
        inline=True)
    embed.add_field(
        name="Creator Only",
        value="Find Server (fserver)\nFind User (fuser)\nMutuals\nBot Mutuals (bm)",
        inline=True)
    embed.add_field(
        name="Misc", value="Help\nInvite\nSay\nSayembed (saye)", inline=True)
    embed.add_field(name="Moderation",
                    value="Warn (w)\nKick (k)\nBan (b)\nUnban (unb)\nPurge\nMute\nUnmute",
                    inline=True)
    embed.add_field(name="Management",
                    value="Text Channel (tc)\nVoice Channel (vc)\nRole (r)\nCategory (cat)",
                    inline=True)
    await ctx.send(embed=embed)

load_dotenv()
TOKEN = os.getenv("token")
bot.run(TOKEN)
