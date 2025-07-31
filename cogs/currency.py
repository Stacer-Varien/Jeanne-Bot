from typing import Optional
from discord import (
    ButtonStyle,
    Member,
    app_commands as Jeanne,
    Interaction,
    ui,
)
from discord.ext.commands import Cog, Bot, GroupCog
from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from config import TOPGG
from topgg import DBLClient
import languages.en.currency as en
import languages.fr.currency as fr
from discord.app_commands import locale_str as T


class vote_button(ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="Top.gg",
                url="https://top.gg/bot/831993597166747679/vote",
            )
        )


class Guess_Group(GroupCog, group_name=T("guess_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
        super().__init__()

    @Jeanne.command(
        name=T("free_name"),
        description=T("guess_free_desc"),
        extras={  # for autocomplete help reasons
            "en": {
                "name": "guess free",
                "description": "Guess my number and you can win 20 QP",
            },
            "fr": {
                "name": "deviner libre",
                "description": "Devinez mon nombre et vous pouvez gagner 20 QP",
            },
        },
    )
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def free(self, ctx: Interaction):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Guess_Group(self.bot).free(ctx)
        elif ctx.locale.value == "fr":
            await fr.Guess_Group(self.bot).free(ctx)

    @Jeanne.command(
        name=T("bet_name"),
        description=T("guess_bet_desc"),
        extras={  # for autocomplete help reasons
            "en": {
                "name": "guess bet",
                "description": "Guess my number and you can win with betting",
                "parameters": [
                    {
                        "name": "bet",
                        "description": "How much are you betting?",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "deviner parier",
                "description": "Devinez mon nombre et vous pouvez gagner avec des paris",
                "parameters": [
                    {
                        "name": "pari",
                        "description": "Combien pariez-vous?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.rename(bet=T("bet_parm_name"))
    @Jeanne.describe(bet=T("bet_parm_desc"))
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def bet(
        self,
        ctx: Interaction,
        bet: Jeanne.Range[int, 5],
    ):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Guess_Group(self.bot).bet(ctx, bet)
        elif ctx.locale.value == "fr":
            await fr.Guess_Group(self.bot).bet(ctx, bet)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Guess_Group(self.bot).free_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Guess_Group(self.bot).free_error(ctx, error)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Guess_Group(self.bot).bet_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Guess_Group(self.bot).bet_error(ctx, error)


class Dice_Group(GroupCog, group_name=T("dice_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
        super().__init__()

    @Jeanne.command(
        name=T("free_name"),
        description=T("dice_free_desc"),
        extras={  # for autocomplete help reasons
            "en": {
                "name": "dice free",
                "description": "Roll a dice and earn 20 QP for free",
            },
            "fr": {
                "name": "dé libre",
                "description": "Lancez un dé et gagnez 20 QP gratuitement",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    async def free(self, ctx: Interaction):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Dice_Group(self.bot).free(ctx)
        elif ctx.locale.value == "fr":
            await fr.Dice_Group(self.bot).free(ctx)

    @Jeanne.command(
        name=T("bet_name"),
        description=T("dice_bet_desc"),
        extras={  # for autocomplete help reasons
            "en": {
                "name": "dice bet",
                "description": "Roll a dice and win with betting",
                "parameters": [
                    {
                        "name": "bet",
                        "description": "How much are you betting?",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "dé parier",
                "description": "Lancez un dé et gagnez avec des paris",
                "parameters": [
                    {
                        "name": "pari",
                        "description": "Combien pariez-vous?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(bet=T("bet_parm_desc"))
    @Jeanne.rename(bet=T("bet_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    async def bet(
        self,
        ctx: Interaction,
        bet: Jeanne.Range[int, 5],
    ):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Dice_Group(self.bot).bet(ctx, bet)
        elif ctx.locale.value == "fr":
            await fr.Dice_Group(self.bot).bet(ctx, bet)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Dice_Group(self.bot).free_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Dice_Group(self.bot).free_error(ctx, error)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Dice_Group(self.bot).bet_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Dice_Group(self.bot).bet_error(ctx, error)


class Flip_Group(GroupCog, group_name=T("flip_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    @Jeanne.command(
        name=T("free_name"),
        description=T("flip_free_desc"),
        extras={  # for autocomplete help reasons
            "en": {
                "name": "flip free",
                "description": "Flip a coin and earn 20 QP for free",
            },
            "fr": {
                "name": "lancer libre",
                "description": "Lancez une pièce et gagnez 20 QP gratuitement",
            },
        },
    )
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def free(self, ctx: Interaction):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Flip_Group(self.bot).free(ctx)
        elif ctx.locale.value == "fr":
            await fr.Flip_Group(self.bot).free(ctx)

    @Jeanne.command(
        name=T("bet_name"),
        description=T("flip_bet_desc"),
        extras={  # for autocomplete help reasons
            "en": {
                "name": "flip bet",
                "description": "Flip a coin and earn with betting",
                "parameters": [
                    {
                        "name": "bet",
                        "description": "How much are you betting?",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "lancer parier",
                "description": "Lancez une pièce et gagnez avec des paris",
                "parameters": [
                    {
                        "name": "pari",
                        "description": "Combien pariez-vous?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(bet=T("bet_parm_desc"))
    @Jeanne.rename(bet=T("bet_parm_name"))
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def bet(self, ctx: Interaction, bet: Jeanne.Range[int, 5]):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Flip_Group(self.bot).bet(ctx, bet)
        elif ctx.locale.value == "fr":
            await fr.Flip_Group(self.bot).bet(ctx, bet)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Flip_Group(self.bot).free_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Flip_Group(self.bot).free_error(ctx, error)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Flip_Group(self.bot).bet_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.Flip_Group(self.bot).bet_error(ctx, error)


class Blackjack_Group(GroupCog, group_name=T("blackjack_group_name")):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name=T("free_name"),
        description=T("bj_free_desc"),
        extras={
            "en": {
                "name": "blackjack free",
                "description": "Play blackjack for free and earn 20 QP",
            },
            "fr": {
                "name": "blackjack libre",
                "description": "Jouez au blackjack gratuitement et gagnez 20 QP",
            },
        },
    )
    @Jeanne.checks.cooldown(1, 3600, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def free(self, ctx: Interaction):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Blackjack_Group(self.bot).free(ctx)
        elif ctx.locale.value == "fr":
            await fr.Blackjack_Group(self.bot).free(ctx)

    @Jeanne.command(
        name=T("bet_name"),
        description=T("bj_bet_desc"),
        extras={
            "en": {
                "name": "blackjack bet",
                "description": "Play a game of blackjack and win with betting",
                "parameters": [
                    {
                        "name": "bet",
                        "description": "How much are you betting?",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "blackjack parier",
                "description": "Jouez au blackjack et gagnez avec des paris",
                "parameters": [
                    {
                        "name": "pari",
                        "description": "Combien pariez-vous?",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(bet=T("bet_parm_desc"))
    @Jeanne.rename(bet=T("bet_parm_name"))
    @Jeanne.checks.cooldown(1, 20, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def bet(self, ctx: Interaction, bet: Jeanne.Range[int, 5]):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.Blackjack_Group(self.bot).bet(ctx, bet)
        elif ctx.locale.value == "fr":
            await fr.Blackjack_Group(self.bot).bet(ctx, bet)

    @free.error
    async def free_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Blackjack_Group(self.bot).free_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Blackjack_Group(self.bot).free_error(ctx, error)

    @bet.error
    async def bet_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.Blackjack_Group(self.bot).bet_error(ctx, error)
        elif ctx.locale.value == "fr":
            await fr.Blackjack_Group(self.bot).bet_error(ctx, error)


class currency(Cog, name="CurrencySlash"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.balance_context = Jeanne.ContextMenu(
            name=T("balance_name"), callback=self.balance_callback
        )
        self.bot.tree.add_command(self.balance_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.balance_context.name, type=self.balance_context.type
        )
        self.balance_callback_error = self.balance_context.error(
            self.balance_callback_error
        )

    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def balance_callback(self, ctx: Interaction, member: Member):
        await self.get_balance(ctx, member)

    async def balance_callback_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.currency(self.bot).balance_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.currency(self.bot).balance_error(ctx, error)

    async def get_balance(self, ctx: Interaction, member: Member):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.currency(self.bot).get_balance(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.currency(self.bot).get_balance(ctx, member)

    @Jeanne.command(
        name=T("daily_name"),
        description=T("daily_desc"),
        extras={
            "en": {"name": "daily", "description": "Claim your daily QP reward"},
            "fr": {
                "name": "quotidien",
                "description": "Réclamez votre récompense quotidienne de QP",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def daily(self, ctx: Interaction):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.currency(self.bot).daily(ctx)
        elif ctx.locale.value == "fr":
            await fr.currency(self.bot).daily(ctx)

    @Jeanne.command(
        name=T("balance_name"),
        description=T("balance_desc"),
        extras={
            "en": {
                "name": "balance",
                "description": "Check your or another user's balance",
                "parameters": [
                    {"name": "member", "description": "Which member?", "required": 1}
                ],
            },
            "fr": {
                "name": "solde",
                "description": "Vérifiez votre solde ou celui d'un autre utilisateur",
                "parameters": [
                    {"name": "member", "description": "Quel membre?", "required": 1}
                ],
            },
        },
    )
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def balance(self, ctx: Interaction, member: Optional[Member] = None):
        member = ctx.user if (member is None) else member
        await self.get_balance(ctx, member)

    @balance.error
    async def balance_error(
        self, ctx: Interaction, error: Jeanne.errors.AppCommandError
    ):
        if isinstance(error, Jeanne.errors.CommandOnCooldown):
            if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
                await en.currency(self.bot).balance_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.currency(self.bot).balance_error(ctx, error)

    @Jeanne.command(
        name=T("vote_name"),
        description=T("vote_desc"),
        extras={
            "en": {"name": "vote", "description": "Vote for Jeanne on Top.gg"},
            "fr": {"name": "voter", "description": "Votez pour Jeanne sur Top.gg"},
        },
    )
    @Jeanne.check(is_suspended)
    async def vote(self, ctx: Interaction):
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            await en.currency(self.bot).vote(ctx)
        elif ctx.locale.value == "fr":
            await fr.currency(self.bot).vote(ctx)


async def setup(bot: Bot):
    await bot.add_cog(Guess_Group(bot))
    await bot.add_cog(Dice_Group(bot))
    await bot.add_cog(Flip_Group(bot))
    await bot.add_cog(Blackjack_Group(bot))
    await bot.add_cog(currency(bot))
