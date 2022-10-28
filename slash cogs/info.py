from ast import alias
from db_functions import check_botbanned_user
from assets.buttons import ViewRoles
from config import db
from time import time
from datetime import timedelta
from sys import version_info as py_version
from discord.ext.commands import Cog, Bot, Context, hybrid_command
from discord import *
from discord import __version__ as discord_version
from typing import Optional


start_time = time()

class slashinfo(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.bot_version="3.5 VarPatch"

    @hybrid_command(description="See the bot's status from development to now", aliases=['botstats'])
    async def stats(self, ctx : Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            botowner = self.bot.get_user(597829930964877369)
            embed = Embed(title="Bot stats", color=0x236ce1)
            embed.add_field(
                name="Developer", value=f"• **Name:** {botowner}\n• **ID:** {botowner.id}", inline=True)
            embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
            embed.add_field(name="Creation Date", value="<t:{}:F>".format(round(self.bot.user.created_at.timestamp())), inline=True)
            embed.add_field(
                name="Version", value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n• **Discord.PY Version:** {discord_version}\n• **Bot:** {self.bot_version}", inline=True)

            cur=db.execute("SELECT * FROM globalxpData").fetchall()
            all_users=len(cur)
            cur1=db.execute("SELECT * FROM bankData").fetchall()
            true_users=len(cur1)
            embed.add_field(name="Count",
                            value=f"• **Server Count:** {len(self.bot.guilds)} servers\n• **User Count:** {len(set(self.bot.get_all_members()))}\n• **Cached Members:** {all_users}\n• **True Members:** {true_users}", inline=True)

            current_time = time()
            difference = int(round(current_time - start_time))
            uptime = str(timedelta(seconds=difference))
            embed.add_field(
                name="Uptime", value=f"{uptime} hours", inline=True)

            embed.add_field(name="Invites",
                            value="• [Invite me to your server](https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1378013736054&scope=bot)\n• [Vote for me](https://top.gg/bot/831993597166747679)\n• [Join the support server](https://discord.gg/VVxGUmqQhF)\n• [Go to my website to learn more about me](https://jeannebot.nicepage.io/)", inline=True)

            embed.set_thumbnail(
                url=self.bot.user.avatar)
            await ctx.send(embed=embed)

    @hybrid_command(description="See the information of a member or yourself", aliases=['uinfo'])
    async def userinfo(self, ctx : Context, member: Optional[Member]= None)->None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if member == None:
                member = ctx.author
            user = await self.bot.fetch_user(member.id)
            hasroles = [role.name for role in member.roles][1:][:: -1]
            view=ViewRoles()

            if member.bot == True:
                botr = "Yes"
            else:
                botr = "No"

            joined_date = round(member.joined_at.timestamp())
            create_date = round(member.created_at.timestamp())
            userinfo = Embed(title="{}'s Info".format(member.name),
                            color=member.color)
            userinfo.add_field(name="Name", value=member, inline=True)
            userinfo.add_field(name="ID", value=member.id, inline=True)
            userinfo.add_field(name="Is Bot?", value=botr, inline=True)
            userinfo.add_field(
                name="Created Account", value='<t:{}:F>'.format(str(create_date)), inline=True)
            userinfo.add_field(
                name="Joined Server", value='<t:{}:F>'.format(str(joined_date)), inline=True)
            userinfo.add_field(name="Number of Roles",
                               value=len(member.roles), inline=True)

            userinfo.set_thumbnail(url=member.display_avatar)
            
            banner=bool(user.banner)
            
            if banner == True:
                userinfo.set_image(url=user.banner)
                await ctx.send(embed=userinfo, view=view)
            else:
                await ctx.send(embed=userinfo, view=view)
            
            await view.wait()
            
            if view.value=="roles":
                embed = Embed(title="{}'s roles".format(member), description='\n'.join(
                    hasroles) + '\n`@everyone`', color=member.color)
                await ctx.send(embed=embed, ephemeral=True)

    @hybrid_command(description="Get information about this server", aliases=['sinfo'])
    async def serverinfo(self, ctx : Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            guild = ctx.guild
            emojis = [str(x) for x in guild.emojis]
            humans=len([member for  member in ctx.guild.members if not member.bot])
            bots = len([bot for bot in ctx.guild.members if bot.bot])
            

            date = round(guild.created_at.timestamp())
            serverinfo = Embed(title="Server's Info", color=ctx.author.color)
            serverinfo.add_field(name="Name", value=guild.name, inline=True)
            serverinfo.add_field(name="ID", value=guild.id, inline=True)
            serverinfo.add_field(
                name="Creation Date", value='<t:{}:F>'.format(str(date)), inline=True)
            serverinfo.add_field(name="Owner", value=f"• **Name: ** {guild.owner}\n• ** ID: ** {guild.owner.id}", inline=True)
            serverinfo.add_field(
                name="Members", value=f"• **Humans:** {humans}\n• **Bots:** {bots}\n• **Total Members:** {guild.member_count}")
            serverinfo.add_field(name="Boost Status",
                                 value=f"• **Boosters:** {len(guild.premium_subscribers)}\n• **Boosts:** {guild.premium_subscription_count}\n• **Tier:** {guild.premium_tier}",
                            inline=True)
            serverinfo.add_field(name="Channel Count",
                                 value=f"• **All channels:** {len(guild.channels)}\n• **Text Channels:** {len(guild.text_channels)}\n• **Voice Channels:** {len(guild.voice_channels)}\n• **Stage Channels:** {len(guild.stage_channels)}\n• **Categories:** {len(guild.categories)}\n• **Forums:** {len(guild.forums)}",
                                 inline=True)
            serverinfo.add_field(name='Features',
                            value=guild.features, inline=False)

            if guild.icon==None:
                pass
            elif guild.icon.is_animated() is True:
                serverinfo.set_thumbnail(url=guild.icon.with_size(512))
            else:
                serverinfo.set_thumbnail(url=guild.icon)

            if guild.splash==None:
                pass
            else:
                serverinfo.set_image(url=guild.splash)

            if len(emojis) == 0:
                await ctx.send(embed=serverinfo)

            else:
                emojie = Embed(title="Emojis", description=''.join(emojis[:40]), color=0x00B0ff)

                e=[serverinfo, emojie]
                
                await ctx.send(embeds=e)


    @hybrid_command(description="Check how fast I respond to a command", aliases=['response'])
    async def ping(self, ctx : Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            start_time = time()
            test = Embed(description="Testing ping", color=ctx.author.color)
            msg = await ctx.send(embed=test)

            ping = Embed(color=ctx.author.color)
            ping.add_field(
                name="Bot Latency", value=f'{round(self.bot.latency * 1000)}ms', inline=False)
            end_time = time()
            ping.add_field(
                name="API Latency", value=f'{round((end_time - start_time) * 1000)}ms', inline=False)
            await msg.edit(embed=ping)

    @hybrid_command(description="See the server's banner", aliases=['gbanner'])
    async def guildbanner(self, ctx : Context):
        await ctx.response.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            guild = ctx.guild

            if guild.premium_subscription_count < 2:
                nobanner = Embed(description="Server is not boosted at tier 2")
                await ctx.send(embed=nobanner)
            
            else:
                try:
                    embed = Embed(colour=ctx.user.color)
                    embed.set_footer(text=f"{guild.name}'s banner")
                    embed.set_image(url=ctx.guild.banner)
                    await ctx.send(embed=embed)
                except:
                    embed=Embed(description='Guild has no banner')
                    await ctx.send(embed=embed)

    @hybrid_command(description="See your avatar or another member's avatar")
    async def avatar(self, ctx: Context, member: Optional[Member]=None)->None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if member==None:
                member=ctx.user

            avatar = Embed(title=f"{member}'s Avatar", color=member.color)
            avatar.set_image(url=member.avatar)
            await ctx.send(embed=avatar)

    @hybrid_command(description="See your guild avatar or a member's guild avatar", aliases=['gavatar'])
    async def guildavatar(self, ctx: Context, member: Optional[Member]=None)->None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            if member == None:
                member = ctx.author
            
            member_avatar = bool(member.guild_avatar)

            guild_avatar = Embed(title=f"{member}'s Avatar", color=member.color)

            if member_avatar == True:
                guild_avatar.set_image(url=member.guild_avatar)
                await ctx.send(embed=guild_avatar)
            else:
                guild_avatar.set_image(url=member.display_avatar)
                guild_avatar.set_footer(
                    text="Member has no server avatar. Passed normal avatar instead")
                await ctx.send(embed=guild_avatar)


async def setup(bot:Bot):
    await bot.add_cog(slashinfo(bot))
