from asyncio import get_event_loop
from functools import partial
from io import BytesIO
import requests
from assets.db_functions import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.abc import GuildChannel
from nextcord.ext.application_checks import *
from PIL import Image

class slashmanage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Create a new role")
    @has_permissions(manage_roles=True)
    async def create_role(self, ctx: Interaction, role_name=SlashOption(description="What will it be named?", required=True), color=SlashOption(description="What color would you like it to be? (use HEX codes)", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if color == None:
                color=Color.default()
            else:
                color = int(color, 16)
            guild = ctx.guild
            await guild.create_role(name=role_name, color=color)
            embed = Embed(color=0x00FF68)
            embed.add_field(name="Role create",
                            value=f"The role named `{role_name}` has been made", inline=False)
            await ctx.followup.send(embed=embed)



    @jeanne_slash(description="Edit a role to change its name and/or color")
    @has_permissions(manage_roles=True)
    async def edit_role(self, ctx: Interaction, role: Role = SlashOption(description="Which role are you editing?"), new_name=SlashOption(description="What will it be named?", required=False), color=SlashOption(description="What will it's new color be (use HEX codes)", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed(title="Role `{}` has been edited".format(role), color=role.color)

            if new_name:
                await role.edit(name=new_name)
                embed.add_field(name="Name changed to:",
                                value=f"`{new_name}`", inline=True)

            if color:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color changed to:",
                                value=f"`{color}`", inline=True)

            await ctx.followup.send(embed=embed)



    @jeanne_slash(description="Delete a role")
    @has_permissions(manage_roles=True)
    async def delete_role(self, ctx: Interaction, role: Role = SlashOption(description="Which one are you deleting?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await role.delete()
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role deleted",
                            value=f"`{role}` has been deleted", inline=False)
            await ctx.followup.send(embed=embed)



    @jeanne_slash(description="Add a role to a member")
    @has_permissions(manage_roles=True)
    async def add_role(self, ctx: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you add?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await member.add_roles(role)
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role given",
                            value=f"`{role}` was given to `{member}`", inline=False)
            await ctx.followup.send(embed=embed)


        

    @jeanne_slash(description="Remove a role from a member")
    @has_permissions(manage_roles=True)
    async def remove_role(self, ctx: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you delete?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await member.remove_roles(role)
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role removed",
                            value=f"`{role}` was removed from `{member}`", inline=False)
            await ctx.followup.send(embed=embed)



    @jeanne_slash(description="Rename a channel")
    @has_permissions(manage_channels=True)
    async def rename_channel(self, ctx: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread, ChannelType.private_thread],
            description="Choose a channel to rename", required=True), new_name=SlashOption(description="Which channel are you renaming?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await channel.edit(name=new_name)
            embed = Embed(color=0x00FF68)
            embed.add_field(name="Channel renamed",
                            value=f"Channel is now `{new_name}`", inline=False)
            await ctx.followup.send(embed=embed)



    @jeanne_slash(description="Delete a channel")
    @has_permissions(manage_channels=True)
    async def delete_channel(self, ctx: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread, ChannelType.private_thread],
            description="Choose a channel to delete")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await channel.delete()
            embed = Embed(color=0x00FF68)
            embed.add_field(name="Channel deleted",
                            value=f"`{channel}` has been deleted", inline=False)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Main create command")
    async def create(self, ctx:Interaction):
        pass

    @create.subcommand(description='Create a channel')
    @has_permissions(manage_channels=True)
    async def channel(self, ctx: Interaction, channel_type=SlashOption(description='Type of channel', choices=['Text Channel', 'Voice Channel', 'Category'], required=True), channel_name=SlashOption(description="What will you name it?", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if channel_type == 'Text Channel':
                    await ctx.guild.create_text_channel(channel_name)
                    embed = Embed(color=0x00FF68)
                    embed.add_field(name="Text channel created",
                                    value=f"A new text channel called **{channel_name}** was created", inline=False)
                    await ctx.followup.send(embed=embed)
            elif channel_type == 'Voice Channel':
                    await ctx.guild.create_voice_channel(channel_name)
                    embed = Embed(color=0x00FF68)
                    embed.add_field(name="Voice channel created",
                                    value=f"A new voice channel called `{channel_name}` was created", inline=False)
                    await ctx.followup.send(embed=embed)
            elif channel_type == 'Category':
                    await ctx.guild.create_category_channel(channel_name)
                    embed = Embed(color=0x00FF68)
                    embed.add_field(name="Category created",
                                    value=f"A new category called **{channel_name}** was created", inline=False)
                    await ctx.followup.send(embed=embed)

    @create.subcommand(description="Create a forum")
    @has_permissions(manage_channels=True)
    async def forum(self, ctx: Interaction, name=SlashOption(description="What will you name it?", required=True)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.guild.create_forum_channel(name=name)
            embed = Embed(color=0x00FF68)
            embed.add_field(name="Forum created",
                            value=f"A new forum called **{name}** was created", inline=False)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Removes a modlog channel that was set from the database")
    @has_permissions(manage_guild=True)
    async def remove(self, ctx: Interaction, type=SlashOption(choices=['welcomer', 'leaver', 'modlog', 'report', 'all'], description='Which one or all?')):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if type == 'welcomer':
                wel=remove_welcomer(ctx.guild.id)

                if wel == False:
                    await ctx.followup.send("You don't have a welcomer channel")
                else:
                    welcomer = Embed(
                        description="Welcomer channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=welcomer)

            elif type == 'leaver':
                leave = remove_leaver(ctx.guild.id)

                if leave == False:
                    await ctx.followup.send("You don't have a leaver channel")
                else:
                    leaver = Embed(
                        description="Leaver channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=leaver)

            elif type == 'modlog':
                modloger = remove_modloger(ctx.guild.id)

                if modloger == False:
                    await ctx.followup.send("You don't have a modlog channel")
                else:
                    modlog = Embed(
                        description="Modlog channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=modlog)

            elif type == 'report':
                reporter = remove_reporter(ctx.guild.id)

                if reporter == False:
                    await ctx.followup.send("You don't have a report channel")
                else:
                    report = Embed(
                        description="Report channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=report)

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
                await ctx.followup.send(embed=all)



    @jeanne_slash(description="Choose a channel to welcome members")
    @has_permissions(manage_guild=True)
    async def set(self, ctx: Interaction, type=SlashOption(choices=['welcomer', 'leaver', 'modlog', 'report_channel'], description="Which one are you setting?", required=True),
                  channel: GuildChannel = SlashOption(
                             channel_types=[
                                 ChannelType.text, ChannelType.news],
                             description="Choose a channel")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if type == 'welcomer':
                    set_welcomer(ctx.guild.id, channel.id)

                    welcomer = Embed(color=0x00FF68)
                    welcomer.add_field(
                        name="Welcomer channel set", value=f"{channel.mention} has been selected to welcomer members in the server.")
                    await ctx.followup.send(embed=welcomer)

            elif type == 'leaver':
                    set_leaver(ctx.guild.id, channel.id)

                    leaver = Embed(color=0x00FF68)
                    leaver.add_field(
                        name="Leave channel set", value=f"{channel.mention} has been selected if someone left the server")
                    await ctx.followup.send(embed=leaver)

            elif type == 'modlog':
                    set_modloger(ctx.guild.id, channel.id)

                    modlog = Embed(color=0x00FF68)
                    modlog.add_field(
                        name="Modlog channel set", value=f"{channel.mention} has been selected to have all moderation actions updated in there.")
                    await ctx.followup.send(embed=modlog)
            
            elif type == 'report_channel':
                set_reporter(ctx.guild.id, channel.id)

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                        name="Report channel set", value=f"{channel.mention} has been selected to have all reported members in there.")
                await ctx.followup.send(embed=modlog)

    @jeanne_slash(description="Make a channel NSFW enabled/disabled")
    @has_permissions(manage_guild=True)
    async def switch_nsfw(self, ctx:Interaction, channel:GuildChannel=SlashOption(channel_types=[ChannelType.text, ChannelType.news])):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if channel.is_nsfw() == False:
                await channel.edit(nsfw=True)
                switched = Embed(description="{} is now NSFW enabled".format(channel.mention), color=0x00FF68)
                await ctx.followup.send(embed=switched)
            elif channel.is_nsfw() == True:
                await channel.edit(nsfw=False)
                switched = Embed(description="{} is now NSFW disabled".format(
                    channel.mention), color=0x00FF68)
                await ctx.followup.send(embed=switched)
    
    @jeanne_slash(description="Change the server's verification level")
    @has_permissions(manage_guild=True)
    async def change_verification(self, ctx:Interaction, level=SlashOption(choices=['none', 'low', 'medium', 'high', 'highest'])):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            verification=Embed(title="Server Verification Changed", color=0x00FF68)

            if level == 'none':
                await ctx.guild.edit(verification_level=VerificationLevel.none)
                verification.description="No verification required"
                await ctx.followup.send(embed=verification)
            
            elif level == 'low':
                await ctx.guild.edit(verification_level=VerificationLevel.low)
                verification.description="Members must have a verified email"
                await ctx.followup.send(embed=verification)
               
            elif level == 'medium':
                await ctx.guild.edit(verification_level=VerificationLevel.medium)
                verification.description="Members must have a verified email and be registered on Discord for more than 5 minutes"
                await ctx.followup.send(embed=verification)

            elif level == 'high':
                await ctx.guild.edit(verification_level=VerificationLevel.high)
                verification.description="Members must have a verified email, be registered on Discord for more than 5 minutes and stay in the server for more than 10 minutes"
                await ctx.followup.send(embed=verification)

            elif level == 'highest':
                await ctx.guild.edit(verification_level=VerificationLevel.highest)
                verification.description="Members must have a verified phone number"
                await ctx.followup.send(embed=verification)

    @jeanne_slash(description="Change the server's name and/or description")
    @has_permissions(manage_guild=True)
    async def edit_server(self, ctx: Interaction, name=SlashOption(required=False), description=SlashOption(required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            edit=Embed(description="Changes made on the server", color=Color.brand_green())

            if name:
                await ctx.guild.edit(name=name)
                edit.add_field(name="New Name:", value=name, inline=False)

            if description:
                if "COMMUNITY" in ctx.guild.features:
                    await ctx.guild.edit(description=description)
                    edit.add_field(name="New Description:", value=name, inline=False)
                else:
                    edit.add_field(name="Unable to change description", value="Server is not a community server", inline=False)

            await ctx.followup.send(embed=edit)

    @jeanne_slash(description="Clone a channel")
    @has_permissions(manage_channels=True)
    async def clone(self, ctx:Interaction, channel:GuildChannel=SlashOption(channel_types=[ChannelType.news, ChannelType.text, ChannelType.voice, ChannelType.stage_voice]), name=SlashOption(required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if name==None:
                name=channel.name

            c = await channel.clone(name=name)

            cloned=Embed(description="{} was cloned as {}".format(channel.mention, c.mention))
            await ctx.followup.send(embed=cloned)


def setup(bot):
    bot.add_cog(slashmanage(bot))
