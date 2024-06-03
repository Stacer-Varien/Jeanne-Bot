from humanfriendly import format_timespan
from assets.components import RolesButton
from functions import (
    check_botbanned_prefix,
    check_disabled_prefixed_command,
    get_cached_users,
    get_true_members,
)
from time import time
from datetime import timedelta
from sys import version_info as py_version
from discord.ext.commands import Cog, Bot, Context
import discord.ext.commands as Jeanne
from discord import (
    ButtonStyle,
    Color,
    DMChannel,
    Embed,
    Member,
    Message,
    PartialEmoji,
    StickerItem,
    utils,
    ui,
)
from discord import __version__ as discord_version
from typing import Optional

start_time = time()


class stat_buttons(ui.View):
    def __init__(self):
        super().__init__()
        invite = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1429553343542&scope=bot%20applications.commands"
        votetopgg = "https://top.gg/bot/831993597166747679"
        votedbl = "https://discordbotlist.com/bots/jeanne/upvote"
        orleans_url = "https://discord.gg/jh7jkuk2pp"
        website = "https://jeannebot.gitbook.io/jeannebot/"
        self.add_item(ui.Button(style=ButtonStyle.link, label="Invite me", url=invite))
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Vote for me", url=votetopgg)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Vote for me (DBL)", url=votedbl)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Support Server", url=orleans_url)
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="Jeanne Website",
                url=website,
            )
        )


