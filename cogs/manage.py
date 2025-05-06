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
    is_suspended,
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
from discord.app_commands import locale_str as T
import languages.en.manage as en
import languages.en.manage as fr


class Create_Group(GroupCog, name="create"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("textchannel_name"),
        description=T("textchannel_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        topic=T("topic_parm_desc"),
        category=T("category_parm_desc"),
        slowmode=T("slowmode_parm_desc"),
        nsfw_enabled=T("nsfw_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        topic=T("topic_parm_name"),
        category=T("category_parm_name"),
        slowmode=T("slowmode_parm_name"),
        nsfw_enabled=T("nsfw_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def textchannel(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        topic: Optional[Jeanne.Range[str, 1, 1024]] = None,
        category: Optional[CategoryChannel] = None,
        slowmode: str = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).textchannel(
                ctx, name, topic, category, slowmode, nsfw_enabled
            )
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).textchannel(
                ctx, name, topic, category, slowmode, nsfw_enabled
            )

    @Jeanne.command(
        name=T("voicechannel_name"),
        description=T("voicechannel_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        category=T("category_parm_desc"),
        users=T("users_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        category=T("category_parm_name"),
        users=T("users_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def voicechannel(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 99]] = None,
    ) -> None:
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).voicechannel(
                ctx, name, category, users
            )
        elif ctx.locale.value=="fr":
            await fr.Create_Group(self.bot).voicechannel(
                ctx, name, category, users
            )

    @Jeanne.command(
        name=T("category_name"),
        description=T("category_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(name=T("name_parm_desc"))
    @Jeanne.rename(name=T("name_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def category(self, ctx: Interaction, name: Jeanne.Range[str, 1, 100]):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).category(ctx, name)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).category(ctx, name)

    @Jeanne.command(
        name=T("stagechannel_name"),
        description=T("stagechannel_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        category=T("category_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        category=T("category_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def stagechannel(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 10000]] = None,
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).stagechannel(ctx, name, category, users)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).stagechannel(ctx, name, category, users)

    @Jeanne.command(
        name=T("forum_name"),
        description=T("forum_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        topic=T("topic_parm_desc"),
        category=T("category_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        topic=T("topic_parm_name"),
        category=T("category_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def forum(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        category: Optional[CategoryChannel] = None,
        topic: Optional[bool] = None,
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).forum(ctx, name, category, topic)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).forum(ctx, name, category, topic)

    @Jeanne.command(
        name=T("role_name"),
        description=T("role_description"),
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        color=T("color_parm_desc"),
        hoisted=T("hoisted_parm_desc"),
        mentionable=T("mentionable_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        color=T("color_parm_name"),
        hoisted=T("hoisted_parm_name"),
        mentionable=T("mentionable_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def role(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, None, 100],
        color: Optional[Jeanne.Range[str, None, 6]] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).role(ctx, name, color, hoisted, mentionable)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).role(ctx, name, color, hoisted, mentionable)

    thread_group = Jeanne.Group(name="thread", description="...")

    @thread_group.command(
        name=T("public_thread_name"),
        description=T("public_thread_description"),
        extras={
            "bot_perms": "Create Public Threads\nManage Threads",
            "member_perms": "Create Public Threads",
        },
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        channel=T("channel_parm_desc"),
        message_id=T("message_id_parm_desc"),
        slowmode=T("slowmode_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        channel=T("channel_parm_name"),
        message_id=T("message_id_parm_name"),
        slowmode=T("slowmode_parm_name"),
    )
    @Jeanne.checks.has_permissions(
        create_public_threads=True,
    )
    @Jeanne.checks.bot_has_permissions(create_public_threads=True, manage_threads=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def public(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        channel: TextChannel,
        message_id: str,
        slowmode: Optional[str] = None,
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).public(ctx, name, channel, message_id, slowmode)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).public(ctx, name, channel, message_id, slowmode)

    @public.error
    async def public_thread_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, NotFound
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).public_thread_error(ctx, error, "NotFound")
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).public_thread_error(ctx, error, "NotFound") 
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).public_thread_error(ctx, error, "Failed")
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).public_thread_error(ctx, error, "Failed")
            

    @thread_group.command(
        name=T("private_thread_name"),
        description=T("private_thread_description"),
        extras={
            "bot_perms": "Create Private Threads\nManage Threads",
            "member_perms": "Create Private Threads",
        },
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        channel=T("channel_parm_desc"),
        slowmode=T("slowmode_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        channel=T("channel_parm_name"),
        slowmode=T("slowmode_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(create_private_threads=True)
    @Jeanne.checks.has_permissions(create_private_threads=True, manage_threads=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def private(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        channel: TextChannel,
        slowmode: Optional[str] = None,
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).private(ctx, name, channel, slowmode)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).private(ctx, name, channel, slowmode)

    @private.error
    async def private_thread_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).private_thread_error(ctx)
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).private_thread_error(ctx)

    @Jeanne.command(
        name=T("emoji_name"),
        description=T("emoji_description"),
        extras={
            "bot_perms": "Manage Expressions, Create Expressions",
            "member_perms": "Manage Expressions,Create Expressions",
        },
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        emoji_link=T("emoji_link_parm_desc"),
        emoji_image=T("emoji_image_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        emoji_link=T("emoji_link_parm_name"),
        emoji_image=T("emoji_image_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True, create_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True, create_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def emoji(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 2, 30],
        emoji_link: Optional[str] = None,
        emoji_image: Optional[Attachment] = None,
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).emoji(ctx, name, emoji_link, emoji_image)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).emoji(ctx, name, emoji_link, emoji_image)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandInvokeError):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).emoji_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).emoji_error(ctx, error)

    @Jeanne.command(
        name=T("sticker_name"),
        description=T("sticker_description"),
        extras={
            "bot_perms": "Manage Expressions, Create Expressions",
            "member_perms": "Manage Expressions,Create Expressions",
        },
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        emoji=T("emoji_parm_desc"),
        sticker_link=T("sticker_link_parm_desc"),
        sticker_image=T("sticker_image_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        emoji=T("emoji_parm_name"),
        sticker_link=T("sticker_link_parm_name"),
        sticker_image=T("sticker_image_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def sticker(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 2, 30],
        emoji: str,
        sticker_link: Optional[str] = None,
        sticker_image: Optional[Attachment] = None,
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Create_Group(self.bot).sticker(ctx, name, emoji, sticker_link, sticker_image)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).sticker(ctx, name, emoji, sticker_link, sticker_image)

    @sticker.error
    async def sticker_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
        if isinstance(error, Jeanne.errors.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).sticker_error(ctx)
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).sticker_error(ctx)


class Delete_Group(GroupCog, name="delete"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("delete_channel_name"),
        description=T("delete_channel_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(channel=T("channel_parm_desc"))
    @Jeanne.rename(channel=T("channel_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def channel(self, ctx: Interaction, channel: abc.GuildChannel):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).channel(ctx, channel)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).channel(ctx, channel)

    @Jeanne.command(
        name=T("delete_role_name"),
        description=T("delete_role_description"),
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(role=T("role_parm_desc"))
    @Jeanne.rename(role=T("role_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def role(self, ctx: Interaction, role: Role):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).role(ctx, role)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).role(ctx, role)

    @Jeanne.command(
        name=T("delete_emoji_name"),
        description=T("delete_emoji_description"),
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(emoji=T("emoji_parm_desc"))
    @Jeanne.rename(emoji=T("emoji_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def emoji(self, ctx: Interaction, emoji: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).emoji(ctx, emoji)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).emoji(ctx, emoji)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).emoji_error(ctx)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).emoji_error(ctx)

    @Jeanne.command(
        name=T("delete_sticker_name"),
        description=T("delete_sticker_description"),
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(sticker=T("sticker_parm_desc"))
    @Jeanne.rename(sticker=T("sticker_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def sticker(self, ctx: Interaction, sticker: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).sticker(ctx, sticker)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).sticker(ctx, sticker)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).sticker_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).sticker_error(ctx, error)


class Edit_Group(GroupCog, name="edit"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("edit_textchannel_name"),
        description=T("edit_textchannel_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        channel=T("channel_parm_desc"),
        name=T("name_parm_desc"),
        topic=T("topic_parm_desc"),
        slowmode=T("slowmode_parm_desc"),
        category=T("category_parm_desc"),
        nsfw_enabled=T("nsfw_parm_desc"),
    )
    @Jeanne.rename(
        channel=T("channel_parm_name"),
        name=T("name_parm_name"),
        topic=T("topic_parm_name"),
        slowmode=T("slowmode_parm_name"),
        category=T("category_parm_name"),
        nsfw_enabled=T("nsfw_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Edit_Group(self.bot).textchannel(
                ctx, channel, name, topic, slowmode, category, nsfw_enabled
            )
        elif ctx.locale.value == "fr":
            await fr.Edit_Group(self.bot).textchannel(
                ctx, channel, name, topic, slowmode, category, nsfw_enabled
            )

    @Jeanne.command(
        name=T("edit_voicechannel_name"),
        description=T("edit_voicechannel_description"),
        extras={"bot_perms": "Manage Channels", "member_perms": "Manage Channels"},
    )
    @Jeanne.describe(
        channel=T("channel_parm_desc"),
        name=T("name_parm_desc"),
        category=T("category_parm_desc"),
        users=T("users_parm_desc"),
    )
    @Jeanne.rename(
        channel=T("channel_parm_name"),
        name=T("name_parm_name"),
        category=T("category_parm_name"),
        users=T("users_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def voicechannel(
        self,
        ctx: Interaction,
        channel: Optional[VoiceChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 99]] = None,
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Edit_Group(self.bot).voicechannel(ctx, channel, name, category, users)
        elif ctx.locale.value == "fr":
            await fr.Edit_Group(self.bot).voicechannel(ctx, channel, name, category, users)

    @Jeanne.command(
        name=T("edit_role_name"),
        description=T("edit_role_description"),
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        role=T("role_parm_desc"),
        name=T("name_parm_desc"),
        color=T("color_parm_desc"),
        hoisted=T("hoisted_parm_desc"),
        mentionable=T("mentionable_parm_desc"),
    )
    @Jeanne.rename(
        role=T("role_parm_name"),
        name=T("name_parm_name"),
        color=T("color_parm_name"),
        hoisted=T("hoisted_parm_name"),
        mentionable=T("mentionable_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def role(
        self,
        ctx: Interaction,
        role: Role,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        color: Optional[Jeanne.Range[str, None, 6]] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Edit_Group(self.bot).role(ctx, role, name, color, hoisted, mentionable)
        elif ctx.locale.value == "fr":
            await fr.Edit_Group(self.bot).role(ctx, role, name, color, hoisted, mentionable)

    @Jeanne.command(
        name=T("edit_server_name"),
        description=T("edit_server_description"),
        extras={"bot_perms": "Manage Server", "member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        name=T("name_parm_desc"),
        description=T("description_parm_desc"),
        avatar=T("avatar_parm_desc"),
        splash=T("splash_parm_desc"),
        banner=T("banner_parm_desc"),
        verification_level=T("verification_level_parm_desc"),
    )
    @Jeanne.rename(
        name=T("name_parm_name"),
        description=T("description_parm_name"),
        avatar=T("avatar_parm_name"),
        splash=T("splash_parm_name"),
        banner=T("banner_parm_name"),
        verification_level=T("verification_level_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Edit_Group(self.bot).server(
                ctx, name, description, avatar, splash, banner, verification_level
            )
        elif ctx.locale.value == "fr":
            await fr.Edit_Group(self.bot).server(
                ctx, name, description, avatar, splash, banner, verification_level
            )


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
        name=T("set_welcomer_name"),
        description=T("set_welcomer_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        welcoming_channel=T("welcoming_channel_parm_desc"),
        leaving_channel=T("leaving_channel_parm_desc"),
    )
    @Jeanne.rename(
        welcoming_channel=T("welcoming_channel_parm_name"),
        leaving_channel=T("leaving_channel_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def welcomer(
        self,
        ctx: Interaction,
        welcoming_channel: Optional[TextChannel] = None,
        leaving_channel: Optional[TextChannel] = None,
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).welcomer(ctx, welcoming_channel, leaving_channel)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).welcomer(ctx, welcoming_channel, leaving_channel)

    @Jeanne.command(
        name=T("set_modlog_name"),
        description=T("set_modlog_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(channel=T("channel_parm_desc"))
    @Jeanne.rename(channel=T("channel_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def modlog(self, ctx: Interaction, channel: TextChannel):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).modlog(ctx, channel)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).modlog(ctx, channel)

    @Jeanne.command(
        name=T("set_welcomingmsg_name"),
        description=T("set_welcomingmsg_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(jsonfile=T("jsonfile_parm_desc"))
    @Jeanne.rename(jsonfile=T("jsonfile_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def welcomingmsg(
        self, ctx: Interaction, jsonfile: Optional[Attachment] = None
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).welcomingmsg(ctx, jsonfile)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).welcomingmsg(ctx, jsonfile)

    @Jeanne.command(
        name=T("set_leavingmsg_name"),
        description=T("set_leavingmsg_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(jsonfile=T("jsonfile_parm_desc"))
    @Jeanne.rename(jsonfile=T("jsonfile_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def leavingmsg(
        self, ctx: Interaction, jsonfile: Optional[Attachment] = None
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).leavingmsg(ctx, jsonfile)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).leavingmsg(ctx, jsonfile)

    @Jeanne.command(
        name=T("set_rolereward_message_name"),
        description=T("set_rolereward_message_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(message=T("message_parm_desc"))
    @Jeanne.rename(message=T("message_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def rolereward_message(
        self, ctx: Interaction, message: Optional[bool] = None
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).rolereward_message(ctx, message)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).rolereward_message(ctx, message)

    @Jeanne.command(
        name=T("set_levelupdate_name"),
        description=T("set_levelupdate_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        channel=T("channel_parm_desc"),
        levelmsg=T("levelmsg_parm_desc"),
    )
    @Jeanne.rename(
        channel=T("channel_parm_name"),
        levelmsg=T("levelmsg_parm_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def levelupdate(
        self, ctx: Interaction, channel: TextChannel, levelmsg: Optional[bool] = None
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).levelupdate(ctx, channel, levelmsg)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).levelupdate(ctx, channel, levelmsg)

    @Jeanne.command(
        name=T("set_confessionchannel_name"),
        description=T("set_confessionchannel_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(channel=T("channel_parm_desc"))
    @Jeanne.rename(channel=T("channel_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def confessionchannel(self, ctx: Interaction, channel: TextChannel) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).confessionchannel(ctx, channel)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).confessionchannel(ctx, channel)

    @Jeanne.command(
        name=T("set_brightness_name"),
        description=T("set_brightness_description"),
    )
    @Jeanne.describe(brightness=T("brightness_parm_desc"))
    @Jeanne.rename(brightness=T("brightness_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def brightness(
        self, ctx: Interaction, brightness: Jeanne.Range[int, 10, 150]
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).brightness(ctx, brightness)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).brightness(ctx, brightness)

    @Jeanne.command(
        name=T("set_bio_name"),
        description=T("set_bio_description"),
    )
    @Jeanne.describe(bio=T("bio_parm_desc"))
    @Jeanne.rename(bio=T("bio_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def bio(self, ctx: Interaction, bio: Jeanne.Range[str, 1, 120]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).bio(ctx, bio)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).bio(ctx, bio)

    @Jeanne.command(
        name=T("set_color_name"),
        description=T("set_color_description"),
    )
    @Jeanne.describe(color=T("color_parm_desc"))
    @Jeanne.rename(color=T("color_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def color(self, ctx: Interaction, color: Jeanne.Range[str, 1]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Set_Group(self.bot).color(ctx, color)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).color(ctx, color)


class manage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name=T("add_role_name"),
        description=T("add_role_description"),
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        member=T("add_role_member_desc"),
        role=T("add_role_role_desc"),
    )
    @Jeanne.rename(
        member=T("add_role_member_name"),
        role=T("add_role_role_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def addrole(self, ctx: Interaction, member: User, role: Role):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.manage(self.bot).addrole(ctx, member, role)
        elif ctx.locale.value == "fr":
            await fr.manage(self.bot).addrole(ctx, member, role)

    @Jeanne.command(
        name=T("remove_role_name"),
        description=T("remove_role_description"),
        extras={"bot_perms": "Manage Roles", "member_perms": "Manage Roles"},
    )
    @Jeanne.describe(
        member=T("remove_role_member_desc"),
        role=T("remove_role_role_desc"),
    )
    @Jeanne.rename(
        member=T("remove_role_member_name"),
        role=T("remove_role_role_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_roles=True)
    @Jeanne.checks.has_permissions(manage_roles=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def removerole(self, ctx: Interaction, member: User, role: Role):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.manage(self.bot).removerole(ctx, member, role)
        elif ctx.locale.value == "fr":
            await fr.manage(self.bot).removerole(ctx, member, role)

    @Jeanne.command(
        name=T("remove_name"),
        description=T("remove_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.checks.bot_has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def remove(self, ctx: Interaction) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.manage(self.bot).remove(ctx)
        elif ctx.locale.value == "fr":
            await fr.manage(self.bot).remove(ctx)

    @Jeanne.command(
        name=T("clone_name"),
        description=T("clone_description"),
        extras={"bot_perms": "Manage Channel", "member_perms": "Manage Channel"},
    )
    @Jeanne.describe(
        channel=T("clone_channel_desc"),
        name=T("clone_name_desc"),
    )
    @Jeanne.rename(
        channel=T("clone_channel_name"),
        name=T("clone_name_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def clone(
        self,
        ctx: Interaction,
        channel: Optional[abc.GuildChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.manage(self.bot).clone(ctx, channel, name, category, nsfw_enabled)
        elif ctx.locale.value == "fr":
            await fr.manage(self.bot).clone(ctx, channel, name, category, nsfw_enabled)


class Rename_Group(GroupCog, name="rename"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("rename_emoji_name"),
        description=T("rename_emoji_description"),
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(
        emoji=T("rename_emoji_emoji_desc"),
        name=T("rename_emoji_name_desc"),
    )
    @Jeanne.rename(
        emoji=T("rename_emoji_emoji_name"),
        name=T("rename_emoji_name_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def emoji(self, ctx: Interaction, emoji: str, name: Jeanne.Range[str, 2, 30]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Rename_Group(self.bot).emoji(ctx, emoji, name)
        elif ctx.locale.value == "fr":
            await fr.Rename_Group(self.bot).emoji(ctx, emoji, name)

    @Jeanne.command(
        name=T("rename_category_name"),
        description=T("rename_category_description"),
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
        },
    )
    @Jeanne.describe(
        category=T("rename_category_category_desc"),
        name=T("rename_category_name_desc"),
    )
    @Jeanne.rename(
        category=T("rename_category_category_name"),
        name=T("rename_category_name_name"),
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    @Jeanne.checks.bot_has_permissions(manage_channels=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def category(
        self,
        ctx: Interaction,
        category: CategoryChannel,
        name: Jeanne.Range[str, 1, 100],
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Rename_Group(self.bot).category(ctx, category, name)
        elif ctx.locale.value == "fr":
            await fr.Rename_Group(self.bot).category(ctx, category, name)

    @Jeanne.command(
        name=T("rename_sticker_name"),
        description=T("rename_sticker_description"),
        extras={
            "bot_perms": "Manage Expressions",
            "member_perms": "Manage Expressions",
        },
    )
    @Jeanne.describe(
        sticker=T("rename_sticker_sticker_desc"),
        name=T("rename_sticker_name_desc"),
    )
    @Jeanne.rename(
        sticker=T("rename_sticker_sticker_name"),
        name=T("rename_sticker_name_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def sticker(
        self, ctx: Interaction, sticker: str, name: Jeanne.Range[str, 2, 30]
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Rename_Group(self.bot).sticker(ctx, sticker, name)
        elif ctx.locale.value == "fr":
            await fr.Rename_Group(self.bot).sticker(ctx, sticker, name)


class Command_Group(GroupCog, name="command"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("disable_command_name"),
        description=T("disable_command_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.autocomplete(command=AutoCompleteChoices.command_choices)
    @Jeanne.describe(command=T("disable_command_param_desc"))
    @Jeanne.rename(command=T("disable_command_param_name"))
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def _disable(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Command_Group(self.bot)._disable(ctx, command)
        elif ctx.locale.value == "fr":
            await fr.Command_Group(self.bot)._disable(ctx, command)

    @Jeanne.command(
        name=T("enable_command_name"),
        description=T("enable_command_description"),
    )
    @Jeanne.autocomplete(command=AutoCompleteChoices.disabled_commands)
    @Jeanne.describe(command=T("enable_command_param_desc"))
    @Jeanne.rename(command=T("enable_command_param_name"))
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def _enable(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Command_Group(self.bot)._enable(ctx, command)
        elif ctx.locale.value == "fr":
            await fr.Command_Group(self.bot)._enable(ctx, command)

    @Jeanne.command(
        name=T("list_disabled_commands_name"),
        description=T("list_disabled_commands_description"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def listdisabled(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Command_Group(self.bot).listdisabled(ctx)
        elif ctx.locale.value == "fr":
            await fr.Command_Group(self.bot).listdisabled(ctx)


class Level_Group(GroupCog, name="level"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    role = Jeanne.Group(name=T("role_reward_group_name"), description=T("role_reward_group_description"))

    @role.command(
        name=T("add_role_reward_name"),
        description=T("add_role_reward_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(
        role=T("add_role_reward_role_desc"),
        level=T("add_role_reward_level_desc"),
    )
    @Jeanne.rename(
        role=T("add_role_reward_role_name"),
        level=T("add_role_reward_level_name"),
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _add(self, ctx: Interaction, role: Role, level: Jeanne.Range[int, 1]):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot)._add(ctx, role, level)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot)._add(ctx, role, level)

    @role.command(
        name=T("remove_role_reward_name"),
        description=T("remove_role_reward_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(role=T("remove_role_reward_role_desc"))
    @Jeanne.rename(role=T("remove_role_reward_role_name"))
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _remove(self, ctx: Interaction, role: Role):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot)._remove(ctx, role)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot)._remove(ctx, role)

    @role.command(
        name=T("list_role_rewards_name"),
        description=T("list_role_rewards_description"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _list(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot)._list(ctx)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot)._list(ctx)

    channel_blacklist = Jeanne.Group(name=T("blacklist_channel_group_name"), description=T("blacklist_channel_group_description"))

    @channel_blacklist.command(
        name=T("add_blacklist_channel_name"),
        description=T("add_blacklist_channel_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(channel=T("add_blacklist_channel_channel_desc"))
    @Jeanne.rename(channel=T("add_blacklist_channel_channel_name"))
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def add(self, ctx: Interaction, channel: TextChannel) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot).add(ctx, channel)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot).add(ctx, channel)

    @channel_blacklist.command(
        name=T("remove_blacklist_channel_name"),
        description=T("remove_blacklist_channel_description"),
        extras={"member_perms": "Manage Server"},
    )
    @Jeanne.describe(channel=T("remove_blacklist_channel_channel_desc"))
    @Jeanne.rename(channel=T("remove_blacklist_channel_channel_name"))
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def remove(self, ctx: Interaction, channel: TextChannel) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot).remove(ctx, channel)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot).remove(ctx, channel)

    @channel_blacklist.command(
        name=T("list_blacklist_channels_name"),
        description=T("list_blacklist_channels_description"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _list(self, ctx: Interaction) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot)._list(ctx)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot)._list(ctx)


async def setup(bot: Bot):
    await bot.add_cog(manage(bot))
    await bot.add_cog(Create_Group(bot))
    await bot.add_cog(Edit_Group(bot))
    await bot.add_cog(Delete_Group(bot))
    await bot.add_cog(Set_Group(bot))
    await bot.add_cog(Rename_Group(bot))
    await bot.add_cog(Command_Group(bot))
    await bot.add_cog(Level_Group(bot))
