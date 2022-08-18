from assets.db_functions import *
from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.abc import GuildChannel
from assets.errormsgs import *
from nextcord.ext.application_checks import *

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

    @create_role.error
    async def create_role_error(self, ctxs: Interaction, error):
        if isinstance(error, ApplicationBotMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

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

    @edit_role.error
    async def edit_role_error(self, ctxs: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

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

    @delete_role.error
    async def delete_role_error(self, ctxs: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

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

    @add_role.error
    async def add_role_error(self, ctxs: Interaction, error):
        await ctxs.response.defer()
        if isinstance(error, ApplicationMissingPermissions):
            await ctxs.followup.send(embed=role_perm)
        

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

    @remove_role.error
    async def remove_role_error(self, ctxs: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

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

    @rename_channel.error
    async def rename_channel_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=channel_perm)

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

    @delete_channel.error
    async def delete_channel_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=channel_perm)

    @jeanne_slash(description='Create a channel')
    @has_permissions(manage_channels=True)
    async def create_channel(self, ctx: Interaction, channel_type=SlashOption(description='Type of channel', choices=['Text Channel', 'Voice Channel', 'Category'], required=True), channel_name=SlashOption(description="Which will you name it?", required=True)):
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

    @create_channel.error
    async def create_channel_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=channel_perm)

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

    @remove.error
    async def remove_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=manage_server_perm)

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


    @set.error
    async def set_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.send(embed=manage_server_perm)


def setup(bot):
    bot.add_cog(slashmanage(bot))
