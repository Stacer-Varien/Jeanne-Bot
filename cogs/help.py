from json import dumps, loads
from typing import List
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    ui,
    app_commands as Jeanne,
)
from discord.ext.commands import GroupCog, Bot
from functions import Botban
from collections import OrderedDict
from assets.help.commands import Commands, Modules
from assets.help.modules import modules


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


class HelpGroup(GroupCog, name="help"):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def command_choices(
        self,
        ctx: Interaction,
        current: str,
    ) -> List[Jeanne.Choice[str]]:
        commands = list(Commands)
        return [
            Jeanne.Choice(name=command.value, value=command.value)
            for command in commands
            if current.lower() in command.value.lower()
        ]

    @Jeanne.command(description="Get help of a certain command")
    @Jeanne.autocomplete(command=command_choices)
    async def command(self, ctx: Interaction, command: Jeanne.Range[str, 4]):
        if Botban(ctx.user).check_botbanned_user:
            return

        await ctx.response.defer()
        cmd = [
            cmd
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Jeanne.Group)
            if cmd.qualified_name == command
        ][0]

        bot_perms=cmd.checks[0] if cmd.checks[0] else None
        member_perms=cmd.checks[0] if cmd.checks[1] else None

        embed = Embed(title=f"{command.title()} Help", color=Color.random())
        embed.description = cmd.description
        parms = []
        descs=[]
        if len(cmd.parameters) > 0:
            for i in cmd.parameters:
                parm = f"[{i.name}]" if i.required is True else f"<{i.name}>"
                desc = f"`{parm}` - {i.description}"
                parms.append(parm)
                descs.append(desc)
            embed.add_field(name="Parameters", value="\n".join(descs))
        
        if bot_perms:
            perms=[]
            for i in bot_perms:
                perm_dict:dict=i.__closure__[0].cell_contents
                perm:list=perm_dict.keys()
                perms.append(perm)
        cmd_usage = "/" + cmd.qualified_name + " " + " ".join(parms)
        embed.add_field(name="Command Usage", value=f"`{cmd_usage}`", inline=False)
        embed.set_footer(
            text="Legend:\n[] - Required\n<> - Optional\n\nIt is best to go to the webiste for detailed explanations and usages"
        )

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Get help of a certain module")
    async def module(self, ctx: Interaction, module: Modules):
        if Botban(ctx.user).check_botbanned_user:
            return
        await ctx.response.defer()
        module_data = dumps(modules[module.value])

        if module_data:
            parms = OrderedDict([("%module%", str(module.name.capitalize()))])

            json_data: dict = loads(replace_all(module_data, parms))

            embed_data = json_data.get("embeds")
            embed = Embed.from_dict(embed_data[0])

        await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Get help from the wiki or join the support server for further help"
    )
    async def support(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return

        view = help_button()
        help = Embed(
            description="Click on one of the buttons to open the documentation or get help on the support server",
            color=Color.random(),
        )
        await ctx.response.send_message(embed=help, view=view)


async def setup(bot: Bot):
    await bot.add_cog(HelpGroup(bot))
