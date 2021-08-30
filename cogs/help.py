import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand != None:
            return
        embed = discord.Embed(title="Help Commands",
                              description="Here are some commands to help you.",
                              color=0x236ce1)
        embed.add_field(name="Fun",
                        value="8 Ball (8b, 8ball)\nHentai (h) **NSFW**\nRoll Dice (rd, dice)\nCombine\nAnimeme (meme, animememe)",
                        inline=True)
        embed.add_field(
            name="Info",
            value="User Info (uinfo, minfo, guild, guildinfo)\nServer Info (sinfo)\nAvavtar (av)",
            inline=True)
        embed.add_field(
            name="Creator Only",
            value="Find Server (fserver)\nFind User (fuser)\nMutuals\nReward",
            inline=True)
        embed.add_field(
            name="Misc", value="Ping\nHelp\nInvite\nSay", inline=True)
        embed.add_field(name="Moderation",
                        value="Warn (w)\nKick (k)\nBan (b)\nUnban (unb)\nPurge\nMute\nUnmute",
                        inline=True)
        embed.add_field(name="Management",
                        value="Text Channel (tc)\nVoice Channel (vc)\nRole (r)",
                        inline=True)
        await ctx.send(embed=embed)

    @help.command()
    async def ping(self, ctx, *arg):
        embed = discord.Embed(title="Ping Help",
                              description="Check how fast I respond to a command",
                              color=0x236ce1)
        embed.add_field(name="Example",
                        value="re!ping",
                        inline=True)

    @help.command(aliases=['8b', '8ball'])
    async def _8ball(self, ctx, *arg):
        embed = discord.Embed(
            title="8 ball help",
            description="Ask 8 ball anything and you will get your awnser\nAliases: 8b, 8ball",
            color=0x0000FF)
        embed.add_field(name="Example:",
                        value="re!8ball QUESTION", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['uinfo', 'minfo'])
    async def userinfo(ctx, *arg):
        embed = discord.Embed(
            title="Serverinfo help",
            description="See the information of a member or yourself\nAliases: uinfo, userinfo, minfo\n\n**NOTE:** It must be someone present in the server.",
            color=0x093cb3)
        embed.add_field(
            name="Example:",
            value="re!uinfo (if for yourself)\nre!uinfo MEMBER (if for a member)",
            inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['sinfo', 'guild', 'guildinfo', 'ginfo'])
    async def serverinfo(self, ctx, *arg):
        embed = discord.Embed(
            title="Serverinfo help",
            description="Get information about this server\nAliases: serverinfo, sinfo, guild, guildinfo, ginfo",
            color=0x093cb3)
        embed.add_field(name="Example:", value="re!serverinfo", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['fuser'])
    async def finduser(self, ctx, *arg):
        embed = discord.Embed(
            title="Finduser help", description="Finds a user in Discord\nAliases: finduser, fuser\n\n**NOTE**: This is an ***OWNER ONLY*** command which means only my creator can use it", color=0x093cb3)
        embed.add_field(name="Example:", value="re!fuser USER", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['fserver'])
    async def findserver(self, ctx, *arg):
        embed = discord.Embed(
            title="Findserver help",
            description="Finds a server I'm mutual with\nAliases: findserver, fserver\n\n**NOTE**: This is an ***OWNER ONLY*** command which means only my creator can use it",
            color=0x093cb3)
        embed.add_field(name="Example:",
                        value="re!fserver SERVER", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['av'])
    async def avatar(self, ctx, *arg):
        embed = discord.Embed(
            title="Avatar help",
            description="See the profile picture of a member or yourself\nAliases: avatar, av\n\n**NOTE**: It must be a member present in the server",
            color=0x093cb3)
        embed.add_field(
            name="Example:",
            value="re!av (if yourself)\nre!av MEMBER (if for a member)",
            inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def say(self, ctx, *arg):
        embed = discord.Embed(
            title="Say help",
            description="Type a message and I will say it.\n\n**Required Permission:** Administrator\n\n**NOTE:** After typing the message, your message will be deleted but said by me.",
            color=0x093cb3)
        embed.add_field(name="Example:", value="re!say MESSAGE", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def mute(self, ctx):
        embed = discord.Embed(
            title="Mute help",
            description="Mute someone and they will not talk.\n\n**Required Permission:** Kick Members\n\n**NOTE:** If a mute role doesn't exist, a new one will made. The member who gets muted will not see the channels except where the mute command happened. If there is no time, it will be infinite",
            color=0x093cb3)
        embed.add_field(name="Example:", value="re!mute MEMBER 10m Stop spamming ", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def purge(self, ctx):
        embed = discord.Embed(
            title="Purge help",
            description="Bulk delete messages.\n\n**Required Permission:** Manage Messages\n\n**NOTE:** Will delete up to 50 messages. You can also mention a member or add a number less than 50 to delete the messages",
            color=0x093cb3)
        embed.add_field(
            name="Example:", value="re!purge 20", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def unmute(self, ctx):
        embed = discord.Embed(
            title="Unmute help",
            description="Unmute a muted member so they can talk.\n\n**Required Permission:** Kick Members",
            color=0x093cb3)
        embed.add_field(
            name="Example:", value="re!unmute MEMBER ", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['h'])
    async def hentai(self, ctx):
        embed = discord.Embed(
            title="Hentai help",
            description="Get a random hentai image. You can add a character or anime as a tag if you want a specific kind of hentai.\nAliase: h\n\n**Required permissions:** Channel must be NSFW\n\n**NOTE:** If looking for a specific kind of hentai, it must be in one word.",
            color=0x002aff)
        embed.add_field(
            name="Example",
            value="re!h (for a random hentai picture)\nre!h MikuNakano (if looking for a hentai picture of a character)\nre!h fate (if looking for a hentai picture of an anime)",
            inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def warn(self, ctx, *arg):
        embed = discord.Embed(
            title="Warn help",
            description="Warn a user for doing someting bad\nAliases: w\n\n**Required permissions:** Kick Members\n\n**NOTE:** A reason must be provided or the command won't work",
            color=0x002aff)
        embed.add_field(
            name="Example", value="re!warn USER REASON", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def ban(self, ctx, *arg):
        embed = discord.Embed(
            title="Ban help",
            description="Bans a user permanently\nAliases: b\n\n**Required permissions:** Ban Members\n\n**NOTE:** A reason must be provided or the command won't work",
            color=0x002aff)
        embed.add_field(
            name="Example", value="re!ban USER REASON", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def kick(self, ctx, *arg):
        embed = discord.Embed(
            title="Kick help",
            description="Kicks a user out of the server. They are able to come back to the server\nAliases: k\n\n**Required permissions:** Kick Members\n\n**NOTE:** A reason must be provided or the command won't work",
            color=0x002aff)
        embed.add_field(
            name="Example", value="re!kick USER REASON", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def unban(self, ctx, *arg):
        embed = discord.Embed(
            title="Unban help",
            description="Unbans a user so they can be able to come back to the server\nAliases: unb\n\n**Required permissions:** Ban Members\n\n**NOTE:**The user's name and tag must be used to unban them or the command won't work",
            color=0x002aff)
        embed.add_field(name="Example", value="re!unban USER", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['tc', 'textchannel'])
    async def text_channel(self, ctx, *arg):
        embed = discord.Embed(title="Text Channel help",
                              description="**Permission required:** Manage Channels", color=0x002aff)
        embed.add_field(name="Create Text Channel",
                        value="Creates a new text channel\n**Aliases:** createtextchannel, ctc\n\nExample:\nre!ctc CHANNEL NAME", inline=True)
        embed.add_field(name="Delete Text Channel",
                        value="Deletes the text channel\n**Aliases:** deletetextchannel, dtc\n\n**NOTE:** This command requires a mentioned channel or a channel ID in order to delete it.\n\nExample:\nre!dtc CHANNEL_NAME (with channel mentioned)\nre!dtc CHANNEL_ID (with channel ID)", inline=True)
        embed.add_field(name="Rename Text Channel",
                        value="Renames the text channel\n**Aliases:** renametextchannel, rntc\n\n**NOTE:** This command requires a mentioned channel or a channel ID in order to rename it.\n\nExample:\nre!rtc CHANNEL_NAME NEW_NAME(with channel mentioned)\nre!rntc CHANNEL_ID NEW_NAME (with channel ID)", inline=True)
        await ctx.send(embed=embed)

    @help.command(aliases=['vc', 'voicechannel'])
    async def voice_channel(self, ctx, *arg):
        embed = discord.Embed(title="Voice Channel help",
                              description="**Permission required:** Manage Channels", color=0x002aff)
        embed.add_field(name="Create Voice Channel",
                        value="Creates a new voice channel\n**Aliases:** createvoicechannel, cvc\n\nExample:\nre!ctc CHANNEL_NAME", inline=True)
        embed.add_field(name="Delete Voice Channel",
                        value="Deletes the voice channel\n**Aliases:** deletevoicechannel, dvc\n\n**NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.\n\nExample:\nre!dvc CHANNEL NAME\nre!dvc CHANNEL_ID (with channel ID)", inline=True)
        embed.add_field(name="Rename Voice Channel",
                        value="Renames the voice channel\n**Aliases:** renametextchannel, rtc\n\n**NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.\n\nExample:\nre!rnvc CHANNEL_NAME NEW_NAME\nre!rvc CHANNEL_ID NEW_NAME (with channel ID)", inline=True)
        await ctx.send(embed=embed)

    @help.command(aliases=['r'])
    async def role(self, ctx, *arg):
        embed = discord.Embed(title="Role help",
                              description="**Permission required:** Manage Roles", color=0x002aff)
        embed.add_field(name="Create Role",
                        value="Creates a new role\n**Aliases:** createrole, cr\n\nExample:\nre!cr ROLE_NAME", inline=True)
        embed.add_field(name="Delete Role",
                        value="Deletes a role\n**Aliases:** deleterole, dr\n\nExample:\nre!dr ROLE_NAME\nre!dvc ROLE_ID (with role ID)", inline=True)
        embed.add_field(name="Rename Role",
                        value="Renames the role\n**Aliases:** renamerole, rnr\n\n**NOTE:** A role ID or role mentioned can be used to acurately delete the channel.\n\nExample:\nre!rnr OLD_NAME NEW_NAME (with role mentioned)\nre!rnr ROLE_ID NEW_NAME (with role ID)", inline=True)
        await ctx.send(embed=embed)

    @help.command()
    async def combine(self, ctx, *arg):
        embed = discord.Embed(
            title="Combine help",
            description="Type two words to get one combined word",
            color=0x002aff)
        embed.add_field(name="Example", value="re!combine WORD_1 WORD_2", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def animeme(self, ctx, *arg):
        embed = discord.Embed(
            title="Animeme help",
            description="Get some animemes\nAliases: meme, animememe",
            color=0x002aff)
        embed.add_field(
            name="Example", value="re!animeme", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))
