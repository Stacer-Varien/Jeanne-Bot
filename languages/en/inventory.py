from assets.components import (
    Confirmation,
    Country_Badge_Buttons,
    buy_function_app,
    use_function_app,
)
from functions import (
    Currency,
    Inventory,  
)
from discord import ButtonStyle, Color, Embed, File, Interaction, app_commands as Jeanne
from discord.ext.commands import Bot
from assets.generators.profile_card import Profile
from reactionmenu import ViewButton, ViewMenu


class Shop_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def country(self, ctx: Interaction):
        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance
        if balance is None or balance < 500:
            nomoney = Embed(description="You do not have enough QP.")
            await ctx.followup.send(embed=nomoney)
            return
        view = Country_Badge_Buttons(self.bot, ctx.user)
        embed = Embed(
            description="Here are the available country badges:", color=Color.random()
        )
        embed.set_footer(text="Click on one of the buttons to buy the badge")
        await ctx.followup.send(embed=embed, view=view)
        await view.wait()

        if view.value:
            country = view.value
            await Inventory(ctx.user).add_country(country)
            embed1 = Embed(
                description="Country badge bought and added to profile",
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
            style="Page $/&",
        )
        embed.color = Color.random()
        for wallpaper in wallpapers:
            name = str(wallpaper[1])
            page_embed = Embed(title=name, color=embed.color)

            page_embed.add_field(
                name="Price", value="1000 <:quantumpiece:1161010445205905418>"
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
                label="Buy",
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
                description=f"You have already tried to preview a background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)


class Background_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    async def buycustom(self, ctx: Interaction, name: str, link: str):
        await ctx.response.defer()
        profile = Profile(self.bot)
        media = await profile.inspect_image(link, ctx.filesize_limit)
        if not media:
            await ctx.followup.send(
                embed=Embed(
                    description="The image is invalid or exceeds this server's upload limit.",
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
                    description="Unlock animated profile cards with `/shop animated-profile` before buying a GIF background.",
                    color=Color.red(),
                )
            )
            return
        balance = Currency(ctx.user).get_balance
        if balance is None or balance < price:
            nomoney = Embed(description=f"You need {price:,} QP for this background.")
            await ctx.followup.send(embed=nomoney)
            return
        await ctx.followup.send(
            embed=Embed(
                description="Creating preview... This will take some time <a:loading:1161038734620373062>"
            )
        )
        image = await profile.generate_profile(
            ctx, ctx.user, link, True, True, "southafrica"
        )
        if not image:
            await ctx.edit_original_response(
                embed=Embed(
                    description="Failed to generate a preview from that image.",
                    color=Color.red(),
                )
            )
            return
        extension = Profile.output_extension(image)
        if animated and extension != "gif":
            await ctx.edit_original_response(
                embed=Embed(
                    description="The animated profile card could not fit within this server's upload limit.",
                    color=Color.red(),
                )
            )
            return
        file = File(fp=image, filename=f"preview_profile_card.{extension}")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.blue(),
            )
            .add_field(
                name="Cost", value=f"{price:,} <:quantumpiece:1161010445205905418>"
            )
            .set_footer(
                text="Confirm this background. ToS or NSFW violations are removed with no refunds."
            )
        )
        view = Confirmation(ctx, ctx.user)
        await ctx.edit_original_response(embed=preview, attachments=[file], view=view)
        await view.wait()
        if view.value:
            url = await Inventory(ctx.user).upload_to_catbox(link)
            if not url:
                failed = Embed(
                    description="Failed to upload the image. Please try again later.",
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
                failed = Embed(
                    description="The purchase could not complete. Check your balance and background name.",
                    color=Color.red(),
                )
                await ctx.edit_original_response(
                    embed=failed, view=None, attachments=[]
                )
                return
            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None, attachments=[])
        else:
            await ctx.edit_original_response(
                embed=Embed(description="Cancelled"), view=None, attachments=[]
            )

    async def buycustom_error(self, ctx: Interaction, error: Jeanne.AppCommandError, type:str):
        if type == "cooldown":
            cooldown = Embed(
                description=f"You have already tried to preview a background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)
            return
        if type == "invalid":
            embed = Embed(description="Invalid image URL", color=Color.red())
            await ctx.edit_original_response(content=None, embed=embed)
 
    async def list(self, ctx: Interaction):
        await ctx.response.defer()
        if Inventory(ctx.user).get_user_inventory is None:
            embed = Embed(description="Your inventory is empty", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        a = Inventory(ctx.user).get_user_inventory
        embed = Embed()
        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Page $/&",
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
                label="Use",
                style=ButtonStyle.green,
                custom_id=ViewButton.ID_CALLER,
                followup=call_followup,
            )
        )
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()

