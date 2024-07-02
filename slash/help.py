from discord import (
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    ui,
    app_commands as Jeanne,
)
from discord.ext.commands import GroupCog, Bot
from functions import AutoCompleteChoices, check_botbanned_app_command

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

    @Jeanne.command(description="Get help on a certain command")
    @Jeanne.autocomplete(command=AutoCompleteChoices.command_choices)
    @Jeanne.describe(command="Which command you need help with?")
    @Jeanne.check(check_botbanned_app_command)
    async def command(self, ctx: Interaction, command: Jeanne.Range[str, 3]):
            await ctx.response.defer()
            cmd = next(
                (
                    cmd
                    for cmd in self.bot.tree.walk_commands()
                    if not isinstance(cmd, Jeanne.Group) and cmd.qualified_name == command
                ),
            )
            try:
                bot_perms = cmd.extras["bot_perms"]
            except:
                bot_perms = None
            try:
                member_perms = cmd.extras["member_perms"]
            except:
                member_perms = None
            try:
                nsfw = cmd.extras["nsfw"]
            except:
                nsfw = None
            embed = Embed(title=f"{command.title()} Help", color=Color.random())
            embed.description = cmd.description
            parms = [
                f"[{i.name}]" if i.required else f"<{i.name}>" for i in cmd.parameters
            ]
            descs = [
                f"`{parm}` - {i.description}" for i, parm in zip(cmd.parameters, parms)
            ]
            if parms:
                embed.add_field(name="Parameters", value="\n".join(descs), inline=False)
            if bot_perms:
                embed.add_field(name="Jeanne Permissions", value=bot_perms, inline=True)
            if member_perms:
                embed.add_field(
                    name="Member Permissions", value=member_perms, inline=True
                )
            if nsfw:
                embed.add_field(name="Requires NSFW Channel", value=nsfw, inline=True)

            cmd_usage = "/" + cmd.qualified_name + " " + " ".join(parms)
            embed.add_field(name="Command Usage", value=f"`{cmd_usage}`", inline=False)
            embed.set_footer(
                text="Legend:\n[] - Required\n<> - Optional\n\nIt is best to go to the websites for detailed explanations and usages"
            )
            await ctx.followup.send(embed=embed)

    @command.error
    async def command_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, (IndexError, RuntimeError)
        ):
            embed = Embed(description="I don't have this command", color=Color.red())
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        description="Get help from the website or join the support server for further help"
    )
    @Jeanne.check(check_botbanned_app_command)
    async def support(self, ctx: Interaction):
        view = help_button()
        help = Embed(
            description="Click on one of the buttons to open the documentation or get help in the support server",
            color=Color.random(),
        )
        await ctx.response.send_message(embed=help, view=view)


async def setup(bot: Bot):
    await bot.add_cog(HelpGroup(bot))
