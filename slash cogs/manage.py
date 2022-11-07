from db_functions import *
from discord import *
from discord.ext.commands import Cog, Bot, Context, hybrid_command, has_permissions, GroupCog, command, Group, group, hybrid_group
from humanfriendly import format_timespan, parse_timespan
from typing import Optional, Literal
from discord_argparse import ArgumentConverter, OptionalArgument, RequiredArgument



class Create_Group(GroupCog, name="create"):
    def __init__(self, bot:Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.command(description="Creates a text channel")
    @has_permissions(manage_channels=True)
    async def text_channel(self, ctx: Interaction, name: str, category: Optional[CategoryChannel] = None, slowmode: str = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:

            embed = Embed()
            embed.color = Color.green()
            embed.description = "Text Channel `{}` has been created".format(
                name)

            channel = await ctx.guild.create_text_channel(name=name)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description='Create a voice channel')
    @has_permissions(manage_channels=True)
    async def voice_channel(self, ctx: Interaction, name: str, category: Optional[CategoryChannel] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Voice Channel `{}` has been created".format(
                name)
            embed.color = Color.green()

            channel = await ctx.guild.create_voice_channel(name=name)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description='Create a category')
    @has_permissions(manage_channels=True)
    async def category(self, ctx: Interaction, name: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.guild.create_category(name=name)
            embed = Embed()
            embed.description = "Category `{}` has been created".format(name)
            embed.color = Color.green()

            await ctx.followup.send(embed=embed)

    @app_commands.command(description='Create a stage channel')
    @has_permissions(manage_channels=True)
    async def stage_channel(self, ctx: Interaction, name: str, topic: str, category: CategoryChannel):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.guild.create_stage_channel(name=name, topic=topic, category=category)
            embed = Embed()
            embed.description = "Stage channel `{}` has been created".format(
                name)
            embed.color = Color.green()

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Create a forum")
    @has_permissions(manage_channels=True)
    async def forum(self, ctx: Interaction, name: str, topic: str, category:CategoryChannel):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            forum = await ctx.guild.create_forum(name=name, topic=topic)
            embed = Embed()
            embed.description = "Forum `{}` has been created".format(
                forum.name)
            embed.color = Color.green()
            if category:
                await forum.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Create a role")
    @has_permissions(manage_roles=True)
    async def role(self, ctx: Interaction, name:str, color:str, hoisted:Literal["true", "false"]=None, mentionable:Literal["true", "false"]=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            role = await ctx.guild.create_role(name=name)
            embed = Embed()
            embed.description = "Role `{}` has been created".format(name)
            embed.color = Color.green()

            if color:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)

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
    @has_permissions(create_public_threads=True)
    async def thread(self, ctx: Interaction, name: str, channel:TextChannel, message_id:int, slowmode: Optional[str]=None):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            channel_:TextChannel=await ctx.guild.get_channel(channel.id)
            message = await channel_.fetch_message(message_id)
            thread = await ctx.channel.create_thread(name=name, message=message, type=ChannelType.public_thread)

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

class Delete_Group(GroupCog, name="delete"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Deletes a channel")
    @has_permissions(manage_channels=True)
    async def channel(self, ctx: Interaction, channel: abc.GuildChannel):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await channel.delete()
            embed = Embed(description="{} has been deleted".format(
                channel.name), color=0x00FF68)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Deletes a role")
    @has_permissions(manage_channels=True)
    async def role(self, ctx: Interaction, role: Role):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await role.delete()
            embed = Embed(description="{} has been deleted".format(
                role.name), color=0x00FF68)
            await ctx.followup.send(embed=embed)

class Edit_Group(GroupCog, name="edit"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Edits a text/news channel")
    @has_permissions(manage_channels=True)
    async def text_channel(self, ctx: Interaction, channel: TextChannel, name: Optional[str]=None, nsfw_enabled:Literal["true", "false"]=None, slowmode: Optional[str]=None, category: Optional[CategoryChannel]=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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

    @app_commands.command(description="Edits a thread")
    @has_permissions(manage_channels=True)
    async def thread(self, ctx: Interaction, thread: Thread, name: Optional[str]=None, slowmode: Optional[str]=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Thread `{}` has been edited".format(
                thread.name)
            embed.color = Color.green()

            if name:
                await thread.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Edit a role")
    @has_permissions(manage_roles=True)
    async def role(self, ctx: Interaction, role: Role, name: Optional[str]=None, color:Optional[str]=None, hoisted:Literal["true", "false"]=None, mentionable:Literal["true", "false"]=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Role `{}` has been edited".format(role.name)
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
    @has_permissions(manage_guild=True)
    async def server(self, ctx: Interaction, name: Optional[str]=None, description: Optional[str]=None, verification_level:Literal['none', 'low', 'medium', 'high', 'highest']=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
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

    @app_commands.command(description="Edits a forum")
    @has_permissions(manage_channels=True)
    async def forum(self, ctx: Interaction, forum: Literal[ChannelType.forum], name: Optional[str]=None, topic: Optional[str]=None, category: CategoryChannel=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:

            embed = Embed()
            embed.description = "Forum {} has been edited".format(forum.name)
            embed.color = Color.green()

            if name:
                await forum.edit(name=name)
                embed.add_field(name="Name",
                                value=name, inline=True)

            if topic:
                await forum.edit(topic=topic)
                embed.add_field(name="Topic",
                                value=topic, inline=True)

            if category:
                await forum.edit(category=category)
                embed.add_field(name="Category",
                                value=category, inline=True)

            await ctx.followup.send(embed=embed)

class manage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @hybrid_command(description="Add a role to a member", aliases=['ar', 'addrole'])
    @has_permissions(manage_roles=True)
    async def add_role(self, ctx: Context, member: Member, role: Role):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await member.add_roles(role)
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role given",
                            value=f"`{role}` was given to `{member}`", inline=False)
            await ctx.send(embed=embed)

    @hybrid_command(description="Remove a role from a member", aliases=['rr', 'removerole'])
    @has_permissions(manage_roles=True)
    async def remove_role(self, ctx: Context, member: Member, role: Role):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await member.remove_roles(role)
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role removed",
                            value=f"`{role}` was removed from `{member}`", inline=False)
            await ctx.send(embed=embed)

    @group(aliases=['make'], invoke_without_command=True)
    async def create(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="```create text_channel NAME CATEGORY SLOWMODE\ncreate voice_channel NAME CATEGORY\ncreate category NAME\ncreate stage_channel NAME TOPIC CATEGORY\ncreate forum NAME TOPIC CATEGORY\ncreate role NAME COLOR HOISTED MENTIONABLE\ncreate thread NAME MESSAGE_ID SLOWMODE```")
            await ctx.send(embed=embed)
    
    create_channel = ArgumentConverter(category=OptionalArgument(
        CategoryChannel, default=None), slowmode=OptionalArgument(str, default=None))

    @create.command(aliases=['txtch', 'tc', 'textchannel'])
    @has_permissions(manage_channels=True)
    async def text_channel(self, ctx: Context, name: str, *, params: create_channel=create_channel.defaults()):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:

            embed = Embed()
            embed.color = Color.green()
            embed.description = "Text Channel `{}` has been created".format(
                name)

            channel = await ctx.guild.create_text_channel(name=name)

            try:
                category:CategoryChannel = params["category"]
                await channel.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)
            except:
                pass

            try:
                slowmode:str = params["slowmode"]
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)
            except:
                pass             

            await ctx.send(embed=embed)

    @create.command(description='Create a category', aliases=['cat', 'catch'])
    @has_permissions(manage_channels=True)
    async def category(self, ctx: Context, name: str):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await ctx.guild.create_category(name=name)
            embed = Embed()
            embed.description = "Category `{}` has been created".format(name)
            embed.color = Color.green()

            await ctx.send(embed=embed)

    create_stage_channel = ArgumentConverter(topic=RequiredArgument(
        str), category=OptionalArgument(CategoryChannel, default=None))

    @create.command(aliases=['stage', 'stagech', 'stagechannel'])
    @has_permissions(manage_channels=True)
    async def stage_channel(self, ctx: Context, name: str, params: create_stage_channel = create_stage_channel.defaults()) -> None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            topic:str=params['topic']
            channel = await ctx.guild.create_stage_channel(name=name, topic=topic)
                
            embed = Embed()
            embed.description = "Stage channel `{}` has been created".format(
                name)
            embed.color = Color.green()

            try:
                category: CategoryChannel = params['category']
                await channel.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)
            except:
                pass

            await ctx.send(embed=embed)

    create_forum = ArgumentConverter(topic=RequiredArgument(
        str), category=OptionalArgument(CategoryChannel, default=None))

    @create.command()
    @has_permissions(manage_channels=True)
    async def forum(self, ctx: Context, name: str, *, params:create_forum=create_forum.defaults()) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            topic:str=params['topic']
            forum = await ctx.guild.create_forum(name=name, topic=topic)
            embed = Embed()
            embed.description = "Forum `{}` has been created".format(
                forum.name)
            embed.color = Color.green()
            try:
                category: CategoryChannel = params['category']
                await forum.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)
            except:
                pass

            await ctx.send(embed=embed)

    create_role = ArgumentConverter(name=RequiredArgument(str),color=OptionalArgument(str, default=Color.default()), hoisted=OptionalArgument(bool, default=False), mentioned=OptionalArgument(bool, default=False))

    @create.command(aliases=['r'])
    @has_permissions(manage_roles=True)
    async def role(self, ctx: Context, *,params:create_role=create_role.defaults()) -> None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed()
            try:
                name:str=params['name']
                role = await ctx.guild.create_role(name=name)
                embed.description = "Role `{}` has been created".format(name)
                embed.color = Color.green()

                try:
                    color=params['color']
                    await role.edit(color=int(color, 16))
                    embed.add_field(name="Color", value=color, inline=True)
                except:
                    pass

                try:
                    hoisted:bool=params['hoisted']
                    if hoisted == True:
                        await role.edit(hoist=True)
                        embed.add_field(name="Hoisted", value="Yes", inline=True)
                    elif hoisted == False:
                        pass
                except:
                    pass
                try:
                    mentionable:bool=params['mentioned']
                    if mentionable == True:
                        await role.edit(mentionable=True)
                        embed.add_field(name="Mentionable",
                                        value="Yes", inline=True)
                    elif mentionable == False:
                        pass
                
                except:
                    pass

                await ctx.send(embed=embed)
            except Exception as e:
                embed.description=e
                embed.color=Color.red()
                await ctx.send(embed=embed)

    @create.command(description="Makes a thread channel")
    @has_permissions(create_public_threads=True)
    async def thread(self, ctx: Context, name: str, message_id: int, slowmode: Optional[str] =None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            message = await ctx.channel.fetch_message(message_id)
            thread = await ctx.channel.create_thread(name=name, message=message, type=ChannelType.public_thread)

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

            await ctx.send(embed=embed)

    @group(invoke_without_command=True, aliases=['del'])
    async def delete(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="```delete channel CHANNEL\ndelete role ROLE```")
            await ctx.send(embed=embed)

    @delete.command(aliases=['ch'])
    @has_permissions(manage_channels=True)
    async def channel(self, ctx: Context, channel: abc.GuildChannel):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await channel.delete()
            embed = Embed(description="{} has been deleted".format(
                channel.name), color=0x00FF68)
            await ctx.send(embed=embed)

    @delete.command(aliases=['r'])
    @has_permissions(manage_channels=True)
    async def role(self, ctx: Context, role: Role):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            await role.delete()
            embed = Embed(description="{} has been deleted".format(
                role.name), color=0x00FF68)
            await ctx.send(embed=embed)

    @group(invoke_without_command=True)
    async def edit(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="```edit text_channel CHANNEL NAME NSFW_ENABLED SLOWMODE CATEGORY\nedit thread THREAD NAME SLOWMODE```")
            await ctx.send(embed=embed)

    @edit.command(aliases=['txtch', 'textchannel', 'tch'])
    @has_permissions(manage_channels=True)
    async def text_channel(self, ctx: Context, channel: TextChannel, *, name: Optional[str] =None, nsfw_enabled: Literal["true", "false"]=None, slowmode: Optional[str]=None, category: Optional[CategoryChannel]=None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
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

            await ctx.send(embed=embed)

    @edit.command()
    @has_permissions(manage_channels=True)
    async def thread(self, ctx: Context, thread: Thread, *, name: Optional[str] =None, slowmode: Optional[str]=None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Thread `{}` has been edited".format(
                thread.name)
            embed.color = Color.green()

            if name:
                await thread.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.send(embed=embed)

    @edit.command(description="Edit a role", aliases=['r'])
    @has_permissions(manage_roles=True)
    async def role(self, ctx: Context, role: Role, *, name: Optional[str] = None, color=None, hoisted: Literal["True", "False"]=None, mentionable:Literal["True", "False"]=None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Role `{}` has been edited".format(role.name)
            embed.color = Color.green()

            if name:
                await role.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if color:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)

            if hoisted:
                if hoisted == "True":
                    await role.edit(hoist=True)
                    embed.add_field(name="Hoisted", value="Yes", inline=True)
                elif hoisted == "False":
                    await role.edit(hoist=False)
                    embed.add_field(name="Hoisted", value="No", inline=True)

            if mentionable:
                if mentionable == "True":
                    await role.edit(mentionable=True)
                    embed.add_field(name="Mentionable",
                                    value="Yes", inline=True)
                elif mentionable == "False":
                    await role.edit(mentionable=False)
                    embed.add_field(name="Mentionable",
                                    value="No", inline=True)

            await ctx.send(embed=embed)

    @edit.command()
    @has_permissions(manage_guild=True)
    async def server(self, ctx: Context, *, name: Optional[str] = None, description: Optional[str] = None, verification_level: Literal['none', 'low', 'medium', 'high', 'highest']=None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
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

            await ctx.send(embed=embed)

    @edit.command(description="Edits a forum")
    @has_permissions(manage_channels=True)
    async def forum_1(self, ctx: Context, forum: ForumChannel, *, name: Optional[str] = None, topic: Optional[str] = None, category: Optional[CategoryChannel] = None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:

            embed = Embed()
            embed.description = "Forum {} has been edited".format(forum.name)
            embed.color = Color.green()

            if name:
                await forum.edit(name=name)
                embed.add_field(name="Name",
                                value=name, inline=True)

            if topic:
                await forum.edit(topic=topic)
                embed.add_field(name="Topic",
                                value=topic, inline=True)

            if category:
                await forum.edit(category=category)
                embed.add_field(name="Category",
                                value=category, inline=True)

            await ctx.send(embed=embed)

    @hybrid_command(description="Removes a welcoming/modlog/report channel that was set from the database")
    @has_permissions(manage_guild=True)
    async def remove(self, ctx: Context, type: Literal['welcomer', 'leaver', 'modlog', 'report', 'all']):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if type == 'welcomer':
                wel = remove_welcomer(ctx.guild.id)

                if wel == False:
                    await ctx.send("You don't have a welcomer channel")
                else:
                    welcomer = Embed(
                        description="Welcomer channel removed", color=0x00FF68)
                    await ctx.send(embed=welcomer)

            elif type == 'leaver':
                leave = remove_leaver(ctx.guild.id)

                if leave == False:
                    await ctx.send("You don't have a leaver channel")
                else:
                    leaver = Embed(
                        description="Leaver channel removed", color=0x00FF68)
                    await ctx.send(embed=leaver)

            elif type == 'modlog':
                modloger = remove_modloger(ctx.guild.id)

                if modloger == False:
                    await ctx.send("You don't have a modlog channel")
                else:
                    modlog = Embed(
                        description="Modlog channel removed", color=0x00FF68)
                    await ctx.send(embed=modlog)

            elif type == 'report':
                reporter = remove_reporter(ctx.guild.id)

                if reporter == False:
                    await ctx.send("You don't have a report channel")
                else:
                    report = Embed(
                        description="Report channel removed", color=0x00FF68)
                    await ctx.send(embed=report)

            elif type == 'all':

                try:
                    remove_welcomer(ctx.guild.id) is True
                except:
                    pass

                try:
                    remove_leaver(ctx.guild.id) is True
                except:
                    pass

                try:
                    remove_modloger(ctx.guild.id) is True
                except:
                    pass

                try:
                    remove_reporter(ctx.guild.id) is True
                except:
                    pass

                all = Embed(
                    description='All channels that were set for the server have been removed from the database.', color=0x00FF68)
                await ctx.send(embed=all)

    @hybrid_group(description="Main set command")
    async def set(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands for this is:",
                          description="```set welcomer CHANNEL\nset leaver CHANNEL\nset modlog CHANNEL\nset report_channel CHANNEL```")
            await ctx.send(embed=embed)

    @set.command(description="Set a welcomer/modlog/report channel")
    @has_permissions(manage_guild=True)
    async def log_channel(self, ctx: Context, type: Literal['welcomer', 'leaver', 'modlog', 'report_channel'], *,
                          channel: TextChannel):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if type == 'welcomer':
                set_welcomer(ctx.guild.id, channel.id)

                welcomer = Embed(color=0x00FF68)
                welcomer.add_field(
                    name="Welcomer channel set", value=f"{channel.mention} has been selected to welcomer members in the server.")
                await ctx.send(embed=welcomer)

            elif type == 'leaver':
                set_leaver(ctx.guild.id, channel.id)

                leaver = Embed(color=0x00FF68)
                leaver.add_field(
                    name="Leave channel set", value=f"{channel.mention} has been selected if someone left the server")
                await ctx.send(embed=leaver)

            elif type == 'modlog':
                set_modloger(ctx.guild.id, channel.id)

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Modlog channel set", value=f"{channel.mention} has been selected to have all moderation actions updated in there.")
                await ctx.send(embed=modlog)

            elif type == 'report_channel':
                set_reporter(ctx.guild.id, channel.id)

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Report channel set", value=f"{channel.mention} has been selected to have all reported members in there.")
                await ctx.send(embed=modlog)

    @hybrid_command(description="Clone a channel", aliases=['copy'])
    @has_permissions(manage_channels=True)
    async def clone(self, ctx: Context, channel: abc.GuildChannel, name: Optional[str] =None) -> None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if name == None:
                name = channel.name

            c = await channel.clone(name=name)

            cloned = Embed(description="{} was cloned as {}".format(
                channel.mention, c.mention))
            await ctx.send(embed=cloned)


async def setup(bot: Bot):
    await bot.add_cog(manage(bot))
    await bot.add_cog(Create_Group(bot))
    await bot.add_cog(Edit_Group(bot))
    await bot.add_cog(Delete_Group(bot))


#needs more work
#must not forget about https://github.com/lukeciel/discord-argparse
