from datetime import datetime, timedelta
from discord.ext.commands import (
    Cog,
    Bot,
    group,
    is_owner,
    guild_only,
    Context,
    Greedy,
    command,
)
from discord import (
    ActivityType,
    Embed,
    File,
    Game,
    Activity,
    Object,
    HTTPException,
    User,
)
from os import execv
from sys import executable, argv

from humanfriendly import format_timespan, parse_timespan
from assets.components import ModuleSelect
from functions import BetaTest, DevPunishment, Hentai, Partner
from typing import Literal, Optional


class OwnerCog(Cog, name="Owner"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def restart_bot():
        execv(executable, [executable] + argv)

    @group(
        invoke_without_command=True, description="Main partner command (Developer Only)"
    )
    @is_owner()
    async def partner(self, ctx: Context):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`partner add USER`\n`partner remove USER`",
        )
        await ctx.send(embed=embed)

    @partner.command(description="Adds a partner (Developer Only)")
    @is_owner()
    async def add(self, ctx: Context, user: User):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await Partner().add(user)
        await ctx.send(f"{user} has been added as a partner")

    @partner.command(description="Removes a partner (Developer Only)")
    @is_owner()
    async def remove(self, ctx: Context, user: User):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await Partner().remove(user)
        await ctx.send(f"{user} has been removed as a partner")

    @group(
        invoke_without_command=True, description="Main beta command (Developer Only)"
    )
    @is_owner()
    async def beta(self, ctx: Context):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`beta add USER`\n`beta remove USER`",
        )
        await ctx.send(embed=embed)

    @beta.command(description="Add a user to the Beta Programme (Developer Only)")
    @is_owner()
    async def add(self, ctx: Context, *, user: User):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await BetaTest(self.bot).add(ctx, user)

    @beta.command(description="Removes a user from the Beta Programme (Developer Only)")
    @is_owner()
    async def remove(self, ctx: Context, *, user: User):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await BetaTest(self.bot).remove(ctx, user)

    @group(
        aliases=["act", "presence"],
        invoke_without_command=True,
        description="Changes my activity (Developer Only)",
    )
    @is_owner()
    async def activity(self, ctx: Context):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`activity play ACTIVITY`\n`activity listen ACTIVITY`\n`activity clear`",
        )
        await ctx.send(embed=embed)

    @activity.command(
        aliases=["playing"], description="Make me play something (Developer Only)"
    )
    @is_owner()
    async def play(self, ctx: Context, *, activity: str):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await self.bot.change_presence(activity=Game(name=activity))
        await ctx.send(f"I am now playing `{activity}`")

    @activity.command(
        aliases=["listening"],
        description="Make me listen to something (Developer Only)",
    )
    @is_owner()
    async def listen(self, ctx: Context, *, activity: str):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await self.bot.change_presence(
            activity=Activity(type=ActivityType.listening, name=activity)
        )
        await ctx.send(f"I'm now listening to `{activity}`")

    @activity.command(
        aliases=["remove", "clean", "stop"],
        description="Clears my activity (Developer Only)",
    )
    @is_owner()
    async def clear(self, ctx: Context):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await self.bot.change_presence(activity=None)
        await ctx.send(f"I have removed my activity")

    @command(aliases=["fuser"], description="Finds a user (Developer Only)")
    @is_owner()
    async def finduser(self, ctx: Context, user_id: int):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        user = await self.bot.fetch_user(user_id)
        botr = ":o:" if user.bot else ":x:"
        fuser = Embed(title="User Found", color=0xCCFF33)
        fuser.add_field(name="Name", value=user, inline=True)
        fuser.add_field(
            name="Creation Date",
            value=f"<t:{int(user.created_at.timestamp())}:F>",
            inline=True,
        )
        fuser.add_field(name="Mutuals", value=len(user.mutual_guilds), inline=True)
        fuser.add_field(name="Bot?", value=botr, inline=True)
        fuser.set_image(url=user.display_avatar)
        if user.banner == None:
            await ctx.send(embed=fuser)
            return
        userbanner = Embed(title="User Banner", color=0xCCFF33)
        userbanner.set_image(url=user.banner)
        await ctx.send(embeds=[fuser, userbanner])

    @command(
        aliases=["restart", "refresh"], description="Updates the bot (Developer Only)"
    )
    @is_owner()
    async def update(self, ctx: Context):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await ctx.send("YAY! NEW UPDATE!")
        self.restart_bot()

    @command(
        aliases=["forbid", "disallow", "bban", "bb"],
        description="Ban a user from using Jeanne PERMANENTLY! (Developer Only)",
    )
    @is_owner()
    async def botban(self, ctx: Context, user_id: int, *, reason: str):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        if not reason:
            await ctx.send("Reason missing for botban", ephemeral=True)
            return
        user = await self.bot.fetch_user(user_id)
        await DevPunishment(user).add_botbanned_user(reason)
        await ctx.send("User botbanned", ephemeral=True)
        orleans = await self.bot.fetch_guild(740584420645535775)
        ha = await self.bot.fetch_guild(925790259160166460)
        vhf = await self.bot.fetch_guild(974028573893595146)
        for server in [orleans, ha, vhf]:
            await server.ban(user, reason=f"DevPunishmentned - {reason}")

    @command(
        aliases=["hb", "slice"],
        description="Blacklists a hentai link to prevent it to be shown again (Developer Only)",
    )
    @is_owner()
    async def hentaiblacklist(self, ctx: Context, link: str):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        await Hentai().add_blacklisted_link(link)
        await ctx.send("Link blacklisted")
        await ctx.message.delete()

    @command(
        aliases=["db", "database"],
        description="Sends the bot's database to the developer (Developer Only)",
    )
    @is_owner()
    async def senddb(self, ctx: Context):
        with open("database.db", "rb") as file:
            try:
                await ctx.author.send(file=File(file))
            except:
                content = """
# ERROR!
## Failed to send database! 
Make sure private messages between **me and you are opened** or check the host if the database exists"""
                await ctx.send(content, delete_after=10)

    @command(description="Synchronizes all commands to servers (Developer Only)")
    @guild_only()
    @is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return
        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except HTTPException:
                pass
            else:
                ret += 1
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @command(description="Warn users suspected of misusing Jeanne or the commands")
    @guild_only()
    @is_owner()
    async def warn(self, ctx: Context, user: User, *, reason: str):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        devpunish = DevPunishment(user)
        await devpunish.warn(reason)

    @command(description="Suspend a user from a certain module/s")
    @guild_only()
    @is_owner()
    async def suspend(self, ctx: Context, user: User, duration:str, *, reason: str):
        if DevPunishment(ctx.author).check_botbanned_user:
            return
        seconds=parse_timespan(duration)
        timestamp = round((datetime.now() + timedelta(seconds=seconds)).timestamp())
        view=ModuleSelect(user, reason, duration=timestamp)
        await ctx.send(view=view)
        



async def setup(bot: Bot):
    await bot.add_cog(OwnerCog(bot))
