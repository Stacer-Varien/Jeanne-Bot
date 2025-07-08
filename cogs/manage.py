from typing import Optional
from discord import (
    Attachment,
    CategoryChannel,
    HTTPException,
    Interaction,
    User,
    NotFound,
    Role,
    TextChannel,
    VerificationLevel,
    VoiceChannel,
    app_commands as Jeanne,
    abc,
)
from discord.ext.commands import Bot, Cog, GroupCog
from functions import (
    AutoCompleteChoices,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from discord.app_commands import locale_str as T
import languages.en.manage as en
import languages.en.manage as fr


class Create_Group(GroupCog, name=T("create_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("textchannel_name"),
        description=T("textchannel_description"),
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Create Text Channel",
                "description": "Create a text channel",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": False,
                    },
                    {
                        "name": "Topic",
                        "description": "What is the channel topic?",
                        "required": False,
                    },
                    {
                        "name": "category",
                        "description": "Place in which category?",
                        "required": False,
                    },
                    {
                        "name": "slowmode",
                        "description": "What is the slowmode (1h, 30m, etc) (Max is 6 hours)",
                        "required": False,
                    },
                    {
                        "name": "nsfw_enabled",
                        "description": "Should it be an NSFW channel?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "Créer un salon textuel",
                "description": "Créer un salon textuel",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment le nommer ?",
                        "required": False,
                    },
                    {
                        "name": "Sujet",
                        "description": "Quel est le sujet du salon ?",
                        "required": False,
                    },
                    {
                        "name": "catégorie",
                        "description": "Dans quelle catégorie ?",
                        "required": False,
                    },
                    {
                        "name": "slowmode",
                        "description": "Quel est le mode lent (1h, 30m, etc) (Max 6 heures)",
                        "required": False,
                    },
                    {
                        "name": "nsfw_enabled",
                        "description": "Doit-il être un salon NSFW ?",
                        "required": False,
                    },
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Create Voice Channel",
                "description": "Create a voice channel",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": False,
                    },
                    {
                        "name": "category",
                        "description": "Place in which category?",
                        "required": False,
                    },
                    {
                        "name": "users",
                        "description": "How many users can join? (Max 99)",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "Créer un salon textuel",
                "description": "Créer un salon textuel",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment le nommer ?",
                        "required": False,
                    },
                    {
                        "name": "catégorie",
                        "description": "Dans quelle catégorie ?",
                        "required": False,
                    },
                    {
                        "name": "utilisateurs",
                        "description": "Combien d'utilisateurs peuvent rejoindre ? (Max 99)",
                        "required": False,
                    },
                ],
            },
        },
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
            await en.Create_Group(self.bot).voicechannel(ctx, name, category, users)
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).voicechannel(ctx, name, category, users)

    @Jeanne.command(
        name=T("category_name"),
        description=T("category_description"),
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Create Category",
                "description": "Create a category",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Créer une catégorie",
                "description": "Créer une catégorie",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment la nommer ?",
                        "required": True,
                    },
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Create Stage Channel",
                "description": "Create a stage channel",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": True,
                    },
                    {
                        "name": "category",
                        "description": "Place in which category?",
                        "required": False,
                    },
                    {
                        "name": "users",
                        "description": "How many users can join? (Max 10000)",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "Créer un salon de scène",
                "description": "Créer un salon de scène",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment le nommer ?",
                        "required": True,
                    },
                    {
                        "name": "catégorie",
                        "description": "Dans quelle catégorie ?",
                        "required": False,
                    },
                    {
                        "name": "utilisateurs",
                        "description": "Combien d'utilisateurs peuvent rejoindre ? (Max 10000)",
                        "required": False,
                    },
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Create Forum Channel",
                "description": "Create a forum channel",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": True,
                    },
                    {
                        "name": "Topic",
                        "description": "What is the channel topic?",
                        "required": False,
                    },
                    {
                        "name": "category",
                        "description": "Place in which category?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "Créer un salon forum",
                "description": "Créer un salon forum",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment le nommer ?",
                        "required": True,
                    },
                    {
                        "name": "Sujet",
                        "description": "Quel est le sujet du salon ?",
                        "required": False,
                    },
                    {
                        "name": "catégorie",
                        "description": "Dans quelle catégorie ?",
                        "required": False,
                    },
                ],
            },
        },
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
            "en": {
                "name": "Create Public Thread",
                "description": "Create a public thread",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name the thread?",
                        "required": True,
                    },
                    {
                        "name": "Channel",
                        "description": "Which channel to create the thread in?",
                        "required": True,
                    },
                    {
                        "name": "Message ID",
                        "description": "ID of the message to start the thread from",
                        "required": True,
                    },
                    {
                        "name": "Slowmode",
                        "description": "What is the slowmode (optional)?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "Créer un fil public",
                "description": "Créer un fil public",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment nommer le fil ?",
                        "required": True,
                    },
                    {
                        "name": "Cannel",
                        "description": "Dans quel cannel créer le fil ?",
                        "required": True,
                    },
                    {
                        "name": "Message ID",
                        "description": "ID du message pour démarrer le fil",
                        "required": True,
                    },
                    {
                        "name": "Slowmode",
                        "description": "Quel est le mode lent (optionnel) ?",
                        "required": False,
                    },
                ],
            },
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
            await en.Create_Group(self.bot).public(
                ctx, name, channel, message_id, slowmode
            )
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).public(
                ctx, name, channel, message_id, slowmode
            )

    @public.error
    async def public_thread_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, NotFound
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).public_thread_error(
                    ctx, error, "NotFound"
                )
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).public_thread_error(
                    ctx, error, "NotFound"
                )
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, HTTPException
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Create_Group(self.bot).public_thread_error(
                    ctx, error, "Failed"
                )
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).public_thread_error(
                    ctx, error, "Failed"
                )

    @thread_group.command(
        name=T("private_thread_name"),
        description=T("private_thread_description"),
        extras={
            "bot_perms": "Create Private Threads\nManage Threads",
            "member_perms": "Create Private Threads",
            "en": {
                "name": "Create Private Thread",
                "description": "Create a private thread",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name the thread?",
                        "required": True,
                    },
                    {
                        "name": "Channel",
                        "description": "Which channel to create the thread in?",
                        "required": True,
                    },
                    {
                        "name": "Slowmode",
                        "description": "What is the slowmode (optional)?",
                        "required": False,
                    },
                ],
            },
            "fr": {
                "name": "Créer un fil privé",
                "description": "Créer un fil privé",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment nommer le fil ?",
                        "required": True,
                    },
                    {
                        "name": "Salon",
                        "description": "Dans quel salon créer le fil ?",
                        "required": True,
                    },
                    {
                        "name": "Mode lent",
                        "description": "Quel est le mode lent (optionnel) ?",
                        "required": False,
                    },
                ],
            },
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
            if ctx.locale.value == "en-GB" or ctx.local.value == "en-US":
                await en.Create_Group(self.bot).private_thread_error(ctx)
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).private_thread_error(ctx)

    @Jeanne.command(
        name=T("emoji_name"),
        description=T("emoji_description"),
        extras={
            "bot_perms": "Manage Expressions, Create Expressions",
            "member_perms": "Manage Expressions,Create Expressions",
            "en": {
                "name": "Create Emoji",
                "description": "Create a custom emoji",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": True,
                    },
                    {
                        "name": "Link",
                        "description": "The link to the emoji image",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Créer emoji",
                "description": "Créer un emoji personnalisé",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment le nommer ?",
                        "required": True,
                    },
                    {
                        "name": "Lien",
                        "description": "Le lien vers l'image de l'emoji",
                        "required": True,
                    },
                ],
            },
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
            if ctx.locale.value == "en-GB" or ctx.local.value == "en-US":
                await en.Create_Group(self.bot).emoji_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Create_Group(self.bot).emoji_error(ctx, error)

    @Jeanne.command(
        name=T("sticker_name"),
        description=T("sticker_description"),
        extras={
            "bot_perms": "Manage Expressions, Create Expressions",
            "member_perms": "Manage Expressions,Create Expressions",
            "en": {
                "name": "Create Sticker",
                "description": "Create a custom sticker",
                "parameters": [
                    {
                        "name": "Name",
                        "description": "What will you name it?",
                        "required": True,
                    },
                    {
                        "name": "Emoji",
                        "description": "The emoji to use for the sticker",
                        "required": True,
                    },
                    {
                        "name": "Link",
                        "description": "The link to the sticker image",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Créer sticker",
                "description": "Créer un autocollant personnalisé",
                "parameters": [
                    {
                        "name": "Nom",
                        "description": "Comment le nommer ?",
                        "required": True,
                    },
                    {
                        "name": "Emoji",
                        "description": "L'emoji à utiliser pour l'autocollant",
                        "required": True,
                    },
                    {
                        "name": "Lien",
                        "description": "Le lien vers l'image de l'autocollant",
                        "required": True,
                    },
                ],
            },
        }
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
            await en.Create_Group(self.bot).sticker(
                ctx, name, emoji, sticker_link, sticker_image
            )
        elif ctx.locale.value == "fr":
            await fr.Create_Group(self.bot).sticker(
                ctx, name, emoji, sticker_link, sticker_image
            )

    @sticker.error
    async def sticker_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Delete_Group(self.bot).sticker_error(ctx)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).sticker_error(ctx)


class Delete_Group(GroupCog, name=T("delete_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("delete_channel_name"),
        description=T("delete_channel_description"),
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Delete Channel",
                "description": "Delete a channel",
                "parameters": [
                    {
                        "name": "Channel",
                        "description": "Which channel to delete?",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Supprimer emoji",
                "description": "Supprimer un salon",
                "parameters": [
                    {
                        "name": "Emoji",
                        "description": "Quel salon supprimer ?",
                        "required": True,
                    },
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Roles",
            "member_perms": "Manage Roles",
            "en": {
                "name": "Delete Role",
                "description": "Delete a role",
                "parameters": [
                    {
                        "name": "Role",
                        "description": "Which role to delete?",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Supprimer un rôle",
                "description": "Supprimer un rôle",
                "parameters": [
                    {
                        "name": "Rôle",
                        "description": "Quel rôle supprimer ?",
                        "required": True,
                    },
                ],
            },
        },
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
            "en": {
                "name": "Delete Emoji",
                "description": "Delete a custom emoji",
                "parameters": [
                    {
                        "name": "Emoji",
                        "description": "Which emoji to delete?",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Supprimer un emoji",
                "description": "Supprimer un emoji personnalisé",
                "parameters": [
                    {
                        "name": "Emoji",
                        "description": "Quel emoji supprimer ?",
                        "required": True,
                    },
                ],
            },
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
            "en": {
                "name": "Delete Sticker",
                "description": "Delete a custom sticker",
                "parameters": [
                    {
                        "name": "Sticker",
                        "description": "Which sticker to delete?",
                        "required": True,
                    },
                ],
            },
            "fr": {
                "name": "Supprimer un sticker",
                "description": "Supprimer un autocollant personnalisé",
                "parameters": [
                    {
                        "name": "Sticker",
                        "description": "Quel sticker supprimer ?",
                        "required": True,
                    },
                ],
            },
        }
    )
    @Jeanne.describe(sticker=T("sticker_parm_desc"))
    @Jeanne.rename(sticker=T("sticker_parm_name"))
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def sticker(
        self, ctx: Interaction, sticker: str, name: Jeanne.Range[str, 2, 30]
    ):
        if ctx.local.value == "en-GB" or ctx.local.value == "en-US":
            await en.Delete_Group(self.bot).sticker(ctx, sticker, name)
        elif ctx.locale.value == "fr":
            await fr.Delete_Group(self.bot).sticker(ctx, sticker, name)


class Edit_Group(GroupCog, name="edit"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("edit_textchannel_name"),
        description=T("edit_textchannel_description"),
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Edit Text Channel",
                "description": "Edit a text channel",
                "parameters": [
                    {"name": "Channel", "description": "Which channel to edit?", "required": True},
                    {"name": "Name", "description": "New name for the channel", "required": False},
                    {"name": "Topic", "description": "New topic for the channel", "required": False},
                    {"name": "Slowmode", "description": "New slowmode (optional)", "required": False},
                    {"name": "Category", "description": "Move to which category?", "required": False},
                    {"name": "NSFW", "description": "Set as NSFW?", "required": False},
                ],
            },
            "fr": {
                "name": "Modifier salon textuel",
                "description": "Modifier un salon textuel",
                "parameters": [
                    {"name": "Salon", "description": "Quel salon modifier ?", "required": True},
                    {"name": "Nom", "description": "Nouveau nom du salon", "required": False},
                    {"name": "Sujet", "description": "Nouveau sujet du salon", "required": False},
                    {"name": "Slowmode", "description": "Nouveau mode lent (optionnel)", "required": False},
                    {"name": "Catégorie", "description": "Déplacer dans quelle catégorie ?", "required": False},
                    {"name": "NSFW", "description": "Définir comme NSFW ?", "required": False},
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Channels",
            "member_perms": "Manage Channels",
            "en": {
                "name": "Edit Voice Channel",
                "description": "Edit a voice channel",
                "parameters": [
                    {"name": "Channel", "description": "Which channel to edit?", "required": True},
                    {"name": "Name", "description": "New name for the channel", "required": False},
                    {"name": "Category", "description": "Move to which category?", "required": False},
                    {"name": "Users", "description": "User limit (optional)", "required": False},
                ],
            },
            "fr": {
                "name": "Modifier salon vocal",
                "description": "Modifier un salon vocal",
                "parameters": [
                    {"name": "Salon", "description": "Quel salon modifier ?", "required": True},
                    {"name": "Nom", "description": "Nouveau nom du salon", "required": False},
                    {"name": "Catégorie", "description": "Déplacer dans quelle catégorie ?", "required": False},
                    {"name": "Utilisateurs", "description": "Limite d'utilisateurs (optionnel)", "required": False},
                ],
            },
        },
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
            await en.Edit_Group(self.bot).voicechannel(
                ctx, channel, name, category, users
            )
        elif ctx.locale.value == "fr":
            await fr.Edit_Group(self.bot).voicechannel(
                ctx, channel, name, category, users
            )

    @Jeanne.command(
        name=T("edit_role_name"),
        description=T("edit_role_description"),
        extras={
            "bot_perms": "Manage Roles",
            "member_perms": "Manage Roles",
            "en": {
                "name": "Edit Role",
                "description": "Edit a role",
                "parameters": [
                    {"name": "Role", "description": "Which role to edit?", "required": True},
                    {"name": "Name", "description": "New name for the role", "required": False},
                    {"name": "Color", "description": "New color (hex)", "required": False},
                    {"name": "Hoisted", "description": "Display role separately?", "required": False},
                    {"name": "Mentionable", "description": "Make role mentionable?", "required": False},
                ],
            },
            "fr": {
                "name": "Modifier rôle",
                "description": "Modifier un rôle",
                "parameters": [
                    {"name": "Rôle", "description": "Quel rôle modifier ?", "required": True},
                    {"name": "Nom", "description": "Nouveau nom du rôle", "required": False},
                    {"name": "Couleur", "description": "Nouvelle couleur (hex)", "required": False},
                    {"name": "Séparé", "description": "Afficher séparément ?", "required": False},
                    {"name": "Mentionnable", "description": "Rendre le rôle mentionnable ?", "required": False},
                ],
            },
        },
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
    @Jeanne.checks.has_permissions(manage_roles=True)
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
            await en.Edit_Group(self.bot).role(
                ctx, role, name, color, hoisted, mentionable
            )
        elif ctx.locale.value == "fr":
            await fr.Edit_Group(self.bot).role(
                ctx, role, name, color, hoisted, mentionable
            )

    @Jeanne.command(
        name=T("edit_server_name"),
        description=T("edit_server_description"),
        extras={
            "bot_perms": "Manage Server",
            "member_perms": "Manage Server",
            "en": {
                "name": "Edit Server",
                "description": "Edit server settings",
                "parameters": [
                    {"name": "Name", "description": "New server name", "required": False},
                    {"name": "Description", "description": "New server description", "required": False},
                    {"name": "Avatar", "description": "New server avatar", "required": False},
                    {"name": "Splash", "description": "New splash image", "required": False},
                    {"name": "Banner", "description": "New banner image", "required": False},
                    {"name": "Verification Level", "description": "Set verification level", "required": False},
                ],
            },
            "fr": {
                "name": "Modifier serveur",
                "description": "Modifier les paramètres du serveur",
                "parameters": [
                    {"name": "Nom", "description": "Nouveau nom du serveur", "required": False},
                    {"name": "Description", "description": "Nouvelle description du serveur", "required": False},
                    {"name": "Avatar", "description": "Nouvel avatar du serveur", "required": False},
                    {"name": "Splash", "description": "Nouvelle image splash", "required": False},
                    {"name": "Bannière", "description": "Nouvelle bannière", "required": False},
                    {"name": "Niveau de vérification", "description": "Définir le niveau de vérification", "required": False},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Welcomer",
                "description": "Configure welcome and leave channels",
                "parameters": [
                    {"name": "Welcoming Channel", "description": "Channel for welcome messages", "required": False},
                    {"name": "Leaving Channel", "description": "Channel for leave messages", "required": False},
                ],
            },
            "fr": {
                "name": "Configurer l'accueil",
                "description": "Configurer les salons d'accueil et de départ",
                "parameters": [
                    {"name": "Salon d'accueil", "description": "Salon pour les messages d'accueil", "required": False},
                    {"name": "Salon de départ", "description": "Salon pour les messages de départ", "required": False},
                ],
            },
        },
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
            await en.Set_Group(self.bot).welcomer(
                ctx, welcoming_channel, leaving_channel
            )
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).welcomer(
                ctx, welcoming_channel, leaving_channel
            )

    @Jeanne.command(
        name=T("set_modlog_name"),
        description=T("set_modlog_description"),
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Modlog",
                "description": "Configure moderation log channel",
                "parameters": [
                    {"name": "Channel", "description": "Channel for moderation logs", "required": True},
                ],
            },
            "fr": {
                "name": "Configurer modlog",
                "description": "Configurer le salon de logs de modération",
                "parameters": [
                    {"name": "Salon", "description": "Salon pour les logs de modération", "required": True},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Welcoming Message",
                "description": "Set the welcoming message (JSON file)",
                "parameters": [
                    {"name": "JSON File", "description": "JSON file for welcome message", "required": False},
                ],
            },
            "fr": {
                "name": "Configurer message d'accueil",
                "description": "Définir le message d'accueil (fichier JSON)",
                "parameters": [
                    {"name": "Fichier JSON", "description": "Fichier JSON pour le message d'accueil", "required": False},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Leaving Message",
                "description": "Set the leaving message (JSON file)",
                "parameters": [
                    {"name": "JSON File", "description": "JSON file for leave message", "required": False},
                ],
            },
            "fr": {
                "name": "Configurer message de départ",
                "description": "Définir le message de départ (fichier JSON)",
                "parameters": [
                    {"name": "Fichier JSON", "description": "Fichier JSON pour le message de départ", "required": False},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Role Reward Message",
                "description": "Set the role reward message",
                "parameters": [
                    {"name": "Message", "description": "Enable/disable role reward message", "required": False},
                ],
            },
            "fr": {
                "name": "Configurer message de récompense de rôle",
                "description": "Définir le message de récompense de rôle",
                "parameters": [
                    {"name": "Message", "description": "Activer/désactiver le message de récompense de rôle", "required": False},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Level Update",
                "description": "Set the channel and message for level updates",
                "parameters": [
                    {"name": "Channel", "description": "Channel for level updates", "required": True},
                    {"name": "Level Message", "description": "Enable/disable level message", "required": False},
                ],
            },
            "fr": {
                "name": "Configurer mise à jour de niveau",
                "description": "Définir le salon et le message pour les mises à jour de niveau",
                "parameters": [
                    {"name": "Salon", "description": "Salon pour les mises à jour de niveau", "required": True},
                    {"name": "Message de niveau", "description": "Activer/désactiver le message de niveau", "required": False},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Set Confession Channel",
                "description": "Set the confession channel",
                "parameters": [
                    {"name": "Channel", "description": "Channel for confessions", "required": True},
                ],
            },
            "fr": {
                "name": "Configurer salon de confessions",
                "description": "Définir le salon de confessions",
                "parameters": [
                    {"name": "Salon", "description": "Salon pour les confessions", "required": True},
                ],
            },
        },
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
        extras={
            "en": {
                "name": "Set Brightness",
                "description": "Set the brightness value",
                "parameters": [
                    {"name": "Brightness", "description": "Brightness value (10-150)", "required": True},
                ],
            },
            "fr": {
                "name": "Définir la luminosité",
                "description": "Définir la valeur de luminosité",
                "parameters": [
                    {"name": "Luminosité", "description": "Valeur de luminosité (10-150)", "required": True},
                ],
            },
        },
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
        extras={
            "en": {
                "name": "Set Bio",
                "description": "Set your bio",
                "parameters": [
                    {"name": "Bio", "description": "Your bio text", "required": True},
                ],
            },
            "fr": {
                "name": "Définir la bio",
                "description": "Définir votre bio",
                "parameters": [
                    {"name": "Bio", "description": "Votre texte de bio", "required": True},
                ],
            },
        },
    )
    @Jeanne.describe(bio=T("bio_parm_desc"))
    @Jeanne.rename(bio=T("bio_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def bio(self, ctx: Interaction, bio: Jeanne.Range[str, 1, 120]):
        if ctx.locale.value == "en-GB" or ctx.local.value == "en-US":
            await en.Set_Group(self.bot).bio(ctx, bio)
        elif ctx.locale.value == "fr":
            await fr.Set_Group(self.bot).bio(ctx, bio)

    @Jeanne.command(
        name=T("set_color_name"),
        description=T("set_color_description"),
        extras={
            "en": {
                "name": "Set Color",
                "description": "Set your color",
                "parameters": [
                    {"name": "Color", "description": "Color value (hex or name)", "required": True},
                ],
            },
            "fr": {
                "name": "Définir la couleur",
                "description": "Définir votre couleur",
                "parameters": [
                    {"name": "Couleur", "description": "Valeur de la couleur (hex ou nom)", "required": True},
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Roles",
            "member_perms": "Manage Roles",
            "en": {
                "name": "Add Role",
                "description": "Add a role to a member",
                "parameters": [
                    {"name": "Member", "description": "Member to add the role to", "required": True},
                    {"name": "Role", "description": "Role to add", "required": True},
                ],
            },
            "fr": {
                "name": "Ajouter un rôle",
                "description": "Ajouter un rôle à un membre",
                "parameters": [
                    {"name": "Membre", "description": "Membre à qui ajouter le rôle", "required": True},
                    {"name": "Rôle", "description": "Rôle à ajouter", "required": True},
                ],
            },
        },
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
        extras={
            "bot_perms": "Manage Roles",
            "member_perms": "Manage Roles",
            "en": {
                "name": "Remove Role",
                "description": "Remove a role from a member",
                "parameters": [
                    {"name": "Member", "description": "Member to remove the role from", "required": True},
                    {"name": "Role", "description": "Role to remove", "required": True},
                ],
            },
            "fr": {
                "name": "Retirer un rôle",
                "description": "Retirer un rôle d'un membre",
                "parameters": [
                    {"name": "Membre", "description": "Membre à qui retirer le rôle", "required": True},
                    {"name": "Rôle", "description": "Rôle à retirer", "required": True},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Remove Server Data",
                "description": "Remove all server data",
                "parameters": [],
            },
            "fr": {
                "name": "Supprimer les données du serveur",
                "description": "Supprimer toutes les données du serveur",
                "parameters": [],
            },
        },
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
        extras={
            "bot_perms": "Manage Channel",
            "member_perms": "Manage Channel",
            "en": {
                "name": "Clone Channel",
                "description": "Clone a channel",
                "parameters": [
                    {"name": "Channel", "description": "Channel to clone", "required": False},
                    {"name": "Name", "description": "Name for the new channel", "required": False},
                    {"name": "Category", "description": "Category for the new channel", "required": False},
                    {"name": "NSFW", "description": "Set as NSFW?", "required": False},
                ],
            },
            "fr": {
                "name": "Cloner un salon",
                "description": "Cloner un salon",
                "parameters": [
                    {"name": "Salon", "description": "Salon à cloner", "required": False},
                    {"name": "Nom", "description": "Nom du nouveau salon", "required": False},
                    {"name": "Catégorie", "description": "Catégorie du nouveau salon", "required": False},
                    {"name": "NSFW", "description": "Définir comme NSFW ?", "required": False},
                ],
            },
        },
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
            "en": {
                "name": "Rename Emoji",
                "description": "Rename a custom emoji",
                "parameters": [
                    {"name": "Emoji", "description": "Emoji to rename", "required": True},
                    {"name": "Name", "description": "New name for the emoji", "required": True},
                ],
            },
            "fr": {
                "name": "Renommer un emoji",
                "description": "Renommer un emoji personnalisé",
                "parameters": [
                    {"name": "Emoji", "description": "Emoji à renommer", "required": True},
                    {"name": "Nom", "description": "Nouveau nom de l'emoji", "required": True},
                ],
            },
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
    @Jeanne.rename(
        emoji=T("rename_emoji_emoji_name"),
        name=T("rename_emoji_name_name"),
    )
    @Jeanne.checks.bot_has_permissions(manage_expressions=True)
    @Jeanne.checks.has_permissions(manage_expressions=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def emoji(self, ctx: Interaction, emoji: str, name: Jeanne.Range[str, 2, 30]
    ):
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
            "en": {
                "name": "Rename Category",
                "description": "Rename a category",
                "parameters": [
                    {"name": "Category", "description": "Category to rename", "required": True},
                    {"name": "Name", "description": "New name for the category", "required": True},
                ],
            },
            "fr": {
                "name": "Renommer une catégorie",
                "description": "Renommer une catégorie",
                "parameters": [
                    {"name": "Catégorie", "description": "Catégorie à renommer", "required": True},
                    {"name": "Nom", "description": "Nouveau nom de la catégorie", "required": True},
                ],
            },
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
            "en": {
                "name": "Rename Sticker",
                "description": "Rename a custom sticker",
                "parameters": [
                    {"name": "Sticker", "description": "Sticker to rename", "required": True},
                    {"name": "Name", "description": "New name for the sticker", "required": True},
                ],
            },
            "fr": {
                "name": "Renommer un sticker",
                "description": "Renommer un autocollant personnalisé",
                "parameters": [
                    {"name": "Sticker", "description": "Sticker à renommer", "required": True},
                    {"name": "Nom", "description": "Nouveau nom du sticker", "required": True},
                ],
            },
        }
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Disable Command",
                "description": "Disable a command for this server",
                "parameters": [
                    {"name": "Command", "description": "Command to disable", "required": True},
                ],
            },
            "fr": {
                "name": "Désactiver une commande",
                "description": "Désactiver une commande pour ce serveur",
                "parameters": [
                    {"name": "Commande", "description": "Commande à désactiver", "required": True},
                ],
            },
        },
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
        extras={
            "en": {
                "name": "Enable Command",
                "description": "Enable a previously disabled command",
                "parameters": [
                    {"name": "Command", "description": "Command to enable", "required": True},
                ],
            },
            "fr": {
                "name": "Activer une commande",
                "description": "Activer une commande précédemment désactivée",
                "parameters": [
                    {"name": "Commande", "description": "Commande à activer", "required": True},
                ],
            },
        },
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
        description=T("list_disabled_cmds_description"),
        extras={
            "en": {
                "name": "List Disabled Commands",
                "description": "List all disabled commands for this server",
                "parameters": [],
            },
            "fr": {
                "name": "Lister les commandes désactivées",
                "description": "Lister toutes les commandes désactivées pour ce serveur",
                "parameters": [],
            },
        },
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

    role = Jeanne.Group(name=T("role_reward_group_name"), description="...")

    @role.command(
        name=T("add_role_reward_name"),
        description=T("add_role_reward_description"),
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Add Role Reward",
                "description": "Add a role reward for a level",
                "parameters": [
                    {"name": "Role", "description": "Role to reward", "required": True},
                    {"name": "Level", "description": "Level required for the reward", "required": True},
                ],
            },
            "fr": {
                "name": "Ajouter une récompense de rôle",
                "description": "Ajouter une récompense de rôle pour un niveau",
                "parameters": [
                    {"name": "Rôle", "description": "Rôle à récompenser", "required": True},
                    {"name": "Niveau", "description": "Niveau requis pour la récompense", "required": True},
                ],
            },
        },
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
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Remove Role Reward",
                "description": "Remove a role reward",
                "parameters": [
                    {"name": "Role", "description": "Role to remove from rewards", "required": True},
                ],
            },
            "fr": {
                "name": "Retirer une récompense de rôle",
                "description": "Retirer une récompense de rôle",
                "parameters": [
                    {"name": "Rôle", "description": "Rôle à retirer des récompenses", "required": True},
                ],
            },
        },
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
        extras={
            "en": {
                "name": "List Role Rewards",
                "description": "List all role rewards",
                "parameters": [],
            },
            "fr": {
                "name": "Lister les récompenses de rôle",
                "description": "Lister toutes les récompenses de rôle",
                "parameters": [],
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _list(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Level_Group(self.bot)._list(ctx)
        elif ctx.locale.value == "fr":
            await fr.Level_Group(self.bot)._list(ctx)

    channel_blacklist = Jeanne.Group(
        name=T("blacklist_channel_group_name"), description="..."
    )

    @channel_blacklist.command(
        name=T("add_blacklist_channel_name"),
        description=T("add_blacklist_ch_description"),
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Add Blacklist Channel",
                "description": "Add a channel to the level blacklist",
                "parameters": [
                    {"name": "Channel", "description": "Channel to blacklist", "required": True},
                ],
            },
            "fr": {
                "name": "Ajouter un salon à la liste noire",
                "description": "Ajouter un salon à la liste noire des niveaux",
                "parameters": [
                    {"name": "Salon", "description": "Salon à mettre sur liste noire", "required": True},
                ],
            },
        },
    )
    @Jeanne.describe(channel=T("add_blacklist_ch_channel_desc"))
    @Jeanne.rename(channel=T("add_blacklist_ch_channel_name"))
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
        description=T("remove_blacklist_ch_description"),
        extras={
            "member_perms": "Manage Server",
            "en": {
                "name": "Remove Blacklist Channel",
                "description": "Remove a channel from the level blacklist",
                "parameters": [
                    {"name": "Channel", "description": "Channel to remove from blacklist", "required": True},
                ],
            },
            "fr": {
                "name": "Retirer un salon de la liste noire",
                "description": "Retirer un salon de la liste noire des niveaux",
                "parameters": [
                    {"name": "Salon", "description": "Salon à retirer de la liste noire", "required": True},
                ],
            },
        },
    )
    @Jeanne.describe(channel=T("remove_blacklist_ch_channel_desc"))
    @Jeanne.rename(channel=T("remove_blcklist_ch_channel_name"))
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
        description=T("list_blacklist_channels_desc"),
        extras={
            "en": {
                "name": "List Blacklist Channels",
                "description": "List all blacklisted channels",
                "parameters": [],
            },
            "fr": {
                "name": "Lister les salons sur liste noire",
                "description": "Lister tous les salons sur liste noire",
                "parameters": [],
            },
        },
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
