from config import db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.abc import GuildChannel
from assets.errormsgs import *

class slashmanage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Create a new role")
    async def create_role(self, interaction: Interaction, role_name=SlashOption(description="What will it be named?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_roles is True:
                guild = interaction.guild
                await guild.create_role(name=role_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Role create",
                                value=f"The role named `{role_name}` has been made", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_roles is False:
                await interaction.followup.send(embed=role_perm)

    @jeanne_slash(description="Rename a role")
    async def rename_role(self, interaction: Interaction, role: Role = SlashOption(description="Which role are you renaming?"), new_name=SlashOption(description="What will it be named?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_roles is True:
                await role.edit(name=new_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Role renamed",
                                value=f"Role has been renamed to `{new_name}`", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_roles is False:
                await interaction.followup.send(embed=role_perm)

    @jeanne_slash(description="Delete a role")
    async def delete_role(self, interaction: Interaction, role: Role = SlashOption(description="Which one are you deleting?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_roles is True:
                await role.delete()
                embed = Embed(color=0x00FF68)
                embed.add_field(name=f"Role deleted",
                                value=f"`{role}` has been deleted", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_roles is False:
                await interaction.followup.send(embed=role_perm)

    @jeanne_slash(description="Add a role to a member")
    async def add_role(self, interaction: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you add?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_roles is True:
                await member.add_roles(role)
                embed = Embed(color=0x00FF68)
                embed.add_field(name=f"Role given",
                                value=f"`{role}` was given to `{member}`", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_roles is False:
                await interaction.followup.send(embed=role_perm)

    @jeanne_slash(description="Remove a role from a member")
    async def remove_role(self, interaction: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you delete?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_roles is True:
                await member.remove_roles(role)
                embed = Embed(color=0x00FF68)
                embed.add_field(name=f"Role removed",
                                value=f"`{role}` was removed from `{member}`", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_roles is False:
                await interaction.followup.send(embed=role_perm)

    @jeanne_slash(description="Rename a channel")
    async def rename_channel(self, interaction: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread],
            description="Choose a channel to rename", required=True), new_name=SlashOption(description="Which channel are you renaming?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_channels is True:
                await channel.edit(name=new_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Channel renamed",
                                value=f"Channel is now `{new_name}`", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_channels is False:
                await interaction.followup.send(embed=channel_perm)

    @jeanne_slash(description="Delete a channel")
    async def delete_channel(self, interaction: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread],
            description="Choose a channel to delete")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_channels is True:
                await channel.delete()
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Channel deleted",
                                value=f"`{channel}` has been deleted", inline=False)
                await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_channels is False:
                await interaction.followup.send(embed=channel_perm)

    @jeanne_slash(description='Create a channel')
    async def create_channel(self, interaction: Interaction, channel_type=SlashOption(description='Type of channel', choices=['Text Channel', 'Voice Channel', 'Category'], required=True), channel_name=SlashOption(description="Which will you name it?", required=True)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_channels is True:
                if channel_type == 'Text Channel':
                    await interaction.guild.create_text_channel(channel_name)
                    embed = Embed(color=0x00FF68)
                    embed.add_field(name="Text channel created",
                                    value=f"A new text channel called **{channel_name}** was created", inline=False)
                    await interaction.followup.send(embed=embed)
                elif channel_type == 'Voice Channel':
                    await interaction.guild.create_voice_channel(channel_name)
                    embed = Embed(color=0x00FF68)
                    embed.add_field(name="Voice channel created",
                                    value=f"A new voice channel called `{channel_name}` was created", inline=False)
                    await interaction.followup.send(embed=embed)
                elif channel_type == 'Category':
                    await interaction.guild.create_category_channel(channel_name)
                    embed = Embed(color=0x00FF68)
                    embed.add_field(name="Category created",
                                    value=f"A new category called **{channel_name}** was created", inline=False)
                    await interaction.followup.send(embed=embed)
            elif interaction.permissions.manage_channels is False:
                await interaction.followup.send(embed=channel_perm)

    @jeanne_slash(description="Choose a channel for logging warns, mutes and bans")
    async def set_modlog(self, interaction: Interaction,
                         channel: GuildChannel = SlashOption(
                             channel_types=[ChannelType.text],
                             description="Choose a channel to log moderation events")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_guild is True:
                cursor = db.execute(
                    "INSERT OR IGNORE INTO modlogData (guild_id, channel_id) VALUES (?,?)", (interaction.guild.id, channel.id))

                if cursor.rowcount==0:
                    db.execute(
                        f"UPDATE modlogData SET channel_id = {channel.id} WHERE guild_id = {interaction.guild.id}")
                db.commit()

                modlog = Embed(color=0x00FF68)
                modlog.add_field(name="Modlog channel set", value=f"{channel.mention} has been selected to have all moderation actions updated in there.")
                await interaction.followup.send(embed=modlog)
            elif interaction.permissions.manage_guild is False:
                await interaction.followup.send(embed=manage_server_perm)

    @jeanne_slash(description="Removes a modlog channel that was set from the database")
    async def remove_modlog(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_guild is True:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM modlogData WHERE guild_id = {interaction.guild.id}")
                result = cur.fetchone()

                if result == None:
                    await interaction.followup.send("You have no modlog channel set")

                else:
                    cur.execute(
                        f"SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}")
                    result = cur.fetchone()
                    cur.execute(
                        f"DELETE FROM modlogData WHERE channel_id = {result[0]}")
                    channel=interaction.guild.get_channel(result[0])
                    db.commit()


                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Modlog channel removed", value=f"{channel.name} been removed from the modlog database.")
                await interaction.followup.send(embed=modlog)
            elif interaction.permissions.manage_guild is False:
                await interaction.followup.send(embed=manage_server_perm)

    @jeanne_slash(description="Choose a channel to welcome members")
    async def set_welcomer(self, interaction: Interaction,
                         channel: GuildChannel = SlashOption(
                             channel_types=[ChannelType.text],
                             description="Choose a channel to welcome members")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_guild is True:
                cursor = db.execute(
                    "INSERT OR IGNORE INTO welcomerData (guild_id, channel_id) VALUES (?,?)", (interaction.guild.id, channel.id))

                if cursor.rowcount == 0:
                    db.execute(
                        f"UPDATE welcomerData SET channel_id = {channel.id} WHERE guild_id = {interaction.guild.id}")
                db.commit()

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Welcomer channel set", value=f"{channel.mention} has been selected to welcomer members in the server.")
                await interaction.followup.send(embed=modlog)
            elif interaction.permissions.manage_guild is False:
                await interaction.followup.send(embed=manage_server_perm)

    @jeanne_slash(description="Choose a channel when someone leaves")
    async def set_leaver(self, interaction: Interaction,
                         channel: GuildChannel = SlashOption(
                             channel_types=[ChannelType.text],
                             description="Choose a channel to alert someone left")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_guild is True:
                cursor = db.execute(
                    "INSERT OR IGNORE INTO leaverData (guild_id, channel_id) VALUES (?,?)", (interaction.guild.id, channel.id))

                if cursor.rowcount == 0:
                    db.execute(
                        f"UPDATE leaverData SET channel_id = {channel.id} WHERE guild_id = {interaction.guild.id}")
                db.commit()

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Leave channel set", value=f"{channel.mention} has been selected if someone left the server")
                await interaction.followup.send(embed=modlog)
            elif interaction.permissions.manage_guild is False:
                await interaction.followup.send(embed=manage_server_perm)

    @jeanne_slash(description="Removes a welcomer channel that was set from the database")
    async def remove_welcomer(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_guild is True:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM welcomerData WHERE guild_id = {interaction.guild.id}")
                result = cur.fetchone()

                if result == None:
                    await interaction.followup.send("You have no welcomer channel set")

                else:
                    cur.execute(
                        f"SELECT channel_id FROM welcomerData WHERE guild_id = {interaction.guild.id}")
                    result = cur.fetchone()
                    cur.execute(
                        f"DELETE FROM welcomerData WHERE channel_id = {result[0]}")
                    channel = interaction.guild.get_channel(result[0])
                    db.commit()

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Welcomer channel removed", value=f"{channel.name} been removed from the welcomer database.")
                await interaction.followup.send(embed=modlog)
            elif interaction.permissions.manage_guild is False:
                await interaction.followup.send(embed=manage_server_perm)

    @jeanne_slash(description="Removes a leaver channel that was set from the database")
    async def remove_leaver(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                pass
        except:
            if interaction.permissions.manage_guild is True:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM leaverData WHERE guild_id = {interaction.guild.id}")
                result = cur.fetchone()

                if result == None:
                    await interaction.followup.send("You have no welcomer channel set")

                else:
                    cur.execute(
                        f"SELECT channel_id FROM leaverData WHERE guild_id = {interaction.guild.id}")
                    result = cur.fetchone()
                    cur.execute(
                        f"DELETE FROM leaverData WHERE channel_id = {result[0]}")
                    channel = interaction.guild.get_channel(result[0])
                    db.commit()

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Leaver channel removed", value=f"{channel.name} been removed from the leaver database.")
                await interaction.followup.send(embed=modlog)
            elif interaction.permissions.manage_guild is False:
                await interaction.followup.send(embed=manage_server_perm)

def setup(bot):
    bot.add_cog(slashmanage(bot))
