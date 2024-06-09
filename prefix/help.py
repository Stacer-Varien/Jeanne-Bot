from json import dumps, loads
from discord import ButtonStyle, Color, Embed, Interaction, SelectOption, ui
from discord.ext.commands import Bot, Cog, group, Context, Range
import discord.ext.commands as Jeanne
from reactionmenu import Page, ViewButton, ViewMenu, ViewSelect
from functions import (
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from re import findall


class HelpMenu(ui.Select):
    def __init__(self, bot: Bot):
        self.bot = bot

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
            "ReactionsSlash",
            "embed",
            "slashutilities",
            "reminder",
            "moderation",
        ]

        options = []
        self.embeds = {}

        for cog_name, cog in self.bot.cogs.items():
            if cog_name in excluded_cogs:
                continue

            cmds = [
                command.qualified_name
                for command in cog.walk_commands()
                if not command.description.startswith("Main")
            ]

            embed = Embed(color=Color.random())

            if cog_name == "Level":
                embed.description = (
                    "## How to gain XP\n"
                    "You gain XP by sending a message. You gain **5XP/2 Minutes/Message** "
                    "meaning if you send a message **now**, you will gain **5XP** but you "
                    "have to wait for **2 minutes** to gain another 5XP on the next message. "
                    "On weekends, you get **10XP/2 Minutes/Message**. Voting rewards are "
                    "available depending if you have voted in TopGG and/or DiscordBotList."
                )
                embed.add_field(
                    name=f"**{cog.qualified_name.title()}**", value="\n".join(cmds)
                )
            elif cog_name == "Manage":
                embed.description = (
                    "Channel commands require the **manage channel** permission, role commands "
                    "require the **manage role** permission, and setting a logging channel and "
                    "editing the server require the **manage server** permission. Creating, "
                    "renaming, and deleting emojis and stickers requires the **manage emojis "
                    "and stickers** permission. As for profile-related commands, everyone can use them."
                )
                create_group = [cmd for cmd in cmds if cmd.startswith("create")]
                delete_group = [cmd for cmd in cmds if cmd.startswith("delete")]
                set_group = [cmd for cmd in cmds if cmd.startswith("set")]
                edit_group = [cmd for cmd in cmds if cmd.startswith("edit")]
                level_group = [cmd for cmd in cmds if cmd.startswith("level")]
                other_group = [
                    cmd
                    for cmd in cmds
                    if not cmd.startswith(("create", "delete", "set", "edit", "level"))
                ]

                embed.add_field(
                    name="create", value="\n".join(create_group), inline=True
                )
                embed.add_field(
                    name="delete", value="\n".join(delete_group), inline=True
                )
                embed.add_field(name="set", value="\n".join(set_group), inline=True)
                embed.add_field(name="edit", value="\n".join(edit_group), inline=True)
                embed.add_field(name="level", value="\n".join(level_group), inline=True)
                embed.add_field(
                    name=f"**{cog.qualified_name.title()}**",
                    value="\n".join(other_group),
                )
            elif cog_name == "Inventory":
                embed.description = "This module has 2 systems working together. It is still under development but functional."
                embed.add_field(
                    name=f"**{cog.qualified_name.title()}**", value="\n".join(cmds)
                )
            elif cog_name == "Currency":
                embed.description = "When using the commands related to this module, please respect the [rules](https://jeannebot.gitbook.io/jeannebot/tos-and-privacy#terms-of-services)."
                embed.add_field(
                    name=f"**{cog.qualified_name.title()}**", value="\n".join(cmds)
                )
            else:
                embed.add_field(
                    name=f"**{cog.qualified_name.title()}**", value="\n".join(cmds)
                )

            embed.set_footer(
                text='If you need help on a specific command, please use "help command COMMAND". COMMAND must be the full command name.'
            )

            options.append(
                SelectOption(label=cog.qualified_name.title(), value=cog_name)
            )
            self.embeds[cog_name] = embed

        super().__init__(
            placeholder="Select an option", max_values=1, min_values=1, options=options
        )

    async def callback(self, ctx: Interaction):
        selected_cog_name = self.values[0]
        embed = self.embeds.get(selected_cog_name)
        if embed:
            await ctx.response.edit_message(embed=embed)


class HelpSelect(ui.View):
    def __init__(self, bot:Bot):
        self.bot=bot
        super().__init__(timeout=120)
        self.add_item(HelpMenu(self.bot))


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

    @staticmethod
    def splitsegs(input:str)->list[str]:
        segments= findall(r"\[.*?\]|\<.*?\>", input)
        return [f"`{segment}`" for segment in segments]

    @group(
        aliases=["h"],
        invoke_without_command=True,
        description="Main Help command for the help subcommands and shows all the commands and modules available",
    )
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def help(self, ctx: Context):
        async with ctx.typing():
            view=HelpSelect(self.bot)
            embed=Embed(color=Color.random())
            embed.description="""
## The available modules are:
- Currency
- Fun
- Hentai (NSFW)
- Image
- Info
- Inventory
- Levelling
- Manage
- Moderation
- Reaction
- Uitilities

To check availability of commands in each module, use the dropmenu below
"""

            await ctx.send(embed=embed, view=view)

    @help.command(aliases=["cmd"], description="Get help on a certain command", usage="[COMMAND NAME]")
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.check(check_botbanned_prefix)
    async def command(self, ctx: Context, *, command: Range[str, 3]):
        cmd = next(
            (cmd for cmd in self.bot.walk_commands() if cmd.qualified_name == command),
            None,
        )
        if cmd:
            try:
                bot_perms = cmd.extras["bot_perms"]
            except:
                bot_perms=None
            try:
                member_perms = cmd.extras["member_perms"]
            except:
                member_perms=None
            try:
                nsfw=cmd.extras["nsfw"]
            except:
                nsfw=None
            embed = Embed(title=f"{command.title()} Help", color=Color.random())
            embed.description = cmd.description
            if len(cmd.aliases) >= 1:
                embed.add_field(
                    name="Aliases", value=", ".join(cmd.aliases), inline=True
                )

            parms = None if cmd.usage==None else "\n".join(self.splitsegs(cmd.usage))
            if parms:
                embed.add_field(name="Parameters", value=parms, inline=False)
            if bot_perms:
                embed.add_field(
                    name="Jeanne Permissions", value=bot_perms, inline=True
                )
            if member_perms:
                embed.add_field(
                    name="Member Permissions", value=member_perms, inline=True
                )
            if nsfw:
                embed.add_field(
                    name="Requires NSFW Channel", value=nsfw, inline=True
                )
            if not cmd.description.startswith("Main"):
                cmd_usage = "j!" + cmd.qualified_name + " " + cmd.usage
                embed.add_field(
                    name="Command Usage", value=f"`{cmd_usage}`", inline=False
                )
            embed.set_footer(
                text="Legend:\n[] - Required\n<> - Optional\n | - CHOICES\n\nIt is best to go to the website for detailed explanations and usages"
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
