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
            ui.Button(
                style=ButtonStyle.link, label=("Site Web de Jeanne"), url=wiki_url
            )
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link, label=("Serveur de Support"), url=orleans_url
            )
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label=("Conditions d'utilisation et Politique de Confidentialité"),
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
        command = cmd["fr"]
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

        embed = Embed(
            title=(f"Aide pour {name}"),
            description=description,
            color=Color.random(),
        )

        try:

            parms = [
                f"[{i["name"]}]" if bool(i["required"]) else f"<{i["name"]}>"
                for i in command["parameters"]
            ]
            descs = [
                f"`{parm}` - {i["description"]}"
                for i, parm in zip(command["parameters"], parms)
            ]
            embed.add_field(name="Paramètres", value="\n".join(descs), inline=False)
        except Exception:
            parms = []

        if bot_perms:
            embed.add_field(name="Permissions de Jeanne", value=bot_perms, inline=True)
        if member_perms:
            embed.add_field(
                name="Permissions du Membre", value=member_perms, inline=True
            )
        if nsfw:
            embed.add_field(name="Nécessite un Canal NSFW", value=nsfw, inline=True)

        cmd_usage = "/" + name + " " + " ".join(parms)
        embed.add_field(
            name="Utilisation de la Commande", value=f"`{cmd_usage}`", inline=False
        )
        embed.set_footer(
            text="Légende:\n[] - Requis\n<> - Optionnel\n\nIl est préférable de visiter les sites web pour des explications et utilisations détaillées"
        )

        await ctx.followup.send(embed=embed)

    async def command_error(self, ctx: Interaction):
        embed = Embed(description=("Je n'ai pas cette commande"), color=Color.red())
        await ctx.followup.send(embed=embed)

    async def support(self, ctx: Interaction):
        view = help_button()
        help = Embed(
            description=(
                "Cliquez sur l'un des boutons pour ouvrir la documentation ou obtenir de l'aide sur le serveur de support"
            ),
            color=Color.random(),
        )
        await ctx.response.send_message(embed=help, view=view)
