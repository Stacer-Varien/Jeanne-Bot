from discord import (
    ButtonStyle,
    ChannelType,
    Interaction,
    SelectOption,
    TextChannel,
    app_commands as Jeanne,
    ui,
)
from discord.ext.commands import Bot, Cog
from discord.app_commands import locale_str as T
from functions import (
    Manage,
    ServerSettings,
    check_botbanned_app_command,
    get_command_locale,
    is_suspended,
)
import languages.en.serverops as en
import languages.fr.serverops as fr
import languages.de.serverops as de


def _language_for_locale(locale: str):
    if locale == "fr":
        return fr
    if locale == "de":
        return de
    return en


def _language(ctx: Interaction):
    return _language_for_locale(get_command_locale(ctx))


class SetupCurrencyModal(ui.Modal):
    def __init__(self, view: "SetupDashboardView") -> None:
        self.dashboard_view = view
        language = view.language
        super().__init__(title=language.TEXT["currency_modal_title"])
        settings = ServerSettings(view.guild)
        self.name_input = ui.TextInput(
            label=language.TEXT["currency_name_label"],
            default=settings.currency_name,
            min_length=1,
            max_length=32,
            required=True,
        )
        self.emoji_input = ui.TextInput(
            label=language.TEXT["currency_emoji_label"],
            default=settings.currency_emoji,
            max_length=80,
            required=False,
        )
        self.add_item(self.name_input)
        self.add_item(self.emoji_input)

    async def on_submit(self, interaction: Interaction) -> None:
        settings = ServerSettings(interaction.guild)
        await settings.set_currency_display(
            str(self.name_input.value), str(self.emoji_input.value)
        )
        view = SetupDashboardView(interaction, self.dashboard_view.bot)
        await interaction.response.send_message(
            embed=view.make_embed(),
            view=view,
            ephemeral=True,
        )


class SetupAreaSelect(ui.Select):
    def __init__(self, language) -> None:
        super().__init__(
            placeholder=language.TEXT["area_placeholder"],
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label=label, value=value)
                for value, label in language.AREA_LABELS.items()
            ],
            row=0,
        )

    async def callback(self, interaction: Interaction) -> None:
        view: SetupDashboardView = self.view
        view.selected_area = self.values[0]
        await interaction.response.send_message(
            view.language.TEXT["updated"], ephemeral=True
        )


class SetupChannelSelect(ui.ChannelSelect):
    def __init__(self, language) -> None:
        super().__init__(
            placeholder=language.TEXT["channel_placeholder"],
            channel_types=[ChannelType.text],
            min_values=1,
            max_values=1,
            row=1,
        )

    async def callback(self, interaction: Interaction) -> None:
        view: SetupDashboardView = self.view
        language = view.language
        if view.selected_area is None:
            await interaction.response.send_message(
                language.TEXT["select_area_first"], ephemeral=True
            )
            return

        channel = self.values[0]
        if not isinstance(channel, TextChannel):
            channel = interaction.guild.get_channel(channel.id)

        manager = Manage(interaction.guild)
        if view.selected_area == "welcome":
            await manager.set_welcomer(channel)
        elif view.selected_area == "leave":
            await manager.set_leaver(channel)
        elif view.selected_area == "modlog":
            await manager.set_modloger(channel)
        elif view.selected_area == "level":
            await manager.add_level_channel(channel)
        elif view.selected_area == "confession":
            await manager.add_confession_channel(channel)

        await interaction.response.edit_message(embed=view.make_embed(), view=view)


class SetupLanguageSelect(ui.Select):
    def __init__(self, language) -> None:
        super().__init__(
            placeholder=language.TEXT["language_placeholder"],
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label=label, value=value)
                for value, label in language.LANGUAGE_LABELS.items()
            ],
            row=2,
        )

    async def callback(self, interaction: Interaction) -> None:
        settings = ServerSettings(interaction.guild)
        await settings.set_language_override(self.values[0])
        view: SetupDashboardView = self.view
        view.language = _language(interaction)
        await interaction.response.edit_message(embed=view.make_embed(), view=view)


class SetupModuleSelect(ui.Select):
    def __init__(self, language) -> None:
        super().__init__(
            placeholder=language.TEXT["module_placeholder"],
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label=label, value=module)
                for module, label in ServerSettings.MODULES.items()
            ],
            row=3,
        )

    async def callback(self, interaction: Interaction) -> None:
        module = self.values[0]
        settings = ServerSettings(interaction.guild)
        await settings.set_module_enabled(
            module, enabled=settings.is_module_disabled(module)
        )
        view: SetupDashboardView = self.view
        await interaction.response.edit_message(embed=view.make_embed(), view=view)


class CurrencyButton(ui.Button):
    def __init__(self, language) -> None:
        super().__init__(
            label=language.TEXT["currency_button"],
            style=ButtonStyle.secondary,
            row=4,
        )

    async def callback(self, interaction: Interaction) -> None:
        view: SetupDashboardView = self.view
        await interaction.response.send_modal(SetupCurrencyModal(view))


class RefreshButton(ui.Button):
    def __init__(self, language) -> None:
        super().__init__(
            label=language.TEXT["refresh_button"],
            style=ButtonStyle.primary,
            row=4,
        )

    async def callback(self, interaction: Interaction) -> None:
        view: SetupDashboardView = self.view
        await interaction.response.edit_message(embed=view.make_embed(), view=view)


class SetupDashboardView(ui.View):
    def __init__(self, ctx: Interaction, bot: Bot) -> None:
        super().__init__(timeout=600)
        self.bot = bot
        self.author_id = ctx.user.id
        self.guild = ctx.guild
        self.language = _language(ctx)
        self.selected_area: str | None = None
        self.add_item(SetupAreaSelect(self.language))
        self.add_item(SetupChannelSelect(self.language))
        self.add_item(SetupLanguageSelect(self.language))
        self.add_item(SetupModuleSelect(self.language))
        self.add_item(CurrencyButton(self.language))
        self.add_item(RefreshButton(self.language))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                self.language.TEXT["unauthorized"], ephemeral=True
            )
            return False
        if not interaction.user.guild_permissions.manage_guild:
            raise Jeanne.MissingPermissions(["Manage Server"])
        return True

    def make_embed(self):
        settings = ServerSettings(self.guild)
        embed = self.language.setup_embed(
            self.guild, settings, settings.setup_status(self.guild)
        )
        if self.selected_area:
            label = self.language.AREA_LABELS[self.selected_area]
            embed.set_footer(text=f"{label}")
        return embed


class SetupCog(Cog, name="SetupSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name=T("setup_name"),
        description=T("setup_desc"),
        extras={
            "en": {
                "name": "setup",
                "description": "Open Jeanne's private server setup dashboard",
                "member_perms": "Manage Server",
            },
            "fr": {
                "name": "configuration",
                "description": "Ouvrir le panneau privé de configuration serveur de Jeanne",
                "member_perms": "Gérer le serveur",
            },
            "de": {
                "name": "einrichtung",
                "description": "Jeannes privates Server-Einrichtungspanel öffnen",
                "member_perms": "Server verwalten",
            },
        },
    )
    @Jeanne.guild_only()
    @Jeanne.checks.has_permissions(manage_guild=True)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(is_suspended)
    async def setup_dashboard(self, ctx: Interaction):
        view = SetupDashboardView(ctx, self.bot)
        await ctx.response.send_message(
            embed=view.make_embed(),
            view=view,
            ephemeral=True,
        )


async def setup(bot: Bot):
    await bot.add_cog(SetupCog(bot))
