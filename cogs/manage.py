from nextcord import Member, Role, CategoryChannel, TextChannel, Embed, VoiceChannel
from nextcord.ext.commands import command as jeanne, Cog, has_permissions as perms, MissingPermissions
from assets.errormsgs import channel_perm, role_perm, cat_perm


class manage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne(aliases=['ctc', 'createtextchannel'])
    @perms(manage_channels=True)
    async def create_text_channel(self, ctx, channel_name):
        channel = await ctx.guild.create_text_channel(channel_name)

        embed = Embed(color=0x00FF68)
        embed.add_field(name="Text channel created",
                        value=f"A new text channel called **{channel}** was created", inline=False)
        await ctx.send(embed=embed)

    @create_text_channel.error
    async def ctc_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=channel_perm)

    @jeanne(aliases=['dtc', 'deletetextchannel'])
    @perms(manage_channels=True)
    async def delete_text_channel(self, ctx, channel: TextChannel):
        await channel.delete()
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Text channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @delete_text_channel.error
    async def dtc_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=channel_perm)    

    @jeanne(aliases=['rntc', 'renametextchannel'])
    @perms(manage_channels=True)
    async def rename_text_channel(self, ctx, channel: TextChannel, *, new_name):
        await channel.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Text channel renamed",
                        value=f"Channel is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @rename_text_channel.error
    async def rntc_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=channel_perm)

    @jeanne(aliases=['cvc', 'createvoicechannel'])
    @perms(manage_channels=True)
    async def create_voice_channel(self, ctx, channel_name):
        await ctx.guild.create_voice_channel(channel_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Voice channel created",
                        value=f"A new voice channel called `{channel_name}` was created", inline=False)
        await ctx.send(embed=embed)

    @create_voice_channel.error
    async def cvc_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=channel_perm)

    @jeanne(aliases=['dvc', 'deletevoicechannel'])
    @perms(manage_channels=True)
    async def delete_voice_channel(self, ctx, channel: VoiceChannel):
        await channel.delete()
        embed = Embed(color=0x00ff68)
        embed.add_field(name="Voice channel deleted",
                        value=f"`{channel}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @delete_voice_channel.error
    async def dvc_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=channel_perm)        

    @jeanne(aliases=['rnvc', 'renamevoicechannel'])
    @perms(manage_channels=True)
    async def rename_voice_channel(self, ctx, channel: VoiceChannel, *, new_name):
        await channel.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Voice channel renamed",
                        value=f"Channel has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @create_text_channel.error
    async def rnvc_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=channel_perm)        

    @jeanne(aliases=['cr', 'createrole'])
    @perms(manage_roles=True)
    async def create_role(self, ctx, *, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Role create",
                        value=f"The role named `{name}` has been made", inline=False)
        await ctx.send(embed=embed)

    @create_role.error
    async def cr_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=role_perm)        

    @jeanne(aliases=['rnr', 'renamerole'])
    @perms(manage_roles=True)
    async def rename_role(self, ctx, role: Role, *, new_name):
        await role.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Role renamed",
                        value=f"Role has been renamed to `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @rename_role.error
    async def rnr_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=role_perm)         

    @jeanne(aliases=['dr', 'deleterole'])
    @perms(manage_roles=True)
    async def delete_role(self, ctx, role: Role):
        await role.delete()
        embed = Embed(color=0x00FF68)
        embed.add_field(name=f"Role deleted",
                        value=f"`{role}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @delete_role.error
    async def dr_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=role_perm) 

    @jeanne(aliases=['ar', 'addrole'])
    @perms(manage_roles=True)
    async def add_role(self, ctx, member: Member, role: Role):
        await member.add_roles(role)
        embed = Embed(color=0x00FF68)
        embed.add_field(name=f"Role given",
                        value=f"`{role}` was given to `{member}`", inline=False)
        await ctx.send(embed=embed)

    @add_role.error
    async def ar_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=role_perm)         

    @jeanne(aliases=['rr', 'removerole'])
    @perms(manage_roles=True)
    async def remove_role(self, ctx, member: Member, role: Role):
        await member.remove_roles(role)
        embed = Embed(color=0x00FF68)
        embed.add_field(name=f"Role removed",
                        value=f"`{role}` was removed from `{member}`", inline=False)
        await ctx.send(embed=embed)

    @rename_role.error
    async def rr_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=role_perm) 

    @jeanne(aliases=['ccat', 'createcatagory', 'createcat', 'ccategory'])
    @perms(manage_channels=True)
    async def create_category(self, ctx, channel_name):
        await ctx.guild.create_category_channel(channel_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Category created",
                        value=f"A new category called **{channel_name}** was created", inline=False)
        await ctx.send(embed=embed)

    @create_category.error
    async def ccat_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=cat_perm)         

    @jeanne(aliases=['dcat', 'deletecat', 'delcat', 'deletecategory', 'dcategory'])
    @perms(manage_channels=True)
    async def delete_category(self, ctx, category: CategoryChannel):
        await category.delete()
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Category deleted",
                        value=f"`{category}` has been deleted", inline=False)
        await ctx.send(embed=embed)

    @delete_category.error
    async def dcat_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=cat_perm)        

    @jeanne(aliases=['rncat', 'renamecat', 'rncategory', 'renamecategory'])
    @perms(manage_channels=True)
    async def rename_category(self, ctx, category: CategoryChannel, *, new_name):
        await category.edit(name=new_name)
        embed = Embed(color=0x00FF68)
        embed.add_field(name="Category renamed",
                        value=f"Category is now `{new_name}`", inline=False)
        await ctx.send(embed=embed)

    @rename_category.error
    async def rncat_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=cat_perm) 




def setup(bot):
    bot.add_cog(manage(bot))
