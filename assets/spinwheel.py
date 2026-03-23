import asyncio
import random

from discord import Color, Embed, Interaction
from discord.ext import commands


class Wheel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_wheel(self, multipliers, pointer_index=None):
        display = [["", "", ""], ["", "🎡", ""], ["", "", ""]]

        positions = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

        for i, (r, c) in enumerate(positions):
            value = f"{multipliers[i]}x"
            if pointer_index == i:
                display[r][c] = f"👉{value}👈"
            else:
                display[r][c] = value

        wheel_text = ""
        for row in display:
            wheel_text += "   ".join(row) + "\n"

        return f"```\n{wheel_text}\n```"

    async def spin(self, ctx:Interaction, bet:int):
        negatives = [round(random.uniform(-2.0, -0.5), 1) for _ in range(5)]
        small_positives = [round(random.uniform(0.1, 0.5), 1) for _ in range(2)]
        big_positive = [round(random.uniform(1.5, 2.0), 1)]

        multipliers = negatives + small_positives + big_positive
        random.shuffle(multipliers)

        negative_indexes = [i for i, m in enumerate(multipliers) if m < 0]
        small_positive_indexes = [i for i, m in enumerate(multipliers) if 0 < m <= 0.5]
        big_positive_index = [i for i, m in enumerate(multipliers) if m > 1][0]

        roll = random.random()

        if roll <= 0.80:
            winner_index = random.choice(negative_indexes)
        elif roll <= 0.98:
            winner_index = random.choice(small_positive_indexes)
        else:
            winner_index = big_positive_index

        winner_multiplier = multipliers[winner_index]

        if ctx.locale.value==["en-US", "en-GB"]:
            await ctx.response.send_message("🎡 Spinning the wheel...")
            message = await ctx.original_response()

            total_spins = random.randint(20, 28)
            current_index = 0

            for i in range(total_spins):
                wheel_visual = self.build_wheel(multipliers, current_index)

                embed = Embed(
                    title="🎡 Spinning...",
                    description=wheel_visual,
                    color=Color.gold()
                )

                await message.edit(embed=embed)
                current_index = (current_index + 1) % 8
                await asyncio.sleep(0.07 + (i / total_spins) * 0.3)

            wheel_visual = self.build_wheel(multipliers, winner_index)

            winnings = round(bet * winner_multiplier, 2)

            if winnings > 0:
                result_text = f"🎉 You won {winnings}!"
                color = Color.green()
            elif winnings < 0:
                result_text = f"💀 You lost {abs(winnings)}..."
                color = Color.red()
            else:
                result_text = "😐 You broke even!"
                color = Color.blurple()

            final_embed = Embed(
                title="🎯 Wheel Result",
                description=wheel_visual,
                color=color
            )
            final_embed.add_field(name="💰 Bet", value=str(bet))
            final_embed.add_field(name="📈 Multiplier", value=f"{winner_multiplier}x")
            final_embed.add_field(name="🏆 Result", value=result_text)
            await message.edit(embed=final_embed)

        elif ctx.locale.value=="fr":
            await ctx.response.send_message("🎡 La roue tourne...")
            message = await ctx.original_response()

            total_spins = random.randint(20, 28)
            current_index = 0

            for i in range(total_spins):
                wheel_visual = self.build_wheel(multipliers, current_index)

                embed = Embed(
                    title="🎡 Tour de la roue...",
                    description=wheel_visual,
                    color=Color.gold()
                )

                await message.edit(embed=embed)
                current_index = (current_index + 1) % 8
                await asyncio.sleep(0.07 + (i / total_spins) * 0.3)

            wheel_visual = self.build_wheel(multipliers, winner_index)

            winnings = round(bet * winner_multiplier, 2)

            if winnings > 0:
                result_text = f"🎉 Vous avez gagné {winnings}!"
                color = Color.green()
            elif winnings < 0:
                result_text = f"💀 Vous avez perdu {abs(winnings)}..."
                color = Color.red()
            else:
                result_text = "😐 Vous êtes à égalité!"
                color = Color.blurple()

            final_embed = Embed(
                title="🎯 Résultat de la roue",
                description=wheel_visual,
                color=color
            )
            final_embed.add_field(name="💰 Mise", value=str(bet))
            final_embed.add_field(name="📈 Multiplicateur", value=f"{winner_multiplier}x")
            final_embed.add_field(name="🏆 Résultat", value=result_text)
            await message.edit(embed=final_embed)

        elif ctx.locale.value=="de":
            await ctx.response.send_message("🎡 Das Rad dreht sich...")
            message = await ctx.original_response()

            total_spins = random.randint(20, 28)
            current_index = 0

            for i in range(total_spins):
                wheel_visual = self.build_wheel(multipliers, current_index)

                embed = Embed(
                    title="🎡 Rad dreht sich...",
                    description=wheel_visual,
                    color=Color.gold()
                )

                await message.edit(embed=embed)
                current_index = (current_index + 1) % 8
                await asyncio.sleep(0.07 + (i / total_spins) * 0.3)

            wheel_visual = self.build_wheel(multipliers, winner_index)

            winnings = round(bet * winner_multiplier, 2)

            if winnings > 0:
                result_text = f"🎉 Sie haben {winnings} gewonnen!"
                color = Color.green()
            elif winnings < 0:
                result_text = f"💀 Sie haben {abs(winnings)} verloren..."
                color = Color.red()
            else:
                result_text = "😐 Sie haben das Spiel unentschieden beendet!"
                color = Color.blurple()

            final_embed = Embed(
                title="🎯 Ergebnis des Radspiel",
                description=wheel_visual,
                color=color
            )
            final_embed.add_field(name="💰 Einsatz", value=str(bet))
            final_embed.add_field(name="📈 Multiplikator", value=f"{winner_multiplier}x")
            final_embed.add_field(name="🏆 Ergebnis", value=result_text)

            await message.edit(embed=final_embed)
