from assets.components import Confirmation
from functions import AutoCompleteChoices, Botban, Command, Currency, Inventory
from discord import Color, Embed, File, Interaction, app_commands as Jeanne
from PIL import UnidentifiedImageError
from discord.ext.commands import Bot, GroupCog
from assets.generators.profile_card import Profile
from asyncio import get_event_loop
from functools import partial
from requests import exceptions
from reactionmenu import ViewButton, ViewMenu


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Check all the wallpapers available")
    async def backgrounds(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.backgrounds.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
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
            page_embed = Embed(title=f"Item ID: {wallpaper[0]}", color=embed.color)
            page_embed.add_field(name="Name", value=str(wallpaper[1]), inline=True)
            page_embed.add_field(
                name="Price", value="1000 <:quantumpiece:1161010445205905418>"
            )
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)

        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())

        await menu.start()


class Background_Group(GroupCog, name="background"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    def get_card(self, args):
        image = Profile().generate_profile(**args)
        return image

    @Jeanne.command(description="Buy a background pic for your level card")
    @Jeanne.describe(name="Which background you are buying?")
    @Jeanne.autocomplete(name=AutoCompleteChoices.get_all_wallpapers)
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def buy(self, ctx: Interaction, name: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.buy.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        balance = Currency(ctx.user).get_balance

        if balance == 0:
            nomoney = Embed(
                description="You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=nomoney)
            return

        if balance < 1000:
            notenough = Embed(
                description="You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=notenough)
            return

        try:
            Inventory.get_wallpaper(name)
        except:
            await ctx.followup.send(
                embed=Embed(description="Unable to find wallpaper", color=Color.red())
            )
            return

        image_url = Inventory().get_wallpaper(name)[1]

        await ctx.followup.send(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )
        args = {
            "bg_image": image_url,
            "profile_image": str(ctx.user.avatar.with_format("png")),
            "font_color": None,
            "server_level": 100,
            "server_user_xp": 50,
            "server_next_xp": 100,
            "global_level": 100,
            "global_user_xp": 50,
            "global_next_xp": 100,
            "user_name": str(ctx.user),
            "grank": 1,
            "srank": 1,
            "voted": True,
            "rrank": 1,
            "creator": self.bot.application.owner.id,
            "partner": self.bot.application.owner.id,
            "beta": self.bot.application.owner,
            "balance": 100,
            "bio": "This is a preview",
            "brightness": 100,
        }

        func = partial(self.get_card, args)
        image = await get_event_loop().run_in_executor(None, func)

        file = File(fp=image, filename=f"preview_profile_card.png")

        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.random(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
        )
        view = Confirmation(ctx.user)
        await ctx.edit_original_response(
            content=None, attachments=[file], embed=preview, view=view
        )
        await view.wait()

        if view.value == None:
            await ctx.edit_original_response(
                content="Timeout", view=None, embed=None, attachments=[]
            )
            return

        if view.value == True:
            Inventory(ctx.user).add_user_wallpaper(name)
            embed1 = Embed(
                description=f"Background wallpaper bought and selected",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None)

        else:
            await ctx.edit_original_response(
                content="Cancelled", view=None, embed=None, attachments=[]
            )

    @buy.error
    async def buy_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.buy.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            cooldown = Embed(
                description=f"You have already tried to preview this background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Jeanne.command(description="Select a wallpaper")
    @Jeanne.autocomplete(name=AutoCompleteChoices.list_all_user_inventory)
    @Jeanne.describe(name="What is the name of the background?")
    async def use(self, ctx: Interaction, name: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.use.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()

        try:
            Inventory(ctx.user).use_wallpaper(name)
            embed = Embed(description=f"{name} has been selected", color=Color.random())
            await ctx.followup.send(embed=embed)
        except:
            embed = Embed(
                description="This background image is not in your inventory",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    @Jeanne.command(
        name="buy-custom", description="Buy a custom background pic for your level card"
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    @Jeanne.describe(name="What will you name it?", link="Add an image link")
    async def buycustom(self, ctx: Interaction, name: str, link: str):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.buycustom.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        balance = Currency(ctx.user).get_balance

        if balance == None:
            nomoney = Embed(
                description="You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=nomoney)
            return

        if balance < 1000:
            notenough = Embed(
                description="You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=notenough)
            return

        await ctx.followup.send(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )

        args = {
            "bg_image": link,
            "profile_image": str(ctx.user.avatar.with_format("png")),
            "font_color": None,
            "server_level": 100,
            "server_user_xp": 50,
            "server_next_xp": 100,
            "global_level": 100,
            "global_user_xp": 50,
            "global_next_xp": 100,
            "user_name": str(ctx.user),
            "grank": 1,
            "srank": 1,
            "voted": True,
            "rrank": 1,
            "creator": self.bot.application.owner.id,
            "partner": self.bot.application.owner.id,
            "beta": self.bot.application.owner,
            "balance": 100,
            "bio": "This is a preview",
            "brightness": 100,
        }

        func = partial(self.get_card, args)
        image = await get_event_loop().run_in_executor(None, func)

        file = File(fp=image, filename="preview_profile_card.png")

        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.blue(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
            .set_footer(
                text="Please note that if the custom background violates ToS (both Discord and Bot) or is NSFW, it will be removed with NO REFUNDS!"
            )
        )
        view = Confirmation(ctx.user)
        await ctx.edit_original_response(
            content=None, embed=preview, attachments=[file], view=view
        )
        await view.wait()

        if view.value == True:
            Inventory(ctx.user).add_user_custom_wallpaper(name, link)

            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None, attachments=[])

        else:
            await ctx.edit_original_response(
                content="Cancelled", embed=None, view=None, attachments=[]
            )

    @buycustom.error
    async def buycustom_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.buycustom.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            cooldown = Embed(
                description=f"You have already tried to preview this background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.response.send_message(embed=cooldown)
            return

        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original,
            (
                exceptions.MissingSchema,
                exceptions.ConnectionError,
                UnidentifiedImageError,
            ),
        ):
            embed = Embed(description="Invalid image URL", color=Color.red())
            await ctx.edit_original_response(content=None, embed=embed)

    @Jeanne.command(description="Check which backgrounds you have")
    async def list(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.list.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        if Inventory(ctx.user).get_user_inventory == None:
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
            page_embed = Embed(color=embed.color)
            page_embed.add_field(name="Name", value=str(wallpaper[1]), inline=True)
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)

        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())

        await menu.start()


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))
