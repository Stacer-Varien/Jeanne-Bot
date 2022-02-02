from asyncio import TimeoutError
from random import choice, randint
from nextcord import Embed, File, slash_command as jeanne_slash, Interaction
from glob import glob
from nextcord.ext.commands import Cog
from assets.needed import eight_ball_answers, wrong_answer_or_timeout, correct_answer


class slashfun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(name='8ball', description="Ask 8 ball anything and you will get your awnser")
    async def _8ball(self, interaction: Interaction, question):
        embed = Embed(color=0x0000FF)
        embed.add_field(name="Question:", value=f'{question}', inline=False)
        embed.add_field(
            name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
        await interaction.response.send_message(embed=embed)

    @jeanne_slash(description="Roll a dice")
    async def dice(self, interaction: Interaction):
        rolled = randint(1, 6)
        embed = Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled",
                        value=f"You rolled a **{rolled}**!", inline=False)
        await interaction.response.send_message(embed=embed)

    @jeanne_slash(description="Flip a coin")
    async def flip(self, interaction: Interaction):
        await interaction.response.send_message(embed=Embed(color=0x0000FF,
                                                            description=f"`{choice(['Heads', 'Tails'])}`"))

    @jeanne_slash(description="Say something and I will say it in reversed text")
    async def reverse(self, interaction: Interaction, text):
        await interaction.response.send_message(text[::-1])

    @jeanne_slash(description="Guess my number")
    async def guess(self, interaction: Interaction):
        await interaction.response.defer()
        guessit = Embed(
            description="I'm thinking of a number between 1 to 10.\nYou have 5 seconds to guess it!", color=0x00FFFF)
        await interaction.followup.send(embed=guessit)

        def is_correct(m):
            return m.author == interaction.user and m.content.isdigit()

        answer = randint(1, 10)

        try:
            guess = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
        except TimeoutError:
            timeout = Embed(
                description=f"Sorry but you took too long. It was {answer}", color=0xFF0000)
            timeout.set_thumbnail(url=wrong_answer_or_timeout)
            return await interaction.followup.send(embed=timeout)

        if int(guess.content) == answer:
            correct = Embed(description="YES!", color=0x008000)
            correct.set_image(url=correct_answer)
            await interaction.followup.send(embed=correct)
        else:
            wrong = Embed(
                description=f"Wrong answer. It was {answer}", color=0xFF0000)
            wrong.set_thumbnail(url=wrong_answer_or_timeout)
            await interaction.followup.send(embed=wrong)

    @jeanne_slash(description="Get a random animeme")
    async def animeme(self, interaction: Interaction):
        file_path_type = ["./Media/Animemes/*.mp4", "./Media/Animemes/*.jpg"]
        animemes = glob(choice(file_path_type))
        random_animeme = choice(animemes)
        file = File(random_animeme)
        animeme = Embed(color=0x0000FF)
        animeme.set_footer(text="Powered by JeanneBot")
        await interaction.response.defer()
        await interaction.followup.send(file=file, embed=animeme)

    @jeanne_slash(description="Combine 2 words to get 2 combined words")
    async def combine(self, interaction: Interaction, first_word, second_word):
        option_name1letters = first_word[:round(len(first_word) / 2)]
        option_name2letters = second_word[round(len(second_word) / 2):]

        option2_name1letters = first_word[round(len(first_word) / 2):]
        option2_name2letters = second_word[:round(len(second_word) / 2)]

        combine1 = "".join([option_name1letters, option_name2letters])
        combine2 = "".join([option2_name1letters, option2_name2letters])

        combine = Embed(
            description=f"**1st combine word**: {combine1}\n**2nd combined word**:{combine2}", color=0x0000FF)
        combine.set_author(name=f"{first_word} + {second_word}")
        await interaction.response.send_message(embed=combine)

    @jeanne_slash(description="Give me 2 choices and I will pick for you")
    async def choose(self, interaction: Interaction, choice1, choice2):
        pick = [choice1, choice2]
        choose = Embed(
            description=f"I chose **{choice(pick)}**", color=0x0000FF)
        await interaction.response.send_message(embed=choose)


def setup(bot):
    bot.add_cog(slashfun(bot))
