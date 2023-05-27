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
    Game,
    Activity,
    Object,
    HTTPException,
    SyncWebhook,
)
from os import execv
from sys import executable, argv
from functions import Botban, Hentai
from config import BB_WEBHOOK
from typing import Literal, Optional


def restart_bot():
    execv(executable, [executable] + argv)


class OwnerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(aliases=["act", "presence"], invoke_without_command=True)
    @is_owner()
    async def activity(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user():
            return

        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`activity play ACTIVITY`\n`activity listen ACTIVITY`\n`activity clear`",
        )
        await ctx.send(embed=embed)

    @activity.command(aliases=["playing"])
    @is_owner()
    async def play(self, ctx: Context, *, activity: str):
        """Make Jeanne play something as an activity"""
        if Botban(ctx.author).check_botbanned_user():
            return

        await self.bot.change_presence(activity=Game(name=activity))
        await ctx.send(f"Jeanne is now playing `{activity}`")

    @activity.command(aliases=["listening"])
    @is_owner()
    async def listen(self, ctx: Context, *, activity: str):
        """Make Jeanne listen to something as an activity"""
        if Botban(ctx.author).check_botbanned_user():
            return

        await self.bot.change_presence(
            activity=Activity(type=ActivityType.listening, name=activity)
        )
        await ctx.send(f"Jeanne is now listening to `{activity}`")

    @activity.command(aliases=["remove", "clean", "stop"])
    @is_owner()
    async def clear(self, ctx: Context):
        """Clears the bot's activity"""
        if Botban(ctx.author).check_botbanned_user():
            return

        await self.bot.change_presence(activity=None)
        await ctx.send(f"Jeanne's activity has been removed")

    @command(aliases=["fuser"])
    @is_owner()
    async def finduser(self, ctx: Context, user_id: int):
        """Finds a user"""
        await ctx.defer()
        if Botban(ctx.author).check_botbanned_user():
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
        if user.banner is None:
            await ctx.send(embed=fuser)
        else:
            userbanner = Embed(title="User Banner", color=0xCCFF33)
            userbanner.set_image(url=user.banner)

            await ctx.send(embeds=[fuser, userbanner])

    @command(aliases=["restart", "refresh"])
    @is_owner()
    async def update(self, ctx: Context):
        """Restart me so I can be updated"""
        await ctx.defer()
        if Botban(ctx.author).check_botbanned_user():
            return

        await ctx.send(f"YAY! NEW UPDATE!")
        restart_bot()

    @command(aliases=["forbid", "disallow", "bban", "bb"])
    @is_owner()
    async def botban(self, ctx: Context, user_id: int, *, reason: str):
        """Botban a user from using the bot"""
        if Botban(ctx.author).check_botbanned_user():
            return
        if not reason:
            await ctx.send("Reason missing for botban", ephemeral=True)
            return

        user = await self.bot.fetch_user(user_id)
        Botban(user).add_botbanned_user(reason)

        botbanned = Embed(
            title="User has been botbanned!",
            description="They will no longer use Jeanne, permanently!",
        )
        botbanned.add_field(name="User", value=user)
        botbanned.add_field(name="ID", value=user.id, inline=True)
        botbanned.add_field(name="Reason of ban", value=reason, inline=False)
        botbanned.set_footer(
            text="Due to this user botbanned, all data except warnings and soft bans are immediately deleted from the database and banned in the developer's servers! They will have no chance of appealing their botban, including their ban, and all the commands executed by them are now rendered USELESS!"
        )
        botbanned.set_thumbnail(url=user.avatar)
        webhook = SyncWebhook.from_url(BB_WEBHOOK)
        await webhook.send(embed=botbanned)

        await ctx.send("User botbanned", ephemeral=True)

        orleans = await self.bot.fetch_guild(740584420645535775)
        ha = await self.bot.fetch_guild(925790259160166460)
        vhf = await self.bot.fetch_guild(974028573893595146)

        for server in [orleans, ha, vhf]:
            await server.ban(user, reason=f"Botbanned - {reason}")

    @command(aliases=["hb", "slice"])
    @is_owner()
    async def hentaiblacklist(self, ctx: Context, link: str):
        Hentai().add_blacklisted_link(link)
        await ctx.send("Link blacklisted", ephemeral=True)

    @command()
    @guild_only()
    @is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
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


async def setup(bot: Bot):
    await bot.add_cog(OwnerCog(bot))
