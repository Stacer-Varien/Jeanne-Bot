from nextcord import *

class help_menu(ui.Select):
    def __init__(self):
        options=[SelectOption(label="Fun"), SelectOption(label="Currency"),SelectOption(label="Image"), SelectOption(label="Info"),SelectOption(label="Hentai"), SelectOption(label="Inventory"),SelectOption(label="Levelling"), SelectOption(label="Management"),SelectOption(label="Moderation"), SelectOption(label="Reaction"),SelectOption(label="Utility"), SelectOption(label="Creator Only"),]

        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, ctx: Interaction):
        embed=Embed(color=ctx.user.color)
        if self.values[0]== "Fun":
            embed.title="Commands available for Fun"
            embed.add_field(name="8 Ball", value="Ask 8 ball anything and you will get your answer\nExample: `/8ball QUESTION`", inline=False)
            embed.add_field(name="Combine", value="Type two words to get one combined word\nExample: `/combine WORD_1 WORD_2`", inline=False)
            embed.add_field(name="Choose", value="Add some choices and I will choose for you\nExample: `/choose CHOICE_1 CHOICE_2`", inline=False)
            embed.add_field(name="8 Ball", value="Ask 8 ball anything and you will get your answer\nExample: `/8ball QUESTION`", inline=False)

import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)
