import discord
from discord import Embed
from discord.ext import commands
from discord_slash.utils.manage_components import create_actionrow, create_button
from discord_slash import cog_ext
from discord_slash.model import ButtonStyle
from dinteractions_Paginator import Paginator

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        buttons1 = [
            create_button(
                style=ButtonStyle.blue,
                label="Fun",
                custom_id="Fun"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Info",
                custom_id="Info"
            ),
            create_button(
                style=ButtonStyle.green,
                label="Creater Only (OWNER ONLY)",
                custom_id="owner"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Misc",
                custom_id="misc"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Moderation",
                custom_id="mod"
            ), ]

        buttons2 = [
            create_button(
                style=ButtonStyle.blue,
                label="Management",
                custom_id="manage"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Reactions",
                custom_id="reactions"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Images",
                custom_id="image"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Hentai (NSFW CHANNEL REQUIRED)",
                custom_id="nsfw"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Utilities",
                custom_id="utilities"
            ),
        ]

        action_row = create_actionrow(*buttons1)
        action_row2 = create_actionrow(*buttons2)

        await ctx.send("Click on one of the buttons to get help on a command module", components=[action_row, action_row2], delete_after=60)

    @cog_ext.cog_component()
    async def Fun(self, ctx):
            _8ball = Embed(
                title="8 ball help", description="Ask 8 ball anything and you will get your awnser\nAliases: 8b, 8ball", color=0x0000FF)
            _8ball.add_field(name="Example:",
                             value="`j!8ball QUESTION`", inline=False)

            dice = Embed(
                title="Dice help", description="Roll a dice\nAliases: rd, dice", color=0x0000FF)
            dice.add_field(name="Example:",
                           value="`j!roll`", inline=False)

            combine = Embed(
                title="Combine help", description="Type two words to get one combined word", color=0x0000FF)
            combine.add_field(
                name="Example", value="`j!combine WORD_1 WORD_2`", inline=False)

            flip = Embed(
                title="Flip help", description="Flip a coin and get your result\n\nAliases: coinflip, headsortails, piece", color=0x0000FF)
            flip.add_field(name="Example", value="j!flip", inline=False)
            choose = Embed(title="Choose help", description="Add some choices and I will choose for you\n\n**NOTE:** You need to put more than 1 choices. This only works on a prefixed command\nAliases: pick", color=0x0000FF)
            choose.add_field(
                name="Example:", value="`j!pick CHOICE_1 CHOICE_2`", inline=False)

            reverse = Embed(
                title="Reverse Help", description="Say something and I will say it in reversed text", color=0x0000FF)
            reverse.add_field(
                name="Example:", value="`j!reverse TEXT`", inline=False)

            pages = [_8ball, dice, combine, flip, choose, reverse]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def Info(self, ctx):
            userinfo = Embed(
                title="Userinfo help",
                description="See the information of a member or yourself\nAliases: uinfo, userinfo, minfo\n\n**NOTE:** It must be someone present in the server.",
                color=0x093cb3)
            userinfo.add_field(
                name="Example:",
                value="`j!uinfo` (if for yourself)\n`j!uinfo MEMBER` (if for a member)",
                inline=False)

            serverinfo = Embed(
                title="Serverinfo help",
                description="Get information about this server\nAliases: serverinfo, sinfo, guild, guildinfo, ginfo",
                color=0x093cb3)
            serverinfo.add_field(
                name="Example:", value="`j!serverinfo`", inline=False)

            ping = Embed(title="Ping Help",
                         description="Check how fast I respond to a command",
                         color=0x236ce1)
            ping.add_field(name="Example",
                           value="`j!ping`",
                           inline=False)

            stats = Embed(
                title="Stats help", description="See the bot's status from development to now", color=0x236ce1)
            stats.add_field(name="Example",
                            value="`j!stats`",
                            inline=False)

            pages = [userinfo, serverinfo, ping, stats]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def owner(self, ctx):
            fserver = discord.Embed(
                title="Findserver help",
                description="Finds a server I'm mutual with\nAliases: findserver, fserver\n\n**NOTE**: This is an ***OWNER ONLY*** command which means only my creator can use it and can only work on a prefixed command",
                color=0x093cb3)
            fserver.add_field(name="Example:",
                              value="`j!fserver SERVER`", inline=False)

            fuser = discord.Embed(
                title="Finduser help",
                description="Finds a user in Discord\nAliases: finduser, fuser\n\n**NOTE**: This is an ***OWNER ONLY*** command which means only my creator can use it and can only work on a prefixed command",
                color=0x093cb3)
            fuser.add_field(name="Example:",
                            value="`j!fuser USER`", inline=False)

            botmutuals = discord.Embed(
                title="Bot Mutuals help",
                description="See a list of servers Jeanne is in\n\n**NOTE:** This is an ***OWNER ONLY*** command which means only my creator can use it\nAliases: bm",
                color=0x002aff)
            botmutuals.add_field(
                name="Example", value="`j!bm`", inline=False)

            mutuals = discord.Embed(
                title="Bot Mutuals help",
                description="See which servers the user is mutual with Jeanne\n\n**NOTE:** This is an ***OWNER ONLY*** command which means only my creator can use it and can only work on a prefixed command",
                color=0x002aff)
            mutuals.add_field(
                name="Example", value="`j!mutuals USER`", inline=False)

            pages = [fserver, fuser, botmutuals, mutuals]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def misc(self, ctx):
            invite = discord.Embed(title="Invite Help",
                                   description="Invite me to your server or join my creator's servers",
                                   color=0x236ce1)
            invite.add_field(name="Example",
                             value="`j!invite`",
                             inline=True)

            say = discord.Embed(
                title="Say help",
                description="Type a message and I will say it but it will be in plain text.\n\n**Required Permission:** Administrator\n\n**NOTE:** After typing the message, your message will be deleted but said by me. The message will be plain text.",
                color=0x093cb3)
            say.add_field(name="Example:", value="`j!say MESSAGE`", inline=False)

            saye = discord.Embed(
                title="Sayembed help",
                description="Type a message and I will say it but it will be in embed.\n\n**Required Permission:** Administrator\n\n**NOTE:** After typing the message, your message will be deleted but said by me",
                color=0x093cb3)
            saye.add_field(name="Example:",
                           value="`j!saye MESSAGE`", inline=False)

            pages = [invite, say, saye]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def mod(self, ctx):
            warn = Embed(
                title="Warn help",
                description="Warn a user for doing someting bad\nAliases: w\n\n**Required permissions:** Kick Members",
                color=0x002aff)
            warn.add_field(
                name="Example", value="`j!warn USER REASON`", inline=False)

            kick = Embed(
                title="Kick help",
                description="Kicks a user out of the server. They are able to come back to the server\nAliases: k\n\n**Required permissions:** Kick Members",
                color=0x002aff)
            kick.add_field(
                name="Example", value="`j!kick USER REASON`", inline=False)

            ban = Embed(
                title="Ban help",
                description="Bans a user permanently\nAliases: b\n\n**Required permissions:** Ban Members\n\n**NOTE:** For an outside ban, use the prefixed ban command",
                color=0x002aff)
            ban.add_field(
                name="Example", value="`j!ban USER REASON`", inline=False)

            unban = Embed(
                title="Unban help",
                description="Unbans a user so they can be able to come back to the server\nAliases: unb\n\n**Required permissions:** Ban Members\n\n**NOTE:**This command can only work by a prefixed unban command",
                color=0x002aff)
            unban.add_field(
                name="Example", value="`j!unban USER REASON`", inline=False)

            purge = discord.Embed(
                title="Purge help",
                description="Bulk delete messages.\n\n**Required Permission:** Manage Messages\n\n**NOTE:** This is a **slash only** command. Will delete up to 100 messages. You can also mention a member or add a number less than 100 to delete the messages.",
                color=0x093cb3)
            purge.add_field(
                name="Example:", value="`/purge 20 MEMBER`\n**NOTE**: For purging messages up to the limit, use `/purge`", inline=False)

            muterole = Embed(
                title="Muterole help",
                description="Creates a mute role\n\n**Required Permission:** Manage Roles (Bot)\n\n**NOTE:** The permissions set will be `View Channels=False` and `Send Messages=False` but you can readjust the mute role except renaming it.",
                color=0x093cb3)
            muterole.add_field(
                name="Example:", value="`j!muterole`", inline=False)

            mute = Embed(
                title="Mute help",
                description="Mute someone and they will not talk.\n\n**Required Permission:** Kick Members\n\n**NOTE:** If a mute role doesn't exist, make a new 'Muted' role or use the `muterole` command and Jeanne will make a new one or she will ignore the command and will not mute the member. If there is no time given, it will be infinite. All times displayed by Jeanne will be in seconds instead of actual time duration",
                color=0x093cb3)
            mute.add_field(
                name="Example:", value="`j!mute MEMBER 10m Stop spamming`", inline=False)

            unmute = Embed(
                title="Unmute help",
                description="Unmute a muted member so they can talk.\n\n**Required Permission:** Kick Members",
                color=0x093cb3)
            unmute.add_field(
                name="Example:", value="`j!unmute MEMBER`", inline=False)

            pages = [warn, kick, ban, unban, purge, mute, unmute]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def manage(self, ctx):
            tc = Embed(title="Text Channel help",
                       description="**Permission required:** Manage Channels", color=0x002aff)
            tc.add_field(name="Create Text Channel",
                         value="Creates a new text channel\n**Aliases:** createtextchannel, ctc\n\nExample:\n`j!ctc CHANNEL NAME`",
                         inline=True)
            tc.add_field(name="Delete Text Channel",
                         value="Deletes the text channel\n**Aliases:** deletetextchannel, dtc\n\n**NOTE:** This command requires a mentioned channel or a channel ID in order to delete it.\n\nExample:\n`j!dtc CHANNEL_NAME` (with channel mentioned)\n`j!dtc CHANNEL_ID` (with channel ID)",
                         inline=True)
            tc.add_field(name="Rename Text Channel",
                         value="Renames the text channel\n**Aliases:** renametextchannel, rntc\n\n**NOTE:** This command requires a mentioned channel or a channel ID in order to rename it.\n\nExample:\n`j!rtc CHANNEL_NAME NEW_NAME`(with channel mentioned)\n`j!rntc CHANNEL_ID NEW_NAME (with channel ID)`",
                         inline=True)

            vc = Embed(title="Voice Channel help",
                       description="**Permission required:** Manage Channels", color=0x002aff)
            vc.add_field(name="Create Voice Channel",
                         value="Creates a new voice channel\n**Aliases:** createvoicechannel, cvc\n\nExample:\n`j!ctc CHANNEL_NAME`",
                         inline=True)
            vc.add_field(name="Delete Voice Channel",
                         value="Deletes the voice channel\n**Aliases:** deletevoicechannel, dvc\n\n**NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.\n\nExample:\n`j!dvc CHANNEL NAME`\n`j!dvc CHANNEL_ID` (with channel ID)",
                         inline=True)
            vc.add_field(name="Rename Voice Channel",
                         value="Renames the voice channel\n**Aliases:** renametextchannel, rtc\n\n**NOTE:** A channel ID can be used to acurately delete the channel since it can't be mentioned.\n\nExample:\n`j!rnvc CHANNEL_NAME NEW_NAME`\n`j!rvc CHANNEL_ID NEW_NAME` (with channel ID)",
                         inline=True)

            r = Embed(title="Role help",
                      description="**Permission required:** Manage Roles", color=0x002aff)
            r.add_field(name="Create Role",
                        value="Creates a new role\n**Aliases:** createrole, cr\n\nExample:\n`j!cr ROLE_NAME`",
                        inline=True)
            r.add_field(name="Delete Role",
                        value="Deletes a role\n**Aliases:** deleterole, dr\n\nExample:\n`j!dr ROLE_NAME`\n`j!dvc ROLE_ID` (with role ID)",
                        inline=True)
            r.add_field(name="Rename Role",
                        value="Renames the role\n**Aliases:** renamerole, rnr\n\n**NOTE:** A role ID or role mentioned can be used to acurately delete the role.\n\nExample:\n`j!rnr OLD_NAME NEW_NAME` (with role mentioned)\n`j!rnr ROLE_ID NEW_NAME` (with role ID)",
                        inline=True)

            cat = Embed(title="Category help",
                        description="**Permission required:** Manage Channels", color=0x002aff)
            cat.add_field(name="Create Category",
                          value="Creates a new category\n**Aliases:** ccat, createcatagory, createcat, ccategory\n\nExample:\n`j!ccat CATEGORY NAME`",
                          inline=True)
            cat.add_field(name="Delete Category",
                          value="Deletes the category\n**Aliases:** dcat, deletecat, delcat, deletecategory, dcategory\n\n**NOTE:** This command requires a category ID to accurately delete it in case it cannot be found.\n\nExample:\n`j!dcat CATEGORY NAME` (with category name)\n`j!dcat CATEGORY ID` (with category ID)",
                          inline=True)
            cat.add_field(name="Rename Category",
                          value="Renames the category\n**Aliases:** rncat, renamecat, rncategory, renamecategory\n\n**NOTE:** This command requires a category ID to accurately rename it in case it cannot be found.\n\nExample:\n`j!rncat CATEGORY NAME NEW_NAME`(with category name)\n`j!rncat CATEGORY ID NEW_NAME` (with category ID)",
                          inline=True)

            pages = [tc, vc, r, cat]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def reactions(self, ctx):
            hug = Embed(title="Hug Help",
                        description="Hug someone or yourself\n**Note:** You cannot hug multiple people at once or role(s). You should also hug someone in this server",
                                    color=0x236ce1)
            hug.add_field(
                name="Example", value="Example: `j!hug` (if yourself)\n`j!hug MEMBER` (if member mentioned)", inline=False)

            slap = Embed(title="Slap Help",
                         description="Slap someone or yourself\n**Note:** You cannot slap multiple people at once or role(s). You should also slap someone in this server",
                         color=0x236ce1)
            slap.add_field(
                name="Example", value="`j!slap` (if yourself)\n`j!slap MEMBER` (if member mentioned)", inline=False)

            smug = Embed(title="Smug Help",
                         description="Hug someone or yourself\n**Note:** You cannot make multiple people or role(s) smug as you are the only one smugging.",
                         color=0x236ce1)
            smug.add_field(
                name="Example", value="Example: `j!smug`", inline=False)

            tickle = Embed(title="Tickle Help",
                           description="Tickle someone or yourself\n**Note:** You cannot tickle multiple people at once or role(s). You should also tickle someone in this server",
                           color=0x236ce1)
            tickle.add_field(
                name="Example", value="`j!tickle` (if yourself)\n`j!tickle MEMBER` (if member mentioned)", inline=False)

            poke = Embed(title="Poke Help",
                         description="Poke someone or yourself\n**Note:** You cannot poke multiple people at once or role(s). You should also poke someone in this server",
                         color=0x236ce1)
            poke.add_field(
                name="Example", value="`j!poke` (if yourself)\n`j!poke MEMBER` (if member mentioned)", inline=False)

            pat = Embed(title="Pat Help",
                        description="Pat someone or yourself\n**Note:** You cannot pat multiple people at once or role(s). You should also pat someone in this server",
                        color=0x236ce1)
            pat.add_field(
                name="Example", value="`j!pat` (if yourself)\n`j!pat MEMBER` (if member mentioned)", inline=False)

            kiss = Embed(title="Kiss Help",
                         description="Kiss someone or yourself\n**Note:** You cannot kiss multiple people at once or role(s). You should also kiss someone in this server",
                         color=0x236ce1)
            kiss.add_field(
                name="Example", value="`j!kiss` (if yourself)\n`j!kiss MEMBER` (if member mentioned)", inline=False)

            baka = Embed(title="Baka Help",
                         description="Call someone or yourself a baka!\n**Note:** You cannot call multiple people or role(s) a baka at once. You should call someone a baka in this server",
                         color=0x236ce1)
            baka.add_field(
                name="Example", value="`j!baka` (if yourself)\n`j!baka MEMBER` (if member mentioned)", inline=False)

            feed = Embed(title="Feed Help",
                         description="Feed someone or yourself\n**Note:** You cannot feed multiple people at once or role(s). You should also feed someone in this server",
                         color=0x236ce1)
            feed.add_field(
                name="Example", value="`j!feed` (if yourself)\n`j!feed MEMBER` (if member mentioned)", inline=False)

            pages = [hug, slap, smug, tickle, poke, pat, kiss, baka, feed]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def image(self, ctx):
            kitsune = Embed(title="Kitsune Help",
                            description="Get a random kitsune (foxgirl) image from nekos.life",
                            color=0x236ce1)
            kitsune.add_field(
                name="Example", value="`j!kitsune`", inline=False)

            wallpaper = Embed(title="Wallpaper Help",
                              description="Need a wallpaper? Get a random wallpaper from nekos.life",
                              color=0x236ce1)
            wallpaper.add_field(
                name="Example", value="`j!wallpaper`", inline=False)

            jeanne = Embed(title="Jeanne Help",
                           description="Get a random Jeanne d'Arc image from Yande.re or Gelbooru",
                           color=0x236ce1)
            jeanne.add_field(
                name="Example", value="`j!jeanne`", inline=False)

            saber = Embed(title="Saber Help",
                          description="Get a random Saber image from Yande.re or Gelbooru",
                          color=0x236ce1)
            saber.add_field(
                name="Example", value="`j!saber`", inline=False)

            pages = [kitsune, wallpaper, jeanne, saber]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def nsfw(self, ctx):
            yandere = Embed(title="Yandere Help",
                            description="Get a random hentai from Yande.re. You can include a tag too for a specific hentai\n\n**NOTE**: Certain tags have been blacklisted for the sake of the viewer and/or due to Discord's ToS.",
                            color=0x236ce1)
            yandere.add_field(
                name="Example", value="`j!yandere` (for a random hentai)\n`j!yandere TAG` (for a specific tag)", inline=False)

            gelbooru = Embed(title="Gelbooru Help",
                             description="Get a random hentai from Gelbooru. You can include a tag too for a specific hentai\n\n**NOTE**: Certain tags have been blacklisted for the sake of the viewer and/or due to Discord's ToS.",
                             color=0x236ce1)
            gelbooru.add_field(
                name="Example", value="`j!gelbooru` (for a random hentai)\n`j!gelbooru TAG` (for a specific tag)", inline=False)

            danbooru = Embed(title="Danbooru Help",
                             description="Get a random hentai from Danbooru. You can include a tag too for a specific hentai\n\n**NOTE**: Certain tags have been blacklisted for the sake of the viewer and/or due to Discord's ToS.",
                             color=0x236ce1)
            danbooru.add_field(
                name="Example", value="`j!danbooru` (for a random hentai)\n`j!danbooru TAG` (for a specific tag)", inline=False)

            pages = [yandere, gelbooru, danbooru]

            await Paginator(bot=self.bot, ctx=ctx, pages=pages, hidden=True).run()

    @cog_ext.cog_component()
    async def utilities(self, ctx):
            weather = Embed(
                title="Weather help", description="Get weather information on a city", color=0x0000FF)
            weather.add_field(name="Example:",
                             value="`j!weather CITY`", inline=False)
            
            await ctx.send(embed=weather, hidden=True)

def setup(bot):
    bot.add_cog(help(bot))
