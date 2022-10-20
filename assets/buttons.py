from nextcord import ui, ButtonStyle, Interaction

class Confirmation(ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.value = None

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = False
        self.stop()


class Heads_or_Tails(ui.View):
    def __init__(self):
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

class ViewRoles(ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @ui.button(label="Roles", style=ButtonStyle.green)
    async def roles(self, button: ui.Button, ctx: Interaction):
        self.value = "roles"
        self.stop()
    

    