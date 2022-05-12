from asyncio import TimeoutError
from random import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from glob import glob
from nextcord.ext.commands import Cog
from assets.needed import *
from config import db

class slashfun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(name='8ball', description="Ask 8 ball anything and you will get your awnser")
    async def _8ball(self, interaction: Interaction, question=SlashOption(description="What question do you have?")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            embed = Embed(color=0x0000FF)
            embed.add_field(name="Question:", value=f'{question}', inline=False)
            embed.add_field(
                name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
            await interaction.followup.send(embed=embed)

    @jeanne_slash(description="Roll a dice")
    async def dice(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            rolled = randint(1, 6)
            embed = Embed(color=0x0000FF)
            embed.add_field(name="Dice Rolled",
                            value=f"You rolled a **{rolled}**!", inline=False)
            await interaction.followup.send(embed=embed)

    @jeanne_slash(description="Flip a coin")
    async def flip(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            await interaction.followup.send(embed=Embed(color=0x0000FF,
                                                            description=f"`{choice(['Heads', 'Tails'])}`"))

    @jeanne_slash(description="Say something and I will say it in reversed text")
    async def reverse(self, interaction: Interaction, text=SlashOption(description="Type something")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            await interaction.followup.send(text[::-1])

    @jeanne_slash(description="Guess my number")
    async def guess(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
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
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            file_path_type = ["./Media/Animemes/*.mp4", "./Media/Animemes/*.jpg"]
            animemes = glob(choice(file_path_type))
            random_animeme = choice(animemes)
            file = File(random_animeme)
            animeme = Embed(color=0x0000FF)
            animeme.set_footer(text="Powered by JeanneBot")
            await interaction.followup.send(file=file, embed=animeme)

    @jeanne_slash(description="Combine 2 words to get 2 combined words")
    async def combine(self, interaction: Interaction, first_word=SlashOption(description="Enter first word"), second_word=SlashOption(description="Enter second word")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            option_name1letters = first_word[:round(len(first_word) / 2)]
            option_name2letters = second_word[round(len(second_word) / 2):]

            option2_name1letters = first_word[round(len(first_word) / 2):]
            option2_name2letters = second_word[:round(len(second_word) / 2)]

            combine1 = "".join([option_name1letters, option_name2letters])
            combine2 = "".join([option2_name1letters, option2_name2letters])

            combine = Embed(
                description=f"**1st combine word**: {combine1}\n**2nd combined word**:{combine2}", color=0x0000FF)
            combine.set_author(name=f"{first_word} + {second_word}")
            await interaction.followup.send(embed=combine)

    @jeanne_slash(description="Give me 2 choices and I will pick for you")
    async def choose(self, interaction: Interaction, choice1=SlashOption(description="Enter first choice"), choice2=SlashOption(description="Enter second word")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if interaction.user.id == botbanned:
                pass
        except:
            pick = [choice1, choice2]
            choose = Embed(
                description=f"I chose **{choice(pick)}**", color=0x0000FF)
            await interaction.followup.send(embed=choose)


def setup(bot):
    bot.add_cog(slashfun(bot))
