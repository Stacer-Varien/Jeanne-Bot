from json import dumps, loads
from discord import ButtonStyle, Color, Embed, SelectOption, ui
from discord.ext.commands import Bot, Cog, group, Context, Range
import discord.ext.commands as Jeanne
from reactionmenu import Page, ViewButton, ViewMenu, ViewSelect
from functions import (
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from collections import OrderedDict
from assets.help.slash.modules import modules, SlashModules


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


class HelpGroupPrefix(Cog, name="Help"):
    def __init__(self, bot: Bot):
        self.bot = bot

    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @group(
        aliases=["h"],
        invoke_without_command=True,
        description="Main Help command for the help subcommands and shows all the commands and modules available",
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def help(self, ctx: Context):
        async with ctx.typing():

            excluded_cogs = [
                "listenersCog",
                "tasksCog",
                "WelcomerCog",
                "cmdlogger",
                "ErrorsPrefix",
                "CommandLogSlash",
                "Owner",
                "Jishaku",
                "guess",
                "dice",
                "flip",
                "CurrencySlash",
                "ErrorsSlash",
                "FunSlash",
                "help",
                "nsfw",
                "ImagesSlash",
                "InfoSlash",
                "shop",
                "background",
                "rank",
                "levelling",
                "manage",
                "create",
                "edit",
                "delete",
                "set",
                "rename",
                "command",
                "level",
                "moderation",
                "ReactionsSlash",
                "embed",
                "slashutilities",
                "reminder",
            ]

            menu = ViewMenu(
                ctx,
                menu_type=ViewMenu.TypeEmbed,
                disable_items_on_timeout=True,
                style="Page $/& | If you need help on a specific command, please use `help command COMMAND`. COMMAND must be the full command name",
            )
            for i in self.bot.cogs.items():
                cog_name = i[0]
                cog = i[1]
                if cog_name in excluded_cogs:
                    pass
                else:
                    cmds = [
                        command.qualified_name
                        for command in cog.walk_commands()
                        if not command.description.startswith("Main")
                    ]
                    embed = Embed(
                        color=Color.random(),
                    )
                    embed.add_field(
                        name=f"**{cog.qualified_name.title()}**",
                        value="\n".join(cmds),
                    )
                    menu.add_page(embed=embed)

            menu.add_button(ViewButton.go_to_first_page())
            menu.add_button(ViewButton.back())
            menu.add_button(ViewButton.next())
            menu.add_button(ViewButton.go_to_last_page())
            menu.add_go_to_select(ViewSelect.GoTo(title="Go to page", page_numbers=...))
            await menu.start()

    @help.command(aliases=["cmd"], description="Get help on a certain command")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def command(self, ctx: Context, *, command: Range[str, 3]):
        cmd = next(
            (cmd for cmd in self.bot.walk_commands() if cmd.qualified_name == command),
            None,
        )
        if cmd:
            bot_perms: dict = getattr(cmd, "bot_perms", None)
            member_perms: dict = getattr(cmd, "member_perms", None)
            embed = Embed(title=f"{command.title()} Help", color=Color.random())
            embed.description = cmd.description
            if len(cmd.aliases) >= 1:
                embed.add_field(
                    name="Aliases", value=", ".join(cmd.aliases), inline=True
                )
            try:
                actions = cmd.clean_params["parser"].default._actions
                parms = "".join(
                    [
                        (
                            f"<{i.option_strings[1]} {i.help}> "
                            if i.required
                            else f"[{i.option_strings[1]} {i.help}] "
                        )
                        for i in actions
                    ]
                )
                desc = [
                    (
                        f"`<{i.option_strings[1]} {i.help}>`"
                        if i.required
                        else f"`[{i.option_strings[1]} {i.help}]`"
                    )
                    for i in actions
                ]
                value = "\n".join(desc)
            except:
                parms = cmd.signature
                value = f"`{parms}`"
            if parms:
                embed.add_field(name="Parameters", value=value, inline=False)
            if bot_perms:
                perms = [str(i).replace("_", " ").title() for i in bot_perms.keys()]
                embed.add_field(
                    name="Bot Permissions", value="\n".join(perms), inline=True
                )
            if member_perms:
                perms = [str(i).replace("_", " ").title() for i in member_perms.keys()]
                embed.add_field(
                    name="User Permissions", value="\n".join(perms), inline=True
                )
            if not cmd.description.startswith("Main"):
                cmd_usage = "j!" + cmd.qualified_name + " " + parms
                embed.add_field(
                    name="Command Usage", value=f"`{cmd_usage}`", inline=False
                )
            embed.set_footer(
                text="Legend:\n<> - Required\n[] - Optional\n\nIt is best to go to the website for detailed explanations and usages"
            )
            await ctx.send(embed=embed)
            return
        embed = Embed(description="I don't have this command", color=Color.red())
        await ctx.send(embed=embed)

    @help.command(description="Get help of a certain module")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def module(self, ctx: Context, module: str):
        module_mapping = {
            "currency": SlashModules.currency,
            "fun": SlashModules.fun,
            "hentai": SlashModules.hentai,
            "image": SlashModules.image,
            "pictures": SlashModules.image,
            "pics": SlashModules.image,
            "images": SlashModules.image,
            "info": SlashModules.info,
            "information": SlashModules.info,
            "levelling": SlashModules.levelling,
            "lvl": SlashModules.levelling,
            "rank": SlashModules.levelling,
            "moderation": SlashModules.moderation,
            "mod": SlashModules.moderation,
            "reactions": SlashModules.reactions,
            "react": SlashModules.reactions,
        }
        module_instance = module_mapping.get(module.lower())
        module_data = dumps(modules[module_instance.value])
        if module_data:
            parms = OrderedDict([("%module%", str(module.capitalize()))])
            json_data: dict = loads(self.replace_all(module_data, parms))
            embed_data = json_data.get("embeds")
            embed = Embed.from_dict(embed_data[0])
        await ctx.send(embed=embed)

    @help.command(
        description="Get help from the website or join the support server for further help"
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def support(self, ctx: Context):
        view = help_button()
        help = Embed(
            description="Click on one of the buttons to open the documentation or get help in the support server",
            color=Color.random(),
        )
        await ctx.send(embed=help, view=view)
        return


async def setup(bot: Bot):
    await bot.add_cog(HelpGroupPrefix(bot))
