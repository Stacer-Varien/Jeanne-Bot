from assets.components import (
    Confirmation,
    Country_Badge_Buttons,
    buy_function_app,
    use_function_app,
)
from functions import (
    Currency,
    Inventory,
    ServerSettings,
)
from discord import ButtonStyle, Color, Embed, File, Interaction, app_commands as Jeanne
from discord.ext.commands import Bot
from assets.generators.profile_card import Profile
from reactionmenu import ViewButton, ViewMenu


def qp(ctx: Interaction, amount: int) -> str:
    return ServerSettings.format_currency_for(ctx.guild, amount)


class Shop_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def country(self, ctx: Interaction):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance is None or balance < 500:
            nomoney = Embed(description="Du hast nicht genug Währung.")
            await ctx.followup.send(embed=nomoney)
            return
        view = Country_Badge_Buttons(self.bot, ctx.user)
        embed = Embed(
            description="Hier sind die verfügbaren Länderabzeichen:", color=Color.random()
        )
        embed.set_footer(text="Klicke auf einen der Buttons, um das Abzeichen zu kaufen")
        await ctx.followup.send(embed=embed, view=view)
        await view.wait()

        if view.value:
            country = view.value
            await Inventory(ctx.user).add_country(country)
            embed1 = Embed(
                description="Landabzeichen gekauft und dem Profil hinzugefügt",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None)
            return
        await ctx.delete_original_response()

    async def backgrounds(self, ctx: Interaction):
        await ctx.response.defer()
        disabled = False
        balance = Currency(ctx.user).get_balance
        if balance < 1000:
            disabled = True
        wallpapers = Inventory().fetch_wallpapers()
        embed = Embed()
        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Pagina $/&",
        )
        embed.color = Color.random()
        for wallpaper in wallpapers:
            name = str(wallpaper[1])
            page_embed = Embed(title=name, color=embed.color)

            page_embed.add_field(
                name="Preis", value=qp(ctx, 1000)
            )
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)

        async def buy_callback():
            await buy_function_app(self.bot, ctx, menu.last_viewed.embed.title)
            menu.remove_all_buttons()

        call_followup = ViewButton.Followup(
            details=ViewButton.Followup.set_caller_details(buy_callback)
        )

        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(
            ViewButton(
                label="Kopen",
                style=ButtonStyle.green,
                custom_id=ViewButton.ID_CALLER,
                followup=call_followup,
                disabled=disabled,
            )
        )
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()

    async def backgrounds_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        cooldown = Embed(
            description=f"Du hast bereits versucht, ein Hintergrundbild anzusehen!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
            color=Color.random(),
        )
        await ctx.response.send_message(embed=cooldown)


class Background_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def buycustom(self, ctx: Interaction, name: str, link: str):
        await ctx.response.defer()
        profile = Profile(self.bot)
        media = await profile.inspect_image(link, ctx.filesize_limit)
        if not media:
            await ctx.followup.send(
                embed=Embed(
                    description="Das Bild ist ungültig oder überschreitet das Upload-Limit dieses Servers.",
                    color=Color.red(),
                )
            )
            return
        animated = media.animated
        price = 5000 if animated else 1500
        inventory = Inventory(ctx.user)
        if animated and not inventory.animated_profile_unlocked:
            await ctx.followup.send(
                embed=Embed(
                    description="Schalte animierte Profile mit `/shop animated-profile` frei, bevor du einen GIF-Hintergrund kaufst.",
                    color=Color.red(),
                )
            )
            return
        balance = Currency(ctx.user).get_balance
        if balance is None or balance < price:
            nomoney = Embed(description=f"Du benötigst {qp(ctx, price)}.")
            await ctx.followup.send(embed=nomoney)
            return
        await ctx.followup.send(
            embed=Embed(
                description="Vorschau wird erstellt... Das kann eine Weile dauern <a:loading:1161038734620373062>"
            )
        )
        image = await profile.generate_profile(
            ctx, ctx.user, link, True, True, "southafrica"
        )
        if not image:
            size_error = Embed(
                description="Aus diesem Bild konnte keine Vorschau erstellt werden."
            )
            await ctx.edit_original_response(embed=size_error)
            return
        extension = Profile.output_extension(image)
        if animated and extension != "gif":
            await ctx.edit_original_response(
                embed=Embed(
                    description="Die animierte Profilkarte überschreitet das Upload-Limit dieses Servers.",
                    color=Color.red(),
                )
            )
            return
        file = File(fp=image, filename=f"preview_profile_card.{extension}")
        preview = (
            Embed(
                description="Dies ist die Vorschau der Profilkarte.",
                color=Color.blue(),
            )
            .add_field(
                name="Kosten", value=qp(ctx, price)
            )
            .set_footer(
                text="Achtung: Wenn der benutzerdefinierte Hintergrund gegen die ToS verstößt oder NSFW ist, wird er OHNE RÜCKERSTATTUNG entfernt!"
            )
        )
        view = Confirmation(ctx, ctx.user)
        await ctx.edit_original_response(embed=preview, attachments=[file], view=view)
        await view.wait()
        if view.value:
            url = await Inventory(ctx.user).upload_to_catbox(link)
            if not url:
                failed = Embed(
                    description="Das Hochladen des Bildes ist fehlgeschlagen. Bitte versuche es spaeter erneut.",
                    color=Color.red(),
                )
                await ctx.edit_original_response(
                    embed=failed, view=None, attachments=[]
                )
                return

            added = await inventory.add_user_custom_wallpaper(
                name, url, price=price, animated=animated
            )
            if not added:
                await ctx.edit_original_response(
                    embed=Embed(
                        description="Der Kauf konnte nicht abgeschlossen werden.",
                        color=Color.red(),
                    ),
                    view=None,
                    attachments=[],
                )
                return
            embed1 = Embed(
                description="Hintergrund gekauft und ausgewählt",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None, attachments=[])
        else:
            await ctx.edit_original_response(
                embed=Embed(description="Abgebrochen"), view=None, attachments=[]
            )

    async def buycustom_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError, type: str
    ):
        if type == "cooldown":
            cooldown = Embed(
                description=f"Du hast bereits versucht, ein Hintergrundbild anzusehen!\nVersuche es erneut in `{round(error.retry_after, 2)} Sekunden`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)
            return
        if type == "invalid":
            embed = Embed(description="Ungültige Bild-URL", color=Color.red())
            await ctx.edit_original_response(content=None, embed=embed)

    async def list(self, ctx: Interaction):
        await ctx.response.defer()
        if Inventory(ctx.user).get_user_inventory is None:
            embed = Embed(description="Dein Inventar ist leer", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        a = Inventory(ctx.user).get_user_inventory
        embed = Embed()
        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Pagina $/&",
        )
        embed.color = Color.random()
        for wallpaper in a:
            page_embed = Embed(title=str(wallpaper[1]), color=embed.color)
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)

        async def use_callback():
            await use_function_app(ctx, menu.last_viewed.embed.title)
            menu.remove_all_buttons()

        call_followup = ViewButton.Followup(
            details=ViewButton.Followup.set_caller_details(use_callback)
        )
        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(
            ViewButton(
                label="Verwenden",
                style=ButtonStyle.green,
                custom_id=ViewButton.ID_CALLER,
                followup=call_followup,
            )
        )
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()
