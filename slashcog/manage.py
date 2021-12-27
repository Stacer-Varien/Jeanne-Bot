from discord import Member, Role, CategoryChannel, TextChannel, Embed, VoiceChannel
from discord.ext.commands import Cog, has_permissions as perms
from discord_slash.cog_ext import cog_slash as jeanne_slash

class manage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Create a new text channel")
    @perms(manage_channels=True)
    async def create_text_channel(self, ctx, channel_name):
        await ctx.guild.create_text_channel(channel_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Text channel created",
                        value=f"A new text channel called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Delete a text channel")
    @perms(manage_channels=True)
    async def delete_text_channel(self, ctx, channel: TextChannel):
        await channel.delete()
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Text channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Rename a text channel")
    @perms(manage_channels=True)
    async def rename_text_channel(self, ctx, channel: TextChannel, new_name):
        await channel.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Text channel renamed",
                        value=f"Channel is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Create a new voice channel")
    @perms(manage_channels=True)
    async def create_voice_channel(self, ctx, channel_name):
        await ctx.guild.create_voice_channel(channel_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Voice channel created",
                        value=f"A new voice channel called `{channel_name}` was created", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Delete a voice channel")
    @perms(manage_channels=True)
    async def delete_voice_channel(self, ctx, channel: VoiceChannel):
        await channel.delete()
        embed = Embed(color=0x00ff68)
        embed.add_field(name="Voice channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Rename a new voice channel")
    @perms(manage_channels=True)
    async def rename_voice_channel(self, ctx, channel: VoiceChannel, new_name):
        await channel.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Voice channel renamed",
                        value=f"Channel has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Create a new role")
    @perms(manage_roles=True)
    async def create_role(self, ctx, role_name):
        guild = ctx.guild
        await guild.create_role(name=role_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Role create",
                        value=f"The role named `{role_name}` has been made", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Rename a role")
    @perms(manage_roles=True)
    async def rename_role(self, ctx, role: Role, new_name):
        await role.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Role renamed",
                        value=f"Role has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Delete a role")
    @perms(manage_roles=True)
    async def delete_role(self, ctx, role: Role):
        await role.delete()
        embed = Embed(color=0x00FF68)
        embed.add_field(name=f"Role deleted",
                        value=f"`{role}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Add a role to a member")
    @perms(manage_roles=True)
    async def add_role(self, ctx, member: Member, role: Role):
        await member.add_roles(role)
        embed = Embed(color=0x00FF68)
        embed.add_field(name=f"Role given",
                        value=f"`{role}` was given to `{member}`", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Remove a role from a member")
    @perms(manage_roles=True)
    async def remove_role(self, ctx, member: Member, role: Role):
        await member.remove_roles(role)
        embed = Embed(color=0x00FF68)
        embed.add_field(name=f"Role removed",
                        value=f"`{role}` was removed from `{member}`", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Create a new category")
    @perms(manage_channels=True)
    async def create_category(self, ctx, channel_name):
        await ctx.guild.create_category_channel(channel_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Category created",
                        value=f"A new category called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Delete a category")
    @perms(manage_channels=True)
    async def delete_category(self, ctx, category: CategoryChannel):
        await category.delete()
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Category deleted",
                        value=f"`{category}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @jeanne_slash(description="Rename a category")
    @perms(manage_channels=True)
    async def rename_category(self, ctx, category: CategoryChannel, *, new_name):
        await category.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Category renamed",
                        value=f"Category is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(manage(bot))
