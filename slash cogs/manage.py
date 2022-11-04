from db_functions import *
from discord import *
from discord.ext.commands import Cog, Bot, Context, hybrid_command, has_permissions, GroupCog, command, Group, group

from humanfriendly import format_timespan, parse_timespan
from typing import Optional
from discord_argparse import ArgumentConverter, OptionalArgument


class Create_Group(GroupCog, group_name='create', group_description='Main create command'):
    @command(description='Creates a text channel')
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

    @command(description='Create a voice channel')
    @has_permissions(manage_channels=True)
    async def voice_channel(self, ctx: Interaction, name: str, *, category: Optional[CategoryChannel] = None) -> None:
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
        await ctx.defer()
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


async def setup(bot: Bot):
    await bot.add_cog(Create_Group())
    await bot.add_cog(manage(bot))


#needs more work
#must not forget about https://github.com/lukeciel/discord-argparse
