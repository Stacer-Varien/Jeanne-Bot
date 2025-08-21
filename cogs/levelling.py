from discord.ext.commands import Cog, Bot, GroupCog
from discord import (
    Interaction,
    Member,
    app_commands as Jeanne,
)
from config import TOPGG
from functions import (
    Levelling,
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from typing import Optional
from topgg import DBLClient
import languages.en.levelling as en
import languages.fr.levelling as fr
import languages.de.levelling as de
from discord.app_commands import locale_str as T


class Rank_Group(GroupCog, name="rank"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    async def send_leaderboard(
        self, ctx: Interaction, title: str, leaderboard: list, exp_index: int
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Rank_Group(self.bot).send_leaderboard(
                ctx, title, leaderboard, exp_index
            )
        elif ctx.locale.value == "fr":
            await fr.Rank_Group(self.bot).send_leaderboard(
                ctx, title, leaderboard, exp_index
            )
        elif ctx.locale.value == "de":
            await de.Rank_Group(self.bot).send_leaderboard(
                ctx, title, leaderboard, exp_index
            )

    @Jeanne.command(
        name="global",
        description=T("global_desc"),
        extras={
            "en": {
                "name": "global",
                "description": "Check the users with the most XP globally",
            },
            "fr": {
                "name": "global",
                "description": "Vérifiez les utilisateurs avec le plus d'XP globalement",
            },
            "de": {
                "name": "global",
                "description": "Überprüfen Sie die Benutzer mit dem meisten XP global",
            },
        },
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _global(self, ctx: Interaction):
        leaderboard = Levelling().get_global_rank
        await self.send_leaderboard(ctx, "Global XP Leaderboard", leaderboard, 2)

    @Jeanne.command(
        description=T("server_desc"),
        extras={
            "en": {
                "name": "server",
                "description": "Check the users with the most XP in this server",
            },
            "fr": {
                "name": "serveur",
                "description": "Vérifiez les utilisateurs avec le plus d'XP dans ce serveur",
            },
            "de": {
                "name": "server",
                "description": "Überprüfen Sie die Benutzer mit dem meisten XP auf diesem Server",
            },
        },
    )
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
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.levelling(self.bot).generate_profile_card(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.levelling(self.bot).generate_profile_card(ctx, member)
        elif ctx.locale.value == "de":
            await de.levelling(self.bot).generate_profile_card(ctx, member)

    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def profile_generate(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    async def profile_generate_error(self, ctx: Interaction, error: Exception) -> None:
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.levelling(self.bot).profile_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.levelling(self.bot).profile_error(ctx, error)
            elif ctx.locale.value == "de":
                await de.levelling(self.bot).profile_error(ctx, error)

    @Jeanne.command(
        name=T("profile_name"),
        description=T("profile_desc"),
        extras={
            "en": {
                "name": "profile",
                "description": "See your profile or someone else's profile",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "profil",
                "description": "Voir votre profil ou celui d'un autre membre",
                "parameters": [
                    {"name": "membre", "description": "Quel membre?", "required": False}
                ],
            },
            "de": {
                "name": "profil",
                "description": "Sehen Sie Ihr Profil oder das eines anderen Mitglieds",
                "parameters": [
                    {"name": "mitglied", "description": "Welches Mitglied?", "required": False}
                ],
            },
        },
    )
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def profile(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.levelling(self.bot).profile(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.levelling(self.bot).profile(ctx, member)
        elif ctx.locale.value == "de":
            await de.levelling(self.bot).profile(ctx, member)

    @profile.error
    async def profile_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.levelling(self.bot).profile_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.levelling(self.bot).profile_error(ctx, error)
            elif ctx.locale.value == "de":
                await de.levelling(self.bot).profile_error(ctx, error)


async def setup(bot: Bot):
    await bot.add_cog(Rank_Group(bot))
    await bot.add_cog(levelling(bot))
