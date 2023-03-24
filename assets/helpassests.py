from discord import Embed, utils, ui, SelectOption, Interaction
from discord.ext.commands import Bot
['Currency', 'Fun', 'Hentai', 'Image', 'Info', 'Inventory', 'Levelling', 'Manage', 'Moderation', 'Reactions', 'Utilities']

class HelpMenu(ui.Select):
    def __init__(self, bot:Bot,modules:str) -> None:
        self.modules=modules
        self.bot=bot

        if self.modules=="Currency":
            options = [
                SelectOption(label="Guess"),
                SelectOption(label="Dice"),
                SelectOption(label="Flip"),
                SelectOption(label="Daily"),SelectOption(label="Balance"),SelectOption(label="Vote")
            ]
        super().__init__(options=options)

    async def callback(self, ctx: Interaction):
        cmds = self.bot.tree.walk_commands()
        cmd = utils.get(cmds, name=self.values[0].lower())

        try:
            embed=Embed()
            embed.title=f"{self.values[0]} Help"
            for i in cmd.commands:
                subcmd = utils.get(cmd.commands, name=i.name)
                parms=[a for a in subcmd.parameters]
                for b in parms:
                    if b.required==True:
                        req=f"[{b.name}]"
                    else:
                        req=f"({b.name})"
                parms2=" ".join(req)
                describe=f"{i.description}\n\n __Example__\n`/{cmd.name} {i.name} {parms2}"
                embed.add_field(name=i.name, value=describe, inline=True)
        except:
            ...
        
        await ctx.edit_original_response(embed=embed)
