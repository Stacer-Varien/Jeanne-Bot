from random import choice, randint
from typing import Optional
from discord import Color, Embed, Member
from discord.ext.commands import Bot, Cog, Context
from discord.ext import commands as Jeanne
from assets.images import get_animeme_pic
from functions import BetaTest, Botban, Command
import argparse


class fun(Cog, name="Fun"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        aliases=["8b", "eightball"],
        description="Ask 8 ball anything and you will get your awnser",
        name="8ball",
    )
    async def _8ball(self, ctx: Context, *, question: str):
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self._8ball.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return

            await ctx.defer()
            eight_ball_answers = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes – definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Why ask me? Just do it!",
                "Why ask me? Just don't do it!",
                "Yeah... no",
                "Yeah... whatever",
                "Yeah... I don't know",
                "Yes? No? I don't know!",
            ]

            embed = Embed(color=Color.random())
            embed.add_field(name="Question:", value=f"{question}", inline=False)
            embed.add_field(
                name="Answer:", value=f"{choice(eight_ball_answers)}", inline=False
            )
            await ctx.send(embed=embed)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Jeanne.command(
        aliases=["backwards"],
        description="Say something and I will say it in reversed text",
    )
    async def reverse(self, ctx: Context, *, text: str):
        if Botban(ctx.author).check_botbanned_user:
            return

        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.reverse.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            await ctx.defer()
            filtered_words = ["riffak", "reggin", "aggin"]
            if any(word in text for word in filtered_words):
                await Botban(ctx.author).add_botbanned_user(
                    "Using the reversed version of a common racial slur"
                )
                return

            msg = Embed(description=text[::-1], color=Color.random()).set_footer(
                text="Author: {} | {}".format(ctx.author, ctx.author.id)
            )
            await ctx.send(embed=msg)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Jeanne.command(description="Get a random animeme")
    async def animeme(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.reverse.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            await ctx.defer()
            embed, file = get_animeme_pic()
            await ctx.send(embed=embed, file=file)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
                "--first", "-f", type=str, help="First Word", required=True, nargs="+"
            )
    parser.add_argument(
                "--second", "-s", type=str, help="Second Word", required=True, nargs="+"
            )

    @Jeanne.command(
        aliases=["join"],
        description="Combine 2 words to get 2 combined words",
    )
    async def combine(self, ctx: Context, *words:str, parser=parser): # type: ignore
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.combine.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            await ctx.defer()
            try:
                namespace = parser.parse_known_args(words)
            except:
                await ctx.send(embed=Embed(description=f"You are missing some arguments for this command", color=Color.red()))
                return
            option_name1letters = namespace.first[: round(len(' '.join(namespace.first)) / 2)]
            option_name2letters = namespace.second[round(len(' '.join(namespace.second)) / 2) :]

            option2_name1letters = namespace.first[
                round(len(" ".join(namespace.first)) / 2) :
            ]
            option2_name2letters = namespace.second[: round(len(' '.join(namespace.second)) / 2)]

            combine1 = "".join([option_name1letters, option_name2letters])
            combine2 = "".join([option2_name1letters, option2_name2letters])

            combine = Embed(
                description=f"**1st combine word**: {combine1}\n**2nd combined word**:{combine2}",
                color=Color.random(),
            )
            combine.set_author(name=f"""{namespace.first} + {namespace.second}""")
            await ctx.send(embed=combine)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Jeanne.command(
        aliases=["pick", "choice"],
        description="Give me a lot of choices and I will pick one for you. Separate them with ','",
    )
    async def choose(self, ctx: Context, *, choices: str):
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.choose.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            await ctx.defer()

            options = choices.split(sep=",")
            choose = Embed(
                description=f"I chose **{choice(options)}**", color=Color.random()
            )
            await ctx.send(embed=choose)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Jeanne.command(
        aliases=["simp"], description="Check how much of a simp you or a member are"
    )
    async def simprate(self, ctx: Context, member: Optional[Member] = None):
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.simprate.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            await ctx.defer()
            perc = randint(0, 100)

            member = member if member else ctx.author

            simp = Embed(
                description="{}'s simp rate is {}%".format(member, perc),
                color=Color.random(),
            )

            if perc >= 75:
                simp.set_image(url="https://i.imgur.com/W4u4Igk.jpg")

            elif perc >= 50:
                simp.set_image(url="https://i.imgur.com/Rs1IP2I.jpg")

            await ctx.send(embed=simp)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )

    @Jeanne.command(description="Check how gay you are")
    async def gayrate(self, ctx: Context, member: Optional[Member] = None):
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.gayrate.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            await ctx.defer()
            perc = randint(0, 100)

            member = member if member else ctx.author

            gay = Embed(
                description="{}'s gay rate is {}%".format(member, perc),
                color=Color.random(),
            )

            if perc >= 75:
                gay.set_image(url="https://i.imgur.com/itOD0Da.png?1")

            elif perc >= 50:
                gay.set_image(url="https://i.imgur.com/tYAbWCl.jpg")

            await ctx.send(embed=gay)
            return
        await ctx.send(
            embed=Embed(
                description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                color=Color.red(),
            ),
            ephemeral=True,
        )


async def setup(bot: Bot):
    await bot.add_cog(fun(bot))
