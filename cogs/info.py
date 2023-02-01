from db_functions import check_botbanned_user, get_cached_users, get_true_members
from time import time
from datetime import timedelta
from sys import version_info as py_version
from discord.ext.commands import Cog, Bot
from discord import *
from discord import __version__ as discord_version
from typing import Optional


start_time = time()


class slashinfo(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot_version = "4.2"

    @app_commands.command(description="See the bot's status from development to now")
    async def stats(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            botowner = self.bot.get_user(597829930964877369)
            all_users = get_cached_users()
            true_users = get_true_members()
            embed = Embed(title="Bot stats", color=Color.random())
            embed.add_field(
                name="Developer", value=f"• **Name:** {botowner}\n• **ID:** {botowner.id}", inline=True)
            embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
            embed.add_field(name="Creation Date", value="<t:{}:F>".format(
                round(self.bot.user.created_at.timestamp())), inline=True)
            embed.add_field(
                name="Version", value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n• **Discord.PY Version:** {discord_version}\n• **Bot:** {self.bot_version}", inline=True)

            embed.add_field(name="Count",
                            value=f"• **Server Count:** {len(self.bot.guilds)} servers\n• **User Count:** {len(set(self.bot.get_all_members()))}\n• **Cached Members:** {all_users}\n• **True Members:** {true_users}", inline=True)

            current_time = time()
            difference = int(round(current_time - start_time))
            uptime = str(timedelta(seconds=difference))
            embed.add_field(
                name="Uptime", value=f"{uptime} hours", inline=True)

            embed.add_field(name="Invites",
                            value="• [Invite me to your server]https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1429553343542&scope=bot%20applications.commands)\n• [Vote for me](https://top.gg/bot/831993597166747679)\n• [Join the support server](https://discord.gg/jh7jkuk2pp)\n• [Go to my website to learn more about me](https://jeannebot.gitbook.io/jeannebot/)", inline=True)

            embed.set_thumbnail(
                url=self.bot.user.avatar)
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="See the information of a member or yourself")
    @app_commands.describe(member="Which member?")
    async def userinfo(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member == None:
                member = ctx.user
            user = await self.bot.fetch_user(member.id)
            hasroles = [role.name for role in member.roles][1:][:: -1]

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
            roles = Embed(title="{}'s roles".format(member), description=''.join(
                hasroles) + '`@everyone`', color=member.color)

            embeds = [userinfo, roles]

            banner = bool(user.banner)

            if banner == True:
                userinfo.set_image(url=user.banner)
                await ctx.followup.send(embed=embeds)
            else:
                await ctx.followup.send(embed=embeds)

    @app_commands.command(description="Get information about this server")
    async def serverinfo(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            guild = ctx.guild
            emojis = [str(x) for x in guild.emojis]
            humans = len(
                [member for member in ctx.guild.members if not member.bot])
            bots = len([bot for bot in ctx.guild.members if bot.bot])

            date = round(guild.created_at.timestamp())
            serverinfo = Embed(title="Server's Info", color=Color.random())
            serverinfo.add_field(name="Name", value=guild.name, inline=True)
            serverinfo.add_field(name="ID", value=guild.id, inline=True)
            serverinfo.add_field(
                name="Creation Date", value='<t:{}:F>'.format(str(date)), inline=True)
            serverinfo.add_field(
                name="Owner", value=f"• **Name: ** {guild.owner}\n• ** ID: ** {guild.owner.id}", inline=True)
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

            if guild.icon == None:
                pass
            elif guild.icon.is_animated() is True:
                serverinfo.set_thumbnail(url=guild.icon.with_size(512))
            else:
                serverinfo.set_thumbnail(url=guild.icon)

            if guild.splash == None:
                pass
            else:
                serverinfo.set_image(url=guild.splash)

            if len(emojis) == 0:
                await ctx.followup.send(embed=serverinfo)

            else:
                emojie = Embed(title="Emojis", description=''.join(
                    emojis[:40]), color=Color.random())

                e = [serverinfo, emojie]

                await ctx.followup.send(embeds=e)

    @app_commands.command(description="Check how fast I respond to a command")
    async def ping(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            start_time = time()
            test = Embed(description="Testing ping", color=Color.random())
            await ctx.followup.send(embed=test)

            ping = Embed(color=Color.random())
            ping.add_field(
                name="Bot Latency", value=f'{round(self.bot.latency * 1000)}ms', inline=False)
            end_time = time()
            ping.add_field(
                name="API Latency", value=f'{round((end_time - start_time) * 1000)}ms', inline=False)
            await ctx.edit_original_response(embed=ping)

    @app_commands.command(description="See the server's banner")
    async def serverbanner(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            guild = ctx.guild

            if guild.premium_subscription_count < 2:
                nobanner = Embed(
                    description="Server is not boosted at tier 2", color=Color.red())
                await ctx.followup.send(embed=nobanner)

            elif guild.banner == None:
                embed = Embed(description='Server has no banner',
                              color=Color.red())
                await ctx.followup.send(embed=embed)
            else:
                embed = Embed(colour=Color.random())
                embed.set_footer(text=f"{guild.name}'s banner")
                embed.set_image(url=ctx.guild.banner)
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="See your avatar or another member's avatar")
    @app_commands.describe(member="Which member?")
    async def avatar(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if member == None:
                member = ctx.user

            avatar = Embed(title=f"{member}'s Avatar", color=Color.random())
            avatar.set_image(url=member.avatar)
            await ctx.followup.send(embed=avatar)

    @app_commands.command(description="See your server avatar or a member's server avatar")
    @app_commands.describe(member="Which member?")
    async def serveravatar(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            if member == None:
                member = ctx.user

            member_avatar = bool(member.guild_avatar)

            guild_avatar = Embed(
                title=f"{member}'s Avatar", color=member.color)

            if member_avatar == True:
                guild_avatar.set_image(url=member.guild_avatar)
                await ctx.followup.send(embed=guild_avatar)
            else:
                guild_avatar.set_image(url=member.display_avatar)
                guild_avatar.set_footer(
                    text="Member has no server avatar. Passed normal avatar instead")
                await ctx.followup.send(embed=guild_avatar)

    @app_commands.command(description="View a sticker")
    @app_commands.describe(sticker="Insert message ID with the sticker or name of the sticker in the server")
    async def sticker(self, ctx: Interaction, sticker: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            
            try:
                m: Message = await ctx.channel.fetch_message(int(sticker))
                s: StickerItem = m.stickers[0]
            except:
                s: StickerItem = utils.get(ctx.guild.stickers, name=sticker)

            q = await self.bot.fetch_sticker(s.id)
            embed = Embed()
            embed.colour = Color.random()
            embed.add_field(name="Sticker Name",
                            value=q.name, inline=False)
            embed.add_field(name="Sticker ID",
                            value=q.id, inline=False)
            embed.set_image(url=q.url)

            if 'apng' in q.format:
                embed.add_field(
                    name="Anitmated Sticker URL", value=q.url, inline=False)

            await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if IndexError:
                embed = Embed(
                    description="No sticker is in that message or the sticker got deleted from its server", color=Color.red())
                await ctx.followup.send(embed=embed)
            elif AttributeError:
                embed = Embed(
                    description="This sticker doesn't exist in the server", color=Color.red())
                await ctx.followup.send(embed=embed)

    @app_commands.command(description="View an emoji")
    @app_commands.describe(emoji="What is the name of the emoji?")
    async def emoji(self, ctx: Interaction, emoji: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            try:
                e = emoji.split(':')[-1].rstrip('>')
                emote = self.bot.get_emoji(int(e))
            except:
                emote = utils.get(ctx.guild.emojis, name=emoji)

            embed = Embed()
            embed.color = Color.random()
            embed.add_field(
                name="Name", value=emote.name, inline=False)
            embed.add_field(name="ID", value=emote.id, inline=False)
            embed.set_image(url=emote.url)
            await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            if AttributeError:
                embed = Embed(
                    description="This emoji doesn't exist in the server", color=Color.red())
                await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(slashinfo(bot))
