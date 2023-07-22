from json import loads
from typing import Optional
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    ui,
    app_commands as Jeanne,
)
from discord.ext.commands import Cog, Bot
from functions import Botban
from collections import OrderedDict
from assets.help.helpcmds import HelpCommands, HelpModules

def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class help_button(ui.View):
    def __init__(self):
        super().__init__()

        wiki_url = "https://jeannebot.gitbook.io/jeannebot/help"
        orleans_url = "https://discord.gg/jh7jkuk2pp"
        tos_and_policy_url = "https://jeannebot.gitbook.io/jeannebot/tos-and-privacy"

        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Jeanne Webiste", url=wiki_url)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Support Server", url=orleans_url)
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="ToS and Privacy Policy",
                url=tos_and_policy_url,
            )
        )


class help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        description="Get help from the wiki or join the support server for further help"
    )
    async def help(self, ctx: Interaction, module:Optional[HelpModules]=None, command:Optional[HelpCommands]=None):
        if Botban(ctx.user).check_botbanned_user():
            return
        
        if module:
            parms={"%module%" : str(module.value), "%color%": str(Color.random().value)}
            json_data: dict = loads(
                    replace_all('', parms)
                )
            embed_data = json_data.get("embeds")
            embed=Embed.from_dict(embed_data[0])

        view = help_button()
        help = Embed(
            description="Click on one of the buttons to open the documentation or get help on the support server",
            color=Color.random(),
        )
        await ctx.response.send_message(embed=help, view=view)


async def setup(bot: Bot):
    await bot.add_cog(help(bot))
