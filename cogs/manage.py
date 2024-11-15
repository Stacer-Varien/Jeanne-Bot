from typing import Optional
from json import loads
from discord import (
    AllowedMentions,
    Attachment,
    CategoryChannel,
    Color,
    Embed,
    File,
    GuildSticker,
    HTTPException,
    Interaction,
    User,
    NotFound,
    Role,
    StageChannel,
    TextChannel,
    VerificationLevel,
    VoiceChannel,
    app_commands as Jeanne,
    abc,
    utils,
)
from PIL import ImageColor
from discord.ext.commands import Bot, Cog, GroupCog
from humanfriendly import format_timespan, parse_timespan, InvalidTimespan
from collections import OrderedDict
from functions import (
    AutoCompleteChoices,
    Command,
    Inventory,
    Levelling,
    Manage,
    check_botbanned_app_command,
    check_disabled_app_command,
)
from assets.components import (
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


class Create_Group(GroupCog, name="create"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description="Creates a text channel",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name="What will you name it?",
        topic="What is the channel topic?",
        category="Place in which category?",
        slowmode="What is the slowmode (1h, 30m, etc) (Max is 6 hours)",
        nsfw_enabled="Should it be an NSFW channel?",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def textchannel(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        topic: Optional[Jeanne.Range[str, 1, 1024]] = None,
        category: Optional[CategoryChannel] = None,
        slowmode: str = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        name = "new-channel" if name == None else name
        channel = await ctx.guild.create_text_channel(name=name)
        embed = Embed()
        embed.color = Color.random()
        embed.description = "{} has been created".format(channel.jump_url)
        if category:
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
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Create a voice channel",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name="What will you name it?",
        category="Place in which category?",
        users="How many users are allowed in the channel",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def voicechannel(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 99]] = None,
    ) -> None:
        await ctx.response.defer()
        name = "new-channel" if name == None else name
        channel = await ctx.guild.create_voice_channel(name=name)
        embed = Embed()
        embed.description = "{} has been created".format(channel.jump_url)
        embed.color = Color.random()
        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        if users:
            await channel.edit(user_limit=users)
            embed.add_field(name="User Limit", value=users, inline=True)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Create a category",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(name="What will you name it?")
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def category(self, ctx: Interaction, name: Jeanne.Range[str, 1, 100]):
        await ctx.response.defer()
        cat = await ctx.guild.create_category(name=name)
        embed = Embed()
        embed.description = "{} has been created".format(cat.mention)
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Create a stage channel",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name="What will you name it?",
        category="Place in which category?",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def stagechannel(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 10000]] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        channel: StageChannel = await ctx.guild.create_stage_channel(name=name)
        embed.description = "{} has been created".format(channel.jump_url)
        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Moved to category", value=category.mention, inline=True
            )
        if users:
            await channel.edit(user_limit=users)
            embed.add_field(name="Users", value=users, inline=True)
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    @stagechannel.error
    async def stagechannel_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Couldn't make a new stage channel. Please make sure the server is community enabled"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Create a forum",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name="What will you name it?",
        topic="What is the topic",
        category="Place in which category?",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def forum(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        category: Optional[CategoryChannel] = None,
        topic: Optional[bool] = None,
    ):
        if topic:
            await ctx.response.send_modal(ForumGuildlines(name, category))
            return
        await ctx.response.defer()
        embed = Embed()
        forum = await ctx.guild.create_forum(name=name, topic=topic)
        embed.description = "{} has been created".format(forum.jump_url)
        embed.color = Color.random()
        if category:
            await forum.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )
        await ctx.followup.send(embed=embed)

    @forum.error
    async def forum_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):

            embed = Embed()
            embed.description = "Couldn't make a new forum. Please make sure the server is community enabled"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Create a role",
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        name="What will you name it?",
        color="What color will it be? (use HEX codes)",
        hoisted="Should it be shown in member list?",
        mentionable="Should it be mentioned?",
    )
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def role(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, None, 100],
        color: Optional[Jeanne.Range[str, None, 6]] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)

    thread_group = Jeanne.Group(name="thread", description="...")

    @thread_group.command(
        description="Make a public thread",
        extras={
            "bot_perms": "Create Public Threads\nManage Threads",
            "member_perms": "Create Public Threads",
        },
    )
    @Jeanne.describe(
        name="What will you name it?",
        channel="Which channel is the message in?",
        message_id="What is the message ID? You can leave it blank for a private thread",
        slowmode="What is the slowmode (1h, 30m, etc) (Max is 6 hours)",
    )
    @Jeanne.checks.has_permissions(
        create_public_threads=True,
    )
    @Jeanne.checks.bot_has_permissions(create_public_threads=True, manage_threads=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def public(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        channel: TextChannel,
        message_id: str,
        slowmode: Optional[str] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        embed.add_field(name="Channel", value=channel.jump_url, inline=True)
        message = await channel.fetch_message(int(message_id))
        thread = await channel.create_thread(name=name, message=message)
        embed.add_field(name="Found in message", value=message.jump_url, inline=True)
        await thread.add_user(ctx.user)
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
        await ctx.followup.send(embed=embed)

    @public.error
    async def public_thread_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, NotFound
        ):
            embed = Embed()
            embed.description = "Message could not be found. Please make sure you have added the correct message ID"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Failed to create public thread. Please try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @thread_group.command(
        description="Make a private thread",
        extras={
            "bot_perms": "Create Private Threads\nManage Threads",
            "member_perms": "Create Private Threads",
        },
    )
    @Jeanne.describe(
        name="What will you name it?",
        channel="Which channel is the message in?",
        slowmode="What is the slowmode (1h, 30m, etc) (Max is 6 hours)",
    )
    @Jeanne.checks.bot_has_permissions(create_private_threads=True)
    @Jeanne.checks.has_permissions(create_private_threads=True, manage_threads=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def private(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        channel: TextChannel,
        slowmode: Optional[str] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        embed.add_field(name="Channel", value=channel.jump_url, inline=True)
        thread = await channel.create_thread(name=name)
        await thread.add_user(ctx.user)
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
        await ctx.followup.send(embed=embed)

    @private.error
    async def private_thread_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed()
            embed.description = "Failed to create private thread. Please try again"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Make a new emoji",
        extras={
            "bot_perms": "Manage Expressions, Create Expressions",
            "member_perms": "Manage Expressions,Create Expressions",
        },
    )
    @Jeanne.describe(
        name="What will you name it?",
        emoji_link="Insert emoji URL here",
        emoji_image="Insert emoji image here",
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True, create_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True, create_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def emoji(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 2, 30],
        emoji_link: Optional[str] = None,
        emoji_image: Optional[Attachment] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        if emoji_link == None and emoji_image == None:
            embed.description = "Please add either an emoji URL or emoji image"
            embed.color = Color.red()
        elif emoji_link and emoji_image:
            embed.description = "Please use either an emoji URL or emoji image"
            embed.color = Color.red()
        else:
            emojibytes = get(emoji_link if emoji_link else emoji_image.url).content
            emote = await ctx.guild.create_custom_emoji(
                name=name.replace(" ", "_"), image=emojibytes
            )
            embed.description = "{} | {} has been created".format(
                emote.name, str(emote)
            )
            embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
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
                await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Make a new sticker",
        extras={
            "bot_perms": "Manage Expressions, Create Expressions",
            "member_perms": "Manage Expressions,Create Expressions",
        },
    )
    @Jeanne.describe(
        name="What will you name it?",
        emoji="Emoji that will repesent the sticker",
        sticker_link="Insert sticker URL here",
        sticker_image="Insert sticker image here",
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def sticker(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 2, 30],
        emoji: str,
        sticker_link: Optional[str] = None,
        sticker_image: Optional[Attachment] = None,
    ):
        embed = Embed()
        if sticker_link is None and sticker_image is None:
            embed.description = "Please add either an sticker URL or sticker image"
            embed.color = Color.red()
        elif sticker_link and sticker_image:
            embed.description = "Please use either an sticker URL or sticker image"
            embed.color = Color.red()
        else:
            url = sticker_link if sticker_link else sticker_image.url
            stickerbytes = BytesIO(get(url).content)
            stickerfile = File(fp=stickerbytes, filename="sticker.png")
            sticker = await ctx.guild.create_sticker(
                name=name.lower(), description="None", emoji=emoji, file=stickerfile
            )
            embed.description = "{} has been created".format(sticker.name)
            embed.color = Color.random()
            embed.set_image(url=url)
        await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            embed = Embed(color=Color.red())
            embed.description = "There was a problem making the sticker. Please check that the sticker you are making is:\n\n1. 512kb or less\n2. The file is in a PNG or APNG format\n3. The correct emoji was added\n\nIf all meet the conditions but still fail, that means you have reached the limit of sticker slots"
            await ctx.followup.send(embed=embed)


class Delete_Group(GroupCog, name="delete"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description="Deletes a channel",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(channel="Which channel are you deleting?")
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def channel(self, ctx: Interaction, channel: abc.GuildChannel):
        await ctx.response.defer()
        embed = Embed(
            description="{} has been deleted".format(channel.name), color=Color.random()
        )
        await channel.delete()
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Deletes a role",
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        role="Which role are you deleting?",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def role(self, ctx: Interaction, role: Role):
        await ctx.response.defer()
        embed = Embed(
            description="{} has been deleted".format(role.name), color=Color.random()
        )
        await role.delete()
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Deletes an emoji",
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(emoji="Which emoji are you deleting?")
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def emoji(self, ctx: Interaction, emoji: str):
        await ctx.response.defer()
        try:
            e = emoji.strip().split(":")[-1].rstrip(">")
            emote = await ctx.guild.fetch_emoji(int(e))
        except:
            emote = utils.get(ctx.guild.emojis, name=emoji.replace(" ", "_"))
        embed = Embed(
            description="{} has been deleted".format(str(emote)), color=0x00FF68
        )
        await emote.delete()
        await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="This emoji doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Deletes a sticker",
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(sticker="Which sticker are you deleting?")
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def sticker(self, ctx: Interaction, sticker: str):
        await ctx.response.defer()
        stick = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` has been deleted".format(str(stick.name)), color=0x00FF68
        )
        await stick.delete()
        await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)


class Edit_Group(GroupCog, name="edit"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description="Edits a text/news channel",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        channel="Which channel are you editing?",
        name="What will be the new name?",
        topic="What should be the new topic?",
        slowmode="What is the slowmode (1hr, 30m, etc) (Max is 6 hours)",
        category="Place in which category?",
        nsfw_enabled="Should it be an NSFW channel?",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def textchannel(
        self,
        ctx: Interaction,
        channel: Optional[TextChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        topic: Optional[Jeanne.Range[str, 1, 1024]] = None,
        slowmode: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        channel = ctx.channel if channel == None else channel
        embed = Embed()
        embed.description = "Channel `{}` has been edited".format(channel.name)
        embed.color = Color.green()
        if name:
            await channel.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)
        if category:
            await channel.edit(category=category)
            embed.add_field(name="Moved to category", value=category, inline=True)
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
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Edits a voice channel",
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        channel="Which channel are you editing?",
        name="What will be the new name?",
        category="Place in which category?",
        users="How many users are allowed in the channel",
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def voicechannel(
        self,
        ctx: Interaction,
        channel: Optional[VoiceChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 99]] = None,
    ) -> None:
        await ctx.response.defer()
        channel = ctx.channel if channel == None else channel
        embed = Embed()
        embed.description = "Channel `{}` has been edited".format(channel.name)
        embed.color = Color.green()
        if name:
            await channel.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)
        if category:
            await channel.edit(category=category)
            embed.add_field(name="Moved to category", value=category, inline=True)
        if users:
            if users > 99:
                users = 99
            await channel.edit(user_limit=users)
            embed.add_field(name="Users", value=users, inline=True)

        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Edit a role",
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        role="Which role are you editing?",
        name="What is the new name?",
        color="What is the new color? (use HEX codes)",
        hoisted="Should it be shown in member list?",
        mentionable="Should it be mentioned?",
    )
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def role(
        self,
        ctx: Interaction,
        role: Role,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        color: Optional[Jeanne.Range[str, None, 6]] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Edits the server",
        extras={"bot_perms": "Manage Server", "member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        name="What is the new name?",
        description="What is the new description (only for public servers)",
        avatar="What is the new server avatar?",
        splash="What will be the new invite splash screen?",
        banner="What will be the new banner?",
        verification_level="How high should the verification level be?",
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def server(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 2, 100]] = None,
        description: Optional[Jeanne.Range[str, None, 120]] = None,
        avatar: Optional[Attachment] = None,
        splash: Optional[Attachment] = None,
        banner: Optional[Attachment] = None,
        verification_level: Optional[VerificationLevel] = None,
    ) -> None:
        await ctx.response.defer()
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
        if avatar:
            try:
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
        if splash:
            if ctx.guild.premium_tier == 0:
                embed.add_field(
                    name="Splash not added",
                    value="This server is not boosted to Tier 1",
                    inline=True,
                )
            else:
                try:
                    splash_url = splash.url
                    splash_bytes = get(splash_url).content
                    await ctx.guild.edit(splash=splash_bytes)
                    embed.add_field(
                        name="Server's New Splash Screen",
                        value=ctx.guild.splash.url,
                        inline=True,
                    )
                except:
                    pass
        if banner:
            if ctx.guild.premium_tier <= 1:
                embed.add_field(
                    name="Banner not added",
                    value="This server is not boosted to Tier 2",
                    inline=True,
                )
            else:
                try:
                    bannerbytes = get(banner.url).content
                    await ctx.guild.edit(banner=bannerbytes)
                    embed.add_field(
                        name="Server's New Banner",
                        value=ctx.guild.banner.url,
                        inline=True,
                    )
                except:
                    pass
        if verification_level:
            if verification_level.name == "none":
                await ctx.guild.edit(verification_level=VerificationLevel.none)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nNo verification required".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "low":
                await ctx.guild.edit(verification_level=VerificationLevel.low)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified email".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "medium":
                await ctx.guild.edit(verification_level=VerificationLevel.medium)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified email and be registered on Discord for more than 5 minutes".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "high":
                await ctx.guild.edit(verification_level=VerificationLevel.high)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified email, be registered on Discord for more than 5 minutes and stay in the server for more than 10 minutes".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "highest":
                await ctx.guild.edit(verification_level=VerificationLevel.highest)
                embed.add_field(
                    name="Verification Level",
                    value="**{}**\nMembers must have a verified phone number".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
        await ctx.followup.send(embed=embed)


class Set_Group(GroupCog, name="set"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @Jeanne.command(
        description="Set a welcomer and/or leaver channel",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        welcoming_channel="Which channel should alert members when someone join",
        leaving_channel="Which channel should members when someone leaves?",
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def welcomer(
        self,
        ctx: Interaction,
        welcoming_channel: Optional[TextChannel] = None,
        leaving_channel: Optional[TextChannel] = None,
    ) -> None:
        await ctx.response.defer()
        if (welcoming_channel == None) and (leaving_channel == None):
            error = Embed(
                description="Both options are empty. Please set at least a welcomer or leaving channel",
                color=Color.red(),
            )
            await ctx.followup.send(embed=error)
            return
        setup = Embed(description="Welcomer channels set", color=Color.random())
        if welcoming_channel:
            await Manage(ctx.guild).set_welcomer(welcoming_channel)
            setup.add_field(
                name="Channel welcoming users",
                value=welcoming_channel.mention,
                inline=True,
            )
        if leaving_channel:
            await Manage(ctx.guild).set_leaver(leaving_channel)
            setup.add_field(
                name="Channel showing users that left",
                value=leaving_channel.mention,
                inline=True,
            )
        await ctx.followup.send(embed=setup)

    @Jeanne.command(
        description="Set a modlog channel",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        channel="Which channel should log warns, timeouts, kicks and bans?"
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def modlog(self, ctx: Interaction, channel: TextChannel):
        await ctx.response.defer()
        await Manage(ctx.guild).set_modloger(channel)
        embed = Embed(description="Modlog channel set", color=Color.red())
        embed.add_field(name="Channel selected", value=channel.mention, inline=True)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Set a welcoming message when someone joins the server",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(jsonfile="Upload JSON file with the welcoming message")
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def welcomingmsg(
        self, ctx: Interaction, jsonfile: Optional[Attachment] = None
    ) -> None:
        if jsonfile == None:
            await ctx.response.send_modal(Welcomingmsg())
            return
        if jsonfile != None:
            await ctx.response.defer()
            humans = str(
                len([member for member in ctx.guild.members if not member.bot])
            )
            parameters = OrderedDict(
                [
                    ("%member%", str(ctx.user)),
                    ("%pfp%", str(ctx.user.display_avatar)),
                    ("%server%", str(ctx.guild.name)),
                    ("%mention%", str(ctx.user.mention)),
                    ("%name%", str(ctx.user.name)),
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
            view = Confirmation(ctx.user)
            await ctx.followup.send(
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
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif view.value == False:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )

    @Jeanne.command(
        description="Set a leaving message when someone leaves the server",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(jsonfile="Upload JSON file with the welcoming message")
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def leavingmsg(
        self, ctx: Interaction, jsonfile: Optional[Attachment] = None
    ) -> None:
        if jsonfile == None:
            await ctx.response.send_modal(Leavingmsg())
            return
        if jsonfile != None:
            await ctx.response.defer()
            humans = str(
                len([member for member in ctx.guild.members if not member.bot])
            )
            parameters = OrderedDict(
                [
                    ("%member%", str(ctx.user)),
                    ("%pfp%", str(ctx.user.display_avatar)),
                    ("%server%", str(ctx.guild.name)),
                    ("%mention%", str(ctx.user.mention)),
                    ("%name%", str(ctx.user.name)),
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
            view = Confirmation(ctx.user)
            await ctx.followup.send(
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
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif view.value == False:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )

    @Jeanne.command(
        description="Set a role reward message. This will be posted in the levelup channel",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def rolereward_message(
        self, ctx: Interaction, message: Optional[bool] = None
    ) -> None:
        if message == True:
            await ctx.response.send_modal(RankUpmsg())
            return
        await ctx.response.defer()
        await Manage(ctx.guild).add_rankup_rolereward(message)
        embed = Embed()
        embed.description = "Default Role Reward message set"
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Set a level up notification channel",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        channel="Which channel will update when a member levels up?",
        levelmsg="Add your level message here. Use Discohooks to generate the embed",
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def levelupdate(
        self, ctx: Interaction, channel: TextChannel, levelmsg: Optional[bool] = None
    ) -> None:
        if levelmsg == True:
            await ctx.response.send_modal(Levelmsg(channel))
            return
        await ctx.response.defer()
        await Manage(server=ctx.guild).add_level_channel(channel)
        embed = Embed()
        embed.description = "{} will post level updates when someone levels up".format(
            channel.mention
        )
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="confession-channel",
        description="Set a confession channel",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        channel="Which channel will receive anonymous confessions from members?",
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def confessionchannel(self, ctx: Interaction, channel: TextChannel) -> None:
        await ctx.response.defer()
        embed = Embed(
            description=f"{channel.mention} will recieve anonymous confessions from members",
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="profile-brightness",
        description="Change the brightness of your level and profile card background",
    )
    @Jeanne.describe(
        brightness="Set the level of brightness between 10 - 150. Default is 100"
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def brightness(
        self, ctx: Interaction, brightness: Jeanne.Range[int, 10, 150]
    ):
        await ctx.response.defer()
        embed = Embed()
        if Inventory(ctx.user).set_brightness(brightness) == False:
            embed.description = "You have no background wallpaper"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return
        await Inventory(ctx.user).set_brightness(brightness)
        embed.description = "Brightness has been changed to {}%".format(brightness)
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    @Jeanne.command(name="profile-bio", description="Change your profile bio")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def bio(self, ctx: Interaction, bio: Jeanne.Range[str, 1, 120]):
        await ctx.response.defer()
        if len(bio) > 60 <= 120:
            bio = bio[:60] + "\n" + bio[60:120]
        embed = Embed(title="New bio has been set to:", color=Color.random())
        await Inventory(ctx.user).set_bio(bio)
        embed.description = bio
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="profile-color",
        description="Change your level and profile card font and bar color",
    )
    @Jeanne.describe(color="Add your color")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def color(self, ctx: Interaction, color: Jeanne.Range[str, 1]):
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)


class manage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name="add-role",
        description="Add a role to a member",
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(member="Which member?", role="Which role are you adding?")
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def addrole(self, ctx: Interaction, member: User, role: Role):
        await ctx.response.defer()
        await member.add_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Role given", value=f"`{role}` was given to `{member}`", inline=False
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="remove-role",
        description="Remove a role from a member",
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(member="Which member?", role="Which role are you removing?")
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def removerole(self, ctx: Interaction, member: User, role: Role):
        await ctx.response.defer()
        m=await ctx.guild.fetch_member(member.id)
        await m.remove_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Role removed",
            value=f"`{role}` was removed from `{member}`",
            inline=False,
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Remove something for the server.",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def remove(self, ctx: Interaction) -> None:
        await ctx.response.defer()
        embed = Embed(
            description="Click on one of the buttons to remove", color=Color.random()
        )
        view = RemoveManage(ctx.user)
        await ctx.followup.send(embed=embed, view=view)
        await view.wait()
        if view.value == None:
            embed.description = "All buttons removed due to timeout"
            await ctx.edit_original_response(embed=embed, view=None)

    @Jeanne.command(
        description="Clone a channel",
        extras={"bot_perms": "Manage Channel", "member_perms": "Manage Channel"},
    )
    @Jeanne.describe(
        channel="Which channel are you cloning?", name="What is the new name?"
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def clone(
        self,
        ctx: Interaction,
        channel: Optional[abc.GuildChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        channel = ctx.channel if channel == None else channel
        name = channel.name if (name == None) else name
        c = await channel.clone(name=name)
        cloned = Embed(
            description="{} was cloned as {}".format(channel.jump_url, c.jump_url)
        )
        cloned_channel = await ctx.guild.fetch_channel(c.id)
        if category:
            if channel is CategoryChannel:
                cloned.add_field(
                    name="Moved to category",
                    value="Cannot move a category to a category",
                    inline=True,
                )
            else:
                await cloned_channel.edit(category=category)
                cloned.add_field(
                    name="Moved to category", value=category.name, inline=True
                )
        if nsfw_enabled:
            await cloned_channel.edit(nsfw=nsfw_enabled)
            cloned.add_field(name="NSFW Enabled", value=nsfw_enabled, inline=True)
        cloned.color = Color.random()
        await ctx.followup.send(embed=cloned)


class Rename_Group(GroupCog, name="rename"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        description="Renames an emoji",
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(emoji="What emoji are you renaming?", name="What is the new name?")
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def emoji(self, ctx: Interaction, emoji: str, name: Jeanne.Range[str, 2, 30]):
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="This emoji doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Renames a category",
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(
        category="Which category are you renaming?", name="What is the new name?"
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def category(
        self,
        ctx: Interaction,
        category: CategoryChannel,
        name: Jeanne.Range[str, 1, 100],
    ):
        await ctx.response.defer()
        embed = Embed(colour=Color.random())
        embed.description = f"`{category.name}` has been renamed as `{name}`"
        await category.edit(name=name)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Renames a sticker",
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(
        sticker="What sticker are you renaming?", name="What is the new name?"
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def sticker(
        self, ctx: Interaction, sticker: str, name: Jeanne.Range[str, 2, 30]
    ):
        await ctx.response.defer()
        sticker: GuildSticker = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` has been renamed to `{}`".format(str(sticker.name), name),
            color=Color.random(),
        )
        await sticker.edit(name=name)
        await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):

            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)


