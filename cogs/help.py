import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        embed = discord.Embed(title="Help Commands",
                              description="Here are some commands to help you.",
                              color=0x236ce1)
        embed.add_field(name="Fun",
                        value="8 Ball (8b, 8ball)\nHentai (h) **NSFW**\nRoll Dice (rd, dice)\nCombine\nFlip (coinflip, headsortails, piece)\nChoose (pick)\nReverse",
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
        embed.add_field(name="Reactions",
                        value="Hug\nSlap\nSmug\nTickle\nPoke\nPat\nKiss",
                        inline=True)
        await ctx.send(embed=embed)

    @help.command()
    async def reactions(self, ctx, *arg):
        embed = discord.Embed(title="Reaction Help",
                              description="Here is the full reaction help menu",
                              color=0x236ce1)
        embed.add_field(name="Hug", value="Hug someone or yourself\n**Note:** You cannot hug multiple people at once or role(s). You should also hug someone in this server\n\nExample: j!hug (if yourself)\nre!hug MEMBER (if member mentioned)", inline=True)
        embed.add_field(name="Slap", value="Slap someone or yourself\n**Note:** You cannot slap multiple people at once or role(s). You should also slap someone in this server\n\nExample: j!slap (if yourself)\nre!slap MEMBER (if member mentioned)", inline=True)
        embed.add_field(name="Smug", value="Show a smuggy look\n**Note:** You cannot smug a member as you are the only one who can smug. if you do mentioned someone, Jeanne will ignore the mentioned member and still say you are smugging\n\nExample: j!smug", inline=True)
        embed.add_field(name="Tickle", value="Tickle someone or yourself\n**Note:** You cannot tickle multiple people at once or role(s). You should also tickle someone in this server\n\nExample: j!tickle (if yourself)\nre!tickle MEMBER (if member mentioned)", inline=True)
        embed.add_field(name="Poke", value="Poke someone or yourself\n**Note:** You cannot poke multiple people at once or role(s). You should also poke someone in this server\n\nExample: j!poke (if yourself)\nre!poke MEMBER (if member mentioned)", inline=True)
        embed.add_field(name="Pat", value="Pat someone or yourself\n**Note:** You cannot pat multiple people at once or role(s). You should also pat someone in this server\n\nExample: j!pat (if yourself)\nre!pat MEMBER (if member mentioned)", inline=True)
        embed.add_field(name="Kiss", value="Kiss someone or yourself\n**Note:** You cannot kiss multiple people at once or role(s). You should also kiss someone in this server\n\nExample: j!kiss (if yourself)\nre!kiss MEMBER (if member mentioned)", inline=True)
        await ctx.send(embed=embed)

    @help.command()
    async def ping(self, ctx, *arg):
        embed = discord.Embed(title="Ping Help",
                              description="Check how fast I respond to a command",
                              color=0x236ce1)
        embed.add_field(name="Example",
                        value="j!ping",
                        inline=True)

    @help.command(aliases=['8b', '8ball'])
    async def _8ball(self, ctx, *arg):
        embed = discord.Embed(
            title="8 ball help",
            description="Ask 8 ball anything and you will get your awnser\nAliases: 8b, 8ball",
            color=0x0000FF)
        embed.add_field(name="Example:",
                        value="j!8ball QUESTION", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['uinfo', 'minfo'])
    async def userinfo(ctx, *arg):
        embed = discord.Embed(
            title="Userinfo help",
            description="See the information of a member or yourself\nAliases: uinfo, userinfo, minfo\n\n**NOTE:** It must be someone present in the server.",
            color=0x093cb3)
        embed.add_field(
            name="Example:",
            value="j!uinfo (if for yourself)\nre!uinfo MEMBER (if for a member)",
            inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['sinfo', 'guild', 'guildinfo', 'ginfo'])
    async def serverinfo(self, ctx, *arg):
        embed = discord.Embed(
            title="Serverinfo help",
            description="Get information about this server\nAliases: serverinfo, sinfo, guild, guildinfo, ginfo",
            color=0x093cb3)
        embed.add_field(name="Example:", value="j!serverinfo", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['fuser'])
    async def finduser(self, ctx, *arg):
        embed = discord.Embed(
            title="Finduser help",
            description="Finds a user in Discord\nAliases: finduser, fuser\n\n**NOTE**: This is an ***OWNER ONLY*** command which means only my creator can use it",
            color=0x093cb3)
        embed.add_field(name="Example:", value="j!fuser USER", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['fserver'])
    async def findserver(self, ctx, *arg):
        embed = discord.Embed(
            title="Findserver help",
            description="Finds a server I'm mutual with\nAliases: findserver, fserver\n\n**NOTE**: This is an ***OWNER ONLY*** command which means only my creator can use it",
            color=0x093cb3)
        embed.add_field(name="Example:",
                        value="j!fserver SERVER", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['av'])
    async def avatar(self, ctx, *arg):
        embed = discord.Embed(
            title="Avatar help",
            description="See the profile picture of a member or yourself\nAliases: avatar, av\n\n**NOTE**: It must be a member present in the server",
            color=0x093cb3)
        embed.add_field(
            name="Example:",
            value="j!av (if yourself)\nre!av MEMBER (if for a member)",
            inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def say(self, ctx, *arg):
        embed = discord.Embed(
            title="Say help",
            description="Type a message and I will say it but it will be in plain text.\n\n**Required Permission:** Administrator\n\n**NOTE:** After typing the message, your message will be deleted but said by me. The message will be plain text.",
            color=0x093cb3)
        embed.add_field(name="Example:", value="j!say MESSAGE", inline=False)
        await ctx.send(embed=embed)

    @help.command(alises=['saye'])
    async def sayembed(self, ctx, *arg):
        embed = discord.Embed(
            title="Sayembed help",
            description="Type a message and I will say it but it will be in embed.\n\n**Required Permission:** Administrator\n\n**NOTE:** After typing the message, your message will be deleted but said by me",
            color=0x093cb3)
        embed.add_field(name="Example:", value="j!saye MESSAGE", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def mute(self, ctx):
        embed = discord.Embed(
            title="Mute help",
            description="Mute someone and they will not talk.\n\n**Required Permission:** Kick Members\n\n**NOTE:** If a mute role doesn't exist, a new one will made. The member who gets muted will not see the channels except where the mute command happened. If there is no time, it will be infinite",
            color=0x093cb3)
        embed.add_field(
            name="Example:", value="j!mute MEMBER 10m Stop spamming ", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def purge(self, ctx):
        embed = discord.Embed(
            title="Purge help",
            description="Bulk delete messages.\n\n**Required Permission:** Manage Messages\n\n**NOTE:** Will delete up to 50 messages. You can also mention a member or add a number less than 50 to delete the messages",
            color=0x093cb3)
        embed.add_field(
            name="Example:", value="j!purge 20", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def unmute(self, ctx):
        embed = discord.Embed(
            title="Unmute help",
            description="Unmute a muted member so they can talk.\n\n**Required Permission:** Kick Members",
            color=0x093cb3)
        embed.add_field(
            name="Example:", value="j!unmute MEMBER ", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def warn(self, ctx, *arg):
        embed = discord.Embed(
            title="Warn help",
            description="Warn a user for doing someting bad\nAliases: w\n\n**Required permissions:** Kick Members\n\n**NOTE:** A reason must be provided or the command won't work",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!warn USER REASON", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def ban(self, ctx, *arg):
        embed = discord.Embed(
            title="Ban help",
            description="Bans a user permanently\nAliases: b\n\n**Required permissions:** Ban Members\n\n**NOTE:** A reason must be provided or the command won't work",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!ban USER REASON", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def kick(self, ctx, *arg):
        embed = discord.Embed(
            title="Kick help",
            description="Kicks a user out of the server. They are able to come back to the server\nAliases: k\n\n**Required permissions:** Kick Members\n\n**NOTE:** A reason must be provided or the command won't work",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!kick USER REASON", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def unban(self, ctx, *arg):
        embed = discord.Embed(
            title="Unban help",
            description="Unbans a user so they can be able to come back to the server\nAliases: unb\n\n**Required permissions:** Ban Members\n\n**NOTE:**The user's name and tag must be used to unban them or the command won't work",
            color=0x002aff)
        embed.add_field(name="Example", value="j!unban USER", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['tc', 'textchannel'])
    async def text_channel(self, ctx, *arg):
        embed = discord.Embed(title="Text Channel help",
                              description="**Permission required:** Manage Channels", color=0x002aff)
        embed.add_field(name="Create Text Channel",
                        value="Creates a new text channel\n**Aliases:** createtextchannel, ctc\n\nExample:\nre!ctc CHANNEL NAME",
                        inline=True)
        embed.add_field(name="Delete Text Channel",
                        value="Deletes the text channel\n**Aliases:** deletetextchannel, dtc\n\n**NOTE:** This command requires a mentioned channel or a channel ID in order to delete it.\n\nExample:\nre!dtc CHANNEL_NAME (with channel mentioned)\nre!dtc CHANNEL_ID (with channel ID)",
                        inline=True)
        embed.add_field(name="Rename Text Channel",
                        value="Renames the text channel\n**Aliases:** renametextchannel, rntc\n\n**NOTE:** This command requires a mentioned channel or a channel ID in order to rename it.\n\nExample:\nre!rtc CHANNEL_NAME NEW_NAME(with channel mentioned)\nre!rntc CHANNEL_ID NEW_NAME (with channel ID)",
                        inline=True)
        await ctx.send(embed=embed)

    @help.command(aliases=['vc', 'voicechannel'])
    async def voice_channel(self, ctx, *arg):
        embed = discord.Embed(title="Voice Channel help",
                              description="**Permission required:** Manage Channels", color=0x002aff)
        embed.add_field(name="Create Voice Channel",
                        value="Creates a new voice channel\n**Aliases:** createvoicechannel, cvc\n\nExample:\nre!ctc CHANNEL_NAME",
                        inline=True)
        embed.add_field(name="Delete Voice Channel",
                        value="Deletes the voice channel\n**Aliases:** deletevoicechannel, dvc\n\n**NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.\n\nExample:\nre!dvc CHANNEL NAME\nre!dvc CHANNEL_ID (with channel ID)",
                        inline=True)
        embed.add_field(name="Rename Voice Channel",
                        value="Renames the voice channel\n**Aliases:** renametextchannel, rtc\n\n**NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.\n\nExample:\nre!rnvc CHANNEL_NAME NEW_NAME\nre!rvc CHANNEL_ID NEW_NAME (with channel ID)",
                        inline=True)
        await ctx.send(embed=embed)

    @help.command(aliases=['r'])
    async def role(self, ctx, *arg):
        embed = discord.Embed(title="Role help",
                              description="**Permission required:** Manage Roles", color=0x002aff)
        embed.add_field(name="Create Role",
                        value="Creates a new role\n**Aliases:** createrole, cr\n\nExample:\nre!cr ROLE_NAME",
                        inline=True)
        embed.add_field(name="Delete Role",
                        value="Deletes a role\n**Aliases:** deleterole, dr\n\nExample:\nre!dr ROLE_NAME\nre!dvc ROLE_ID (with role ID)",
                        inline=True)
        embed.add_field(name="Rename Role",
                        value="Renames the role\n**Aliases:** renamerole, rnr\n\n**NOTE:** A role ID or role mentioned can be used to acurately delete the channel.\n\nExample:\nre!rnr OLD_NAME NEW_NAME (with role mentioned)\nre!rnr ROLE_ID NEW_NAME (with role ID)",
                        inline=True)
        await ctx.send(embed=embed)

    @help.command()
    async def combine(self, ctx, *arg):
        embed = discord.Embed(
            title="Combine help",
            description="Type two words to get one combined word",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!combine WORD_1 WORD_2", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['meme'])
    async def animeme(self, ctx, *arg):
        embed = discord.Embed(
            title="Animeme help",
            description="Get some animemes\nAliases: meme, animememe",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!animeme", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['cat'])
    async def category(self, ctx, *arg):
        embed = discord.Embed(title="Category help",
                              description="**Permission required:** Manage Channels", color=0x002aff)
        embed.add_field(name="Create Category",
                        value="Creates a new category\n**Aliases:** ccat, createcatagory, createcat, ccategory\n\nExample:\nre!ccat CATEGORY NAME",
                        inline=True)
        embed.add_field(name="Delete Category",
                        value="Deletes the category\n**Aliases:** dcat, deletecat, delcat, deletecategory, dcategory\n\n**NOTE:** This command requires a category ID to accurately delete it in case it cannot be found.\n\nExample:\nre!dcat CATEGORY NAME (with category name)\nre!dcat CATEGORY ID (with category ID)",
                        inline=True)
        embed.add_field(name="Rename Category",
                        value="Renames the category\n**Aliases:** rncat, renamecat, rncategory, renamecategory\n\n**NOTE:** This command requires a category ID to accurately rename it in case it cannot be found.\n\nExample:\nre!rncat CATEGORY NAME NEW_NAME(with category name)\nre!rncat CATEGORY ID NEW_NAME (with category ID)",
                        inline=True)
        await ctx.send(embed=embed)

    @help.command(name='bot mutuals', aliases=['bm'])
    async def botmutuals(self, ctx, *arg):
        embed = discord.Embed(
            title="Bot Mutuals help",
            description="See where which servers Jeanne is in\n\n**NOTE:** This is an ***OWNER ONLY*** command which means only my creator can use it\nAliases: bm",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!bm", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['coinflip, headsortails, piece'])
    async def flip(self, ctx, *arg):
        embed = discord.Embed(
            title="Flip help",
            description="Flip a coin and get your result\n\nAliases: coinflip, headsortails, piece",
            color=0x002aff)
        embed.add_field(
            name="Example", value="j!flip", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['pick'])
    async def choose(self, ctx, *arg):
        embed = discord.Embed(
            title="Choose help",
            description="Add some choices and I will choose for you\n\n**NOTE:** You need to put more than 1 choices\nAliases: pick",
            color=0x0000FF)
        embed.add_field(name="Example:",
                        value="j!pick CHOICE_1 CHOICE_2", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def reverse(self, ctx, *arg):
        embed = discord.Embed(
            title="Reverse help",
            description="Type something and the text will be reversed\n\n**NOTE:** This only works on a slash command. The prefixed command is still faulty",
            color=0x0000FF)
        embed.add_field(name="Example:",
                        value="/reverse TEXT (Make sure its Jeanne doing the command)", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))
