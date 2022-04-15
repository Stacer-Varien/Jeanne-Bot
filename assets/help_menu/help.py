from assets.help_menu.fun import *
from assets.help_menu.hentai import *
from nextcord import *
from nextcord.ui import *

from assets.help_menu.image import imageview
from assets.help_menu.info import infoview


class helpmenu(ui.Select):
    def __init__(self):

        options = [
            SelectOption(label="Fun"), SelectOption(
                label="Hentai"), SelectOption(label="Image"), SelectOption(
                label="Info"), SelectOption(label="Level"), SelectOption(
                label="Manage"), SelectOption(label="Misc"), SelectOption(
                label="Moderation"), SelectOption(label="Owner (BOT OWNER ONLY)"), SelectOption(
                label="Reactions"), SelectOption(label="Utilities"), SelectOption(
                label="Welcomer"), SelectOption(label="More Help")
        ]

        super().__init__(placeholder='Module', options=options)


    async def callback(self, ctx: Interaction):
        if self.values[0] == "Fun":
            await ctx.edit_original_message(embed=fun, view=funview())
        if self.values[0] == "Hentai":
            await ctx.edit_original_message(embed=fun, view=hentaiview())
        if self.values[0] == "Image":
            await ctx.edit_original_message(embed=fun, view=imageview())
        if self.values[0] == "Info":
            await ctx.edit_original_message(embed=fun, view=infoview())
        if self.values[0] == "Level":
            await ctx.edit_original_message(embed=fun, view=funview())
        if self.values[0] == "Hentai":
            await ctx.edit_original_message(embed=fun, view=hentaiview())


class helpview(View):
    def __init__(self):
        super().__init__()
        self.add_item(helpmenu())
