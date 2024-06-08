import argparse
from typing import Optional
from discord import (
    CategoryChannel,
    Color,
    Embed,
    File,
    GuildSticker,
    HTTPException,
    Member,
    NotFound,
    Role,
    StageChannel,
    TextChannel,
    VerificationLevel,
    abc,
    utils,
)
from PIL import ImageColor
import discord.ext.commands as Jeanne
from discord.ext.commands import Bot, Cog, Context
from humanfriendly import format_timespan, parse_timespan, InvalidTimespan
from functions import (
    Command,
    Inventory,
    Levelling,
    Manage,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from assets.components import (
    LevelSetButtons,
    RemoveManage,
    TopicButton,
    WelcomerSetButtons,
)
from requests import get
from io import BytesIO
from assets.argparsers import manage_parser


class ManagePrefix(Cog, name="Manage"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Jeanne.group(description="Main create command", invoke_without_command=True)
    async def create(self, ctx: Context): ...

    @create.command(aliases=["tc"], description="Creates a text channel", usage="<-n NAME> <-t TOPIC> <-cat CATEGORY | CATEGORY NAME | CATEGORY ID> <-s SLOWMODE> <-nsfw Enable NSFW. Just type '-nsfw'>", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def textchannel(
        self, ctx: Context, *words: str, parser=manage_parser
    ) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            topic = None if parsed_args.topic == None else " ".join(
                parsed_args.topic)
            category = (
                None if parsed_args.category == None else " ".join(
                    parsed_args.category)
            )
            slowmode = (
                None if parsed_args.slowmode == None else " ".join(
                    parsed_args.slowmode)
            )
            nsfw_enabled: bool = parsed_args.nsfw
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        channel = await ctx.guild.create_text_channel(name=name)

        embed = Embed()
        embed.color = Color.random()
        embed.description = "{} has been created".format(channel.jump_url)
        if category:
            category = utils.find(
                lambda cat: (cat.name or cat.id or cat.mention) == category,
                ctx.guild.categories,
            )
            await channel.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        if topic:
            if len(topic) > 1024:
                topic = topic[:1024]
            await channel.edit(topic=topic)
            embed.add_field(name="Topic", value=topic, inline=True)
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Slowmode", value=added_slowmode, inline=True)
        if nsfw_enabled:
            embed.add_field(name="NSFW", value="Yes", inline=True)
            await channel.edit(nsfw=True)
        await ctx.send(embed=embed)

    @create.command(aliases=["vc"], description="Create a voice channel", usage="<-n NAME> <-cat CATEGORY | CATEGORY NAME | CATEGORY ID> <-u USERS>", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def voicechannel(
        self, ctx: Context, *words: str, parser=manage_parser
    ) -> None:
        try:
            (parsed_args,) = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            category = (
                None if parsed_args.category == None else " ".join(
                    parsed_args.category)
            )
            users: int = 99 if parsed_args.users == None else parsed_args.users
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        channel = await ctx.guild.create_voice_channel(name=name)
        embed = Embed()
        embed.description = "{} has been created".format(channel.jump_url)
        embed.color = Color.random()
        if category:
            category = utils.find(
                lambda r: (r.name or r.id) == category, ctx.guild.categories
            )
            await channel.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        if users:
            if users > 99:
                users = 99
            await channel.edit(user_limit=users)
            embed.add_field(name="User Limit", value=users, inline=True)
        await ctx.send(embed=embed)

    @create.command(aliases=["cat"], description="Create a category", usage="<NAME>", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def category(
        self,
        ctx: Context,
        *,
        name: Optional[Jeanne.Range[str, 1, 100]] = "New Category",
    ):
        cat = await ctx.guild.create_category(name=name)
        embed = Embed()
        embed.description = "{} has been created".format(cat.mention)
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @create.command(aliases=["stage"], description="Create a stage channel",usage="<-n NAME> <-cat CATEGORY | CATEGORY NAME | CATEGORY ID> <-u USERS>", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def stagechannel(
        self, ctx: Context, *words: str, parser=manage_parser
    ) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            category = (
                None if parsed_args.category == None else " ".join(
                    parsed_args.category)
            )
            users: int = 1000 if parsed_args.users == None else parsed_args.users
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        embed = Embed()
        channel: StageChannel = await ctx.guild.create_stage_channel(name=name)
        embed.description = "{} has been created".format(channel.jump_url)
        if category:
            category = utils.find(
                lambda r: (r.name or r.id) == category, ctx.guild.categories
            )
            await channel.edit(category=category)
            embed.add_field(
                name="Moved to category", value=category.mention, inline=True
            )
        if users:
            if users > 1000:
                users = 1000
            await channel.edit(user_limit=users)
            embed.add_field(name="Users", value=users, inline=True)
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @stagechannel.error
    async def stagechannel_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Couldn't make a new stage channel. Please make sure the server is community enabled"
            embed.color = Color.red()
            await ctx.send(embed=embed)

    @create.command(description="Create a forum", usage="<-n NAME> <-cat CATEGORY | CATEGORY NAME | CATEGORY ID>", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def forum(self, ctx: Context, *words: str, parser=manage_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            category = (
                None if parsed_args.category == None else " ".join(
                    parsed_args.category)
            )
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        embed = Embed()
        forum = await ctx.guild.create_forum(
            name=("Forum Discussion" if name == None else name), topic="None"
        )
        embed.description = "{} has been created".format(forum.jump_url)
        embed.color = Color.random()
        if category:
            category = utils.find(
                lambda r: (r.name or r.id) == category, ctx.guild.categories
            )
            await forum.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        view = TopicButton(ctx.author, name, category)
        m = await ctx.send(embed=embed, view=view)
        if view == None:
            await m.edit(view=None)

    @forum.error
    async def forum_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Couldn't make a new forum. Please make sure the server is community enabled"
            embed.color = Color.red()
            await ctx.send(embed=embed)

    @create.command(aliases=["r"], name="role", description="Create a role", usage="<-n NAME> <-c COLOR> <-h Make it hoisted. Just type '-h'>", extras={"bot_perms":"Manage Roles", "member_perms": "Manage Roles"})
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def createrole(self, ctx: Context, *words: str, parser=manage_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "New Role" if parsed_args.name == None else " ".join(
                    parsed_args.name)
            )
            color = None if parsed_args.color == None else " ".join(
                parsed_args.color)
            hoisted: bool = parsed_args.hoisted
            mentionable: bool = parsed_args.mentioned
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        if name == None:
            name = "New Role"
        role = await ctx.guild.create_role(name=name)
        embed = Embed()
        embed.description = "Role `{}` has been created".format(name)
        if color != None:
            try:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)
                embed.color = int(color, 16)
            except:
                embed.add_field(
                    name="Color", value="Invalid color code", inline=True)
        else:
            embed.color = Color.random()
        if hoisted:
            if hoisted == True:
                await role.edit(hoist=True)
                embed.add_field(name="Hoisted", value="Yes", inline=True)
            elif hoisted == False:
                embed.add_field(name="Hoisted", value="No", inline=True)
        if mentionable:
            if mentionable == True:
                await role.edit(mentionable=True)
                embed.add_field(name="Mentionable", value="Yes", inline=True)
            elif mentionable == False:
                embed.add_field(name="Mentionable", value="No", inline=True)
        await ctx.send(embed=embed)

    @create.group(
        description="Main create thread command",
        invoke_without_command=True,
    )
    async def thread(self, ctx: Context): ...

    @thread.command(description="Make a public thread", usage="[-msg MESSAGE ID] <-n NAME> <-s SLOWMODE>", extras={"bot_perms":"Create Public Threads", "member_perms": "Create Public Threads\nManage Threads"})
    @Jeanne.has_permissions(create_public_threads=True)
    @Jeanne.bot_has_permissions(
        create_public_threads=True, manage_threads=True
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def public(self, ctx: Context, *words: str, parser=manage_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "New Thread" if parsed_args.name == None else " ".join(
                    parsed_args.name)
            )
            channel = (
                None if parsed_args.channel == None else " ".join(
                    parsed_args.channel)
            )
            message_id: int = parsed_args.message
            slowmode = (
                None if parsed_args.slowmode == None else " ".join(
                    parsed_args.slowmode)
            )
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        if channel == None:
            await ctx.send(
                embed=Embed(
                    description="You didn't add a `channel`. Please try again",
                    color=Color.red(),
                )
            )
            return
        channel = utils.find(
            lambda channel: (
                channel.id or channel.name or channel.mention) == channel,
            ctx.guild.text_channels,
        )
        embed = Embed()
        embed.add_field(name="Channel", value=channel.jump_url, inline=True)
        message = await channel.fetch_message(message_id)
        thread = await channel.create_thread(name=name, message=message)
        embed.add_field(name="Found in message",
                        value=message.jump_url, inline=True)
        await thread.add_user(ctx.author)
        embed.description = "{} has been created".format(thread.jump_url)
        embed.color = Color.random()
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Slowmode", value=added_slowmode, inline=True)
        await ctx.send(embed=embed)

    @public.error
    async def public_thread_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, NotFound
        ):
            embed = Embed()
            embed.description = "Message could not be found. Please make sure you have added the correct message ID"
            embed.color = Color.red()
            await ctx.send(embed=embed)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Failed to create public thread. Please try again"
            embed.color = Color.red()
            await ctx.send(embed=embed)

    @thread.command(description="Make a private thread",usage="<-n NAME> <-s SLOWMODE>", extras={"bot_perms":"Create Private Threads", "member_perms": "Create Private Threads\nManage Threads"})
    @Jeanne.has_permissions(create_private_threads=True)
    @Jeanne.bot_has_permissions(create_private_threads=True, manage_threads=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def private(
        self, ctx: Context, channel: TextChannel, *words: str, parser=manage_parser
    ) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "New Thread" if parsed_args.name == None else " ".join(
                    parsed_args.name)
            )
            slowmode = (
                None if parsed_args.slowmode == None else " ".join(
                    parsed_args.slowmode)
            )
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return

        if channel == None:
            await ctx.send(
                embed=Embed(
                    description="You didn't add a `channel`. Please try again",
                    color=Color.red(),
                )
            )
            return
        embed = Embed()
        embed.add_field(name="Channel", value=channel.jump_url, inline=True)
        thread = await channel.create_thread(name=name)
        await thread.add_user(ctx.author)
        embed.description = "{} has been created".format(thread.jump_url)
        embed.color = Color.random()
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Slowmode", value=added_slowmode, inline=True)
        await ctx.send(embed=embed)

    @private.error
    async def private_thread_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Failed to create private thread. Please try again"
            embed.color = Color.red()
            await ctx.send(embed=embed)

    @create.command(aliases=["emote"], description="Make a new emoji", usage="[NAME] [EMOJI LINK]",extras={"bot_perms":"Manage Expressions", "member_perms": "Manage Expressions"})
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def emoji(
        self,
        ctx: Context,
        *,
        name: Jeanne.Range[str, 2, 30],
        emoji_link: Optional[str] = None,
    ):
        embed = Embed()
        if emoji_link == None and ctx.message.attachments[0] == None:
            embed.description = "Please add either an emoji URL or emoji image"
            embed.color = Color.red()
        elif emoji_link and ctx.message.attachments[0]:
            embed.description = "Please use either an emoji URL or emoji image"
            embed.color = Color.red()
        else:
            emojibytes = get(
                emoji_link if emoji_link else ctx.message.attachments[0].url
            ).content
            emote = await ctx.guild.create_custom_emoji(
                name=name.replace(" ", "_"), image=emojibytes
            )
            embed.description = "{} | {} has been created".format(
                emote.name, str(emote)
            )
            embed.color = Color.random()
        await ctx.send(embed=embed)

    @emoji.error
    async def createemoji_error(self, ctx: Context, error: Jeanne.errors.CommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError):
            a_emojis = len(
                [emote for emote in ctx.guild.emojis if emote.animated == True]
            )
            emojis = len(
                [emote for emote in ctx.guild.emojis if emote.animated == False]
            )
            limit = 50 + (50 * ctx.guild.premium_tier)
            if HTTPException:
                embed = Embed(color=Color.red())
                if a_emojis == limit or emojis == limit:
                    embed.description = "You have reached the maximum emoji limit"
                else:
                    embed.description = "There was a problem making the emoji. Please check that the emoji you are making is a PNG, JPEG or GIF"
                await ctx.send(embed=embed)

    @Jeanne.command(
        aliases=["makesticker", "csticker"], description="Make a new sticker", usage="[NAME] [EMOJI] [STICKER LINK]",extras={"bot_perms":"Manage Expressions", "member_perms": "Manage Expressions"})
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def createsticker(
        self,
        ctx: Context,
        *,
        name: Jeanne.Range[str, 2, 30],
        emoji: str,
        sticker_link: Optional[str] = None,
    ):
        embed = Embed()
        if sticker_link is None and ctx.message.attachments[0] is None:
            embed.description = "Please add either an sticker URL or sticker image"
            embed.color = Color.red()
        elif sticker_link and ctx.message.attachments[0]:
            embed.description = "Please use either an sticker URL or sticker image"
            embed.color = Color.red()
        else:
            url = sticker_link if sticker_link else ctx.message.attachments[0].url
            stickerbytes = BytesIO(get(url).content)
            stickerfile = File(fp=stickerbytes, filename="sticker.png")
            sticker = await ctx.guild.create_sticker(
                name=name.lower(), description="None", emoji=emoji, file=stickerfile
            )
            embed.description = "{} has been created".format(sticker.name)
            embed.color = Color.random()
            embed.set_image(url=url)
        await ctx.send(embed=embed)

    @createsticker.error
    async def sticker_error(self, ctx: Context, error: Jeanne.errors.CommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed(color=Color.red())

            embed.description = "There was a problem making the sticker. Please check that the sticker you are making is:\n\n1. 512kb or less\n2. The file is in a PNG or APNG format\n3. The correct emoji was added\n\nIf all meet the conditions but still fail, that means you have reached the limit of sticker slots"
            await ctx.send(embed=embed)

    @Jeanne.command(aliases=["ch"], description="Deletes a channel", usage="[CHANNEL | CHANNEL NAME | CHANNEL ID]", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def deletechannel(self, ctx: Context, *, channel: abc.GuildChannel):
        embed = Embed(
            description="{} has been deleted".format(channel.name), color=Color.random()
        )
        await channel.delete()
        await ctx.send(embed=embed)

    @Jeanne.command(aliases=["dr"], description="Deletes a role", usage="[ROLE | ROLE NAME | ROLE ID]",extras={"bot_perms":"Manage Roles", "member_perms": "Manage Roles"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def deleterole(self, ctx: Context, *, role: Role):
        embed = Embed(
            description="{} has been deleted".format(role.name), color=Color.random()
        )
        await role.delete()
        await ctx.send(embed=embed)

    @Jeanne.command(aliases=["delemote", "delemoji"], description="Deletes an emoji", usage="[EMOJI | EMOJI NAME | EMOJI ID]", extras={"bot_perms":"Manage Expressions", "member_perms": "Manage Expressions"})
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def deleteemoji(self, ctx: Context, *, emoji: str):
        try:
            e = emoji.strip().split(":")[-1].rstrip(">")
            emote = await ctx.guild.fetch_emoji(int(e))
        except:
            emote = utils.get(ctx.guild.emojis, name=emoji.replace(" ", "_"))
        embed = Embed(
            description="{} has been deleted".format(str(emote)), color=0x00FF68
        )
        await emote.delete()
        await ctx.send(embed=embed)

    @deleteemoji.error
    async def emoji_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (AttributeError, HTTPException)
        ):
            embed = Embed(
                description="This emoji doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    @Jeanne.command(aliases=["delsticker"], description="Deletes a sticker", usage="[STICKER NAME | STICKER ID]",extras={"bot_perms":"Manage Expressions", "member_perms": "Manage Expressions"})
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def deletesticker(self, ctx: Context, *, sticker: Optional[str] = None):
        if sticker == None:
            sticker = ctx.message.stickers[0].name
        stick = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` has been deleted".format(str(stick.name)), color=0x00FF68
        )
        await stick.delete()
        await ctx.send(embed=embed)

    @deletesticker.error
    async def sticker_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (AttributeError, HTTPException)
        ):
            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    @Jeanne.group(description="Main edit command", invoke_without_command=True)
    async def edit(self, ctx: Context): ...

    @edit.command(aliases=["tc", "text"], description="Edits a text/news channel", usage="<CHANNEL | CHANNEL NAME | CHANNEL ID> <-n NAME> <-t TOPIC> <-cat CATEGORY | CATEGORY NAME | CATEGORY ID> <-s SLOWMODE> <-nsfw Enable NSFW. Just type '-nsfw'>", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def textchannel(
    self,
    ctx: Context,
    channel: Optional[TextChannel] = None,
    *words: str,
    parser=manage_parser,
    ) -> None:
        channel = ctx.channel if channel is None else channel
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = " ".join(parsed_args.name) if parsed_args.name else None
            topic = " ".join(parsed_args.topic) if parsed_args.topic else None
            category = " ".join(parsed_args.category) if parsed_args.category else None
            slowmode = " ".join(parsed_args.slowmode) if parsed_args.slowmode else None
            nsfw_enabled: bool = parsed_args.nsfw
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description="You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return

        embed = Embed(description=f"Channel `{channel.name}` has been edited", color=Color.green())

        if name:
            await channel.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)

        if category:
            await channel.edit(category=category)
            embed.add_field(name="Category", value=category, inline=True)

        if topic:
            topic = topic[:1024] if len(topic) > 1024 else topic
            await channel.edit(topic=topic)
            embed.add_field(name="Topic", value=topic, inline=True)

        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                delay = min(delay, 21600)
                await channel.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = str(e)
            embed.add_field(name="Slowmode", value=added_slowmode, inline=True)

        if nsfw_enabled:
            await channel.edit(nsfw=nsfw_enabled)
            embed.add_field(name="NSFW enabled", value="Yes" if nsfw_enabled else "No", inline=True)

        await ctx.send(embed=embed)

    @edit.command(description="Edit a role", usage="[ROLE | ROLE NAME | ROLE ID] <-n NAME> <-c COLOR> <-h Make it hoisted. Just type '-h'>", extras={"bot_perms":"Manage Roles", "member_perms": "Manage Roles"})
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def role(
        self, ctx: Context, role: Role, *words: str, parser=manage_parser
    ) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            color = None if parsed_args.color == None else " ".join(
                parsed_args.color)
            color = " ".join(color)
            hoisted: bool = parsed_args.hoisted
            mentionable: bool = parsed_args.mentioned
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        embed = Embed()
        embed.description = "Role `{}` has been edited".format(role.name)
        if name:
            await role.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)
        if color != None:
            try:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)
                embed.color = role.color
            except:
                embed.add_field(
                    name="Color", value="Invalid color code", inline=True)
        else:
            embed.color = Color.random()
        if hoisted:
            if hoisted == True:
                await role.edit(hoist=True)
                embed.add_field(name="Hoisted", value="Yes", inline=True)
            elif hoisted == False:
                await role.edit(hoist=False)
                embed.add_field(name="Hoisted", value="No", inline=True)
        if mentionable:
            if mentionable == True:
                await role.edit(mentionable=True)
                embed.add_field(name="Mentionable", value="Yes", inline=True)
            elif mentionable == False:
                await role.edit(mentionable=False)
                embed.add_field(name="Mentionable", value="No", inline=True)
        await ctx.send(embed=embed)

    @edit.command(
        description="Edits the server's name, description and verification level", usage="<-n NAME> <-d DESCRIPTION> <-v none | low | medium | high | highest>",extras={"bot_perms": "Manage Server","member_perms": "Manage Server"}
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def server(self, ctx: Context, *words: str, parser=manage_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            description = (
                None
                if parsed_args.description == None
                else " ".join(parsed_args.description)
            )
            verification_level: str = (
                "none"
                if parsed_args.verification_level == None
                else parsed_args.verification_level
            )
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        embed = Embed()
        embed.description = "{} has been edited".format(ctx.guild.name)
        embed.color = Color.green()
        if name:
            await ctx.guild.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)
        if description:
            if "PUBLIC" in ctx.guild.features:
                await ctx.guild.edit(description=description)
                embed.add_field(name="Description",
                                value=description, inline=True)
            else:
                embed.add_field(
                    name="Description",
                    value="Your server is not public to have a description edited",
                    inline=True,
                )
        if verification_level:
            if verification_level == "none":
                await ctx.guild.edit(verification_level=VerificationLevel.none)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nNo verification required".format(
                        verification_level.title()
                    ),
                    inline=True,
                )
            elif verification_level == "low":
                await ctx.guild.edit(verification_level=VerificationLevel.low)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified email".format(
                        verification_level.title()
                    ),
                    inline=True,
                )
            elif verification_level == "medium":
                await ctx.guild.edit(verification_level=VerificationLevel.medium)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified email and be registered on Discord for more than 5 minutes".format(
                        verification_level.title()
                    ),
                    inline=True,
                )
            elif verification_level == "high":
                await ctx.guild.edit(verification_level=VerificationLevel.high)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified email, be registered on Discord for more than 5 minutes and stay in the server for more than 10 minutes".format(
                        verification_level.title()
                    ),
                    inline=True,
                )
            elif verification_level == "highest":
                await ctx.guild.edit(verification_level=VerificationLevel.highest)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified phone number".format(
                        verification_level.title()
                    ),
                    inline=True,
                )
        await ctx.send(embed=embed)

    @edit.command(aliases=["pfp"], description="Change the server's avatar", usage="[IMAGE]",extras={"bot_perms": "Manage Server","member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def icon(self, ctx: Context):
        embed = Embed()
        try:
            embed.description = f"{ctx.guild.name}'s icon has been changed"
            avatar = ctx.message.attachments[0]
            avatar_url = avatar.url
            embed.set_thumbnail(url=avatar_url)
            avatarbytes = get(avatar_url).content
            await ctx.guild.edit(icon=avatarbytes)
        except:
            embed.add_field(
                name="Icon not added",
                value="There has been a problem adding the avatar",
                inline=True,
            )
        await ctx.send(embed=embed)

    @edit.command(description="Change the server's banner", usage="[IMAGE]",extras={"bot_perms": "Manage Server","member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def banner(self, ctx: Context):
        embed = Embed()
        if ctx.guild.premium_tier <= 1:
            embed.add_field(
                name="Banner not added",
                value="This server is not boosted to Tier 2",
                inline=True,
            )
        else:
            try:
                banner = ctx.message.attachments[0]
                bannerbytes = get(banner.url).content
                await ctx.guild.edit(banner=bannerbytes)
                embed.add_field(
                    name="Server's New Banner",
                    value=ctx.guild.banner.url,
                    inline=True,
                )
            except:
                embed.add_field(
                    name="Banner not added",
                    value="There has been a problem adding the banner",
                    inline=True,
                )
        await ctx.send(embed=embed)

    @edit.command(description="Change the server's splash screen", usage="[IMAGE]",extras={"bot_perms": "Manage Server","member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def splash(self, ctx: Context):
        embed = Embed()
        if ctx.guild.premium_tier == 0:
            embed.add_field(
                name="Splash not added",
                value="This server is not boosted to Tier 1",
                inline=True,
            )
        else:
            try:
                splash = ctx.message.attachments[0]
                splash_url = splash.url
                splash_bytes = get(splash_url).content
                await ctx.guild.edit(splash=splash_bytes)
                embed.add_field(
                    name="Server's New Splash Screen",
                    value=ctx.guild.splash.url,
                    inline=True,
                )
            except:
                embed.add_field(
                    name="Splash screen not added",
                    value="There has been a problem adding the splash screen",
                    inline=True,
                )
        await ctx.send(embed=embed)



    @Jeanne.group(
        name="set", description="Main set command", invoke_without_command=True
    )
    async def _set(self, ctx: Context): ...

    @_set.command(description="Set a welcomer and/or leaver channel", usage="<-w CHANNEL | CHANNEL NAME | CHANNEL ID> <-l CHANNEL | CHANNEL NAME | CHANNEL ID>", extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def welcomer(self, ctx: Context, *words: str, parser=manage_parser) -> None:
        try:
            parsed_args = parser.parse_known_args(words)[0]
            welcomer = (
                None if parsed_args.welcomer == None else " ".join(
                    parsed_args.welcomer)
            )
            leaving = (
                None if parsed_args.leaving == None else " ".join(
                    parsed_args.leaving)
            )

        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        if (welcoming_channel == None) and (leaving_channel == None):
            error = Embed(
                description="Both options are empty. Please set at least a welcomer or leaving channel",
                color=Color.red(),
            )
            await ctx.send(embed=error)
            return
        setup = Embed(description="Welcomer channels set",
                      color=Color.random())
        if welcoming_channel:
            welcoming_channel = utils.find(
                lambda ch: (ch.name or ch.id or ch.mention) == welcomer,
                ctx.guild.text_channels,
            )
            await Manage(ctx.guild).set_welcomer(welcoming_channel)
            setup.add_field(
                name="Channel welcoming users",
                value=welcoming_channel.mention,
                inline=True,
            )
        if leaving_channel:
            leaving_channel = utils.find(
                lambda ch: (ch.name or ch.id or ch.mention) == leaving,
                ctx.guild.text_channels,
            )
            await Manage(ctx.guild).set_leaver(leaving_channel)
            setup.add_field(
                name="Channel showing users that left",
                value=leaving_channel.mention,
                inline=True,
            )
        m = await ctx.send(embed=setup)
        view = WelcomerSetButtons(ctx.author, m)
        m = await m.edit(embed=setup, view=view)
        await view.wait()
        if view.value == None:
            await m.edit(view=None)

    @_set.command(description="Set a modlog channel", usage="[CHANNEL | CHANNEL NAME | CHANNEL ID]",extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def modlog(self, ctx: Context, *, channel: TextChannel):
        await Manage(ctx.guild).set_modloger(channel)
        embed = Embed(description="Modlog channel set", color=Color.red())
        embed.add_field(name="Channel selected",
                        value=channel.mention, inline=True)
        await ctx.send(embed=embed)

    @_set.command(description="Set a level up notification channel", usage="[CHANNEL | CHANNEL NAME | CHANNEL ID]",extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def levelupdate(self, ctx: Context, *, channel: TextChannel) -> None:
        await Manage(ctx.guild).add_level_channel(channel)
        embed = Embed()
        embed.description = "{} will post level updates when someone levels up".format(
            channel.mention
        )
        embed.color = Color.random()
        m = await ctx.send(embed=embed)
        view = LevelSetButtons(ctx.author, m, channel)
        m = await m.edit(view=view)
        await view.wait()
        if view.value == None:
            await m.edit(view=None)

    @_set.command(
        aliases=["profile-brightness", "pbright"],
        description="Change the brightness of your level and profile card background", usage="[BRIGHTNESS]"
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def brightness(self, ctx: Context, brightness: Jeanne.Range[int, 10, 150]):
        embed = Embed()
        if Inventory(ctx.author).set_brightness(brightness) == False:
            embed.description = "You have no background wallpaper"
            embed.color = Color.red()
            await ctx.send(embed=embed)
            return
        await Inventory(ctx.author).set_brightness(brightness)
        embed.description = "Brightness has been changed to {}".format(
            brightness)
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @_set.command(
        aliases=["profile-bio", "pbio"], description="Change your profile bio", usage="[BIO]"
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def bio(self, ctx: Context, *, bio: Jeanne.Range[str, 1, 120]):
        if len(bio) > 60 <= 120:
            bio = bio[:60] + "\n" + bio[60:120]
        embed = Embed(title="New bio has been set to:", color=Color.random())
        await Inventory(ctx.author).set_bio(bio)
        embed.description = bio
        await ctx.send(embed=embed)

    @_set.command(
        aliases=["profile-color", "pcolor"],
        description="Change your level and profile card font and bar color", usage="[HEX COLOR CODE]"
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def color(self, ctx: Context, color: Jeanne.Range[str, 1]):
        embed = Embed()
        try:
            c = ImageColor.getcolor(color, "RGB")
            await Inventory(ctx.author).set_color(color)
            embed.description = "Profile card font and bar color changed to {} as showing in the embed color".format(
                color
            )
            embed.color = int("{:02X}{:02X}{:02X}".format(*c), 16)
        except:
            embed.description = "Invalid color"
            embed.color = Color.red()
        await ctx.send(embed=embed)

    @Jeanne.command(aliases=["ar"], description="Add a role to a member", usage="[MEMBER | MEMBER NAME | MEMBER ID] [ROLE | ROLE NAME | ROLE ID]", extras={"bot_perms":"Manage Roles", "member_perms": "Manage Roles"})
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def addrole(self, ctx: Context, *, member: Member, role: Role):
        await member.add_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Role given", value=f"`{role}` was given to `{member}`", inline=False
        )
        await ctx.send(embed=embed)

    @addrole.error
    async def addrole_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed(
                description="Role is missing or could not be found", color=Color.red()
            )
            await ctx.send(embed=embed)

    @Jeanne.command(
        aliases=["remove-role", "rr"], description="Remove a role from a member", usage="[MEMBER | MEMBER NAME | MEMBER ID] [ROLE | ROLE NAME | ROLE ID]", extras={"bot_perms":"Manage Roles", "member_perms": "Manage Roles"}
    )
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def removerole(self, ctx: Context, *, member: Member, role: Role):
        await member.remove_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Role removed",
            value=f"`{role}` was removed from `{member}`",
            inline=False,
        )
        await ctx.send(embed=embed)

    @removerole.error
    async def removerole_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed(
                description="Role is missing or could not be found", color=Color.red()
            )
            await ctx.send(embed=embed)

    @Jeanne.command(description="Remove something for the server.", extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def remove(self, ctx: Context) -> None:
        embed = Embed(
            description="Click on one of the buttons to remove", color=Color.random()
        )
        view = RemoveManage(ctx.author)
        m = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == None:
            embed.description = "All buttons removed due to timeout"
            await m.edit(embed=embed, view=None)

    @Jeanne.command(description="Clone a channel", usage="<CHANNEL | CHANNEL NAME| CHANNEL ID> <-n NAME> <-t TOPIC> <-cat CATEGORY> <-nsfw Enables NSFW. Just type '-nsfw'>",extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def clone(
        self,
        ctx: Context,
        channel: Optional[TextChannel] = None,
        *words: str,
        parser=manage_parser,
    ) -> None:
        channel = ctx.channel if channel == None else channel
        try:
            (parsed_args,) = parser.parse_known_args(words)
            parsed_args = parser.parse_known_args(words)[0]
            name = (
                "new-channel"
                if parsed_args.name == None
                else " ".join(parsed_args.name)
            )
            topic = None if parsed_args.topic == None else " ".join(
                parsed_args.topic)
            category = (
                None if parsed_args.category == None else " ".join(
                    parsed_args.category)
            )
            slowmode = (
                None if parsed_args.slowmode == None else " ".join(
                    parsed_args.slowmode)
            )
            nsfw_enabled: bool = parsed_args.nsfw
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        name = channel.name if (name == None) else name
        c = await channel.clone(name=name)
        cloned = Embed(
            description="{} was cloned as {}".format(
                channel.jump_url, c.jump_url)
        )
        cloned_channel = await ctx.guild.fetch_channel(c.id)
        if category:
            category = utils.find(
                lambda r: (r.name or r.id) == category, ctx.guild.categories
            )
            cloned_channel.edit(category=category)
            cloned.add_field(name="Category", value=category.name, inline=True)
        if topic:
            if len(topic) > 1024:
                topic = topic[:1024]
            await cloned_channel.edit(topic=topic)
            cloned.add_field(name="Topic", value=topic, inline=True)
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await cloned_channel.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            cloned.add_field(
                name="Slowmode", value=added_slowmode, inline=True)
        if nsfw_enabled:
            if nsfw_enabled == True:
                await cloned_channel.edit(nsfw=True)
                cloned.add_field(name="NSFW enabled", value="Yes", inline=True)
            elif nsfw_enabled == False:
                await cloned_channel.edit(nsfw=False)
                cloned.add_field(name="NSFW enabled", value="No", inline=True)
        await ctx.send(embed=cloned)

    @Jeanne.command(aliases=["rnemote", "rnemoji"], description="Renames an emoji", usage="[EMOJI | EMOJI ID | EMOJI NAME] [NEW NAME]",extras={"bot_perms":"Manage Expressions", "member_perms": "Manage Expressions"})
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def renameemoji(self, ctx: Context, *, emoji: str, name: str):

        try:
            e: int = emoji.strip().split(":")[-1].rstrip(">")
            emote = await ctx.guild.fetch_emoji(e)
        except:
            emote = utils.get(ctx.guild.emojis, name=emoji.replace(" ", "_"))
        embed = Embed(
            description="{} has been renamed to {}".format(str(emote), name),
            color=0x00FF68,
        )
        if len(name) > 32:
            name = name[:32]
        await emote.edit(name=name.replace(" ", "_"))
        await ctx.send(embed=embed)

    @renameemoji.error
    async def emoji_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (AttributeError, NotFound, HTTPException)
        ):
            embed = Embed(
                description="This emoji doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    @Jeanne.command(aliases=["rncat"], description="Renames a category", usage="[CATEGORY | CATEGORY NAME | CATEGORY ID | CATEGORY | CATEGORY NAME | CATEGORY ID ID | CATEGORY | CATEGORY NAME | CATEGORY ID NAME] [NEW NAME]", extras={"bot_perms":"Manage Channels", "member_perms": "Manage Channels"})
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def renamecategory(
        self, ctx: Context, *, category: CategoryChannel, name: str
    ):

        embed = Embed(colour=Color.random())
        if len(name) > 100:
            name = name[:100]
        embed.description = f"`{category.name}` has been renamed as `{name}`"
        await category.edit(name=name)
        await ctx.send(embed=embed)

    @Jeanne.command(aliases=["rnstick"], description="Renames a sticker", usage="[STICKER ID | STICKER NAME] [NEW NAME]",extras={"bot_perms":"Manage Expressions", "member_perms": "Manage Expressions"})
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def renamesticker(self, ctx: Context, *, sticker: Optional[str], name: str):
        if sticker == None:
            sticker = ctx.message.stickers[0].name
        sticker: GuildSticker = utils.get(ctx.guild.stickers, name=sticker)
        if len(name) > 32:
            name = name[:32]
        embed = Embed(
            description="`{}` has been renamed to `{}`".format(
                str(sticker.name), name),
            color=Color.random(),
        )
        await sticker.edit(name=name)
        await ctx.send(embed=embed)

    @renamesticker.error
    async def sticker_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (AttributeError, HTTPException)
        ):
            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    @Jeanne.command(name="disable", description="Disable a command", usage="[COMMAND]",extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    async def _disable(
        self,
        ctx: Context,
        *,
        command: Jeanne.Range[str, 3],
    ):
        cmd = Command(ctx.guild)
        embed = Embed()
        if command.startswith(("help", "command")):
            embed.color = Color.red()
            embed.description = "WOAH! Don't disable that command!"
        elif command not in [
            cmd.qualified_name
            for cmd in self.bot.walk_commands()
            if not isinstance(cmd, Jeanne.Group)
        ]:
            embed.color = Color.red()
            embed.description = "There is no such command that I have..."
        elif cmd.check_disabled(command):
            embed.color = Color.red()
            embed.description = "This command is currently disabled"
        else:
            embed.title = "Command Disabled"
            embed.description = f"`{command}` has been disabled"
            embed.color = Color.random()
            await cmd.disable(command)
        await ctx.send(embed=embed)

    @Jeanne.command(name="enable", description="Enable a command", usage="[COMMAND]", extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    async def _enable(
        self,
        ctx: Context,
        *,
        command: Jeanne.Range[str, 3],
    ):
        embed = Embed()
        cmd = Command(ctx.guild)
        if command not in [
            cmd.qualified_name
            for cmd in self.bot.walk_commands()
            if not isinstance(cmd, Jeanne.Group)
        ]:
            embed.color = Color.red()
            embed.description = "There is no such command that I have..."
        elif cmd.check_disabled(command) == None:
            embed.color = Color.red()
            embed.description = "This command is currently enabled"
        else:
            embed.title = "Command Enabled"
            embed.description = f"`{command}` has been enabled"
            embed.color = Color.random()
            await cmd.enable(command)
        await ctx.send(embed=embed)

    @Jeanne.command(aliases=["list-disabled"], description="List all disabled commands")
    @Jeanne.check(check_botbanned_prefix)
    async def listdisabled(self, ctx: Context):
        cmd = Command(ctx.guild)
        embed = Embed()
        if cmd.list_all_disabled() == None:
            embed.description = "There are no commands currently disabled"
            embed.color = Color.red()
        else:
            embed.title = "List of disabled commands:"
            embed.description = "\n".join(cmd.list_all_disabled())
            embed.color = Color.random()
        await ctx.send(embed=embed)

    @Jeanne.group(
        aliases=["lvl"], description="Main level command", invoke_without_command=True
    )
    async def level(self, ctx: Context): ...

    @level.group(
        aliases=["r"], description="Main role command", invoke_without_command=True
    )
    async def role(self, ctx: Context): ...

    @role.command(
        name="add", description="Add a level role reward when a user levels up", usage="[ROLE | ROLE NAME | ROLE ID] [LEVEL]",extras={"member_perms": "Manage Server"}
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def _add(self, ctx: Context, *, role: Role, level: Jeanne.Range[int, 1]):
        botmember = await ctx.guild.fetch_member(self.bot.user.id)
        if role.position >= botmember.top_role.position:
            embed = Embed(color=Color.red())
            embed.description = "This role is above me"
            await ctx.send(embed=embed)
            return
        await Manage(server=ctx.guild).add_role_reward(role, level)
        embed = Embed(color=Color.random())
        embed.description = (
            "{} will be given to a member if they level up to {}".format(
                role.mention, level
            )
        )
        await ctx.send(embed=embed)

    @role.command(name="remove", description="Removes a level role reward", usage="[ROLE | ROLE NAME | ROLE ID]",extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def _remove(self, ctx: Context, *, role: Role):
        await Manage(server=ctx.guild).remove_role_reward(role)
        embed = Embed(color=Color.random())
        embed.description = "{} has been removed for level role reward".format(
            role.mention
        )
        await ctx.send(embed=embed)

    @role.command(name="list")
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def _list(self, ctx: Context):
        roles = Levelling(server=ctx.guild).list_all_roles
        data = []
        for i in roles:
            role = f"<@&{i[1]}>"
            level = i[2]
            data.append(f"Level {level}: {role}\n")
        embed = Embed(color=Color.random())
        embed.description = "".join(data)
        embed.title = "Level Rewards"
        await ctx.send(embed=embed)

    @level.group(
        aliases=["blchannel", "blacklist-channel"],
        description="Main blacklist channel command",
    )
    async def channel_blacklist(self, ctx: Context): ...

    @channel_blacklist.command(description="Blacklists a channel for gaining XP", usage="[CHANNEL | CHANNEL NAME | CHANNEL ID]",extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def add(self, ctx: Context, *, channel: TextChannel) -> None:
        if Levelling(server=ctx.guild).check_xpblacklist_channel(channel) == False:
            await Manage(server=ctx.guild).add_xpblacklist(channel)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="Channel XP blacklisted",
                value=f"{channel.jump_url} has been added to the XP blacklist",
                inline=False,
            )
            await ctx.send(embed=embed)
            return
        embed = Embed(color=Color.red())
        embed.description = f"{channel.jump_url} is already XP blacklisted"
        await ctx.send(embed=embed)

    @channel_blacklist.command(description="Unblacklists a channel for gaining XP", usage="[TEXT CHANNEL | CHANNEL NAME | CHANNEL ID]",extras={"member_perms": "Manage Server"})
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def remove(self, ctx: Context, *, channel: TextChannel) -> None:
        if Levelling(server=ctx.guild).check_xpblacklist_channel(channel) == False:
            embed = Embed(color=Color.red())
            embed.description = f"{channel.jump_url} is not in the XP blacklisted"
            embed.color = Color.red()
            await ctx.send(embed=embed)
            return
        await Manage(server=ctx.guild).remove_blacklist(channel)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Channel XP unblacklisted",
            value=f"{channel.jump_url} has been removed from the XP blacklist",
            inline=False,
        )
        await ctx.send(embed=embed)

    @channel_blacklist.command(
        name="list", description="List all XP blacklisted channels"
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def _list(self, ctx: Context) -> None:
        embed = Embed()
        channels = Levelling(server=ctx.guild).get_blacklisted_channels
        if channels == None:
            embed.description = "There are no XP blacklisted channels"
            embed.color = Color.red()
        else:
            embed.color = Color.random()
            embed.title = "List of XP blacklisted channels"
            blchannels = []
            for channel in channels:
                blchannel = await ctx.guild.fetch_channel(channel)
                blchannels.append(blchannel.jump_url)
            embed.description = "\n".join(blchannels)
        await ctx.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(ManagePrefix(bot))
