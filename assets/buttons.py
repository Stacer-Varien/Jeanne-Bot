from discord import  ui, ButtonStyle, Interaction, User
from assets.modals import ReportContentModal


class Confirmation(ui.View):

    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, ctx: Interaction, button: ui.Button):
        self.value = True
        button.disabled = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = False
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Heads_or_Tails(ui.View):

    def __init__(self, author: User):
        self.author = author
        super().__init__(timeout=30)
        self.value = None

    @ui.button(label="Heads", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = "Heads"
        self.stop()

    @ui.button(label="Tails", style=ButtonStyle.green)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = 'Tails'
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Cancellation(ui.View):

    def __init__(self, author: User):
        super().__init__()
        self.author = author
        self.value = None

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = 'cancel'
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class ReportContent(ui.View):

    def __init__(self, link: str):
        super().__init__()
        self.link = link

    @ui.button(label="Report Content", style=ButtonStyle.grey)
    async def report1(self, ctx: Interaction, button: ui.Button):
        self.value = 'report'
        await ctx.response.send_modal(ReportContentModal(self.link))
        



