import discord
from discord import Member, Role, CategoryChannel, TextChannel
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Create a new text channel")
    @commands.has_permissions(manage_channels=True)
    async def create_text_channel(self, ctx:SlashContext, channel_name):
        await ctx.guild.create_text_channel(channel_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Text channel created",
                        value=f"A new text channel called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Delete a text channel")
    @commands.has_permissions(manage_channels=True)
    async def delete_text_channel(self, ctx:SlashContext, channel: TextChannel):
        await channel.delete()
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Text channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Rename a text channel")
    @commands.has_permissions(manage_channels=True)
    async def rename_text_channel(self, ctx:SlashContext, channel: TextChannel, new_name):
        await channel.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Text channel renamed",
                        value=f"Channel is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Create a new voice channel")
    @commands.has_permissions(manage_channels=True)
    async def create_voice_channel(self, ctx:SlashContext, channel_name):
        await ctx.guild.create_voice_channel(channel_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Voice channel created",
                        value=f"A new voice channel called `{channel_name}` was created", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Delete a voice channel")
    @commands.has_permissions(manage_channels=True)
    async def delete_voice_channel(self, ctx:SlashContext, channel: discord.VoiceChannel):
        await channel.delete()
        embed = discord.Embed(color=0x00ff68)
        embed.add_field(name="Voice channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Rename a new voice channel")
    @commands.has_permissions(manage_channels=True)
    async def rename_voice_channel(self, ctx:SlashContext, channel: discord.VoiceChannel, new_name):
        await channel.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Voice channel renamed",
                        value=f"Channel has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Create a new role")
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx:SlashContext, role_name):
        guild = ctx.guild
        await guild.create_role(name=role_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Role create",
                        value=f"The role named `{role_name}` has been made", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Rename a role")
    @commands.has_permissions(manage_roles=True)
    async def rename_role(self, ctx:SlashContext, role: discord.Role, new_name):
        await role.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Role renamed",
                        value=f"Role has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Delete a role")
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx:SlashContext, role: discord.Role):
        await role.delete()
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name=f"Role deleted",
                        value=f"`{role}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Add a role to a member")
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: Member, role: Role):
        await member.add_roles(role)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name=f"Role given",
                        value=f"`{role}` was given to `{member}`", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Remove a role from a member")
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx:SlashContext, member: Member, role: Role):
        await member.remove_roles(role)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name=f"Role removed",
                        value=f"`{role}` was removed from `{member}`", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Create a new category")
    @commands.has_permissions(manage_channels=True)
    async def create_category(self, ctx:SlashContext, channel_name):
        await ctx.guild.create_category_channel(channel_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Category created",
                        value=f"A new category called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Delete a category")
    @commands.has_permissions(manage_channels=True)
    async def delete_category(self, ctx:SlashContext, category: CategoryChannel):
        await category.delete()
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Category deleted",
                        value=f"`{category}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Rename a category")
    @commands.has_permissions(manage_channels=True)
    async def rename_category(self, ctx, category: CategoryChannel, *, new_name):
        await category.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Category renamed",
                        value=f"Category is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(manage(bot))
