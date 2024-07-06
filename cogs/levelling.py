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
)
from typing import Optional
from assets.generators.profile_card import Profile
from topgg import DBLClient


class Rank_Group(GroupCog, name="rank"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name="global", description="Check the users with the most XP globally"
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def _global(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name="Global XP Leaderboard")
        leaderboard = Levelling().get_global_rank
        if leaderboard == None:
            embed.description = "No global leaderboard provided"
            await ctx.followup.send(embed=embed)
            return
        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[2]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)
        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Check the users with the most XP in the server")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def server(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name="Server XP Leaderboard")
        leaderboard = Levelling(server=ctx.guild).get_server_rank
        if leaderboard == None:
            embed.description = "No server leaderboard provided"
            await ctx.followup.send(embed=embed)
            return
        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[3]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)
        await ctx.followup.send(embed=embed)


class levelling(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
        self.profile_context = Jeanne.ContextMenu(
            name="Profile", callback=self.profile_generate
        )
        self.bot.tree.add_command(self.profile_context)
        self.profile_generate_error = self.profile_context.error(
            self.profile_generate_error
        )

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.profile_context.name, type=self.profile_context.type
        )

    async def generate_profile_card(self, ctx: Interaction, member: Member):
        try:
            voted = await self.topggpy.get_user_vote(member.id)
            bg_image = Inventory(member).selected_wallpaper
            country = Inventory(member).selected_country
            image = await Profile(self.bot).generate_profile(
                member, bg_image, voted, country
            )
            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.followup.send(file=file)
        except:
            no_exp = Embed(description=f"Failed to make profile card")
            await ctx.followup.send(embed=no_exp)

    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def profile_generate(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    async def profile_generate_error(self, ctx: Interaction, error: Exception) -> None:
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="See your profile or someone else's profile")
    @Jeanne.describe(member="Which member?")
    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def profile(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        member = ctx.user if member == None else member
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    @profile.error
    async def profile_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


async def setup(bot: Bot):
    await bot.add_cog(Rank_Group(bot))
    await bot.add_cog(levelling(bot))
