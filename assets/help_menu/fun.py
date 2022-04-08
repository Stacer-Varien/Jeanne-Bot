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
            await ctx.response.defer(ephemeral=True)
            _8ball = Embed(color=0x7DF9FF)
            _8ball.add_field(
                name="Ask 8 ball anything and you will get your answer", value="• **Example:** `/8ball QUESTION`\n• **Expected result**: `ANSWER FROM JEANNE`")
            await ctx.followup.send(embed=_8ball, ephemeral=True)
        if self.values[0] == "Dice":
            await ctx.response.defer(ephemeral=True)
            dice = Embed(color=0x7DF9FF)
            dice.add_field(
                name="Roll a dice", value="• **Example:** `/dice`\n• **Expected result**: `RANDOM NUMBER BETWEEN 1 AND 6`")
            await ctx.followup.send(embed=dice, ephemeral=True)
        if self.values[0] == "Combine":
            await ctx.response.defer(ephemeral=True)
            combine = Embed(color=0x7DF9FF)
            combine.add_field(
                name="Type two words to get one combined word", value="• **Example:** `/combine FIRST_WORD SECOND_WORD`\n• **Expected result**: `2 WORDS SHOWING A DIFFERENT COMBINED WORD`")
            await ctx.followup.send(embed=combine, ephemeral=True)
        if self.values[0] == "Flip":
            await ctx.response.defer(ephemeral=True)
            flip = Embed(color=0x7DF9FF)
            flip.add_field(
                name="Flip a coin and get your result", value="• **Example:** `/flip`\n• **Expected result**: `HEADS/TAILS`")
            await ctx.followup.send(embed=flip, ephemeral=True)
        if self.values[0] == "Choose":
            await ctx.response.defer(ephemeral=True)
            choose = Embed(color=0x7DF9FF)
            choose.add_field(
                name="Add 2 choices and I will pick for you\n•", value="• **Example:** `/choose CHOICE 1 CHOICE 2`\n• **Expected result**: `ONE OF YOUR CHOICES WERE PICKED`")
            await ctx.followup.send(embed=choose, ephemeral=True)
        if self.values[0] == "Reverse":
            await ctx.response.defer(ephemeral=True)
            reverse = Embed(color=0x7DF9FF)
            reverse.add_field(
                name="Say something and I will say it in reversed text", value="• **Example:** `/reverse TEXT`\n• **Expected result**: `REVERSED TEXT`")
            await ctx.followup.send(embed=reverse, ephemeral=True)
        if self.values[0] == "Guess":
            await ctx.response.defer(ephemeral=True)
            guess = Embed(color=0x7DF9FF)
            guess.add_field(
                name="Guess my number and I will reward you with a hug!\n• **NOTE:** You have to pick a number between 1 to 10. After executing the command, you have to guess the number after she starts asking. You have 5 seconds to guess the correct one.", value="• **Example:** `/guess`\n• **Expected result**: `JEANNE ASKS FOR THE NUMBER. PUT IN THE NUMBER AND IF GUESSED CORRECTLY, SHE WILL SHOW A HUG GIF`\n• **Expected Failure:** `IF YOU TAKE MORE THAN 10 SECONDS OR GUESSED THE WRONG NUMBER")
            await ctx.followup.send(embed=guess, ephemeral=True)
        if self.values[0] == "Animeme":
            await ctx.response.defer(ephemeral=True)
            guess = Embed(color=0x7DF9FF)
            guess.add_field(
                name="Get a random animeme", value="• ** Example: ** `/animeme`")
            await ctx.followup.send(embed=guess, ephemeral=True)

class DropdownView(View):
    def __init__(self):
        super().__init__()
        self.add_item(fun_help())

        

