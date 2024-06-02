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
                show_page_director=False,
                timeout=120.0
            )
            options={}
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
                    if cog_name == "Level":
                        embed.description = "## How to gain XP\nYou gain XP by sending a message. You gain **5XP/2 Minutes/Message** meaning if you send a message **now**, you will gain **5XP** but you have to wait for **2 minutes** to gain another 5XP on the next message. On weekends, you get **10XP/2 Minutes/Message**. Voting rewards are available depending if you have voted in TopGG and/or DiscordBotList"
                    elif cog_name == "Manage":
                        embed.description = "Channel commands requires the **manage channel** permission, role commands require the **manage role** permission and setting a logging channel and editing the server requires the **manage server** permission. Creating, renaming and deleting emojis and stickers requires the **manage emojis and stickers permission**. As for profile related commands, everyone can use it"
                        create_group = [cmd for cmd in cmds if cmd.startswith("create")]
                        delete_group = [cmd for cmd in cmds if cmd.startswith("delete")]
                        set_group = [cmd for cmd in cmds if cmd.startswith("set")]
                        edit_group = [cmd for cmd in cmds if cmd.startswith("edit")]

                        embed.add_field(
                            name="create", value="\n".join(create_group), inline=True
                        )

                        embed.add_field(
                            name="delete", value="\n".join(delete_group), inline=True
                        )
                        embed.add_field(
                            name="set",
                            value="\n".join(set_group),
                            inline=True,
                        )
                        embed.add_field(
                            name="edit",
                            value="\n".join(edit_group),
                            inline=True,
                        )
                    elif cog_name == "Inventory":
                        embed.description = "This module has 2 systems working together. It is still under development but working."
                    elif cog_name == "Currency":
                        embed.description = "When using the commands related to this module, please respect the [rules](https://jeannebot.gitbook.io/jeannebot/tos-and-privacy#terms-of-services)"

                    embed.add_field(
                        name=f"**{cog.qualified_name.title()}**",
                        value="\n".join(cmds),
                    )
                    embed.set_footer(
                        text="""If you need help on a specific command, please use  the "help command COMMAND". COMMAND must be the full command name"""
                    )

                    option={SelectOption(label=cog.qualified_name) : [Page(embed=embed)]}
                    options.update(option)
                    menu.add_page(embed=embed)

            menu.add_button(ViewButton.go_to_first_page())
            menu.add_button(ViewButton.back())
            menu.add_button(ViewButton.next())
            menu.add_button(ViewButton.go_to_last_page())
            menu.add_select(ViewSelect(title="Go to...", options=options))
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
                            f"<{i.option_strings[1]} {i.help}> ".replace(
                                "<", "["
                            ).replace(">", "]")
                            if i.required
                            else f"[{i.option_strings[1]} {i.help}] ".replace(
                                "[", "<"
                            ).replace("]", ">")
                        )
                        for i in actions
                    ]
                )
                desc = [
                    (
                        f"`<{i.option_strings[1]} {i.help}>`".replace("<", "[").replace(
                            ">", "]"
                        )
                        if i.required
                        else f"`[{i.option_strings[1]} {i.help}]`".replace(
                            "[", "<"
                        ).replace("]", ">")
                    )
                    for i in actions
                ]
                value = "\n".join(desc)
            except:
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
                cmd_usage = "j!" + cmd.qualified_name + " " + cmd.usage
                embed.add_field(
                    name="Command Usage", value=f"`{cmd_usage}`", inline=False
                )
            embed.set_footer(
                text="Legend:\n[] - Required\n<> - Optional\n\nIt is best to go to the website for detailed explanations and usages"
            )
            await ctx.send(embed=embed)
            return
        embed = Embed(description="I don't have this command", color=Color.red())
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
