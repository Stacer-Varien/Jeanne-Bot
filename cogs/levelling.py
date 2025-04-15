from discord.ext.commands import Cog, Bot, GroupCog
from discord import (
    Color,
    Embed,
    File,
    Interaction,
    Member,
    app_commands as Jeanne,
)
from config import TOPGG
from functions import (
    Inventory,
    Levelling,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from typing import Optional
from assets.generators.profile_card import Profile
from topgg import DBLClient


class Rank_Group(GroupCog, name="rank"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    async def send_leaderboard(
        self, ctx: Interaction, title: str, leaderboard: list, exp_index: int
    ):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name=title)
        if not leaderboard:
            embed.description = f"No {title.lower()} provided"
            await ctx.followup.send(embed=embed)
            return
        for rank, entry in enumerate(leaderboard, start=1):
            user = await self.bot.fetch_user(entry[0])
            exp = entry[exp_index]
            embed.add_field(name=f"`{rank}.` {user}", value=f"`{exp}XP`", inline=True)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(name="global", description="Check the users with the most XP globally")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _global(self, ctx: Interaction):
        leaderboard = Levelling().get_global_rank
        await self.send_leaderboard(ctx, "Global XP Leaderboard", leaderboard, 2)

    @Jeanne.command(description="Check the users with the most XP in the server")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def server(self, ctx: Interaction):
        leaderboard = Levelling(server=ctx.guild).get_server_rank
        await self.send_leaderboard(ctx, "Server XP Leaderboard", leaderboard, 3)


class levelling(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
        self.profile_context = Jeanne.ContextMenu(
            name="Profile", callback=self.profile_generate
        )
        self.bot.tree.add_command(self.profile_context)
        self.profile_context.error(self.profile_generate_error)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.profile_context.name, type=self.profile_context.type
        )

    async def generate_profile_card(self, ctx: Interaction, member: Member):
        try:
            voted = await self.topggpy.get_user_vote(member.id)
            inventory = Inventory(member)
            image = await Profile(self.bot).generate_profile(
                member,
                bg_image=inventory.selected_wallpaper,
                voted=voted,
                country=inventory.selected_country,
            )
            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.followup.send(file=file)
        except Exception as e:
            embed = Embed(description=f"Failed to generate profile card: {e}", color=Color.red())
            await ctx.followup.send(embed=embed)

    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def profile_generate(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    async def profile_generate_error(self, ctx: Interaction, error: Exception) -> None:
        if isinstance(error, Jeanne.CommandOnCooldown):
            embed = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=embed)

    @Jeanne.command(description="See your profile or someone else's profile")
    @Jeanne.describe(member="Which member?")
    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def profile(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member or ctx.user)

    @profile.error
    async def profile_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            embed = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(Rank_Group(bot))
    await bot.add_cog(levelling(bot))
