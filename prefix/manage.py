import argparse
from typing import Optional
from json import loads
from discord import (
    Interaction,
    ui,
    AllowedMentions,
    Attachment,
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
from collections import OrderedDict
from functions import (
    Command,
    Inventory,
    Levelling,
    Manage,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from assets.components import (
    BioModal,
    Confirmation,
    Levelmsg,
    RemoveManage,
    Welcomingmsg,
    Leavingmsg,
    ForumGuildlines,
    RankUpmsg,
)
from requests import get
from io import BytesIO
from assets.argparsers import parser


class TopicButton(ui.View):
    def __init__(self, name: str, category: CategoryChannel):
        self.value = None
        self.name = name
        self.category = category
        super().__init__(timeout=180)

    @ui.button(label="Add Guidelines")
    async def guidelines(self, button: ui.Button, ctx: Interaction):
        self.value = "guidelines"
        await ctx.response.send_modal(ForumGuildlines(self.name, self.category))


class CreateGroup(Cog, name="CreatePrefix"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Jeanne.group(aliases=["c"], description="Main create command")
    async def create(self, ctx: Context): ...

    @create.command(aliases=["tc"], description="Creates a text channel")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def textchannel(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            topic = parsed_args.topic + unknown
            topic = " ".join(topic)
            category = parsed_args.category + unknown
            category = " ".join(category)
            slowmode = parsed_args.slowmode + unknown
            slowmode = " ".join(slowmode)
            nsfw_enabled: bool = parsed_args.nsfw
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        channel = await ctx.guild.create_text_channel(
            name=("new channel" if name == None else name)
        )
        embed = Embed()
        embed.color = Color.random()
        embed.description = "{} has been created".format(channel.jump_url)
        if category:
            category = (
                utils.get(ctx.guild.categories, id=category)
                if category.isdigit()
                else utils.get(ctx.guild.categories, name=category)
            )
            await channel.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        if topic:
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

    @create.command(aliases=["vc"], description="Create a voice channel")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def voicechannel(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            category = parsed_args.category + unknown
            category = " ".join(category)
            users: int = parsed_args.users
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        channel = await ctx.guild.create_voice_channel(
            name=("new channel" if name == None else name)
        )
        embed = Embed()
        embed.description = "{} has been created".format(channel.jump_url)
        embed.color = Color.random()
        if category:
            category = (
                utils.get(ctx.guild.categories, id=category)
                if category.isdigit()
                else utils.get(ctx.guild.categories, name=category)
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

    @create.command(aliases=["cat"], description="Create a category")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def category(
        self, ctx: Context, *, name: Optional[Jeanne.Range[str, 1, 100]] = None
    ):
        cat = await ctx.guild.create_category(
            name=("New Category" if name == None else name)
        )
        embed = Embed()
        embed.description = "{} has been created".format(cat.mention)
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @create.command(aliases=["stage"], description="Create a stage channel")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def stagechannel(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            category = parsed_args.category + unknown
            category = " ".join(category)
            users: int = parsed_args.users
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        embed = Embed()
        channel: StageChannel = await ctx.guild.create_stage_channel(
            name=("New Channel" if name == None else name)
        )
        embed.description = "{} has been created".format(channel.jump_url)
        if category:
            category = (
                utils.get(ctx.guild.categories, id=category)
                if category.isdigit()
                else utils.get(ctx.guild.categories, name=category)
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

    @create.command(description="Create a forum")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def forum(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            category = parsed_args.category + unknown
            category = " ".join(category)
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
            category = (
                utils.get(ctx.guild.categories, id=category)
                if category.isdigit()
                else utils.get(ctx.guild.categories, name=category)
            )
            await forum.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        view = TopicButton(name, category)
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

    @create.command(aliases=["r"], description="Create a role")
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def role(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            color = parsed_args.color + unknown
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
        role = await ctx.guild.create_role(name=name)
        embed = Embed()
        embed.description = "Role `{}` has been created".format(name)
        if color != None:
            try:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)
                embed.color = role.color
            except:
                embed.add_field(name="Color", value="Invalid color code", inline=True)
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

    @thread.command(description="Make a public thread")
    @Jeanne.has_permissions(create_public_threads=True, create_private_threads=True)
    @Jeanne.bot_has_permissions(
        create_public_threads=True, create_private_threads=True, manage_threads=True
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def public(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            channel = parsed_args.channel + unknown
            channel = " ".join(channel)
            message_id: int = parsed_args.message
            slowmode = parsed_args.slowmode + unknown
            slowmode = " ".join(slowmode)
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        channel = (
            utils.get(ctx.guild.text_channels, id=channel)
            if channel.isdigit()
            else (
                utils.get(ctx.guild.text_channels, mention=channel)
                if channel.startswith("<#")
                else utils.get(ctx.guild.text_channels, name=channel)
            )
        )
        embed = Embed()
        embed.add_field(name="Channel", value=channel.jump_url, inline=True)
        message = await channel.fetch_message(message_id)
        thread = await channel.create_thread(name=name, message=message)
        embed.add_field(name="Found in message", value=message.jump_url, inline=True)
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

    private_thread_parser = argparse.ArgumentParser(add_help=False)
    private_thread_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="NAME",
        nargs="+",
        required=True,
    )
    private_thread_parser.add_argument(
        "-ch",
        "--channel",
        type=str,
        help="CHANNEL",
        nargs="+",
        required=True,
    )
    private_thread_parser.add_argument(
        "-s",
        "--slowmode",
        type=str,
        help="SLOWMODE",
        nargs="+",
        required=False,
        default=None,
    )

    @thread.command(description="Make a private thread")
    @Jeanne.has_permissions(create_private_threads=True)
    @Jeanne.bot_has_permissions(create_private_threads=True, manage_threads=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def private(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            channel = parsed_args.channel + unknown
            channel = " ".join(channel)
            slowmode = parsed_args.slowmode + unknown
            slowmode = " ".join(slowmode)
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        channel = (
            utils.get(ctx.guild.text_channels, id=channel)
            if channel.isdigit()
            else (
                utils.get(ctx.guild.text_channels, mention=channel)
                if channel.startswith("<#")
                else utils.get(ctx.guild.text_channels, name=channel)
            )
        )
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

    @create.command(aliases=["emote"], description="Make a new emoji")
    @Jeanne.has_permissions(manage_emojis_and_stickers=True)
    @Jeanne.bot_has_permissions(manage_emojis_and_stickers=True)
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
        aliases=["makesticker", "csticker"], description="Make a new sticker"
    )
    @Jeanne.has_permissions(manage_emojis_and_stickers=True)
    @Jeanne.bot_has_permissions(manage_emojis_and_stickers=True)
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
            if len(ctx.guild.stickers) == ctx.guild.sticker_limit:
                embed.description = "You have reached the maximum sticker limit"
            else:
                embed.description = "There was a problem making the sticker. Please check that the sticker you are making is:\n\n1. 512kb or less\n2. The file is in a PNG or APNG format\n3. The correct emoji was added"
            await ctx.send(embed=embed)


class DeleteGroup(Cog, name="DeletePrefix"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Jeanne.group(aliases=["d"], description="Main delete command")
    async def delete(self, ctx: Context): ...

    @Jeanne.command(aliases=["c"], description="Deletes a channel")
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

    @Jeanne.command(aliases=["r"], description="Deletes a role")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def role(self, ctx: Context, *, role: Role):

        embed = Embed(
            description="{} has been deleted".format(role.name), color=Color.random()
        )
        await role.delete()
        await ctx.send(embed=embed)

    @Jeanne.command(aliases=["emote"], description="Deletes an emoji")
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def emoji(self, ctx: Context, *, emoji: str):

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

    @emoji.error
    async def emoji_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (AttributeError, HTTPException)
        ):
            embed = Embed(
                description="This emoji doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    @Jeanne.command(description="Deletes a sticker")
    @Jeanne.describe(sticker="Which sticker are you deleting?")
    @Jeanne.has_permissions(manage_expressions=True)
    @Jeanne.bot_has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def sticker(self, ctx: Context, *, sticker: Optional[str] = None):
        if sticker == None:
            sticker = ctx.message.stickers[0].name
        stick = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` has been deleted".format(str(stick.name)), color=0x00FF68
        )
        await stick.delete()
        await ctx.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (AttributeError, HTTPException)
        ):
            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)


class EditGroup(Cog, name="EditPrefix"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Jeanne.group(description="Main edit command", invoke_without_command=True)
    async def edit(self, ctx: Context): ...

    @edit.command(aliases=["tc", "text"], description="Edits a text/news channel")
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def textchannel(
        self,
        ctx: Context,
        *,
        channel: Optional[TextChannel] = None,
        words: tuple[str, ...],
        parser=parser,
    ) -> None:
        channel = ctx.channel if channel == None else channel
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            topic = parsed_args.topic + unknown
            topic = " ".join(topic)
            category = parsed_args.category + unknown
            category = " ".join(category)
            slowmode = parsed_args.slowmode + unknown
            slowmode = " ".join(slowmode)
            nsfw_enabled: bool = parsed_args.nsfw
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return

        embed = Embed()
        embed.description = "Channel `{}` has been edited".format(channel.name)
        embed.color = Color.green()
        if name:
            await channel.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)
        if category:
            await channel.edit(category=category)
            embed.add_field(name="Category", value=category, inline=True)
        if topic:
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
            if nsfw_enabled == True:
                await channel.edit(nsfw=True)
                embed.add_field(name="NSFW enabled", value="Yes", inline=True)
            elif nsfw_enabled == False:
                await channel.edit(nsfw=False)
                embed.add_field(name="NSFW enabled", value="No", inline=True)
        await ctx.send(embed=embed)

    @edit.command(description="Edit a role")
    @Jeanne.describe(
        role="Which role are you editing?",
        name="What is the new name?",
        color="What is the new color? (use HEX codes)",
        hoisted="Should it be shown in member list?",
        mentionable="Should it be mentioned?",
    )
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def role(
        self, ctx: Context, *, role: Role, words: tuple[str, ...], parser=parser
    ) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            color = parsed_args.color + unknown
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
                embed.add_field(name="Color", value="Invalid color code", inline=True)
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
        description="Edits the server's name, description and verification level"
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def server(self, ctx: Context, *words: str, parser=parser) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            description = parsed_args.description + unknown
            description = " ".join(description)
            verification_level: str = parsed_args.verification_level
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
                embed.add_field(name="Description", value=description, inline=True)
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

    @edit.command(aliases=["pfp"], description="Change the server's avatar")
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

    @edit.command(description="Change the server's banner")
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

    @edit.command(description="Change the server's splash screen")
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


class SetGroup(Cog, name="SetPrefix"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @Jeanne.group(name="set",description="Main set command", invoke_without_command=True)
    async def _set(self, ctx:Context):...

    @_set.command(description="Set a welcomer and/or leaver channel")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def welcomer(
        self,
        ctx: Context,
        *words:str
    ) -> None:
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            welcomer = parsed_args.welcomer + unknown
            welcoming_channel = " ".join(welcomer)
            leaving = parsed_args.leaving + unknown
            leaving_channel = " ".join(leaving)
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
        setup = Embed(description="Welcomer channels set", color=Color.random())
        if welcoming_channel:
            welcoming_channel = (
            utils.get(ctx.guild.text_channels, id=welcoming_channel)
            if welcoming_channel.isdigit()
            else (
                utils.get(ctx.guild.text_channels, mention=welcoming_channel)
                if welcoming_channel.startswith("<#")
                else utils.get(ctx.guild.text_channels, name=welcoming_channel)
            )
            )
            await Manage(ctx.guild).set_welcomer(welcoming_channel)
            setup.add_field(
                name="Channel welcoming users",
                value=welcoming_channel.mention,
                inline=True,
            )
        if leaving_channel:
            leaving_channel = (
            utils.get(ctx.guild.text_channels, id=leaving_channel)
            if leaving_channel.isdigit()
            else (
                utils.get(ctx.guild.text_channels, mention=leaving_channel)
                if leaving_channel.startswith("<#")
                else utils.get(ctx.guild.text_channels, name=leaving_channel)
            )
            )
            await Manage(ctx.guild).set_leaver(leaving_channel)
            setup.add_field(
                name="Channel showing users that left",
                value=leaving_channel.mention,
                inline=True,
            )
        await ctx.send(embed=setup)

    @_set.command(description="Set a modlog channel")
    @Jeanne.describe(
        channel="Which channel should log warns, timeouts, kicks and bans?"
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def modlog(self, ctx: Context, *, channel: TextChannel):

        await Manage(ctx.guild).set_modloger(channel)
        embed = Embed(description="Modlog channel set", color=Color.red())
        embed.add_field(name="Channel selected", value=channel.mention, inline=True)
        await ctx.send(embed=embed)

    @_set.command(aliases=["greet"], description="Set a welcoming message when someone joins the server")
    @Jeanne.describe(jsonfile="Upload JSON file with the welcoming message")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def welcomingmsg(
        self, ctx: Context
    ) -> None:
        jsonfile=ctx.message.attachments[0] if len(ctx.message.attachments) ==1 else None
        if jsonfile != None:

            humans = str(
                len([member for member in ctx.guild.members if not member.bot])
            )
            parameters = OrderedDict(
                [
                    ("%member%", str(ctx.author)),
                    ("%pfp%", str(ctx.author.display_avatar)),
                    ("%server%", str(ctx.guild.name)),
                    ("%mention%", str(ctx.author.mention)),
                    ("%name%", str(ctx.author.name)),
                    ("%members%", str(ctx.guild.member_count)),
                    ("%humans%", str(humans)),
                    ("%icon%", str(ctx.guild.icon)),
                ]
            )
            json_request = str(get(jsonfile.url).content)
            json_content = self.replace_all(json_request, parameters)
            json = loads(json_content)
            try:
                content = json["content"]
                embed = Embed.from_dict(json["embeds"][0])
            except:
                content = json_content
            confirm = Embed(
                description="This is the preview of the welcoming message.\nAre you happy with it?"
            )
            embed = Embed.from_dict(json["embeds"][0])
            view = Confirmation(ctx.author)
            m=await ctx.send(
                content=content,
                embeds=[embed, confirm],
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value == True:
                await Manage(ctx.guild).set_welcomer_msg(str(json_request))
                embed = Embed(description="Welcoming message set")
                await m.edit(
                    content=None, embeds=[embed], view=None
                )
            elif view.value == False:
                embed = Embed(description="Action cancelled")
                await m.edit(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await m.edit(
                    content=None, embeds=[embed], view=None
                )

    @_set.command(aliases=["buy"],description="Set a leaving message when someone leaves the server")
    @Jeanne.describe(jsonfile="Upload JSON file with the welcoming message")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def leavingmsg(
        self, ctx: Context) -> None:
        jsonfile=ctx.message.attachments[0] if len(ctx.message.attachments) ==1 else None
        if jsonfile != None:

            humans = str(
                len([member for member in ctx.guild.members if not member.bot])
            )
            parameters = OrderedDict(
                [
                    ("%member%", str(ctx.author)),
                    ("%pfp%", str(ctx.author.display_avatar)),
                    ("%server%", str(ctx.guild.name)),
                    ("%mention%", str(ctx.author.mention)),
                    ("%name%", str(ctx.author.name)),
                    ("%members%", str(ctx.guild.member_count)),
                    ("%humans%", str(humans)),
                    ("%icon%", str(ctx.guild.icon)),
                ]
            )
            json_request = str(get(jsonfile.url).content)
            json_content = self.replace_all(json_request, parameters)
            json = loads(json_content)
            try:
                content = json["content"]
                embed = Embed.from_dict(json["embeds"][0])
            except:
                content = json_content
            confirm = Embed(
                description="This is the preview of the leaving message.\nAre you happy with it?"
            )
            embed = Embed.from_dict(json["embeds"][0])
            view = Confirmation(ctx.author)
            m=await ctx.send(
                content=content,
                embeds=[embed, confirm],
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value == True:
                await Manage(ctx.guild).set_leaving_msg(str(json_request))
                embed = Embed(description="Leaving message set")
                await m.edit(
                    content=None, embeds=[embed], view=None
                )
            elif view.value == False:
                embed = Embed(description="Action cancelled")
                await m.edit(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await m.edit(
                    content=None, embeds=[embed], view=None
                )

    @_set.command(aliases=["rrm"],
        description="Set a role reward message. This will be posted in the levelup channel"
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def rolereward_message(
        self, ctx: Context, *, message: Optional[str] = None
    ) -> None:
        if message == True:
            await ctx.response.send_modal(RankUpmsg())
            return

        await Manage(ctx.guild).add_rankup_rolereward(message)
        embed = Embed()
        embed.description = "Default Role Reward message set"
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @Jeanne.command(description="Set a level up notification channel")
    @Jeanne.describe(
        channel="Which channel will update when a member levels up?",
        levelmsg="Add your level message here. Use Discohooks to generate the embed",
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def levelupdate(
        self, ctx: Context, channel: TextChannel, levelmsg: Optional[bool] = None
    ) -> None:
        if levelmsg == True:
            await ctx.response.send_modal(Levelmsg(channel))
            return

        await Manage(server=ctx.guild).add_level_channel(channel)
        embed = Embed()
        embed.description = "{} will post level updates when someone levels up".format(
            channel.mention
        )
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @Jeanne.command(
        name="profile-brightness",
        description="Change the brightness of your level and profile card background",
    )
    @Jeanne.describe(
        brightness="Set the level of brightness between 10 - 150. Default is 100"
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def brightness(self, ctx: Context, brightness: Jeanne.Range[int, 10, 150]):

        embed = Embed()
        if Inventory(ctx.user).set_brightness(brightness) == False:
            embed.description = "You have no background wallpaper"
            embed.color = Color.red()
            await ctx.send(embed=embed)
            return
        await Inventory(ctx.user).set_brightness(brightness)
        embed.description = "Brightness has been changed to {}".format(brightness)
        embed.color = Color.random()
        await ctx.send(embed=embed)

    @Jeanne.command(name="profile-bio", description="Change your profile bio")
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def bio(self, ctx: Context):
        await ctx.response.send_modal(BioModal())

    @Jeanne.command(
        name="profile-color",
        description="Change your level and profile card font and bar color",
    )
    @Jeanne.describe(color="Add your color")
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def color(self, ctx: Context, color: Jeanne.Range[str, 1]):

        embed = Embed()
        try:
            c = ImageColor.getcolor(color, "RGB")
            await Inventory(ctx.user).set_color(color)
            embed.description = "Profile card font and bar color changed to {} as showing in the embed color".format(
                color
            )
            embed.color = int("{:02X}{:02X}{:02X}".format(*c), 16)
        except:
            embed.description = "Invalid color"
            embed.color = Color.red()
        await ctx.send(embed=embed)


class manage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(name="add-role", description="Add a role to a member")
    @Jeanne.describe(member="Which member?", role="Which role are you adding?")
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def addrole(self, ctx: Context, member: Member, role: Role):

        await member.add_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Role given", value=f"`{role}` was given to `{member}`", inline=False
        )
        await ctx.send(embed=embed)

    @Jeanne.command(name="remove-role", description="Remove a role from a member")
    @Jeanne.describe(member="Which member?", role="Which role are you removing?")
    @Jeanne.has_permissions(manage_roles=True)
    @Jeanne.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def removerole(self, ctx: Context, member: Member, role: Role):

        await member.remove_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Role removed",
            value=f"`{role}` was removed from `{member}`",
            inline=False,
        )
        await ctx.send(embed=embed)

    @Jeanne.command(description="Remove something for the server.")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def remove(self, ctx: Context) -> None:

        embed = Embed(
            description="Click on one of the buttons to remove", color=Color.random()
        )
        view = RemoveManage(ctx.user)
        await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == None:
            embed.description = "All buttons removed due to timeout"
            await ctx.edit_original_response(embed=embed, view=None)

    @Jeanne.command(description="Clone a channel")
    @Jeanne.describe(
        channel="Which channel are you cloning?", name="What is the new name?"
    )
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def clone(
        self,
        ctx: Context,
        channel: abc.GuildChannel,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:

        name = channel.name if (name == None) else name
        c = await channel.clone(name=name)
        cloned = Embed(
            description="{} was cloned as {}".format(channel.jump_url, c.jump_url)
        )
        cloned_channel = await ctx.guild.fetch_channel(c.id)
        if category:
            cloned_channel.edit(category=category)
            cloned.add_field(name="Category", value=category.name, inline=True)
        if nsfw_enabled:
            cloned_channel.edit(nsfw=nsfw_enabled)
            cloned.add_field(name="NSFW Enabled", value=nsfw_enabled, inline=True)
        cloned.color = Color.random()
        await ctx.send(embed=cloned)


class Rename_Group(Cog, name="rename"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Renames an emoji")
    @Jeanne.describe(emoji="What emoji are you renaming?", name="What is the new name?")
    @Jeanne.has_permissions(manage_emojis_and_stickers=True)
    @Jeanne.bot_has_permissions(manage_emojis_and_stickers=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def emoji(self, ctx: Context, emoji: str, name: Jeanne.Range[str, 2, 30]):

        try:
            e: int = emoji.strip().split(":")[-1].rstrip(">")
            emote = await ctx.guild.fetch_emoji(e)
        except:
            emote = utils.get(ctx.guild.emojis, name=emoji.replace(" ", "_"))
        embed = Embed(
            description="{} has been renamed to {}".format(str(emote), name),
            color=0x00FF68,
        )
        await emote.edit(name=name.replace(" ", "_"))
        await ctx.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="This emoji doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    @Jeanne.command(description="Renames a category")
    @Jeanne.describe(
        category="Which category are you renaming?", name="What is the new name?"
    )
    @Jeanne.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def category(
        self,
        ctx: Context,
        category: CategoryChannel,
        name: Jeanne.Range[str, 1, 100],
    ):

        embed = Embed(colour=Color.random())
        embed.description = f"`{category.name}` has been renamed as `{name}`"
        await category.edit(name=name)
        await ctx.send(embed=embed)

    @Jeanne.command(description="Renames a sticker")
    @Jeanne.describe(
        sticker="What sticker are you renaming?", name="What is the new name?"
    )
    @Jeanne.has_permissions(manage_emojis_and_stickers=True)
    @Jeanne.bot_has_permissions(manage_emojis_and_stickers=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def sticker(self, ctx: Context, sticker: str, name: Jeanne.Range[str, 2, 30]):

        sticker: GuildSticker = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` has been renamed to `{}`".format(str(sticker.name), name),
            color=Color.random(),
        )
        await sticker.edit(name=name)
        await ctx.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):

            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)


class Command_Group(Cog, name="command"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(name="disable", description="Disable a command")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    async def _disable(
        self,
        ctx: Context,
        command: Jeanne.Range[str, 3],
    ):

        cmd = Command(ctx.guild)
        embed = Embed()
        if command.startswith(("help", "command")):
            embed.color = Color.red()
            embed.description = "WOAH! Don't disable that command!"
        elif command not in [
            cmd.qualified_name
            for cmd in self.bot.tree.walk_commands()
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

    @Jeanne.command(name="enable", description="Enable a command")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.describe(command="Which command are you enabling?")
    @Jeanne.check(check_botbanned_prefix)
    async def _enable(
        self,
        ctx: Context,
        command: Jeanne.Range[str, 3],
    ):

        embed = Embed()
        cmd = Command(ctx.guild)
        if command not in [
            cmd.qualified_name
            for cmd in self.bot.tree.walk_commands()
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

    @Jeanne.command(name="list-disabled", description="List all disabled commands")
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


class Level_Group(Cog, name="level"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    role = Jeanne.Group(name="role-reward", description="...")

    @role.command(
        name="add", description="Add a level role reward when a user levels up"
    )
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.describe(
        role="Which role should be given when a user levels up?",
        level="Which level should they be to get that role?",
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def _add(self, ctx: Context, role: Role, level: Jeanne.Range[int, 1]):

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

    @role.command(name="remove", description="Removes a level role reward")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.describe(
        role="Which role should be removed?",
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def _remove(self, ctx: Context, role: Role):

        await Manage(server=ctx.guild).remove_role_reward(role)
        embed = Embed(color=Color.random())
        embed.description = "{} has been removed for level role reward".format(
            role.mention
        )
        await ctx.send(embed=embed)

    @role.command(
        name="list", description="Add a level role reward when a user levels up"
    )
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

    channel_blacklist = Jeanne.Group(name="blacklist-channel", description="...")

    @channel_blacklist.command(description="Blacklists a channel for gaining XP")
    @Jeanne.describe(channel="Which channel?")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def add(self, ctx: Context, channel: TextChannel) -> None:

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

    @channel_blacklist.command(description="Unblacklists a channel for gaining XP")
    @Jeanne.describe(channel="Which channel?")
    @Jeanne.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def remove(self, ctx: Context, channel: TextChannel) -> None:

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
    await bot.add_cog(manage(bot))
    await bot.add_cog(CreateGroup(bot))
    await bot.add_cog(DeleteGroup(bot))
    await bot.add_cog(EditGroup(bot))
    await bot.add_cog(SetGroup(bot))
    await bot.add_cog(Rename_Group(bot))
    await bot.add_cog(Command_Group(bot))
    await bot.add_cog(Level_Group(bot))
