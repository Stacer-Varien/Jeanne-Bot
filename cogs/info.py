from humanfriendly import format_timespan
from assets.components import RolesButton
from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    get_cached_users,
    get_true_members,
)
from time import time
from datetime import timedelta
from sys import version_info as py_version
from discord.ext.commands import Cog, Bot
from discord import (
    ButtonStyle,
    Color,
    DMChannel,
    Embed,
    Interaction,
    Member,
    Message,
    PartialEmoji,
    StickerItem,
    app_commands as Jeanne,
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
        orleans_url = "https://discord.gg/jh7jkuk2pp"
        website = "https://jeannebot.gitbook.io/jeannebot/"
        self.add_item(ui.Button(style=ButtonStyle.link, label="Invite me", url=invite))
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Vote for me", url=votetopgg)
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


class InfoCog(Cog, name="InfoSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot_version = "v5.0"
        self.userinfo_context = Jeanne.ContextMenu(
            name="Userinfo", callback=self.userinfo_callback
        )
        self.bot.tree.add_command(self.userinfo_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.userinfo_context.name, type=self.userinfo_context.type
        )

    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def userinfo_callback(self, ctx: Interaction, member: Member):
        await self.get_userinfo(ctx, member)

    async def get_userinfo(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
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
        await ctx.followup.send(embeds=[userinfo], view=view)
        await view.wait()
        if view.value is None:
            await ctx.edit_original_response(embeds=[userinfo], view=None)

    @Jeanne.command(description="See the bot's status from development to now")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def stats(self, ctx: Interaction):
        await ctx.response.defer()
        all_users = get_cached_users()
        true_users = get_true_members()
        embed = Embed(title="Bot stats", color=Color.random())
        embed.add_field(
            name="Developer",
            value=f"• **Name:** {self.bot.application.owner}\n• **ID:** {self.bot.application.owner.id}",
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
            value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n• **Discord.PY Version:** {discord_version}\n• **Bot:** {self.bot_version}",
            inline=True,
        )
        embed.add_field(
            name="Count",
            value=f"• **Server Count:** {len(self.bot.guilds)} servers\n• **Shards:** {self.bot.shard_count}\n• **User Count:** {len(set(
                self.bot.get_all_members()))}\n• **Cached Members:** {all_users}\n• **True Members:** {true_users}",
            inline=True,
        )
        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = timedelta(seconds=difference).total_seconds()
        embed.add_field(name="Uptime", value=format_timespan(uptime), inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.followup.send(embed=embed, view=stat_buttons())

    @Jeanne.command(description="See the information of a member or yourself")
    @Jeanne.describe(member="Which member?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def userinfo(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        member = ctx.user if member is None else member
        await self.get_userinfo(ctx, member)

    @Jeanne.command(description="Get information about this server")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def serverinfo(self, ctx: Interaction):
        await ctx.response.defer()
        emojis = [str(x) for x in ctx.guild.emojis]
        humans = len([member for member in ctx.guild.members if not member.bot])
        bots = len([bot for bot in ctx.guild.members if bot.bot == True])
        date = round(ctx.guild.created_at.timestamp())
        serverinfo = Embed(color=Color.random())
        serverinfo.add_field(name="ID", value=ctx.guild.id, inline=True)
        serverinfo.add_field(
            name="Owner",
            value=f"• **Name: ** {ctx.guild.owner}\n• ** ID: ** {ctx.guild.owner_id}",
            inline=True,
        )
        serverinfo.add_field(name="Creation Date", value=f"<t:{date}:F>", inline=True)
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
            value=f"**All channels:** {len(ctx.guild.channels)} | **Text Channels:** {len(ctx.guild.text_channels)} |  **Voice Channels:** {len(ctx.guild.voice_channels)} |  **Stage Channels:** {len(ctx.guild.stage_channels)} |  **Categories:** {len(ctx.guild.categories)} |  **Forums:** {len(ctx.guild.forums)} |  **Roles:** {len(ctx.guild.roles)} | **Emojis:** {len(emojis)} | **Stickers:** {len(ctx.guild.stickers)}",
            inline=False,
        )
        f = []
        for i in ctx.guild.features:
            f.append(i.replace("_", " ").title())
        serverinfo.add_field(name="Features", value=" | ".join(f), inline=False)
        icon = ctx.guild.icon.url if ctx.guild.icon != None else None
        splash = (
            ctx.guild.splash.url
            if ctx.guild.splash != None and ctx.guild.premium_tier == 1
            else None
        )
        serverinfo.set_thumbnail(url=icon)
        serverinfo.set_image(url=splash)
        serverinfo.set_footer(text=f"Shard ID: {ctx.guild.shard_id}")
        if len(emojis) == 0:
            await ctx.followup.send(embed=serverinfo)
            return
        emojie = Embed(
            title="Emojis", description="".join(emojis[:80]), color=Color.random()
        )
        e = [serverinfo, emojie]
        await ctx.followup.send(embeds=e)

    @Jeanne.command(description="Check how fast I respond to a command")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def ping(self, ctx: Interaction):
        await ctx.response.defer()
        start_time = time()
        test = Embed(description="Testing ping", color=Color.random())
        await ctx.followup.send(embed=test)
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
        await ctx.edit_original_response(embed=ping)

    @Jeanne.command(description="See the server's banner")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def serverbanner(self, ctx: Interaction):
        await ctx.response.defer()
        if ctx.guild.premium_subscription_count < 2:
            nobanner = Embed(
                description="Server is not boosted at tier 2", color=Color.red()
            )
            await ctx.followup.send(embed=nobanner)
            return
        if ctx.guild.banner == None:
            embed = Embed(description="Server has no banner", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        embed = Embed(colour=Color.random())
        embed.set_footer(text=f"{ctx.guild.name}'s banner")
        embed.set_image(url=ctx.guild.banner.url)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="See your avatar or another member's avatar")
    @Jeanne.describe(member="Which member?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def avatar(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await ctx.response.defer()
        member = ctx.user if member is None else member
        globalav = member.avatar
        defaultav = member.default_avatar
        serverav = None if DMChannel else member.guild_avatar
        color = Color.random()
        embeds = []
        normav = Embed(
            description=f"**{member}'s Avatar**",
            url="https://discordapp.com",
            color=color,
            type="image",
        )

        try:
            if ctx.channel.me:
                normav.set_image(url=member.display_avatar)
                await ctx.followup.send(embed=normav)
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

            await ctx.followup.send(embeds=embeds)

    @Jeanne.command(description="View a sticker")
    @Jeanne.describe(
        sticker="Insert message ID with the sticker or name of the sticker in the server"
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def sticker(self, ctx: Interaction, sticker: str):
        await ctx.response.defer()
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
        await ctx.followup.send(embed=embed)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            embed = Embed(
                description="No sticker is in that message",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)
            return
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="This sticker doesn't exist in the server",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)
            return

    @Jeanne.command(description="View an emoji")
    @Jeanne.describe(emoji="What is the name of the emoji?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def emoji(self, ctx: Interaction, emoji: Jeanne.Range[str, 1]):
        await ctx.response.defer()
        emote = PartialEmoji.from_str(emoji)
        embed = Embed()
        if emote.id == None:
            embed.color = Color.red()
            embed.description = "Failed to get emoji."
            await ctx.followup.send(embed=embed)
            return
        embed.color = Color.random()
        embed.add_field(name="Name", value=emote.name, inline=False)
        embed.add_field(name="ID", value=emote.id, inline=False)
        embed.set_image(url=emote.url)
        await ctx.followup.send(embed=embed)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            embed = Embed(
                description="Failed to get emoji",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(InfoCog(bot))