class InfoPrefix(Cog, name="Info"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot_version = "v5.0"

    async def get_userinfo(self, ctx: Context, member: Member):
        user = await self.bot.fetch_user(member.id)
        has_roles = [role.mention for role in member.roles][1:][::-1]
        bot_check = "Yes" if member.bot else "No"
        joined_date = round(member.joined_at.timestamp())
        create_date = round(member.created_at.timestamp())
        userinfo = Embed(title=f"{member.name}'s Info", color=member.color)
        userinfo.add_field(name="Name", value=member, inline=True)
        userinfo.add_field(name="Global Name", value=member.global_name, inline=True)
        if member.nick:
            userinfo.add_field(name="Nickname", value=member.nick, inline=True)
        userinfo.add_field(name="ID", value=member.id, inline=True)
        userinfo.add_field(name="Is Bot?", value=bot_check, inline=True)
        userinfo.add_field(
            name="Created Account", value=f"<t:{create_date}:F>", inline=True
        )
        userinfo.add_field(
            name="Joined Server", value=f"<t:{joined_date}:F>", inline=True
        )
        userinfo.add_field(name="Number of Roles", value=len(member.roles), inline=True)
        userinfo.set_thumbnail(url=member.display_avatar)
        if user.banner:
            userinfo.set_image(url=user.banner)
        view = RolesButton(member, userinfo, has_roles)
        m = await ctx.send(embeds=[userinfo], view=view)
        await view.wait()
        if view.value is None:
            await m.edit(embeds=[userinfo], view=None)

    @Jeanne.command(
        aliases=["botstats"], description="See the bot's status from development to now"
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def stats(self, ctx: Context):
        all_users = get_cached_users()
        true_users = get_true_members()
        embed = Embed(title="Bot stats", color=Color.random())
        embed.add_field(
            name="Developer",
            value=f"• **Name:** {self.bot.application.owner}\n• **ID:** {
                self.bot.application.owner.id}",
            inline=True,
        )
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(
            name="Creation Date",
            value="<t:{}:F>".format(round(self.bot.user.created_at.timestamp())),
            inline=True,
        )
        embed.add_field(
            name="Version",
            value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n• **discordpy Version:** {discord_version}\n• **Bot:** {self.bot_version}",
            inline=True,
        )
        embed.add_field(
            name="Count",
            value=f"• **Server Count:** {len(self.bot.guilds)} servers\n• **User Count:** {len(set(
                self.bot.get_all_members()))}\n• **Cached Members:** {all_users}\n• **True Members:** {true_users}",
            inline=True,
        )
        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = timedelta(seconds=difference).total_seconds()
        embed.add_field(name="Uptime", value=format_timespan(uptime), inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed, view=stat_buttons())

    @Jeanne.command(
        aliases=["uinfo", "minfo"],
        description="See the information of a member or yourself",
        usage="<MEMBER>",
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def userinfo(self, ctx: Context, *, member: Optional[Member] = None) -> None:
        member = ctx.author if member is None else member
        await self.get_userinfo(ctx, member)

    @Jeanne.command(
        aliases=["sinfo", "ginfo"], description="Get information about this server"
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def serverinfo(self, ctx: Context):
        embeds = []
        emojis = [str(x) for x in ctx.guild.emojis]
        humans = len([member for member in ctx.guild.members if not member.bot])
        bots = len([bot for bot in ctx.guild.members if bot.bot == True])
        date = round(ctx.guild.created_at.timestamp())
        serverinfo = Embed(description=f"{ctx.guild.name}'s info", color=Color.random())
        serverinfo.add_field(name="ID", value=ctx.guild.id, inline=True)
        serverinfo.add_field(
            name="Owner",
            value=f"• **Name: ** {ctx.guild.owner}\n• ** ID: ** {ctx.guild.owner.id}",
            inline=True,
        )
        serverinfo.add_field(
            name="Creation Date",
            value=f"<t:{
                             date}:F>",
            inline=True,
        )
        serverinfo.add_field(
            name="Members",
            value=f"• **Humans:** {humans}\n• **Bots:** {bots}\n• **Total Members:** {ctx.guild.member_count}",
            inline=True,
        )
        serverinfo.add_field(
            name="Boost Status",
            value=f"• **Boosters:** {len(ctx.guild.premium_subscribers)}\n• **Boosts:** {ctx.guild.premium_subscription_count}\n• **Tier:** {ctx.guild.premium_tier}",
            inline=True,
        )
        verification_level = (
            ctx.guild.verification_level.name.capitalize()
            if ctx.guild.verification_level.name != "none"
            else None
        )
        serverinfo.add_field(
            name="Verification Lever",
            value=verification_level,
            inline=True,
        )
        serverinfo.add_field(
            name="Count",
            value=f"**All channels:** {len(ctx.guild.channels)} | **Text Channels:** {len(ctx.guild.text_channels)} |  **Voice Channels:** {len(ctx.guild.voice_channels)} |  **Stage Channels:** {len(
                ctx.guild.stage_channels)} |  **Categories:** {len(ctx.guild.categories)} |  **Forums:** {len(ctx.guild.forums)} |  **Roles:** {len(ctx.guild.roles)} | **Emojis:** {len(emojis)} | **Stickers:** {len(ctx.guild.stickers)}",
            inline=False,
        )
        f = []
        for i in ctx.guild.features:
            f.append(i.replace("_", " ").title())
        serverinfo.add_field(name="Features", value=" | ".join(f), inline=False)
        icon = ctx.guild.icon
        splash = (
            ctx.guild.splash.url
            if ctx.guild.splash != None and ctx.guild.premium_tier == 1
            else None
        )
        serverinfo.set_thumbnail(url=icon)
        serverinfo.set_image(url=splash)
        embeds.append(serverinfo)
        if len(emojis) > 0:
            emojie = Embed(
                title="Emojis", description="".join(emojis[:80]), color=Color.random()
            )
            embeds.append(emojie)
        await ctx.send(embeds=embeds)

    @Jeanne.command(description="Check how fast I respond to a command")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def ping(self, ctx: Context):
        start_time = time()
        test = Embed(description="Testing ping", color=Color.random())
        m = await ctx.send(embed=test)
        ping = Embed(color=Color.random())
        ping.add_field(
            name="Bot Latency",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=False,
        )
        end_time = time()
        ping.add_field(
            name="API Latency",
            value=f"{round((end_time - start_time) * 1000)}ms",
            inline=False,
        )
        await m.edit(embed=ping)

    @Jeanne.command(aliases=["sbanner"], description="See the server's banner")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def serverbanner(self, ctx: Context):
        if ctx.guild.premium_subscription_count < 2:
            nobanner = Embed(
                description="Server is not boosted at tier 2", color=Color.red()
            )
            await ctx.send(embed=nobanner)
            return
        if ctx.guild.banner == None:
            embed = Embed(description="Server has no banner", color=Color.red())
            await ctx.send(embed=embed)
            return
        embed = Embed(colour=Color.random())
        embed.set_footer(text=f"{ctx.guild.name}'s banner")
        embed.set_image(url=ctx.guild.banner.url)
        await ctx.send(embed=embed)

    @Jeanne.command(
        aliases=["av", "pfp"],
        description="See your avatar or another member's avatar",
        usage="<MEMBER>",
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def avatar(self, ctx: Context, *, member: Optional[Member] = None) -> None:
        member = ctx.author if member is None else member
        color = Color.random()
        globalav = member.avatar
        defaultav = member.default_avatar
        serverav = None if DMChannel else member.guild_avatar
        color = Color.random()
        embeds = []
        normav = Embed(
            description=f"**{member}'s Avatar**",
            url="https://discordapp.com",
            color=color,
        )
        try:
            if ctx.channel.me:
                normav.set_image(url=member.display_avatar)
                await ctx.send(embed=normav)
                return
        except:
            if globalav == None and serverav:
                guildav = Embed(
                    url="https://discordapp.com",
                    color=color,
                    type="image",
                )
                normav.set_image(url=defaultav)
                guildav.set_image(url=serverav)
                embeds.append(normav)
                embeds.append(guildav)
            elif globalav and serverav == None:
                normav.set_image(url=globalav)
                embeds.append(normav)
            elif globalav and serverav:
                guildav = Embed(
                    url="https://discordapp.com",
                    color=color,
                    type="image",
                )
                normav.set_image(url=globalav)
                guildav.set_image(url=serverav)
                embeds.append(normav)
                embeds.append(guildav)
            await ctx.send(embeds=embeds)

    @Jeanne.command(
        description="View a sticker via message ID or sticker name", usage="[STICKER]"
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def sticker(self, ctx: Context, *, sticker: str):
        try:
            m: Message = await ctx.channel.fetch_message(int(sticker))
            s: StickerItem = m.stickers[0]
        except:
            s: StickerItem = utils.get(ctx.guild.stickers, name=sticker)
        q = await self.bot.fetch_sticker(s.id)
        embed = Embed()
        embed.colour = Color.random()
        embed.add_field(name="Sticker Name", value=q.name, inline=False)
        embed.add_field(name="Sticker ID", value=q.id, inline=False)
        embed.set_image(url=q.url)
        if "apng" in q.format:
            embed.add_field(name="Animated Sticker URL", value=q.url, inline=False)
        await ctx.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            embed = Embed(
                description="No sticker is in that message",
                color=Color.red(),
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.send(embed=embed)
            return

    @Jeanne.command(description="View an emoji", usage="[EMOJI | EMOJI ID]")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def emoji(self, ctx: Context, *, emoji: Jeanne.Range[str, 1]):
        emote = PartialEmoji.from_str(emoji)
        embed = Embed()
        if emote.id == None:
            embed.color = Color.red()
            embed.description = "Failed to get emoji."
            await ctx.send(embed=embed)
            return
        embed.color = Color.random()
        embed.add_field(name="Name", value=emote.name, inline=False)
        embed.add_field(name="ID", value=emote.id, inline=False)
        embed.set_image(url=emote.url)
        await ctx.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="Failed to get emoji",
                color=Color.red(),
            )
            await ctx.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(InfoPrefix(bot))
