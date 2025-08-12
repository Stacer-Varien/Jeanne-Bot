from discord import (
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    ui,
    app_commands as Jeanne,
)
from discord.ext.commands import Bot


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


class HelpGroup:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def command(self, ctx: Interaction, command: Jeanne.Range[str, 3]):
        await ctx.response.defer()
        cmd = next(
            (
                cmd.extras
                for cmd in self.bot.tree.walk_commands()
                if not isinstance(cmd, Jeanne.Group) and cmd.qualified_name == command
            ),
        )
        command = cmd["en"]
        try:
            bot_perms = command["bot_perms"]
        except Exception:
            bot_perms = None
        try:
            member_perms = command["member_perms"]
        except Exception:
            member_perms = None
        try:
            nsfw = cmd["nsfw"]
        except Exception:
            nsfw = None
        name = command["name"]
        description = command["description"]
        embed = Embed(title=f"{name.title()} Help", color=Color.random())
        embed.description = description
        try:
            parms = [
                f"[{i["name"]}]" if bool(i["required"]) else f"<{i["name"]}>"
                for i in command["parameters"]
            ]
            descs = [
                f"`{parm}` - {i["description"]}"
                for i, parm in zip(command["parameters"], parms)
            ]
            embed.add_field(name="Parameters", value="\n".join(descs), inline=False)
        except Exception:
            parms = []
        if bot_perms:
            embed.add_field(name="Jeanne Permissions", value=bot_perms, inline=True)
        if member_perms:
            embed.add_field(name="Member Permissions", value=member_perms, inline=True)
        if nsfw:
            embed.add_field(name="Requires NSFW Channel", value=nsfw, inline=True)

        cmd_usage = "/" + name + " " + " ".join(parms)
        embed.add_field(name="Command Usage", value=f"`{cmd_usage}`", inline=False)
        embed.set_footer(
            text="Legend:\n[] - Required\n<> - Optional\n\nIt is best to go to the websites for detailed explanations and usages"
        )
        await ctx.followup.send(embed=embed)

    async def command_error(self, ctx: Interaction):
        embed = Embed(description="I don't have this command", color=Color.red())
        await ctx.followup.send(embed=embed)

    async def support(self, ctx: Interaction):
        view = help_button()
        help = Embed(
            description="Click on one of the buttons to open the documentation or get help in the support server",
            color=Color.random(),
        )
        await ctx.response.send_message(embed=help, view=view)
