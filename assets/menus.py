from typing import Optional
from discord import Interaction, SelectOption, ui




class ReportContentPlus(ui.Select):

    def __init__(self,
                 link1: Optional[str] = None,
                 link2: Optional[str] = None,
                 link3: Optional[str] = None,
                 link4: Optional[str] = None):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        options = [
            SelectOption(label="Report 1st Media"),
            SelectOption(label="Report 2nd Media"),
            SelectOption(label="Report 3rd Media"),
            SelectOption(label="Report 4th Media")
        ]
        super().__init__(placeholder="Saw something illegal? Report it here",
                         max_values=1,
                         min_values=1,
                         options=options)


    async def callback(self, ctx: Interaction):
        if self.values[0] == "Report 1st Media":
            await ctx.response.edit_message(
                content="This is the first option from the entire list!")
        elif self.values[0] == "Report 2nd Media":
            await ctx.response.send_message(
                "This is the second option from the list entire wooo!",
                ephemeral=False)
        elif self.values[0] == "Report 3rd Media":
            await ctx.response.send_message("Third One!", ephemeral=True)
        elif self.values[0] == "Report 4th Media":
            await ctx.response.send_message("Third One!", ephemeral=True)


class SelectView(ui.View):

    def __init__(self,
                 link1: Optional[str] = None,
                 link2: Optional[str] = None,
                 link3: Optional[str] = None,
                 link4: Optional[str] = None):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        super().__init__()
        self.add_item(ReportContentPlus(self.link1, self.link2, self.link3, self.link4))

class ReportContentReason(ui.Select):

    def __init__(self):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        options = [
            SelectOption(label="Report 1st Media"),
            SelectOption(label="Report 2nd Media"),
            SelectOption(label="Report 3rd Media"),
            SelectOption(label="Report 4th Media")
        ]
        super().__init__(placeholder="Saw something illegal? Report it here",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0] == "Report 1st Media":
            await ctx.response.edit_message(
                content="This is the first option from the entire list!")
        elif self.values[0] == "Report 2nd Media":
            await ctx.response.send_message(
                "This is the second option from the list entire wooo!",
                ephemeral=False)
        elif self.values[0] == "Report 3rd Media":
            await ctx.response.send_message("Third One!", ephemeral=True)
        elif self.values[0] == "Report 4th Media":
            await ctx.response.send_message("Third One!", ephemeral=True)