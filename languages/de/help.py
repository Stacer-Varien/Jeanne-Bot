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
            ui.Button(style=ButtonStyle.link, label="Jeanne-Website", url=wiki_url)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Support-Server", url=orleans_url)
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="ToS und Datenschutz",
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
                f"[{i['name']}]" if bool(i["required"]) else f"<{i['name']}>"
                for i in command["parameters"]
            ]
            descs = [
                f"`{parm}` - {i['description']}"
                for i, parm in zip(command["parameters"], parms)
            ]
            embed.add_field(name="Parameter", value="\n".join(descs), inline=False)
        except Exception:
            parms = []
        if bot_perms:
            embed.add_field(name="Jeanne-Berechtigungen", value=bot_perms, inline=True)
        if member_perms:
            embed.add_field(
                name="Benutzerberechtigungen", value=member_perms, inline=True
            )
        if nsfw:
            embed.add_field(name="NSFW-Kanal erforderlich", value=nsfw, inline=True)

        cmd_usage = "/" + name + " " + " ".join(parms)
        embed.add_field(name="Befehlsverwendung", value=f"`{cmd_usage}`", inline=False)
        embed.set_footer(
            text="Legende:\n[] - Pflicht\n<> - Optional\n\nAm besten besuchst du die Websites für detaillierte Erklärungen und Nutzung"
        )
        await ctx.followup.send(embed=embed)

    async def command_error(self, ctx: Interaction):
        embed = Embed(description="Ich habe diesen Befehl nicht", color=Color.red())
        await ctx.followup.send(embed=embed)

    async def support(self, ctx: Interaction):
        view = help_button()
        help = Embed(
            description="Klicke auf einen der Buttons, um die Dokumentation zu öffnen oder Hilfe im Support-Server zu erhalten",
            color=Color.random(),
        )
        await ctx.response.send_message(embed=help, view=view)
