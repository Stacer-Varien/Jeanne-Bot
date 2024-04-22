from discord.ext.commands import Cog, Bot, Context, BucketType
import discord.ext.commands as Jeanne
from discord import (
    Color,
    Embed,
    File,
    Member,
)
from config import TOPGG
from functions import (
    Inventory,
    Levelling,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from typing import Optional
from assets.generators.profile_card import Profile
from topgg import DBLClient


class levelling(Cog, name="Level"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    async def generate_profile_card(self, ctx: Context, member: Member):
        try:
            voted = await self.topggpy.get_user_vote(member.id)
            bg_image = Inventory(member).selected_wallpaper
            image = await Profile(self.bot).generate_profile(member, bg_image, voted)
            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.send(file=file)
        except:
            no_exp = Embed(description=f"Failed to make profile card")
            await ctx.send(embed=no_exp)

    @Jeanne.group(
        name="rank",
        description="Main rank command",
        invoke_without_command=True,
    )
    async def rank(self, ctx: Context): ...
    @rank.command(
        name="global", description="Check the users with the most XP globally"
    )
    @Jeanne.cooldown(1, 60, type=BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def _global(self, ctx: Context):
        embed = Embed(color=Color.random())
        embed.set_author(name="Global XP Leaderboard")
        leaderboard = Levelling().get_global_rank
        if leaderboard == None:
            embed.description = "No global leaderboard provided"
            await ctx.send(embed=embed)
            return
        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[3]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)
        await ctx.send(embed=embed)

    @rank.command(description="Check the users with the most XP in the server")
    @Jeanne.cooldown(1, 60, type=BucketType.member)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def server(self, ctx: Context):
        embed = Embed(color=Color.random())
        embed.set_author(name="Server XP Leaderboard")
        leaderboard = Levelling(server=ctx.guild).get_server_rank
        if leaderboard == None:
            embed.description = "No server leaderboard provided"
            await ctx.send(embed=embed)
            return
        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[4]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)
        await ctx.send(embed=embed)

    @Jeanne.command(description="See your profile or someone else's profile")
    @Jeanne.cooldown(1, 120, type=BucketType.user)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def profile(self, ctx: Context, member: Optional[Member] = None) -> None:
        member = ctx.author if member == None else member
        async with ctx.typing():
            await self.generate_profile_card(ctx, member)

    @_global.error
    async def _global_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already used this command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @server.error
    async def server_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already used this command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)

    @profile.error
    async def profile_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown)


async def setup(bot: Bot):
    await bot.add_cog(levelling(bot))
