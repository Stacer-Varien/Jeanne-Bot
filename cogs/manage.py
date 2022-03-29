from urllib import response
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
    async def create_role(self, ctx: Interaction, role_name=SlashOption(description="What will it be named?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
                guild = ctx.guild
                await guild.create_role(name=role_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Role create",
                                value=f"The role named `{role_name}` has been made", inline=False)
                await ctx.followup.send(embed=embed)

    @create_role.error
    async def create_role_error(self, ctxs:Interaction, error):
        if isinstance(error, ApplicationBotMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

    @jeanne_slash(description="Rename a role")
    @has_permissions(manage_roles=True)
    async def rename_role(self, ctx: Interaction, role: Role = SlashOption(description="Which role are you renaming?"), new_name=SlashOption(description="What will it be named?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
                await role.edit(name=new_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Role renamed",
                                value=f"Role has been renamed to `{new_name}`", inline=False)
                await ctx.followup.send(embed=embed)

    @rename_role.error
    async def rename_role_error(self, ctxs:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

    @jeanne_slash(description="Delete a role")
    @has_permissions(manage_roles=True)
    async def delete_role(self, ctx: Interaction, role: Role = SlashOption(description="Which one are you deleting?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
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
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
                await member.add_roles(role)
                embed = Embed(color=0x00FF68)
                embed.add_field(name=f"Role given",
                                value=f"`{role}` was given to `{member}`", inline=False)
                await ctx.followup.send(embed=embed)

    @add_role.error
    async def add_role_error(self, ctxs: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctxs.response.defer()
            await ctxs.followup.send(embed=role_perm)

    @jeanne_slash(description="Remove a role from a member")
    @has_permissions(manage_roles=True)
    async def remove_role(self, ctx: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you delete?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
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
                           ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread],
            description="Choose a channel to rename", required=True), new_name=SlashOption(description="Which channel are you renaming?")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
                await channel.edit(name=new_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Channel renamed",
                                value=f"Channel is now `{new_name}`", inline=False)
                await ctx.followup.send(embed=embed)

    @rename_channel.error
    async def rename_channel_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(channel_perm)

    @jeanne_slash(description="Delete a channel")
    @has_permissions(manage_channels=True)
    async def delete_channel(self, ctx: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread],
            description="Choose a channel to delete")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
                await channel.delete()
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Channel deleted",
                                value=f"`{channel}` has been deleted", inline=False)
                await ctx.followup.send(embed=embed)

    @delete_channel.error
    async def delete_channel_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(channel_perm)

    @jeanne_slash(description='Create a channel')
    @has_permissions(manage_channels=True)
    async def create_channel(self, ctx: Interaction, channel_type=SlashOption(description='Type of channel', choices=['Text Channel', 'Voice Channel', 'Category'], required=True), channel_name=SlashOption(description="Which will you name it?", required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
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
            await ctx.followup.send(channel_perm)

    @jeanne_slash(description="Removes a modlog channel that was set from the database")
    @has_permissions(manage_guild=True)
    async def remove(self, ctx: Interaction, type=SlashOption(choices=['welcomer', 'leaver', 'modlog', 'all'], description='Which one or all?')):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
            if type == 'welcomer':
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM welcomerData WHERE guild_id = {ctx.guild.id}")
                result = cur.fetchone()

                if result == None:
                    await ctx.followup.send("You have no welcomer channel set")

                else:
                    cur.execute(
                        f"SELECT channel_id FROM welcomerData WHERE guild_id = {ctx.guild.id}")
                    result = cur.fetchone()
                    cur.execute(
                        f"DELETE FROM welcomerData WHERE channel_id = {result[0]}")
                    channel = ctx.guild.get_channel(result[0])
                    db.commit()

                welcomer = Embed(color=0x00FF68)
                welcomer.add_field(
                    name="Welcomer channel removed", value=f"{channel.name} been removed from the welcomer database.")
                await ctx.followup.send(embed=welcomer)

            elif type == 'leaver':
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM leaverData WHERE guild_id = {ctx.guild.id}")
                result = cur.fetchone()

                if result == None:
                    await ctx.followup.send("You have no welcomer channel set")

                else:
                    cur.execute(
                        f"SELECT channel_id FROM leaverData WHERE guild_id = {ctx.guild.id}")
                    result = cur.fetchone()
                    cur.execute(
                        f"DELETE FROM leaverData WHERE channel_id = {result[0]}")
                    channel = ctx.guild.get_channel(result[0])
                    db.commit()

                leaver = Embed(color=0x00FF68)
                leaver.add_field(
                    name="Leaver channel removed", value=f"{channel.name} been removed from the leaver database.")
                await ctx.followup.send(embed=leaver)

            elif type == 'modlog':
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM modlogData WHERE guild_id = {ctx.guild.id}")
                result = cur.fetchone()

                if result == None:
                    await ctx.followup.send("You have no modlog channel set")

                else:
                    cur.execute(
                        f"SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}")
                    result = cur.fetchone()
                    cur.execute(
                        f"DELETE FROM modlogData WHERE channel_id = {result[0]}")
                    channel=ctx.guild.get_channel(result[0])
                    db.commit()


                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Modlog channel removed", value=f"{channel.name} been removed from the modlog database.")
                await ctx.followup.send(embed=modlog)

            elif type == 'all':
                
                try:
                    cur = db.cursor()
                    cur.execute(
                        f"SELECT * FROM modlogData WHERE guild_id = {ctx.guild.id}")
                    result = cur.fetchone()

                    if result == None:
                        pass

                    else:
                        cur.execute(
                            f"SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}")
                        result = cur.fetchone()
                        cur.execute(
                            f"DELETE FROM modlogData WHERE channel_id = {result[0]}")
                        channel=ctx.guild.get_channel(result[0])
                        db.commit() 
                except:
                    pass

                try:     
                    cur = db.cursor()
                    cur.execute(
                        f"SELECT * FROM leaverData WHERE guild_id = {ctx.guild.id}")
                    result = cur.fetchone()

                    if result == None:
                        pass

                    else:
                        cur.execute(
                            f"SELECT channel_id FROM leaverData WHERE guild_id = {ctx.guild.id}")
                        result = cur.fetchone()
                        cur.execute(
                            f"DELETE FROM leaverData WHERE channel_id = {result[0]}")
                        channel = ctx.guild.get_channel(result[0])
                        db.commit()
                except:
                    pass

                try:
                    cur = db.cursor()
                    cur.execute(
                        f"SELECT * FROM welcomerData WHERE guild_id = {ctx.guild.id}")
                    result = cur.fetchone()

                    if result == None:
                        pass

                    else:
                        cur.execute(
                            f"SELECT channel_id FROM welcomerData WHERE guild_id = {ctx.guild.id}")
                        result = cur.fetchone()
                        cur.execute(
                            f"DELETE FROM welcomerData WHERE channel_id = {result[0]}")
                        channel = ctx.guild.get_channel(result[0])
                        db.commit()
                except:
                    pass

                all = Embed(color=0x00FF68)
                all.add_field(
                    name="Leaver channel removed", value="All channels that were set for the server have been removed from the database.") 

                await ctx.followup.send(embed=all)

    @remove.error
    async def remove_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=manage_server_perm)

    @jeanne_slash(description="Choose a channel to welcome members")
    @has_permissions(manage_guild=True)
    async def set(self, ctx: Interaction, type=SlashOption(choices=['welcomer', 'leaver', 'modlog'], description="Which one are you setting?", required=True),
                         channel: GuildChannel = SlashOption(
                             channel_types=[ChannelType.text, ChannelType.news],
                             description="Choose a channel")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                pass
        except:
                if type == 'welcomer':
                    cursor = db.execute(
                        "INSERT OR IGNORE INTO welcomerData (guild_id, channel_id) VALUES (?,?)", (ctx.guild.id, channel.id))

                    if cursor.rowcount == 0:
                        db.execute(
                            f"UPDATE welcomerData SET channel_id = {channel.id} WHERE guild_id = {ctx.guild.id}")
                    db.commit()

                    welcomer = Embed(color=0x00FF68)
                    welcomer.add_field(
                        name="Welcomer channel set", value=f"{channel.mention} has been selected to welcomer members in the server.")
                    await ctx.followup.send(embed=welcomer)

                elif type == 'leaver':
                    cursor = db.execute(
                        "INSERT OR IGNORE INTO leaverData (guild_id, channel_id) VALUES (?,?)", (ctx.guild.id, channel.id))

                    if cursor.rowcount == 0:
                        db.execute(
                            f"UPDATE leaverData SET channel_id = {channel.id} WHERE guild_id = {ctx.guild.id}")
                    db.commit()

                    leaver = Embed(color=0x00FF68)
                    leaver.add_field(
                        name="Leave channel set", value=f"{channel.mention} has been selected if someone left the server")
                    await ctx.followup.send(embed=leaver)

                elif type == 'modlog':

                    cursor = db.execute(
                        "INSERT OR IGNORE INTO modlogData (guild_id, channel_id) VALUES (?,?)", (ctx.guild.id, channel.id))

                    if cursor.rowcount == 0:
                        db.execute(
                            f"UPDATE modlogData SET channel_id = {channel.id} WHERE guild_id = {ctx.guild.id}")
                    db.commit()

                    modlog = Embed(color=0x00FF68)
                    modlog.add_field(
                        name="Modlog channel set", value=f"{channel.mention} has been selected to have all moderation actions updated in there.")
                    await ctx.followup.send(embed=modlog)

    @set.error
    async def set_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=manage_server_perm)



def setup(bot):
    bot.add_cog(slashmanage(bot))
