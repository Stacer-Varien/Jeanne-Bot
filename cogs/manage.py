from typing import Literal, Optional
from json import loads
from discord import *
from discord.ext.commands import Bot, Cog, GroupCog
from humanfriendly import format_timespan, parse_timespan, InvalidTimespan
from collections import OrderedDict
from db_functions import *
from assets.buttons import Confirmation
import requests
from io import BytesIO

def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Create_Group(GroupCog, name="create"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Creates a text channel")
    @app_commands.describe(name="What will you name it?", topic="What is the channel topic?",category="Place in which category?", slowmode="What is the slowmode (1hr, 30m, etc) (Max is 6 hours)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def textchannel(self, ctx: Interaction, name: str, topic:Optional[str]=None,category: Optional[CategoryChannel] = None, slowmode: str = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            embed = Embed()
            embed.color = Color.random()
            embed.description = "Text Channel `{}` has been created".format(
                name)

            channel = await ctx.guild.create_text_channel(name=name)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)
            
            if topic:
                if len(topic) <= 1024:
                    await channel.edit(topic=topic)
                    added_topic=topic
                else:
                    added_topic="Too many characters! Please make sure your topic has less than 1024 characters"
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
                embed.add_field(name="Slowmode",
                                value=added_slowmode, inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description='Create a voice channel')
    @app_commands.describe(name="What will you name it?", category="Place in which category?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voicechannel(self, ctx: Interaction, name: str, category: Optional[CategoryChannel] = None, users:Optional[int]=None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            embed = Embed()
            embed.description = "Voice Channel `{}` has been created".format(
                name)
            embed.color = Color.random()

            channel = await ctx.guild.create_voice_channel(name=name)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)
            
            if users:
                if users > 99:
                    user_limit=99
                    
                await channel.edit(user_limit=user_limit)
                embed.add_field(name="User Limit", value=user_limit, inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description='Create a category')
    @app_commands.describe(name="What will you name it?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def category(self, ctx: Interaction, name: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            await ctx.guild.create_category(name=name)
            embed = Embed()
            embed.description = "Category `{}` has been created".format(name)
            embed.color = Color.random()

            await ctx.followup.send(embed=embed)

    @app_commands.command(description='Create a stage channel')
    @app_commands.describe(name="What will you name it?", topic="What is the topic?", category="Place in which category?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def stagechannel(self, ctx: Interaction, name: str, topic: str, category: CategoryChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            embed = Embed()
            channel=await ctx.guild.create_stage_channel(name=name, topic=topic)
            embed.description = "Stage channel `{}` has been created".format(
                    name)
            embed.add_field(name="Topic", value=topic, inline=True)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Moved to category", value=category, inline= True)

            embed.color = Color.random()

            await ctx.followup.send(embed=embed)
    
    @stagechannel.error
    async def stagechannel_error(self, ctx:Interaction, error:app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if HTTPException:
                embed=Embed()
                embed.description = "Couldn't make a new stage channel. Please make sure the server is community enabled"
                embed.color=Color.red()
                await ctx.followup.send(embed=embed)
            


    @app_commands.command(description="Create a forum")
    @app_commands.describe(name="What will you name it?", topic="What is the topic", category="Place in which category?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def forum(self, ctx: Interaction, name: str, topic: str, category: CategoryChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            embed = Embed()
            forum = await ctx.guild.create_forum(name=name, topic=topic)
            embed.description = "Forum `{}` has been created".format(
                    forum.name)
            embed.color = Color.random()
            if category:
                await forum.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            await ctx.followup.send(embed=embed)

    @forum.error
    async def forum_error(self, ctx:Interaction, error:app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if HTTPException:
                embed=Embed()
                embed.description = "Couldn't make a new forum. Please make sure the server is community enabled"
                embed.color=Color.red()
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="Create a role")
    @app_commands.describe(name="What will you name it?", color="What color will it be? (use HEX codes)", hoisted="Should it be shown in member list?", mentionable="Should it be mentioned?")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role(self, ctx: Interaction, name: str, color: Optional[str] = None, hoisted: Optional[bool] = None, mentionable: Optional[bool] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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
                if hoisted == "true":
                    await role.edit(hoist=True)
                    embed.add_field(name="Hoisted", value="Yes", inline=True)
                elif hoisted == "false":
                    pass

            if mentionable:
                if mentionable == "true":
                    await role.edit(mentionable=True)
                    embed.add_field(name="Mentionable",
                                    value="Yes", inline=True)
                elif mentionable == "false":
                    pass

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Makes a public thread channel")
    @app_commands.describe(name="What will you name it?", channel="Which channel is the message in?", message_id="What is the message ID?", slowmode="WHat is the slowmode (1hr, 30m, etc) (Max is 6 hours)")
    @app_commands.checks.has_permissions(create_public_threads=True)
    async def thread(self, ctx: Interaction, name: str, channel: TextChannel, message_id: str, slowmode: Optional[str] = None):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            message = await channel.fetch_message(int(message_id))
            thread = await channel.create_thread(name=name, message=message)

            embed = Embed()
            embed.description = "Thread `{}` has been created on [message]({})".format(
                name, message.jump_url)
            embed.color = Color.green()

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Make a new emoji")
    @app_commands.describe(name="What will you name it?", emoji_link="Insert emoji URL here", emoji_image="Insert emoji image here")
    @app_commands.checks.has_permissions(manage_emojis_and_stickers=True)
    async def emoji(self, ctx: Interaction, name: str, emoji_link: Optional[str]=None, emoji_image: Optional[Attachment]=None):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            embed=Embed()

            if emoji_link == None and emoji_image == None:
                embed.description="Please add either an emoji URL or emoji image"
                embed.color=Color.red()
                
            elif emoji_link and emoji_image:
                embed.description = "Please use either an emoji URL or emoji image"
                embed.color = Color.red()
                
            else:
                if emoji_link:
                    emojibytes=requests.get(emoji_link).content
                        
                elif emoji_image:
                    emojibytes = requests.get(emoji_image.url).content

                try:
                    emote = await ctx.guild.create_custom_emoji(name=name, image=emojibytes)
                    embed.description = "{} | {} has been created".format(
                        emote.name, str(emote))
                    embed.color=ctx.user.color
                except HTTPException:
                    embed.description = "There was a problem making the emoji. Please check that the emoji you are making is a PNG, JPEG or GIF"
                    embed.color = Color.red()

        await ctx.followup.send(embed=embed)

    @app_commands.command(description="Make a new sticker")
    @app_commands.describe(name="What will you name it?", description="What does your sticker mean?", emoji="Emoji that will repesent the sticker", sticker_link="Insert sticker URL here", sticker_image="Insert sticker image here")
    @app_commands.checks.has_permissions(manage_emojis_and_stickers=True)
    async def sticker(self, ctx: Interaction, name: str, description:str, emoji:str, sticker_link: Optional[str] = None, sticker_image: Optional[Attachment] = None):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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
                    stickerbytes = BytesIO(requests.get(sticker_link).content)
                    url=sticker_link
                    
                elif sticker_image:
                    stickerbytes = BytesIO(requests.get(sticker_image.url).content)
                    url=sticker_image.url
                
                stickerfile = File(fp=stickerbytes, filename="sticker.png")
                
                try:
                    sticker = await ctx.guild.create_sticker(name=name, description=description, emoji=emoji, file=stickerfile)
                    embed.description = "{} has been created".format(
                        sticker.name)
                    embed.color = ctx.user.color
                    embed.set_image(url=url)
                except HTTPException:
                    embed.description="There was a problem making the sticker. Please check that the sticker you are making is:\n\n 1. 512kb or less. Use [Ezgif](https://ezgif.com/) to compress it\n 2. The file is a PNG or APNG"
                    embed.color=Color.red()

        await ctx.followup.send(embed=embed)


class Delete_Group(GroupCog, name="delete"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Deletes a channel")
    @app_commands.describe(channel="Which channel are you deleting?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def channel(self, ctx: Interaction, channel: abc.GuildChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            await channel.delete()
            embed = Embed(description="{} has been deleted".format(
                channel.name), color=0x00FF68)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Deletes a role")
    @app_commands.describe(role="Which role are you deleting?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def role(self, ctx: Interaction, role: Role):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            await role.delete()
            embed = Embed(description="{} has been deleted".format(
                role.name), color=0x00FF68)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Deletes an emoji")
    @app_commands.describe(emoji="Which emoji are you deleting?")
    @app_commands.checks.has_permissions(manage_emojis_and_stickers=True)
    async def emoji(self, ctx: Interaction, emoji: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            try:
                e = emoji.split(':')[-1].rstrip('>')
                emote = self.bot.get_emoji(int(e))
            except:
                emote = utils.get(ctx.guild.emojis, name=emoji)
            embed = Embed(description="{} has been deleted".format(str(emote)), color=0x00FF68)
            await emote.delete()
            await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This emoji doesn't exist in the server", color=Color.red())
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="Deletes a sticker")
    @app_commands.describe(sticker="Which sticker are you deleting?")
    @app_commands.checks.has_permissions(manage_emojis_and_stickers=True)
    async def sticker(self, ctx: Interaction, sticker: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            
            stick = utils.get(ctx.guild.stickers, name=sticker)
            embed = Embed(description="`{}` has been deleted".format(str(stick.name)), color=0x00FF68)
            await stick.delete()
            await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This sticker doesn't exist in the server", color=Color.red())
                await ctx.followup.send(embed=embed)

class Edit_Group(GroupCog, name="edit"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Edits a text/news channel")
    @app_commands.describe(channel="Which channel are you editing?", name="What will be the new name?", nsfw_enabled="Should it be an NSFW channel?", slowmode="What is the slowmode (1hr, 30m, etc) (Max is 6 hours)", category="Place in which category?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def textchannel(self, ctx: Interaction, channel: TextChannel, name: Optional[str] = None, nsfw_enabled: Literal["true", "false"] = None, slowmode: Optional[str] = None, category: Optional[CategoryChannel] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            embed = Embed()
            embed.description = "Channel `{}` has been edited".format(
                channel.name)
            embed.color = Color.green()

            if name:
                await channel.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Category",
                                value=category, inline=True)

            if nsfw_enabled:
                if nsfw_enabled == "True":
                    await channel.edit(nsfw=True)
                    embed.add_field(name="NSFW enabled",
                                    value="Yes", inline=True)
                elif nsfw_enabled == "False":
                    await channel.edit(nsfw=False)
                    embed.add_field(name="NSFW enabled",
                                    value="No", inline=True)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Edit a role")
    @app_commands.describe(role="Which role are you editing?", name="What is the new name?", color="What is the new color? (use HEX codes)", hoisted="Should it be shown in member list?", mentionable="Should it be mentioned?")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role(self, ctx: Interaction, role: Role, name: Optional[str] = None, color: Optional[str] = None, hoisted: Literal["true", "false"] = None, mentionable: Literal["true", "false"] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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
                if hoisted == "true":
                    await role.edit(hoist=True)
                    embed.add_field(name="Hoisted", value="Yes", inline=True)
                elif hoisted == "false":
                    await role.edit(hoist=False)
                    embed.add_field(name="Hoisted", value="No", inline=True)

            if mentionable:
                if mentionable == "true":
                    await role.edit(mentionable=True)
                    embed.add_field(name="Mentionable",
                                    value="Yes", inline=True)
                elif mentionable == "false":
                    await role.edit(mentionable=False)
                    embed.add_field(name="Mentionable",
                                    value="No", inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Edits the server")
    @app_commands.describe(name="What is the new name?", description="What is the new description (only for public servers)", avatar="What is the new server avatar?", banner="What will be the new banner?", verification_level="How high should the verification level be?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def server(self, ctx: Interaction, name: Optional[str] = None, description: Optional[str] = None, avatar:Optional[Attachment]=None, banner:Optional[Attachment]=None, verification_level: Literal['none', 'low', 'medium', 'high', 'highest'] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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
                    embed.add_field(name="Description",
                                    value=description, inline=True)
                else:
                    embed.add_field(name="Description",
                                    value="Your server is not public to have a description edited", inline=True)
            
            if avatar:
                try:
                    avatarbytes=get(avatar.url).content
                    await ctx.guild.edit(icon=avatarbytes)
                    embed.thumbnail(url=avatar.url)
                except:
                    pass

            if banner:
                if ctx.guild.premium_tier < 1:
                    embed.add_field(name="Banner not added", value="This server is not boosted to Tier 1", inline=True)
                else:
                    try:
                        bannerbytes = get(banner.url).content
                        await ctx.guild.edit(banner=bannerbytes)
                        embed.set_image(url=banner.url)
                    except:
                        pass

            if verification_level:
                if verification_level == 'none':
                    await ctx.guild.edit(verification_level=VerificationLevel.none)
                    embed.add_field(name="Verification Level", value="{}\nNo verification required".format(
                        verification_level), inline=True)

                elif verification_level == 'low':
                    await ctx.guild.edit(verification_level=VerificationLevel.low)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified email".format(
                        verification_level), inline=True)

                elif verification_level == 'medium':
                    await ctx.guild.edit(verification_level=VerificationLevel.medium)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified email and be registered on Discord for more than 5 minutes".format(
                        verification_level), inline=True)

                elif verification_level == 'high':
                    await ctx.guild.edit(verification_level=VerificationLevel.high)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified email, be registered on Discord for more than 5 minutes and stay in the server for more than 10 minutes".format(
                        verification_level), inline=True)

                elif verification_level == 'highest':
                    await ctx.guild.edit(verification_level=VerificationLevel.highest)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified phone number".format(
                        verification_level), inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Renames an emoji")
    @app_commands.describe(emoji="What emoji are you renaming?", name="What is the new name?")
    @app_commands.checks.has_permissions(manage_emojis_and_stickers=True)
    async def emoji(self, ctx: Interaction, emoji: str, name:str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            try:
                e = emoji.split(':')[-1].rstrip('>')
                emote = self.bot.get_emoji(int(e))
            except:
                emote = utils.get(ctx.guild.emojis, name=emoji)
            embed = Embed(description="{} has been renamed to {}".format(str(emote), name), color=0x00FF68)
            await emote.edit(name=name)
            await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This emoji doesn't exist in the server", color=Color.red())
                await ctx.followup.send(embed=embed)
            


class Set_Group(GroupCog, name="set"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Set a welcomer and/or leaver channel")
    @app_commands.describe(welcoming_channel="Which channel should alert members when someone join", leaving_channel="Which channel should members when someone leaves?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def welcomer(self, ctx: Interaction, welcoming_channel: Optional[TextChannel] = None, leaving_channel: Optional[TextChannel] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if welcoming_channel == None and leaving_channel == None:
                error = Embed(
                    description="Both options are empty. Please set at least a welcomer or leaving channel", color=Color.red())
                await ctx.followup.send(embed=error)
            else:
                setup = Embed(description="Welcomer channels set",
                              color=ctx.user.color)
                if welcoming_channel:
                    set_welcomer(ctx.guild.id, welcoming_channel.id)
                    setup.add_field(name='Channel welcoming users',
                                    value=welcoming_channel.mention, inline=True)

                if leaving_channel:
                    set_leaver(ctx.guild.id, leaving_channel.id)
                    setup.add_field(name='Channel showing users that left',
                                    value=leaving_channel.mention, inline=True)

                await ctx.followup.send(embed=setup)

    @app_commands.command(description="Set a modlog channel")
    @app_commands.describe(channel="Which channel should log warns, mutes, timeouts, kicks and bans?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def modlog(self, ctx: Interaction, channel: TextChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            set_modloger(ctx.guild.id, channel.id)
            embed = Embed(description='Modlog channel set', color=Color.red())
            embed.add_field(name="Channel selected",
                            value=channel.mention, inline=True)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Set a report channel")
    @app_commands.describe(channel="Which channel should log reports made by members?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def report(self, ctx: Interaction, channel: TextChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            set_reporter(ctx.guild.id, channel.id)
            embed = Embed(description='Report channel set', color=Color.red())
            embed.add_field(name="Channel selected",
                            value=channel.mention, inline=True)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Set a message logging channel")
    @app_commands.describe(channel="Which channel should log edited and deleted messages?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def messagelog(self, ctx: Interaction, channel: TextChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            set_message_logger(ctx.guild.id, channel.id)
            embed = Embed(
                description='Message logging channel set', color=Color.red())
            embed.add_field(name="Channel selected",
                            value=channel.mention, inline=True)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Set a member logging channel")
    @app_commands.describe(channel="Which channel should log changes to member's tag, name, nickname and avatar?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def memberlog(self, ctx: Interaction, channel: TextChannel):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            set_member_logger(ctx.guild.id, channel.id)
            embed = Embed(
                description='Member logging channel set', color=Color.red())
            embed.add_field(name="Channel selected",
                            value=channel.mention, inline=True)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Set a welcoming message when someone joins the server")
    @app_commands.describe(message="What is the new welcoming message", jsonfile="Upload JSON file with the welcoming message")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def welcomingmsg(self, ctx: Interaction, message: Optional[str] = None, jsonfile: Optional[Attachment] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if message == None and jsonfile == None:
                embed = Embed()
                embed.color = Color.red()
                embed.description = "Please use a JSON script or upload a JSON file\nPlease use [Discohook](https://discohook.org/)"
                await ctx.followup.send(embed=embed)

            elif message and jsonfile:
                embed = Embed()
                embed.color = Color.red()
                embed.description = "Please use either a JSON script or upload a JSON file\nPlease use [Discohook](https://discohook.org/)"
                await ctx.followup.send(embed=embed)

            else:
                humans = str(
                    len([member for member in ctx.guild.members if not member.bot]))
                parameters = OrderedDict([("%member%", str(ctx.user)), ("%pfp%", str(ctx.user.display_avatar)), ("%server%", str(ctx.guild.name)), ("%mention%", str(
                    ctx.user.mention)), ("%name%", str(ctx.user.name)), ("%members%", str(ctx.guild.member_count)), ("%humans%", str(humans)), ("%icon%", str(ctx.guild.icon))])
                if message and not jsonfile:
                    json = loads(replace_all(message, parameters))

                elif jsonfile and not message:
                    json_file = jsonfile.url
                    json_request = get(json_file)
                    json_content = replace_all(
                        json_request.content, parameters)
                    json = loads(json_content)

                try:
                    content = json["content"]
                except:
                    pass

                confirm = Embed(
                    description="This is the preview of the welcoming message.\nAre you happy with it?")

                try:
                    embed = Embed.from_dict(json['embeds'][0])
                    view = Confirmation(ctx.user)
                    await ctx.followup.send(content=content, embeds=[embed, confirm], view=view, allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False), ephemeral=True)
                    await view.wait()

                    if view.value == True:
                        if message:
                            set_welcomer_msg(ctx.guild.id, message)
                        elif jsonfile:
                            json_request = get(json_file)
                            json_content = json_request.content
                            jsondict = loads(json_content)
                            set_welcomer_msg(ctx.guild.id, jsondict)

                        embed = Embed(description="Welcoming message set")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)

                    elif view.value == False:
                        embed = Embed(description="Action cancelled")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)
                    else:
                        embed = Embed(description="Timeout")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)

                except:
                    view = Confirmation(ctx.user)
                    await ctx.followup.send(content=content, embed=confirm, allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False), view=view, ephemeral=True)
                    await view.wait()

                    if view.value == None:
                        embed = Embed(description="Timeout")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)
                    elif view.value:
                        if message:
                            set_welcomer_msg(ctx.guild.id, message)
                        elif jsonfile:
                            json_request = get(json_file)
                            json_content = json_request.content
                            jsondict = loads(json_content)
                            set_welcomer_msg(ctx.guild.id, jsondict)

                        embed = Embed(description="Welcoming message set")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)

                    else:
                        embed = Embed(description="Action cancelled")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)


    @app_commands.command(description="Set a leaving message when someone leaves the server")
    @app_commands.describe(message="What is the new leaving message", jsonfile="Upload JSON file with the welcoming message")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def leavingmsg(self, ctx: Interaction, message: Optional[str] = None, jsonfile: Optional[Attachment] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if message == None and jsonfile == None:
                embed = Embed()
                embed.color = Color.red()
                embed.description = "Please use a JSON script or upload a JSON file\nPlease use [Discohook](https://discohook.org/)"
                await ctx.followup.send(embed=embed)

            elif message and jsonfile:
                embed = Embed()
                embed.color = Color.red()
                embed.description = "Please use either a JSON script or upload a JSON file\nPlease use [Discohook](https://discohook.org/)"
                await ctx.followup.send(embed=embed)

            else:
                humans = str(
                    len([member for member in ctx.guild.members if not member.bot]))
                parameters = OrderedDict([("%member%", str(ctx.user)), ("%pfp%", str(ctx.user.display_avatar)), ("%server%", str(ctx.guild.name)), ("%mention%", str(
                    ctx.user.mention)), ("%name%", str(ctx.user.name)), ("%members%", str(ctx.guild.member_count)), ("%humans%", str(humans)), ("%icon%", str(ctx.guild.icon))])
                if message and not jsonfile:
                    json = loads(replace_all(message, parameters))

                elif jsonfile and not message:
                    json_file = jsonfile.url
                    json_request = get(json_file)
                    json_content = replace_all(
                        json_request.content, parameters)
                    json = loads(json_content)

                try:
                    content = json["content"]
                except:
                    pass

                confirm = Embed(
                    description="This is the preview of the leaving message.\nAre you happy with it?")

                try:
                    embed = Embed.from_dict(json['embeds'][0])
                    view = Confirmation(ctx.user)
                    await ctx.followup.send(content=content, embeds=[embed, confirm], view=view, allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False), ephemeral=True)
                    await view.wait()

                    if view.value == True:
                        if message:
                            set_leaving_msg(ctx.guild.id, message)
                        elif jsonfile:
                            json_request = get(json_file)
                            json_content = json_request.content
                            jsondict = loads(json_content)
                            set_leaving_msg(ctx.guild.id, jsondict)

                        embed = Embed(description="Leaving message set")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)

                    elif view.value == False:
                        embed = Embed(description="Action cancelled")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)
                    else:
                        embed = Embed(description="Timeout")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)

                except:
                    view = Confirmation(ctx.user)
                    await ctx.followup.send(content=content, embed=confirm, allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False), view=view, ephemeral=True)
                    await view.wait()

                    if view.value == True:
                        if message:
                            set_leaving_msg(ctx.guild.id, message)
                        elif jsonfile:
                            json_request = get(json_file)
                            json_content = json_request.content
                            jsondict = loads(json_content)
                            set_leaving_msg(ctx.guild.id, jsondict)

                        embed = Embed(description="Leaving message set")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)

                    elif view.value == False:
                        embed = Embed(description="Action cancelled")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)
                    else:
                        embed = Embed(description="Timeout")
                        await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class XP_Group(GroupCog, name="xp"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Blacklists a channel for gaining XP")
    @app_commands.describe(channel="Which channel?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def blacklist(self, ctx: Interaction, channel: TextChannel) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if check_xpblacklist_channel(ctx.guild.id, channel.id) == True:
                embed = Embed(color=Color.red())
                embed.description = "Channel is already XP blacklisted"
                await ctx.followup.send(embed=embed)
            else:
                add_xpblacklist(ctx.guild.id, channel.id)
                embed = Embed(color=Color.random())
                embed.add_field(name="Channel XP blacklisted",
                                value=f"`{channel}` has been added to the XP blacklist", inline=False)
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="Unblacklists a channel for gaining XP")
    @app_commands.describe(channel="Which channel?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def unblacklist(self, ctx: Interaction, channel: TextChannel) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if check_xpblacklist_channel(ctx.guild.id, channel.id) == False:
                embed = Embed(color=Color.red())
                embed.description = "Channel is not in the XP blacklisted"
                embed.color = Color.red()
                await ctx.followup.send(embed=embed)
            else:
                remove_blacklist(ctx.guild.id, channel.id)
                embed = Embed(color=Color.random())
                embed.add_field(name="Channel XP blacklisted",
                                value=f"`{channel}` has been added to the XP blacklist", inline=False)
                await ctx.followup.send(embed=embed)


class manage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Add a role to a member")
    @app_commands.describe(member="Which member?", role="Which role are you adding?")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def addrole(self, ctx: Interaction, member: Member, role: Role):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            await member.add_roles(role)
            embed = Embed(color=Color.random())
            embed.add_field(name=f"Role given",
                            value=f"`{role}` was given to `{member}`", inline=False)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Remove a role from a member")
    @app_commands.describe(member="Which member?", role="Which role are you removing?")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def removerole(self, ctx: Interaction, member: Member, role: Role):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            await member.remove_roles(role)
            embed = Embed(color=Color.random())
            embed.add_field(name=f"Role removed",
                            value=f"`{role}` was removed from `{member}`", inline=False)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Removes a welcoming/modlog/report channel. Set all options to true to remove all")
    @app_commands.describe(welcomer="Remove welcomer channel?", leaving="Remove leaving channel?", modlog="Remove modlog channel?", report="Remove report channel?", memberlog="Remove member logging channel?", messagelog="Remove lessage logging channel?", welcomingmsg="Remove the welcoming message and reset to default", leavingmsg="Remove the leaving message and reset to default")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove(self, ctx: Interaction, welcomer: Optional[bool] = None, leaving: Optional[bool] = None, modlog: Optional[bool] = None, report: Optional[bool] = None, memberlog: Optional[bool] = None, messagelog: Optional[bool] = None, welcomingmsg:Optional[bool]=None, leavingmsg:Optional[bool]=None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if welcomer==None and leaving==None and modlog==None and report == None and welcomingmsg==None and leavingmsg==None:
                error = Embed(description="Please select a channel to remove")
                await ctx.followup.send(embed=error)
            else:
                embed = Embed(description="Channels removed")

                if welcomer == True:

                    wel = remove_welcomer(ctx.guild.id)

                    if wel == False:
                        embed.add_field(
                            name='Welcomer channel removal status', value='Failed. No welcomer channel set', inline=True)
                    else:
                        embed.add_field(name='Welcomer channel removal status',
                                        value='Successful', inline=True)

                if leaving == True:

                    leav = remove_leaver(ctx.guild.id)

                    if leav == False:
                        embed.add_field(
                            name='Leaving channel removal status', value='Failed. No leaving channel set', inline=True)
                    else:
                        embed.add_field(name='Leaving channel removal status',
                                        value='Successful', inline=True)

                if modlog == True:

                    mod = remove_modloger(ctx.guild.id)

                    if mod == False:
                        embed.add_field(
                            name='Modlog channel removal status', value='Failed. No modlog channel set', inline=True)
                    else:
                        embed.add_field(name='Modlog channel removal status',
                                        value='Successful', inline=True)

                if report == True:

                    rep = remove_reporter(ctx.guild.id)

                    if rep == False:
                        embed.add_field(
                            name='Report channel removal status', value='Failed. No report channel set', inline=True)
                    else:
                        embed.add_field(name='Report channel removal status',
                                        value='Successful', inline=True)

                if memberlog == True:

                    rep = remove_memberlog(ctx.guild.id)

                    if rep == False:
                        embed.add_field(
                            name='Member logging channel removal status', value='Failed. No Member logging channel set', inline=True)
                    else:
                        embed.add_field(name='Member logging channel removal status',
                                        value='Successful', inline=True)

                if messagelog == True:

                    rep = remove_messagelog(ctx.guild.id)

                    if rep == False:
                        embed.add_field(
                            name='Message logging channel removal status', value='Failed. No Message logging channel set', inline=True)
                    else:
                        embed.add_field(name='Message logging channel removal status',
                                        value='Successful', inline=True)
                
                if welcomingmsg == True:
                    
                    msg=remove_welcomer_msg(ctx.guild.id)

                    if msg == 0 or None:
                        embed.add_field(
                            name='Welcoming Message removal status', value='Failed. No welcoming message set', inline=True)
                    else:
                        embed.add_field(name='Welcoming Message removal status',
                                        value='Successful', inline=True)

                if leavingmsg == True:

                    leav = remove_welcomer_msg(ctx.guild.id)

                    if leav == 0 or None:
                        embed.add_field(
                            name='Leaving Message removal status', value='Failed. No leaving message set', inline=True)
                    else:
                        embed.add_field(name='Leaving Message removal status',
                                        value='Successful', inline=True)

                await ctx.followup.send(embed=embed)

    @app_commands.command(description="Clone a channel")
    @app_commands.describe(channel="Which channel are you cloning?", name="What is the new name?")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def clone(self, ctx: Interaction, channel: abc.GuildChannel, name: Optional[str] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if name == None:
                name = channel.name

            c = await channel.clone(name=name)

            cloned = Embed(description="{} was cloned as {}".format(
                channel.mention, c.mention))
            cloned.color = Color.random()
            await ctx.followup.send(embed=cloned)


async def setup(bot: Bot):
    await bot.add_cog(manage(bot))
    await bot.add_cog(Create_Group(bot))
    await bot.add_cog(Edit_Group(bot))
    await bot.add_cog(Delete_Group(bot))
    await bot.add_cog(Set_Group(bot))
    await bot.add_cog(XP_Group(bot))
