import os
import discord
from discord import Member
from discord.ext import commands
import random
import time
import datetime
import sys
from discord.app import Option
from keep_alive import keep_alive
import requests
from dotenv import load_dotenv
from discord.ext.commands.errors import MemberNotFound, NotOwner, UserNotFound, GuildNotFound, NSFWChannelRequired, NotOwner, CommandOnCooldown

intents = discord.Intents().all()
aliases = ['j!', 'J!', 'jeanne ', 'Jeanne ']
bot = commands.Bot(command_prefix=aliases, intents=intents)
start_time = time.time()

bot.remove_command('help')

bot.load_extension("cogs.moderation")
bot.load_extension("cogs.help")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.manage")
bot.load_extension("cogs.info")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.reactions")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('DiscordBots'))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

@bot.slash_command(description="See the bot's status from development to now")
async def stats(ctx):
    embed = discord.Embed(title="Bot stats", color=0x236ce1)
    embed.add_field(name="Name", value="Jeanne#6665", inline=True)
    embed.add_field(name="Bot ID", value="831993597166747679", inline=True)
    embed.add_field(name="Bot Owner",
                    value="<@!597829930964877369>", inline=True)
    embed.add_field(name="Python Version",
                    value=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", inline=True)
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
    embed.set_footer(text="The Discord PY version is different than the usual `re!stats` command because you have used a slash command")
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

@bot.slash_command(description="Type two words to get one combined word")
async def combine(ctx, name1: Option(str, "Enter 1st word"), name2: Option(str, "Enter 2nd word"),):
    name1letters = name1[:round(len(name1) / 2)]
    name2letters = name2[round(len(name2) / 2):]
    join = "".join([name1letters, name2letters])
    emb = (discord.Embed(color=0x36393e, description=f"{join}"))
    emb.set_author(name=f"{name1} + {name2}")
    await ctx.send(embed=emb)

@bot.slash_command(description="Invite me to a server or join these servers")
async def invite(ctx):
    embed = discord.Embed(
        title="Invite me!",
        description="Click on one of these URLs to invite me to you server or join my creator's servers",
        color=0x00bfff)
    embed.add_field(name="Bot Invite",
                    value="[Click here](https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands)",
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
    embed.add_field(name="Jeanne Support Server",
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
                    value="8 Ball (8b, 8ball)\nHentai (h) **NSFW**\nRoll Dice (rd, dice)\nCombine\nFlip (coinflip, headsortails, piece)",
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

@bot.slash_command(description="Roll a dice")
async def dice(ctx):
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled", value="You rolled a {}!".format(
            random.randint(1, 6)), inline=False)
        await ctx.send(embed=embed)

@bot.slash_command(description="Get some hentai from Yande.re or Gelbooru")
async def hentai(ctx):
        if ctx.channel.is_nsfw():
                
                yandere_api = random.choice(requests.get("https://yande.re/post.json?tags=rating:explicit-yiff-loli-ntr-vore-poop-pooping-scat-scat_eating-scat_on_penis-bestiality-furry-shota-blood-rape-bee-animal-hyper-guro").json())
                yandere = discord.Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api["file_url"])
                yandere.set_footer(text="Fetched from Yande.re")

                gelbooru_api = random.choice(requests.get("https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=rating:explicit -yiff-loli-ntr-vore-poop-pooping-scat-scat_eating-scat_on_penis-bestiality-furry-shota-blood-rape-bee-animal-hyper-guro").json())
                gelbooru = discord.Embed(color=0xFFC0CB)
                gelbooru.set_image(url=gelbooru_api["file_url"])
                gelbooru.set_footer(text="Fetched from Gelbooru")

                hentai=[yandere, gelbooru]

                await ctx.send(embed=random.choice(hentai))
        else:
                error=discord.Embed(title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
                error.add_field(name="Reason", value="Channel is not NSFW enabled")
                await ctx.send(embed=error)

@bot.slash_command(description="Type a message and I will say it but it will be in plain text")
async def say(ctx, text):
        if ctx.author.guild_permissions.administrator:
                await ctx.send(text)                
        
        else:
                error=discord.Embed(title='Say Failed', description="I couldn't say this message", color=0xff0000)
                error.add_field(name="Reason", value="Missing Permission: Administrator")
                await ctx.send(embed=error)

@bot.slash_command(description="Type a message and I will say it but it will be in embed")
async def sayembed(ctx, text):
        if ctx.author.guild_permissions.administrator:
                say = discord.Embed(description=f"{text}", color=0xADD8E6)
                await ctx.send(embed=say)                
        
        else:
                error=discord.Embed(title='Say Failed', description="I couldn't say this message", color=0xff0000)
                error.add_field(name="Reason", value="Missing Permission: Administrator")
                await ctx.send(embed=error)

@bot.slash_command(description="Type something and I will reverse the text")
async def reverse(ctx, text):
    await ctx.send(text[::-1])
    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, NotOwner):
       embed = discord.Embed(
           title="Owner only command", description="This command failed to commit because you are not the bot owner", color=0xff0000)
       await ctx.send(embed=embed)
    elif isinstance(error, GuildNotFound):
        embed = discord.Embed(
            description="Bot is not in this server", color=0xff0000)
        await ctx.send(embed=embed)
    elif isinstance(error, UserNotFound):
            no_user = discord.Embed(
                title="User does not exist", description="Please make sure the USER_ID is valid or maybe they have deleted their account.", color=0xff0000)
            await ctx.send(embed=no_user)
    elif isinstance(error, CommandOnCooldown):
        embed = discord.Embed(
            title="Command On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
        await ctx.send(embed=embed)
    elif isinstance(error, NSFWChannelRequired):
        error = discord.Embed(
            title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
        error.add_field(
            name="Reason", value="Channel is not NSFW enabled")
        await ctx.send(embed=error)

load_dotenv()
TOKEN = os.getenv("token")
bot.run(TOKEN)
