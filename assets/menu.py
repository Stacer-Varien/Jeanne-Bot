from random import randint
from nextcord import ui, SelectOption, Interaction, Embed, Color

from assets.db_functions import add_qp


class DiceOptions(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="1"),
            SelectOption(label="2"),
            SelectOption(label="3"),
            SelectOption(label="4"),
            SelectOption(label="5"),
            SelectOption(label="6"),
        ]
        super().__init__(placeholder="Select an option",
                         max_values=1, min_values=1, options=options)

    async def callback(self, ctx: Interaction):
        rolled = randint(1, 6)
        qp = str(self.bot.get_emoji(980772736861343774))
        if int(self.values[0]) == rolled:
            add_qp(ctx.user.id, 20)
            embed = Embed(color=0x0000FF)
            embed.add_field(name=f"YAY! You got it!\n20 {qp} has been added",
                            value=f"Rolled: **{rolled}**\nResult: **{self.values[0]}**!", inline=False)
            await ctx.edit_original_message(embed=embed)
        else:
            embed = Embed(
                description=f"Oh no. It rolled a **{rolled}**", color=Color.red())
            await ctx.edit_original_message(embed=embed)



class DiceSelect(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(DiceSelect())
