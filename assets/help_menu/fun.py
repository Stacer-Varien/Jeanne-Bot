from nextcord import *
from nextcord.ui import *

fun = Embed(title="Fun Module", color=0x7DF9FF)
fun.add_field(name='Available commands',
              value="• 8 Ball\n• Dice\n• Combine\n• Flip\n• Choose\n• Reverse\n• Guess\n• Animeme")
fun.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class fun_help(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="8 Ball"), SelectOption(
                label="Dice"), SelectOption(label="Combine"), SelectOption(label="Flip"), SelectOption(label="Choose"), SelectOption(label="Reverse"), SelectOption(label="Guess"), SelectOption(label="Animeme")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="8 Ball":
            await ctx.response.defer()
            _8ball = Embed(color=0x7DF9FF)
            _8ball.add_field(
                name="Ask 8 ball anything and you will get your answer", value="• **Example:** `/8ball QUESTION`")
            await ctx.edit_original_message(embed=_8ball)
        if self.values[0] == "Dice":
            await ctx.response.defer()
            dice = Embed(color=0x7DF9FF)
            dice.add_field(
                name="Roll a dice", value="• **Example:** `/dice`")
            await ctx.edit_original_message(embed=dice)
        if self.values[0] == "Combine":
            await ctx.response.defer()
            combine = Embed(color=0x7DF9FF)
            combine.add_field(
                name="Type two words to get one combined word", value="• **Example:** `/combine FIRST_WORD SECOND_WORD`")
            await ctx.edit_original_message(embed=combine)
        if self.values[0] == "Flip":
            await ctx.response.defer()
            flip = Embed(color=0x7DF9FF)
            flip.add_field(
                name="Flip a coin and get your result", value="• **Example:** `/flip`")
            await ctx.edit_original_message(embed=flip)
        if self.values[0] == "Choose":
            await ctx.response.defer()
            choose = Embed(color=0x7DF9FF)
            choose.add_field(
                name="Add 2 choices and I will pick for you\n•", value="• **Example:** `/choose CHOICE 1 CHOICE 2`")
            await ctx.edit_original_message(embed=choose)
        if self.values[0] == "Reverse":
            await ctx.response.defer()
            reverse = Embed(color=0x7DF9FF)
            reverse.add_field(
                name="Say something and I will say it in reversed text", value="• **Example:** `/reverse TEXT`")
            await ctx.edit_original_message(embed=reverse)
        if self.values[0] == "Guess":
            await ctx.response.defer()
            guess = Embed(color=0x7DF9FF)
            guess.add_field(
                name="Guess my number and I will reward you with a hug!\n• **NOTE:** You have to pick a number between 1 to 10. After executing the command, you have to guess the number after she starts asking. You have 5 seconds to guess the correct one.", value="• **Example:** `/guess`\n• **Expected Failure:** Jeanne will send a 'crying' gif if you take more than 10 seconds to guess or guessed the wrong answer.")
            await ctx.edit_original_message(embed=guess)
        if self.values[0] == "Animeme":
            await ctx.response.defer()
            guess = Embed(color=0x7DF9FF)
            guess.add_field(
                name="Get a random animeme", value="• ** Example: ** `/animeme`")
            await ctx.edit_original_message(embed=guess)

class funview(View):
    def __init__(self):
        super().__init__()
        self.add_item(fun_help())

        

