from nextcord import *
from nextcord.ui import *

level = Embed(title="Level Module",
              description="**Levelling**\nYou gain experience by sending a message. Right now, the system is incomplete but there will be changes. For now, you gain 5-10 XP/Message but in the future, it will be 5-10XP/1 Minute/Message meaning if you send a message now, you will gain 5-10XP but you have to wait for 1 minute to gain another 5-10 XP on the next message.\n\n• **NOTE:** In the nearby future, there will be a member count requirement for members to gain XP ([click here to read more about it](https://github.com/Varien-1936/ZaneRE544/blob/main/2022%20plans.md)).", color=0x7DF9FF)
level.add_field(name='Available commands',
                 value="• Level\n• Rank")
level.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class infohelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Level"), SelectOption(
                label="Rank")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="Level":
            await ctx.response.defer(ephemeral=True)
            level = Embed(color=0x7DF9FF)
            level.add_field(
                name="See your level or someone's level", value="• **Example:** `/level (IF YOURSELF)` \ `/level MEMBER` (IF MEMBER)\n• **Expected result**: `MEMBER'S LEVEL STATS BOTH GLOBAL AND SERVER`\n• **Expected failure**: `FAILED TO GET LEVEL STATS MESSAGE. THIS IS BECAUSE THE MEMBER HASN'T SAID A MESSAGE YET`")
            await ctx.edit_original_message(embed=level)
        if self.values[0] == "Rank":
            await ctx.response.defer(ephemeral=True)
            rank = Embed(color=0x7DF9FF)
            rank.add_field(
                name="Check who is the top 15 users (if applicable) of the server. You might be lucky if your name shows\n• **NOTE:** You will be given 2 options whether to see the server or global rank.", value="• **Example:** `/rank SERVER` (IF YOU WANT THE RANK OF THE SERVER) / `/rank GLOBAL` (IF FOR EVERYONE IN THE XP DATABASE)\n• **Expected result**: `RANKED MEMBERS IN THE SERVER OR GLOBALY`")
            await ctx.edit_original_message(embed=rank)



class infoview(View):
    def __init__(self):
        super().__init__()
        self.add_item(infohelp())

        

