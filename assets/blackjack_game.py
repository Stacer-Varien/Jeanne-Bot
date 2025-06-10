from random import randint
from typing import Optional
from discord import ButtonStyle, Color, Embed, Interaction, ui
from discord.ext.commands import Bot
from config import TOPGG
from functions import BetaTest, Currency
from topgg import DBLClient

values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}
emoji_map = {"Hearts": "♥️", "Diamonds": "♦️", "Clubs": "♣️", "Spades": "♠️"}


def calculate_hand(hand) -> int:
    value = sum(values[card[0]] for card in hand)
    num_aces = sum(1 for card in hand if card[0] == "A")
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value


def deal_card(deck: list[tuple[str, str]]) -> tuple[str, str]:
    return deck.pop(randint(0, len(deck) - 1))


class BlackjackView(ui.View):
    def __init__(
        self, bot: Bot, deck, player_hand, dealer_hand, bet: Optional[int] = None
    ):
        super().__init__(timeout=60)
        self.deck = deck
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.player_value = calculate_hand(player_hand)
        self.dealer_value = calculate_hand(dealer_hand)
        self.embed = self.create_embed()
        self.bet = bet
        self.value = None
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    def create_embed(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            embed = Embed(title="Blackjack", color=Color.green())
            embed.add_field(
                name="Your Hand",
                value=self.hand_value_string(self.player_hand, self.player_value),
                inline=False,
            )
            embed.add_field(
                name="Dealer's Hand",
                value=f"**?** (Hidden, {self.dealer_hand[1][0]}{emoji_map[self.dealer_hand[1][1]]})",
                inline=False,
            )
            return embed
        elif ctx.locale.value == "fr":
            embed = Embed(title="Blackjack", color=Color.green())
            embed.add_field(
                name="Votre main",
                value=self.hand_value_string(self.player_hand, self.player_value),
                inline=False,
            )
            embed.add_field(
                name="Main du croupier",
                value=f"**?** (Cachée, {self.dealer_hand[1][0]}{emoji_map[self.dealer_hand[1][1]]})",
                inline=False,
            )
            return embed

    def hand_to_string(self, hand):
        return ", ".join([f"{rank}{emoji_map[suit]}" for rank, suit in hand])

    def hand_value_string(self, hand, value):
        return f"**{value}** ({self.hand_to_string(hand)})"

    @ui.button(label="Hit", style=ButtonStyle.primary)
    async def hit(
        self,
        ctx: Interaction,
        button: ui.Button,
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.value = "Hit"
        elif ctx.locale.value == "fr":
            self.value = "Tirer"

        self.player_hand.append(deal_card(self.deck))
        self.player_value = calculate_hand(self.player_hand)
        self.embed = self.create_embed(ctx)

        if self.player_value > 21:
            self.embed.color = Color.red()
            # Locale-based bust message
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                self.embed.title = "You busted! You lose."
                if self.bet:
                    self.embed.description = f"Unfortunately, I have to take away {self.bet} <:quantumpiece:1161010445205905418>"
            elif ctx.locale.value == "fr":
                self.embed.title = "Vous avez dépassé 21 ! Vous perdez."
                if self.bet:
                    self.embed.description = f"Malheureusement, je dois retirer {self.bet} <:quantumpiece:1161010445205905418>"
            if self.bet:
                await Currency(ctx.user).remove_qp(self.bet)
            for item in self.children:
                item.disabled = True
            await ctx.response.edit_message(embed=self.embed, view=self)
            return

        await ctx.response.edit_message(embed=self.embed, view=self)

    @ui.button(label="Stand", style=ButtonStyle.danger)
    async def stand(
        self,
        ctx: Interaction,
        button: ui.Button,
    ):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.value = "Stand"
        elif ctx.locale.value == "fr":
            self.value="Rester"
        for item in self.children:
            item.disabled = True
        await ctx.response.edit_message(view=self)

        while self.dealer_value < 17:
            self.dealer_hand.append(deal_card(self.deck))
            self.dealer_value = calculate_hand(self.dealer_hand)

        # Locale-based result embed
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            result_embed = Embed(title="Blackjack Result", color=Color.red())
            result_embed.add_field(
                name="Your Hand",
                value=self.hand_value_string(self.player_hand, self.player_value),
                inline=False,
            )
            result_embed.add_field(
                name="Dealer's Hand",
                value=self.hand_value_string(self.dealer_hand, self.dealer_value),
                inline=False,
            )
            if self.dealer_value > 21 or self.player_value > self.dealer_value:
                result_embed.title = "You win!"
                if self.bet:
                    result_embed.description = (
                        f"You have won {self.bet} <:quantumpiece:1161010445205905418>"
                    )
                    await Currency(ctx.user).add_qp(self.bet)
                    if await self.topggpy.get_user_vote(ctx.user.id) == True:
                        await Currency(ctx.user).add_qp(round((self.bet * 1.25)))
                        result_embed.add_field(
                            name="DiscordBotList Bonus",
                            value=f"{round((self.bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                        )
                    if await BetaTest(self.bot).check(ctx.user) == True:
                        await Currency(ctx.user).add_qp(round((self.bet * 1.25)))
                        result_embed.add_field(
                            name="Beta User Bonus",
                            value=f"{round((self.bet * 1.25))} <:quantumpiece:1161010445205905418>",
                        )
                else:
                    result_embed.description = (
                        f"You have won 20 <:quantumpiece:1161010445205905418>"
                    )
                    await Currency(ctx.user).add_qp(20)
                    if await self.topggpy.get_user_vote(ctx.user.id) == True:
                        await Currency(ctx.user).add_qp(round((20 * 1.25)))
                        result_embed.add_field(
                            name="DiscordBotList Bonus",
                            value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                        )
                    if await BetaTest(self.bot).check(ctx.user) == True:
                        await Currency(ctx.user).add_qp(round((20 * 1.25)))
                        result_embed.add_field(
                            name="Beta User Bonus",
                            value=f"{round((20 * 1.25))} <:quantumpiece:1161010445205905418>",
                        )
                result_embed.color = Color.green()
            elif self.player_value < self.dealer_value:
                result_embed.title = "You lose!"
                if self.bet:
                    result_embed.description = f"Unfortunately, I have to take away {self.bet} <:quantumpiece:1161010445205905418>"
                    await Currency(ctx.user).remove_qp(self.bet)
            else:
                result_embed.title = "It's a tie!"
        elif ctx.locale.value == "fr":
            result_embed = Embed(title="Résultat du Blackjack", color=Color.red())
            result_embed.add_field(
                name="Votre main",
                value=self.hand_value_string(self.player_hand, self.player_value),
                inline=False,
            )
            result_embed.add_field(
                name="Main du croupier",
                value=self.hand_value_string(self.dealer_hand, self.dealer_value),
                inline=False,
            )
            if self.dealer_value > 21 or self.player_value > self.dealer_value:
                result_embed.title = "Vous gagnez !"
                if self.bet:
                    result_embed.description = f"Vous avez gagné {self.bet} <:quantumpiece:1161010445205905418>"
                    await Currency(ctx.user).add_qp(self.bet)
                    if await self.topggpy.get_user_vote(ctx.user.id) == True:
                        await Currency(ctx.user).add_qp(round((self.bet * 1.25)))
                        result_embed.add_field(
                            name="Bonus DiscordBotList",
                            value=f"{round((self.bet * 1.25),2)} <:quantumpiece:1161010445205905418>",
                        )
                    if await BetaTest(self.bot).check(ctx.user) == True:
                        await Currency(ctx.user).add_qp(round((self.bet * 1.25)))
                        result_embed.add_field(
                            name="Bonus utilisateur bêta",
                            value=f"{round((self.bet * 1.25))} <:quantumpiece:1161010445205905418>",
                        )
                else:
                    result_embed.description = (
                        f"Vous avez gagné 20 <:quantumpiece:1161010445205905418>"
                    )
                    await Currency(ctx.user).add_qp(20)
                    if await self.topggpy.get_user_vote(ctx.user.id) == True:
                        await Currency(ctx.user).add_qp(round((20 * 1.25)))
                        result_embed.add_field(
                            name="Bonus DiscordBotList",
                            value=f"{round((20 * 1.25),2)} <:quantumpiece:1161010445205905418>",
                        )
                    if await BetaTest(self.bot).check(ctx.user) == True:
                        await Currency(ctx.user).add_qp(round((20 * 1.25)))
                        result_embed.add_field(
                            name="Bonus utilisateur bêta",
                            value=f"{round((20 * 1.25))} <:quantumpiece:1161010445205905418>",
                        )
                result_embed.color = Color.green()
            elif self.player_value < self.dealer_value:
                result_embed.title = "Vous perdez !"
                if self.bet:
                    result_embed.description = f"Malheureusement, je dois retirer {self.bet} <:quantumpiece:1161010445205905418>"
                    await Currency(ctx.user).remove_qp(self.bet)
            else:
                result_embed.title = "Égalité !"

        await ctx.edit_original_response(embed=result_embed)
