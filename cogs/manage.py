import discord
from discord import Member, Role, CategoryChannel
from discord.ext import commands


class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['ctc', 'createtextchannel'])
    @commands.has_permissions(manage_channels=True)
    async def create_text_channel(self, ctx, channel_name):
        await ctx.guild.create_text_channel(channel_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Text channel created",
                        value=f"A new text channel called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['dtc', 'deletetextchannel'])
    @commands.has_permissions(manage_channels=True)
    async def delete_text_channel(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Text channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['rntc', 'renametextchannel'])
    @commands.has_permissions(manage_channels=True)
    async def rename_text_channel(self, ctx, channel: discord.TextChannel, *, new_name):
        await channel.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Text channel renamed",
                        value=f"Channel is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['cvc', 'createvoicechannel'])
    @commands.has_permissions(manage_channels=True)
    async def create_voice_channel(self, ctx, channel_name):
        await ctx.guild.create_voice_channel(channel_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Voice channel created",
                        value=f"A new voice channel called `{channel_name}` was created", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['dvc', 'deletevoicechannel'])
    @commands.has_permissions(manage_channels=True)
    async def delete_voice_channel(self, ctx, channel: discord.VoiceChannel):
        await channel.delete()
        embed = discord.Embed(color=0x00ff68)
        embed.add_field(name="Voice channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['rnvc', 'renamevoicechannel'])
    @commands.has_permissions(manage_channels=True)
    async def rename_voice_channel(self, ctx, channel: discord.VoiceChannel, *, new_name):
        await channel.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Voice channel renamed",
                        value=f"Channel has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cr', 'createrole'])
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Role create",
                        value=f"The role named `{name}` has been made", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['rnr', 'renamerole'])
    @commands.has_permissions(manage_roles=True)
    async def rename_role(self, ctx, role: discord.Role, *, new_name):
        await role.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Role renamed",
                        value=f"Role has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dr'])
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, role: discord.Role):
        await role.delete()
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name=f"Role deleted",
                        value=f"`{role}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ar', 'addrole'])
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: Member, role: Role):
        await member.add_roles(role)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name=f"Role given",
                        value=f"`{role}` was given to `{member}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['rr', 'removerole'])
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: Member, role: Role):
        await member.remove_roles(role)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name=f"Role removed",
                        value=f"`{role}` was removed from `{member}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['ccat', 'createcatagory', 'createcat', 'ccategory'])
    @commands.has_permissions(manage_channels=True)
    async def create_category(self, ctx, channel_name):
        await ctx.guild.create_category_channel(channel_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Category created",
                        value=f"A new category called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['dcat', 'deletecat', 'delcat', 'deletecategory', 'dcategory'])
    @commands.has_permissions(manage_channels=True)
    async def delete_category(self, ctx, category: CategoryChannel):
        await category.delete()
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Category deleted",
                        value=f"`{category}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['rncat', 'renamecat', 'rncategory', 'renamecategory'])
    @commands.has_permissions(manage_channels=True)
    async def rename_category(self, ctx, category: CategoryChannel, *, new_name):
        await category.edit(name=new_name)
        embed = discord.Embed(color=0x00FF68)
        embed.add_field(name="Category renamed",
                        value=f"Category is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(manage(bot))
