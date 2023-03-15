from discord import Color, Embed, Interaction, SelectOption, ui


class help_menu(ui.Select):

    def __init__(self):
        options = [
            SelectOption(label="Fun"),
            SelectOption(label="Currency"),
            SelectOption(label="Image"),
            SelectOption(label="Info"),
            SelectOption(label="Hentai"),
            SelectOption(label="Inventory"),
            SelectOption(label="Levelling"),
            SelectOption(label="Management"),
            SelectOption(label="Moderation"),
            SelectOption(label="Reaction"),
            SelectOption(label="Utility"),
            SelectOption(label="Creator Only"),
        ]

        super().__init__(placeholder="Select an option",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, ctx: Interaction):
        embed = Embed(color=Color.random())
        embed.set_footer(
            text=
            "Legend:\n [] = Required | {} = Optional | () = Extra Information")
        if self.values[0] == "Fun":
            embed.title = "Fun Help"
            embed.description = "The reverse command has some words filtered but there is one that will guarantee a botban."
            embed.add_field(
                name="8 Ball",
                value=
                "Ask 8 ball anything and you will get your answer\nExample: `/8ball [QUESTION]`",
                inline=False)
            embed.add_field(
                name="Combine",
                value=
                "Type two words to get one combined word\nExample: `/combine [WORD_1] [WORD_2]`",
                inline=False)
            embed.add_field(
                name="Choose",
                value=
                "Add some choices and I will choose for you. Split them with ','\nExample: `/choose [CHOICES]`",
                inline=False)
            embed.add_field(
                name="Reverse",
                value=
                "Say something and I will say it in reversed text\nExample: `/reverse [TEXT]`",
                inline=False)
            embed.add_field(name="Animeme",
                            value="Get a random animeme\nExample: `/animeme`",
                            inline=False)
            embed.add_field(
                name="Gay Rate",
                value=
                "Check how gay you or the member is\nExample: `/gayrate {member}`",
                inline=False)
            embed.add_field(
                name="Simp Rate",
                value=
                "Check how much of a simp you or the member is\nExample: `/simprate {member}`",
                inline=False)

            await ctx.edit_original_response(embed=embed)

        elif self.values[0] == "Currency":
            embed.title = "Currency Help"
            embed.description = "When using this system, please respect the [rules](https://jeannebot.nicepage.io/ToS-and-Privacy-Policy.html).\nThe free chances can earn you 20QP and they have a 1 hour cooldown while the betting commands have a cooldown of 20 seconds. If using a betting command, please bet higher than 5QP but lower than your QP."
            embed.add_field(
                name="Daily",
                value=
                "Claim your daily. On weekends, you can claim twice the ammount\nExample: `/daily`",
                inline=False)
            embed.add_field(
                name="Guess",
                value=
                "Guess my number and you can win QP. \nExample: `/guess free` then after she asks, `NUMBER`\n`/guess bet [AMOUNT]` then after she asks, `[NUMBER]`",
                inline=False)
            embed.add_field(
                name="Choose",
                value=
                "Add some choices and I will choose for you. Split them with ','\nExample: `/choose [CHOICES]`",
                inline=False)
            embed.add_field(
                name="Reverse",
                value=
                "Say something and I will say it in reversed text\nExample: `/reverse [TEXT]`",
                inline=False)
            embed.add_field(name="Animeme",
                            value="Get a random animeme\nExample: `/animeme`",
                            inline=False)
            embed.add_field(
                name="Gay Rate",
                value=
                "Check how gay you or the member is\nExample: `/gayrate {member}`",
                inline=False)
            embed.add_field(
                name="Simp Rate",
                value=
                "Check how much of a simp you or the member is\nExample: `/simprate {member}`",
                inline=False)

            await ctx.edit_original_response(embed=embed)
