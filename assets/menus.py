from typing import Optional
from discord import Interaction, SelectOption, ui
from assets.modals import ReportContentModal

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
            SelectOption(label="Report 1st Media", value=self.link1),
            SelectOption(label="Report 2nd Media", value=self.link2),
            SelectOption(label="Report 3rd Media", value=self.link3),
            SelectOption(label="Report 4th Media", value=self.link4)
        ]
        super().__init__(placeholder="Saw something illegal? Report it here",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, ctx: Interaction):
        await ctx.response.send_modal(ReportContentModal(self.values[0]))

class ReportSelect(ui.View):

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