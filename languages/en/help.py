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
        wiki_url = "https://jeannebot.vercel.app/help"
        orleans_url = "https://discord.gg/jh7jkuk2pp"
        tos_and_policy_url = "https://jeannebot.vercel.app/tos"
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Jeanne Website", url=wiki_url)
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

    async def command(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
        related_commands: list[str] | None = None,
    ):
        await ctx.response.defer()
        cmd_obj = next(
            (
                cmd
                for cmd in self.bot.tree.walk_commands()
                if not isinstance(cmd, Jeanne.Group) and cmd.qualified_name == command
            ),
        )
        cmd = cmd_obj.extras
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
                for i, parm in zip(command["parameters"], parms, strict=False)
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
        examples = command.get("examples") or [cmd_usage]
        embed.add_field(
            name="Examples",
            value="\n".join(f"`{example}`" for example in examples),
            inline=False,
        )
        cooldown = command.get("cooldown") or cmd.get("cooldown")
        if cooldown:
            embed.add_field(name="Cooldown", value=str(cooldown), inline=True)
        if related_commands:
            embed.add_field(
                name="Related Commands",
                value="\n".join(f"`/{related}`" for related in related_commands),
                inline=False,
            )
        embed.set_footer(
            text="Legend:\n[] - Required\n<> - Optional\n\nIt is best to go to the websites for detailed explanations and usages"
        )
        await ctx.followup.send(embed=embed, view=help_button())

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
