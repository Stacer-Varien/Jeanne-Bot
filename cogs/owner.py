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
from functions import BetaTest, Botban, Hentai, Partner
from typing import Literal, Optional


class OwnerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def restart_bot():
        execv(executable, [executable] + argv)

    @group(invoke_without_command=True)
    @is_owner()
    async def partner(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`partner add USER`\n`partner remove USER`",
        )
        await ctx.send(embed=embed)

    @partner.command(aliases=["add"])
    @is_owner()
    async def _add(self, ctx: Context, user: User):
        if Botban(ctx.author).check_botbanned_user:
            return

        await Partner().add(user)
        await ctx.send(f"{user} has been added as a partner")

    @partner.command(aliases=["remove"])
    @is_owner()
    async def _remove(self, ctx: Context, user: User):
        if Botban(ctx.author).check_botbanned_user:
            return

        await Partner().remove(user)
        await ctx.send(f"{user} has been removed as a partner")

    @group(invoke_without_command=True)
    @is_owner()
    async def beta(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`beta add USER`\n`beta remove USER`",
        )
        await ctx.send(embed=embed)

    @beta.command(aliases=["add"])
    @is_owner()
    async def _add(self, ctx: Context, user: User):
        if Botban(ctx.author).check_botbanned_user:
            return
        server = await self.bot.fetch_guild(740584420645535775)
        betarole = server.get_role(1130430961587335219)
        try:
            m = await server.fetch_member(user.id)
            await m.add_roles(betarole, reason="Added to the Beta Programme")
            await BetaTest().add(user)
            await ctx.send(f"{user} has been added as a Beta Tester")
        except:
            await ctx.send(
                f"Member is not in {server}. This is required so they can be added in the Beta Programme"
            )

    @beta.command(aliases=["remove"])
    @is_owner()
    async def _remove(self, ctx: Context, user: User):
        if Botban(ctx.author).check_botbanned_user:
            return

        server = await self.bot.fetch_guild(740584420645535775)
        betarole = server.get_role(1130430961587335219)
        try:
            m = await server.fetch_member(user.id)
            await m.add_roles(betarole, reason="Removed from the Beta Programme")
        except:
            await ctx.send(
                f"Member is not in {server}. This is required so they can be added in the Beta Programme"
            )
        await BetaTest().remove(user)

    @group(aliases=["act", "presence"], invoke_without_command=True)
    @is_owner()
    async def activity(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return

        embed = Embed(
            title="This is a group command. However, the available commands for this are:",
            description="`activity play ACTIVITY`\n`activity listen ACTIVITY`\n`activity clear`",
        )
        await ctx.send(embed=embed)

    @activity.command(aliases=["playing"])
    @is_owner()
    async def play(self, ctx: Context, *, activity: str):
        if Botban(ctx.author).check_botbanned_user:
            return

        await self.bot.change_presence(activity=Game(name=activity))
        await ctx.send(f"Jeanne is now playing `{activity}`")

    @activity.command(aliases=["listening"])
    @is_owner()
    async def listen(self, ctx: Context, *, activity: str):
        if Botban(ctx.author).check_botbanned_user:
            return

        await self.bot.change_presence(
            activity=Activity(type=ActivityType.listening, name=activity)
        )
        await ctx.send(f"Jeanne is now listening to `{activity}`")

    @activity.command(aliases=["remove", "clean", "stop"])
    @is_owner()
    async def clear(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return

        await self.bot.change_presence(activity=None)
        await ctx.send(f"Jeanne's activity has been removed")

    @command(aliases=["fuser"])
    @is_owner()
    async def finduser(self, ctx: Context, user_id: int):
        await ctx.defer()
        if Botban(ctx.author).check_botbanned_user:
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

    @command(aliases=["restart", "refresh"])
    @is_owner()
    async def update(self, ctx: Context):
        await ctx.defer()
        if Botban(ctx.author).check_botbanned_user:
            return

        await ctx.send("YAY! NEW UPDATE!")
        self.restart_bot()

    @command(aliases=["forbid", "disallow", "bban", "bb"])
    @is_owner()
    async def botban(self, ctx: Context, user_id: int, *, reason: str):
        if Botban(ctx.author).check_botbanned_user:
            return
        if not reason:
            await ctx.send("Reason missing for botban", ephemeral=True)
            return

        user = await self.bot.fetch_user(user_id)
        await Botban(user).add_botbanned_user(reason)

        await ctx.send("User botbanned", ephemeral=True)

        orleans = await self.bot.fetch_guild(740584420645535775)
        ha = await self.bot.fetch_guild(925790259160166460)
        vhf = await self.bot.fetch_guild(974028573893595146)

        for server in [orleans, ha, vhf]:
            await server.ban(user, reason=f"Botbanned - {reason}")

    @command(aliases=["hb", "slice"])
    @is_owner()
    async def hentaiblacklist(self, ctx: Context, link: str):
        if Botban(ctx.author).check_botbanned_user:
            return
        await Hentai().add_blacklisted_link(link)
        await ctx.send("Link blacklisted")

    @command(aliases=["db", "database"])
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

    @command()
    @guild_only()
    @is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if Botban(ctx.author).check_botbanned_user:
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


async def setup(bot: Bot):
    await bot.add_cog(OwnerCog(bot))
