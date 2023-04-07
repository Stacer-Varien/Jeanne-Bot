from typing import Literal, Optional
from json import loads
from discord import (
    AllowedMentions,
    Attachment,
    CategoryChannel,
    Color,
    Embed,
    File,
    HTTPException,
    Interaction,
    Member,
    Role,
    TextChannel,
    VerificationLevel,
    app_commands as Jeanne,
    abc,
    utils,
)
from discord.ext.commands import Bot, Cog, GroupCog
from humanfriendly import format_timespan, parse_timespan, InvalidTimespan
from collections import OrderedDict
from functions import Botban, Inventory, Levelling, Logger, Manage, Welcomer
from assets.components import Confirmation, Levelmsg, Welcomingmsg, Leavingmsg
from requests import get
from io import BytesIO


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Create_Group(GroupCog, name="create"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Creates a text channel")
    @Jeanne.describe(
        name="What will you name it?",
        topic="What is the channel topic?",
        category="Place in which category?",
        slowmode="What is the slowmode (1hr, 30m, etc) (Max is 6 hours)",
        nsfw_enabled="Should it be an NSFW channel?",
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def textchannel(
        self,
        ctx: Interaction,
        name: str,
        topic: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        slowmode: str = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        embed.color = Color.random()
        embed.description = "Text Channel `{}` has been created".format(name)

        channel = await ctx.guild.create_text_channel(name=name)

        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )

        if topic:
            if len(topic) <= 1024:
                await channel.edit(topic=topic)
                added_topic = topic
            else:
                added_topic = "Too many characters! Please make sure your topic has less than 1024 characters"
            embed.add_field(name="Topic", value=added_topic, inline=True)

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
                embed.add_field(name="NSFW", value="Yes", inline=True)
                await channel.edit(nsfw=True)
            else:
                embed.add_field(name="NSFW", value="No", inline=True)
                await channel.edit(nsfw=False)

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Create a voice channel")
    @Jeanne.describe(
        name="What will you name it?",
        category="Place in which category?",
        users="How many users are allowed in the channel",
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def voicechannel(
        self,
        ctx: Interaction,
        name: str,
        category: Optional[CategoryChannel] = None,
        users: Optional[int] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        embed.description = "Voice Channel `{}` has been created".format(name)
        embed.color = Color.random()

        channel = await ctx.guild.create_voice_channel(name=name)

        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )

        if users:
            if users > 99:
                users = 99

            await channel.edit(user_limit=users)
            embed.add_field(name="User Limit", value=users, inline=True)

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Create a category")
    @Jeanne.describe(name="What will you name it?")
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def category(self, ctx: Interaction, name: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        await ctx.guild.create_category(name=name)
        embed = Embed()
        embed.description = "Category `{}` has been created".format(name)
        embed.color = Color.random()

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Create a stage channel")
    @Jeanne.describe(
        name="What will you name it?",
        topic="What is the topic?",
        category="Place in which category?",
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def stagechannel(
        self, ctx: Interaction, name: str, topic: str, category: CategoryChannel
    ):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        channel = await ctx.guild.create_stage_channel(name=name, topic=topic)
        embed.description = "Stage channel `{}` has been created".format(name)
        embed.add_field(name="Topic", value=topic, inline=True)

        if category:
            await channel.edit(category=category)
            embed.add_field(name="Moved to category", value=category, inline=True)

        embed.color = Color.random()

        await ctx.followup.send(embed=embed)

    @stagechannel.error
    async def stagechannel_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if HTTPException:
                embed = Embed()
                embed.description = "Couldn't make a new stage channel. Please make sure the server is community enabled"
                embed.color = Color.red()
                await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Create a forum")
    @Jeanne.describe(
        name="What will you name it?",
        topic="What is the topic",
        category="Place in which category?",
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def forum(
        self, ctx: Interaction, name: str, topic: str, category: CategoryChannel
    ):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        forum = await ctx.guild.create_forum(name=name, topic=topic)
        embed.description = "Forum `{}` has been created".format(forum.name)
        embed.color = Color.random()
        if category:
            await forum.edit(category=category)
            embed.add_field(
                name="Added into category", value=category.name, inline=True
            )

        await ctx.followup.send(embed=embed)

    @forum.error
    async def forum_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if HTTPException:
                embed = Embed()
                embed.description = "Couldn't make a new forum. Please make sure the server is community enabled"
                embed.color = Color.red()
                await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Create a role")
    @Jeanne.describe(
        name="What will you name it?",
        color="What color will it be? (use HEX codes)",
        hoisted="Should it be shown in member list?",
        mentionable="Should it be mentioned?",
    )
    @Jeanne.checks.has_permissions(manage_roles=True)
    async def role(
        self,
        ctx: Interaction,
        name: str,
        color: Optional[str] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        role = await ctx.guild.create_role(name=name)
        embed = Embed()
        embed.description = "Role `{}` has been created".format(name)

        if color:
            await role.edit(color=int(color, 16))
            embed.add_field(name="Color", value=color, inline=True)
        elif not color:
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

    @Jeanne.command(description="Makes a public thread channel")
    @Jeanne.describe(
        name="What will you name it?",
        channel="Which channel is the message in?",
        message_id="What is the message ID?",
        slowmode="What is the slowmode (1hr, 30m, etc) (Max is 6 hours)",
    )
    @Jeanne.checks.has_permissions(create_public_threads=True)
    @Jeanne.checks.bot_has_permissions(create_public_threads=True, manage_threads=True)
    async def thread(
        self,
        ctx: Interaction,
        name: str,
        channel: TextChannel,
        message_id: str,
        slowmode: Optional[str] = None,
    ):
        if Botban(ctx.user).check_botbanned_user() == True:
            return
        await ctx.response.defer()
        message = await channel.fetch_message(int(message_id))
        thread = await channel.create_thread(name=name, message=message)

        embed = Embed()
        embed.description = "Thread `{}` has been created on [message]({})".format(
            name, message.jump_url
        )
        embed.color = Color.green()

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

    @Jeanne.command(description="Make a new emoji")
    @Jeanne.describe(
        name="What will you name it?",
        emoji_link="Insert emoji URL here",
        emoji_image="Insert emoji image here",
    )
    @Jeanne.checks.has_permissions(manage_emojis_and_stickers=True)
    async def emoji(
        self,
        ctx: Interaction,
        name: str,
        emoji_link: Optional[str] = None,
        emoji_image: Optional[Attachment] = None,
    ):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()

        if emoji_link == None and emoji_image == None:
            embed.description = "Please add either an emoji URL or emoji image"
            embed.color = Color.red()

        elif emoji_link and emoji_image:
            embed.description = "Please use either an emoji URL or emoji image"
            embed.color = Color.red()

        else:
            if emoji_link:
                emojibytes = get(emoji_link).content

            elif emoji_image:
                emojibytes = get(emoji_image.url).content

            try:
                emote = await ctx.guild.create_custom_emoji(name=name, image=emojibytes)
                embed.description = "{} | {} has been created".format(
                    emote.name, str(emote)
                )
                embed.color = Color.random()
            except HTTPException:
                embed.description = "There was a problem making the emoji. Please check that the emoji you are making is a PNG, JPEG or GIF"
                embed.color = Color.red()

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Make a new sticker")
    @Jeanne.describe(
        name="What will you name it?",
        description="What does your sticker mean?",
        emoji="Emoji that will repesent the sticker",
        sticker_link="Insert sticker URL here",
        sticker_image="Insert sticker image here",
    )
    @Jeanne.checks.has_permissions(manage_emojis_and_stickers=True)
    async def sticker(
        self,
        ctx: Interaction,
        name: str,
        description: str,
        emoji: str,
        sticker_link: Optional[str] = None,
        sticker_image: Optional[Attachment] = None,
    ):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        if sticker_link == None and sticker_image == None:
            embed.description = "Please add either an sticker URL or sticker image"
            embed.color = Color.red()

        elif sticker_link and sticker_image:
            embed.description = "Please use either an sticker URL or sticker image"
            embed.color = Color.red()

        else:
            if sticker_link:
                stickerbytes = BytesIO(get(sticker_link).content)
                url = sticker_link

            elif sticker_image:
                stickerbytes = BytesIO(get(sticker_image.url).content)
                url = sticker_image.url

            stickerfile = File(fp=stickerbytes, filename="sticker.png")

            try:
                sticker = await ctx.guild.create_sticker(
                    name=name, description=description, emoji=emoji, file=stickerfile
                )
                embed.description = "{} has been created".format(sticker.name)
                embed.color = Color.random()
                embed.set_image(url=url)
            except HTTPException:
                embed.description = "There was a problem making the sticker. Please check that the sticker you are making is:\n\n 1. 512kb or less. Use [Ezgif](https://ezgif.com/) to compress it\n 2. The file is a PNG or APNG"
                embed.color = Color.red()

        await ctx.followup.send(embed=embed)


class Delete_Group(GroupCog, name="delete"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Deletes a channel")
    @Jeanne.describe(channel="Which channel are you deleting?")
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def channel(self, ctx: Interaction, channel: abc.GuildChannel):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        await channel.delete()
        embed = Embed(
            description="{} has been deleted".format(channel.name), color=Color.random()
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Deletes a role")
    @Jeanne.describe(role="Which role are you deleting?")
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def role(self, ctx: Interaction, role: Role):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        await role.delete()
        embed = Embed(
            description="{} has been deleted".format(role.name), color=Color.random()
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Deletes an emoji")
    @Jeanne.describe(emoji="Which emoji are you deleting?")
    @Jeanne.checks.has_permissions(manage_emojis_and_stickers=True)
    async def emoji(self, ctx: Interaction, emoji: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        try:
            e = emoji.split(":")[-1].rstrip(">")
            emote = self.bot.get_emoji(int(e))
        except:
            emote = utils.get(ctx.guild.emojis, name=emoji)
        embed = Embed(
            description="{} has been deleted".format(str(emote)), color=0x00FF68
        )
        await emote.delete()
        await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This emoji doesn't exist in the server",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Deletes a sticker")
    @Jeanne.describe(sticker="Which sticker are you deleting?")
    @Jeanne.checks.has_permissions(manage_emojis_and_stickers=True)
    async def sticker(self, ctx: Interaction, sticker: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()

        stick = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` has been deleted".format(str(stick.name)), color=0x00FF68
        )
        await stick.delete()
        await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This sticker doesn't exist in the server",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=embed)


class Edit_Group(GroupCog, name="edit"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Edits a text/news channel")
    @Jeanne.describe(
        channel="Which channel are you editing?",
        name="What will be the new name?",
        topic="What should be the new topic?",
        slowmode="What is the slowmode (1hr, 30m, etc) (Max is 6 hours)",
        category="Place in which category?",
        nsfw_enabled="Should it be an NSFW channel?",
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def textchannel(
        self,
        ctx: Interaction,
        channel: TextChannel,
        name: Optional[str] = None,
        topic: Optional[str] = None,
        slowmode: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
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
            if len(topic) <= 1024:
                await channel.edit(topic=topic)
                added_topic = topic
            else:
                added_topic = "Too many characters! Please make sure your topic has less than 1024 characters"
            embed.add_field(name="Topic", value=added_topic, inline=True)

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

    @Jeanne.command(description="Edit a role")
    @Jeanne.describe(
        role="Which role are you editing?",
        name="What is the new name?",
        color="What is the new color? (use HEX codes)",
        hoisted="Should it be shown in member list?",
        mentionable="Should it be mentioned?",
    )
    @Jeanne.checks.has_permissions(manage_roles=True)
    async def role(
        self,
        ctx: Interaction,
        role: Role,
        name: Optional[str] = None,
        color: Optional[str] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        embed.description = "Role `{}` has been edited".format(role.name)

        if color:
            embed.color = color
        else:
            embed.color = Color.green()

        if name:
            await role.edit(name=name)
            embed.add_field(name="Name", value=name, inline=True)

        if color:
            await role.edit(color=int(color, 16))
            embed.add_field(name="Color", value=color, inline=True)

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

    @Jeanne.command(description="Edits the server")
    @Jeanne.describe(
        name="What is the new name?",
        description="What is the new description (only for public servers)",
        avatar="What is the new server avatar?",
        banner="What will be the new banner?",
        verification_level="How high should the verification level be?",
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def server(
        self,
        ctx: Interaction,
        name: Optional[str] = None,
        description: Optional[str] = None,
        avatar: Optional[Attachment] = None,
        banner: Optional[Attachment] = None,
        verification_level: Literal["none", "low", "medium", "high", "highest"] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

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
                avatarbytes = get(avatar.url).content
                await ctx.guild.edit(icon=avatarbytes)
                embed.thumbnail(url=avatar.url)
            except:
                return

        if banner:
            if ctx.guild.premium_tier < 1:
                embed.add_field(
                    name="Banner not added",
                    value="This server is not boosted to Tier 1",
                    inline=True,
                )
            else:
                try:
                    bannerbytes = get(banner.url).content
                    await ctx.guild.edit(banner=bannerbytes)
                    embed.set_image(url=banner.url)
                except:
                    return

        if verification_level:
            if verification_level == "none":
                await ctx.guild.edit(verification_level=VerificationLevel.none)
                embed.add_field(
                    name="Verification Level",
                    value="{}\nNo verification required".format(verification_level),
                    inline=True,
                )

            elif verification_level == "low":
                await ctx.guild.edit(verification_level=VerificationLevel.low)
                embed.add_field(
                    name="Verification Level",
                    value="{}\nMembers must have a verified email".format(
                        verification_level
                    ),
                    inline=True,
                )

            elif verification_level == "medium":
                await ctx.guild.edit(verification_level=VerificationLevel.medium)
                embed.add_field(
                    name="Verification Level",
                    value="{}\nMembers must have a verified email and be registered on Discord for more than 5 minutes".format(
                        verification_level
                    ),
                    inline=True,
                )

            elif verification_level == "high":
                await ctx.guild.edit(verification_level=VerificationLevel.high)
                embed.add_field(
                    name="Verification Level",
                    value="{}\nMembers must have a verified email, be registered on Discord for more than 5 minutes and stay in the server for more than 10 minutes".format(
                        verification_level
                    ),
                    inline=True,
                )

            elif verification_level == "highest":
                await ctx.guild.edit(verification_level=VerificationLevel.highest)
                embed.add_field(
                    name="Verification Level",
                    value="{}\nMembers must have a verified phone number".format(
                        verification_level
                    ),
                    inline=True,
                )

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Renames an emoji")
    @Jeanne.describe(emoji="What emoji are you renaming?", name="What is the new name?")
    @Jeanne.checks.has_permissions(manage_emojis_and_stickers=True)
    async def emoji(self, ctx: Interaction, emoji: str, name: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        try:
            e = emoji.split(":")[-1].rstrip(">")
            emote = self.bot.get_emoji(int(e))
        except:
            emote = utils.get(ctx.guild.emojis, name=emoji)
        embed = Embed(
            description="{} has been renamed to {}".format(str(emote), name),
            color=0x00FF68,
        )
        await emote.edit(name=name)
        await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This emoji doesn't exist in the server",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=embed)


class Set_Group(GroupCog, name="set"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Set a welcomer and/or leaver channel")
    @Jeanne.describe(
        welcoming_channel="Which channel should alert members when someone join",
        leaving_channel="Which channel should members when someone leaves?",
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def welcomer(
        self,
        ctx: Interaction,
        welcoming_channel: Optional[TextChannel] = None,
        leaving_channel: Optional[TextChannel] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        if welcoming_channel == None and leaving_channel == None:
            error = Embed(
                description="Both options are empty. Please set at least a welcomer or leaving channel",
                color=Color.red(),
            )
            await ctx.followup.send(embed=error)
        else:
            setup = Embed(description="Welcomer channels set", color=Color.random())
            if welcoming_channel:
                Manage(ctx.guild, welcoming_channel).set_welcomer()
                setup.add_field(
                    name="Channel welcoming users",
                    value=welcoming_channel.mention,
                    inline=True,
                )

            if leaving_channel:
                Manage(ctx.guild, leaving_channel).set_leaver()
                setup.add_field(
                    name="Channel showing users that left",
                    value=leaving_channel.mention,
                    inline=True,
                )

            await ctx.followup.send(embed=setup)

    @Jeanne.command(description="Set a modlog channel")
    @Jeanne.describe(
        channel="Which channel should log warns, mutes, timeouts, kicks and bans?"
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def modlog(self, ctx: Interaction, channel: TextChannel):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        Manage(ctx.guild).set_modloger(channel)
        embed = Embed(description="Modlog channel set", color=Color.red())
        embed.add_field(name="Channel selected", value=channel.mention, inline=True)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Set a message logging channel")
    @Jeanne.describe(channel="Which channel should log edited and deleted messages?")
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def messagelog(self, ctx: Interaction, channel: TextChannel):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        Logger(ctx.guild).set_message_logger(channel)
        embed = Embed(description="Message logging channel set", color=Color.red())
        embed.add_field(name="Channel selected", value=channel.mention, inline=True)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Set a welcoming message when someone joins the server")
    @Jeanne.describe(jsonfile="Upload JSON file with the welcoming message")
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def welcomingmsg(
        self, ctx: Interaction, jsonfile: Optional[Attachment] = None
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        if jsonfile == None:
            await ctx.response.send_modal(Welcomingmsg())

        elif jsonfile != None:
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

            json_file = jsonfile.url
            json_request = get(json_file)
            json_content = replace_all(json_request.content, parameters)
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
                Welcomer(ctx.guild).set_welcomer_msg(str(json_request.content))

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

    @Jeanne.command(description="Set a leaving message when someone leaves the server")
    @Jeanne.describe(jsonfile="Upload JSON file with the welcoming message")
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def leavingmsg(
        self, ctx: Interaction, jsonfile: Optional[Attachment] = None
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        if jsonfile == None:
            await ctx.response.send_modal(Leavingmsg())

        elif jsonfile != None:
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

            json_file = jsonfile.url
            json_request = get(json_file)
            json_content = replace_all(json_request.content, parameters)
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
                Welcomer(ctx.guild).set_leaving_msg(str(json_request.content))

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

    @Jeanne.command(description="Set a level up notification channel")
    @Jeanne.describe(
        channel="Which channel will update when a member levels up?",
        levelmsg="Add your level message here. Use Discohooks to generate the embed",
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def levelupdate(
        self, ctx: Interaction, channel: TextChannel, levelmsg: Optional[bool] = None
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        if levelmsg == None or False:
            await ctx.response.defer()
            Levelling(server=ctx.guild).add_level_channel(channel)
            embed = Embed()
            embed.description = (
                "{} will post level updates when someone levels up".format(
                    channel.mention
                )
            )
            embed.color = Color.random()
            await ctx.followup.send(embed=embed)

        elif levelmsg == True:
            await ctx.response.send_modal(Levelmsg(channel))

    @Jeanne.command(
        description="Change the brightness of your level and profile card background"
    )
    @Jeanne.describe(
        brightness="Set the level of brightness between 10 - 150. Default is 100"
    )
    async def brightness(self, ctx: Interaction, brightness: int):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        if brightness > 150:
            embed.description = "This is too bright!\nPlease make sure it is higher than 10 and lower than 150"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
        elif brightness < 10:
            embed.description = "This is too dark!\nPlease make sure it is higher than 10 and lower than 150"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
        elif Inventory(ctx.user).set_brightness(brightness) == False:
            embed.description = "You have no background wallpaper"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
        else:
            Inventory(ctx.user).set_brightness(brightness)
            embed.description = "Brightness has been changed to {}".format(brightness)
            embed.color = Color.random()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Change your profile bio")
    @Jeanne.describe(bio="Add your bio. Make sure its 60 characters per line")
    async def bio(self, ctx: Interaction, bio: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        if len(bio) > 120:
            embed.description = (
                "Too many words!\nPlease make sure your bio has 60 words."
            )
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
        else:
            Inventory(ctx.user).set_bio(bio)
            embed.description = "New bio has been set to\n{}".format(bio)
            embed.color = Color.random()
            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Change your level and profile card font and bar color")
    @Jeanne.describe(color="Add your color. Must be in HEX code")
    async def color(self, ctx: Interaction, color: str):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        try:
            Inventory(ctx.user).set_color(color)
            embed.description = "Profile and Level card font and bar color changed to {} as showing in the embed color".format(
                color
            )
            embed.color = int(color, 16)
        except:
            embed.description = "Invalid HEX code entered"
            embed.color = Color.red()
        await ctx.followup.send(embed=embed)


class XP_Group(GroupCog, name="xp"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Blacklists a channel for gaining XP")
    @Jeanne.describe(channel="Which channel?")
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def blacklist(self, ctx: Interaction, channel: TextChannel) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        if Levelling(server=ctx.guild).check_xpblacklist_channel(channel) == True:
            embed = Embed(color=Color.red())
            embed.description = "Channel is already XP blacklisted"
            await ctx.followup.send(embed=embed)
        else:
            Levelling(server=ctx.guild).add_xpblacklist(channel)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="Channel XP blacklisted",
                value=f"`{channel}` has been added to the XP blacklist",
                inline=False,
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Unblacklists a channel for gaining XP")
    @Jeanne.describe(channel="Which channel?")
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def unblacklist(self, ctx: Interaction, channel: TextChannel) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        if Levelling(server=ctx.guild).check_xpblacklist_channel(channel) == False:
            embed = Embed(color=Color.red())
            embed.description = "Channel is not in the XP blacklisted"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
        else:
            Levelling(server=ctx.guild).remove_blacklist(channel)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="Channel XP blacklisted",
                value=f"`{channel}` has been added to the XP blacklist",
                inline=False,
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="List all XP blacklisted channels")
    async def blacklistedchannels(self, ctx: Interaction) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        embed = Embed()
        channels = Levelling(server=ctx.guild).get_blacklisted_channels()

        if channels == None:
            embed.description = "There are no XP blacklisted channels"
            embed.color = Color.red()
        else:
            embed.color = Color.random()
            embed.title = "List of XP blacklisted channels"
            embed.description = ""
            for channel in channels:
                embed.description += ctx.guild.get_channel(int(channel)).mention
            await ctx.followup.send(embed=embed)


class manage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(description="Add a role to a member")
    @Jeanne.describe(member="Which member?", role="Which role are you adding?")
    @Jeanne.checks.has_permissions(manage_roles=True)
    async def addrole(self, ctx: Interaction, member: Member, role: Role):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        await member.add_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name=f"Role given", value=f"`{role}` was given to `{member}`", inline=False
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Remove a role from a member")
    @Jeanne.describe(member="Which member?", role="Which role are you removing?")
    @Jeanne.checks.has_permissions(manage_roles=True)
    async def removerole(self, ctx: Interaction, member: Member, role: Role):
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        await member.remove_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name=f"Role removed",
            value=f"`{role}` was removed from `{member}`",
            inline=False,
        )
        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Removes a welcoming/modlog/report channel. Set all options to true to remove all"
    )
    @Jeanne.describe(
        welcomer="Remove welcomer channel?",
        leaving="Remove leaving channel?",
        modlog="Remove modlog channel?",
        messagelog="Remove lessage logging channel?",
        welcomingmsg="Remove the welcoming message and reset to default",
        leavingmsg="Remove the leaving message and reset to default",
        levelupchannel="Remove the level up update channel",
    )
    @Jeanne.checks.has_permissions(manage_guild=True)
    async def remove(
        self,
        ctx: Interaction,
        welcomer: Optional[bool] = None,
        leaving: Optional[bool] = None,
        modlog: Optional[bool] = None,
        messagelog: Optional[bool] = None,
        welcomingmsg: Optional[bool] = None,
        leavingmsg: Optional[bool] = None,
        levelupchannel: Optional[bool] = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        if (
            welcomer == None
            and leaving == None
            and modlog == None
            and welcomingmsg == None
            and leavingmsg == None
        ):
            error = Embed(description="Please select a channel to remove")
            await ctx.followup.send(embed=error)
        else:
            embed = Embed(description="Channels removed")

            if welcomer == True:

                wel = Manage(ctx.guild).remove_welcomer()

                if wel == False:
                    embed.add_field(
                        name="Welcomer channel removal status",
                        value="Failed. No welcomer channel set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Welcomer channel removal status",
                        value="Successful",
                        inline=True,
                    )

            if leaving == True:

                leav = Manage(ctx.guild).remove_leaver()

                if leav == False:
                    embed.add_field(
                        name="Leaving channel removal status",
                        value="Failed. No leaving channel set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Leaving channel removal status",
                        value="Successful",
                        inline=True,
                    )

            if modlog == True:

                mod = Manage(ctx.guild).remove_modloger()

                if mod == False:
                    embed.add_field(
                        name="Modlog channel removal status",
                        value="Failed. No modlog channel set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Modlog channel removal status",
                        value="Successful",
                        inline=True,
                    )

            if messagelog == True:

                rep = Logger(ctx.guild).remove_messagelog()

                if rep == False:
                    embed.add_field(
                        name="Message logging channel removal status",
                        value="Failed. No Message logging channel set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Message logging channel removal status",
                        value="Successful",
                        inline=True,
                    )

            if welcomingmsg == True:

                msg = Welcomer(ctx.guild).remove_welcomer_msg()

                if msg == 0 or None:
                    embed.add_field(
                        name="Welcoming Message removal status",
                        value="Failed. No welcoming message set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Welcoming Message removal status",
                        value="Successful",
                        inline=True,
                    )

            if leavingmsg == True:

                leav = Welcomer(ctx.guild).remove_welcomer_msg()

                if leav == 0 or None:
                    embed.add_field(
                        name="Leaving Message removal status",
                        value="Failed. No leaving message set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Leaving Message removal status",
                        value="Successful",
                        inline=True,
                    )

            if levelupchannel == True:
                lvlup = Manage(ctx.guild).remove_levelup()

                if lvlup == 0 or None:
                    embed.add_field(
                        name="Level Up Channel Update removal status",
                        value="Failed. No Level Up Channel Update set",
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="Level Up Channel Update removal status",
                        value="Successful",
                        inline=True,
                    )

            await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Clone a channel")
    @Jeanne.describe(
        channel="Which channel are you cloning?", name="What is the new name?"
    )
    @Jeanne.checks.has_permissions(manage_channels=True)
    async def clone(
        self, ctx: Interaction, channel: abc.GuildChannel, name: Optional[str] = None
    ) -> None:
        if Botban(ctx.user).check_botbanned_user() == True:
            return

        await ctx.response.defer()
        if name == None:
            name = channel.name

        c = await channel.clone(name=name)

        cloned = Embed(
            description="{} was cloned as {}".format(channel.mention, c.mention)
        )
        cloned.color = Color.random()
        await ctx.followup.send(embed=cloned)


async def setup(bot: Bot):
    await bot.add_cog(manage(bot))
    await bot.add_cog(Create_Group(bot))
    await bot.add_cog(Edit_Group(bot))
    await bot.add_cog(Delete_Group(bot))
    await bot.add_cog(Set_Group(bot))
    await bot.add_cog(XP_Group(bot))