class Command_Group(GroupCog, name="command"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name="disable",
        description="Disable a command",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.autocomplete(command=AutoCompleteChoices.command_choices)
    @Jeanne.describe(command="Which command are you disabling?")
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    async def _disable(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
    ):
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)

    @Jeanne.command(name="enable", description="Enable a command")
    @Jeanne.autocomplete(command=AutoCompleteChoices.disabled_commands)
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.describe(command="Which command are you enabling?")
    @Jeanne.check(check_botbanned_app_command)
    async def _enable(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
    ):
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)

    @Jeanne.command(name="list-disabled", description="List all disabled commands")
    @Jeanne.check(check_botbanned_app_command)
    async def listdisabled(self, ctx: Interaction):
        await ctx.response.defer()
        cmd = Command(ctx.guild)
        embed = Embed()
        if cmd.list_all_disabled() == None:
            embed.description = "There are no commands currently disabled"
            embed.color = Color.red()
        else:
            embed.title = "List of disabled commands:"
            embed.description = "\n".join(cmd.list_all_disabled())
            embed.color = Color.random()
        await ctx.followup.send(embed=embed)


class Level_Group(GroupCog, name="level"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    role = Jeanne.Group(name="role-reward", description="...")

    @role.command(
        name="add",
        description="Add a level role reward when a user levels up",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.describe(
        role="Which role should be given when a user levels up?",
        level="Which level should they be to get that role?",
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def _add(self, ctx: Interaction, role: Role, level: Jeanne.Range[int, 1]):
        await ctx.response.defer()
        botmember = await ctx.guild.fetch_member(self.bot.user.id)
        if role.position >= botmember.top_role.position:
            embed = Embed(color=Color.red())
            embed.description = "This role is above me"
            await ctx.followup.send(embed=embed)
            return
        await Manage(server=ctx.guild).add_role_reward(role, level)
        embed = Embed(color=Color.random())
        embed.description = (
            "{} will be given to a member if they level up to {}".format(
                role.mention, level
            )
        )
        await ctx.followup.send(embed=embed)

    @role.command(
        name="remove",
        description="Removes a level role reward",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.describe(
        role="Which role should be removed?",
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def _remove(self, ctx: Interaction, role: Role):
        await ctx.response.defer()
        await Manage(server=ctx.guild).remove_role_reward(role)
        embed = Embed(color=Color.random())
        embed.description = "{} has been removed for level role reward".format(
            role.mention
        )
        await ctx.followup.send(embed=embed)

    @role.command(
        name="list", description="Add a level role reward when a user levels up"
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def _list(self, ctx: Interaction):
        await ctx.response.defer()
        roles = Levelling(server=ctx.guild).list_all_roles
        data = []
        for i in roles:
            role = f"<@&{i[1]}>"
            level = i[2]
            data.append(f"Level {level}: {role}\n")
        embed = Embed(color=Color.random())
        embed.description = "".join(data)
        embed.title = "Level Rewards"
        await ctx.followup.send(embed=embed)

    channel_blacklist = Jeanne.Group(name="blacklist-channel", description="...")

    @channel_blacklist.command(
        description="Blacklists a channel for gaining XP",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(channel="Which channel?")
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def add(self, ctx: Interaction, channel: TextChannel) -> None:
        await ctx.response.defer()
        if Levelling(server=ctx.guild).check_xpblacklist_channel(channel) == False:
            await Manage(server=ctx.guild).add_xpblacklist(channel)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="Channel XP blacklisted",
                value=f"{channel.jump_url} has been added to the XP blacklist",
                inline=False,
            )
            await ctx.followup.send(embed=embed)
            return
        embed = Embed(color=Color.red())
        embed.description = f"{channel.jump_url} is already XP blacklisted"
        await ctx.followup.send(embed=embed)

    @channel_blacklist.command(
        description="Unblacklists a channel for gaining XP",
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(channel="Which channel?")
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def remove(self, ctx: Interaction, channel: TextChannel) -> None:
        await ctx.response.defer()
        if Levelling(server=ctx.guild).check_xpblacklist_channel(channel) == False:
            embed = Embed(color=Color.red())
            embed.description = f"{channel.jump_url} is not in the XP blacklisted"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return
        await Manage(server=ctx.guild).remove_blacklist(channel)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Channel XP unblacklisted",
            value=f"{channel.jump_url} has been removed from the XP blacklist",
            inline=False,
        )
        await ctx.followup.send(embed=embed)

    @channel_blacklist.command(
        name="list", description="List all XP blacklisted channels"
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def _list(self, ctx: Interaction) -> None:
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(manage(bot))
    await bot.add_cog(Create_Group(bot))
    await bot.add_cog(Edit_Group(bot))
    await bot.add_cog(Delete_Group(bot))
    await bot.add_cog(Set_Group(bot))
    await bot.add_cog(Rename_Group(bot))
    await bot.add_cog(Command_Group(bot))
    await bot.add_cog(Level_Group(bot))
