from aiosqlite import connect
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.abc import GuildChannel
from assets.errormsgs import channel_perm, role_perm

db=connect("/home/jeanne/database.db")
class slashmanage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Create a new role")
    async def create_role(self, interaction: Interaction, role_name=SlashOption(description="What will it be named?")):
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
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=role_perm)

    @jeanne_slash(description="Rename a role")
    async def rename_role(self, interaction: Interaction, role: Role = SlashOption(description="Which role are you renaming?"), new_name=SlashOption(description="What will it be named?")):
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
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=role_perm)

    @jeanne_slash(description="Delete a role")
    async def delete_role(self, interaction: Interaction, role: Role = SlashOption(description="Which one are you deleting?")):
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
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=role_perm)

    @jeanne_slash(description="Add a role to a member")
    async def add_role(self, interaction: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you add?")):
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
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=role_perm)

    @jeanne_slash(description="Remove a role from a member")
    async def remove_role(self, interaction: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you delete?")):
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
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=role_perm)

    @jeanne_slash(description="Rename a channel")
    async def rename_channel(self, interaction: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category],
            description="Choose a channel to rename", required=True), new_name=SlashOption(description="Which channel are you renaming?")):
        if interaction.permissions.manage_channels is True:
            await channel.edit(name=new_name)
            embed = Embed(color=0x00FF68)
            embed.add_field(name="Channel renamed",
                            value=f"Channel is now `{new_name}`", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=channel_perm)

    @jeanne_slash(description="Delete a channel")
    async def delete_channel(self, interaction: Interaction,
                             channel: GuildChannel = SlashOption(
            channel_types=[ChannelType.text,
                           ChannelType.voice, ChannelType.category],
            description="Choose a channel to delete")):
        if interaction.permissions.manage_channels is True:
            await channel.delete()
            embed = Embed(color=0x00FF68)
            embed.add_field(name="Channel deleted",
                            value=f"`{channel}` has been deleted", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=channel_perm)

    @jeanne_slash(description='Create a channel')
    async def create_channel(self, interaction: Interaction, channel_type=SlashOption(description='Type of channel', choices=['Text Channel', 'Voice Channel', 'Category'], required=True), channel_name=SlashOption(description="Which will you name it?", required=True)):
        if interaction.permissions.manage_channels is True:
            if channel_type == 'Text Channel':
                await interaction.guild.create_text_channel(channel_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Text channel created",
                                value=f"A new text channel called **{channel_name}** was created", inline=False)
                await interaction.response.send_message(embed=embed)
            elif channel_type == 'Voice Channel':
                await interaction.guild.create_voice_channel(channel_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Voice channel created",
                                value=f"A new voice channel called `{channel_name}` was created", inline=False)
                await interaction.response.send_message(embed=embed)
            elif channel_type == 'Category':
                await interaction.guild.create_category_channel(channel_name)
                embed = Embed(color=0x00FF68)
                embed.add_field(name="Category created",
                                value=f"A new category called **{channel_name}** was created", inline=False)
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=channel_perm)


def setup(bot):
    bot.add_cog(slashmanage(bot))
