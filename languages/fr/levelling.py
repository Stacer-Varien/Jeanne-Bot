from discord.ext.commands import Cog, Bot
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
)
from typing import Optional
from assets.generators.profile_card import Profile
from topgg import DBLClient


class Rank_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_leaderboard(
        self, ctx: Interaction, title: str, leaderboard: list, exp_index: int
    ):
        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name=title)
        if not leaderboard:
            embed.description = f"Aucun {title.lower()} fourni"
            await ctx.followup.send(embed=embed)
            return
        for rank, entry in enumerate(leaderboard, start=1):
            user = await self.bot.fetch_user(entry[0])
            exp = entry[exp_index]
            embed.add_field(name=f"`{rank}.` {user}", value=f"`{exp}XP`", inline=True)
        await ctx.followup.send(embed=embed)


    async def _global(self, ctx: Interaction):
        leaderboard = Levelling().get_global_rank
        await self.send_leaderboard(ctx, "Global XP Leaderboard", leaderboard, 2)


    async def server(self, ctx: Interaction):
        leaderboard = Levelling(server=ctx.guild).get_server_rank
        await self.send_leaderboard(ctx, "Server XP Leaderboard", leaderboard, 3)


class levelling(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
 


    async def generate_profile_card(self, ctx: Interaction, member: Member):
        try:
            #voted = await self.topggpy.get_user_vote(member.id)
            inventory = Inventory(member)
            image = await Profile(self.bot).generate_profile(ctx,
                member,
                bg_image=inventory.selected_wallpaper,
                voted=False,
                country=inventory.selected_country,
            )
            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.followup.send(file=file)
        except Exception as e:
            embed = Embed(description=f"Échec de la génération de la carte de profil : {e}", color=Color.red())
            await ctx.followup.send(embed=embed)

    async def profile_generate(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    async def profile_generate_error(self, ctx: Interaction, error: Exception) -> None:
            embed = Embed(
                description=f"Vous avez déjà utilisé la commande de profil !\nRéessayez après `{round(error.retry_after, 2)} secondes`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=embed)


    async def profile(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member or ctx.user)

    async def profile_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            embed = Embed(
                description=f"Vous avez déjà utilisé la commande de profil !\nRéessayez après `{round(error.retry_after, 2)} secondes`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=embed)
