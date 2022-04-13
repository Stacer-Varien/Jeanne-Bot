from nextcord import *
from nextcord.ui import *

image = Embed(title="Image Module", description="Kitsune is the only command that uses the Nekoslife API. The rest are fetched from local storage", color=0x7DF9FF)
image.add_field(name='Available commands',
                 value="• Kitsune\n• Wallpaper\n• Jeanne\n• Saber\n• Neko")
image.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")


class link_button(View):
    def __init__(self):
        super().__init__()

        wiki_url = 'https://github.com/ZaneRE544/Jeanne-Bot/wiki/JeanneBot-Wiki#welcome-to-the-jeanne-bot-wiki'
        haze_url = 'https://discord.gg/VVxGUmqQhF'

        self.add_item(Button(style=ButtonStyle.url,
                      label="Jeanne Wiki", url=wiki_url))
        self.add_item(Button(style=ButtonStyle.url,
                      label="Support Server", url=haze_url))


        

