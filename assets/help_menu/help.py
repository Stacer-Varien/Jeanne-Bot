from assets.help_menu.fun import *
from assets.help_menu.hentai import *
from nextcord import *
from nextcord.ui import *


class helpmenu(ui.Select):
    def __init__(self):

        options = [
            SelectOption(label="Fun"), SelectOption(
                label="Hentai"), SelectOption(label="Image"), SelectOption(
                label="Info"), SelectOption(label="Level"), SelectOption(
                label="Manage"), SelectOption(label="Misc"), SelectOption(
                label="Moderation"), SelectOption(label="Owner (BOT OWNER ONLY)"), SelectOption(
                label="Reactions"), SelectOption(label="Utilities"), SelectOption(
                label="Welcomer")
        ]

        super().__init__(placeholder='Module', options=options)
