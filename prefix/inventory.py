import argparse
from assets.components import Confirmation
from functions import (
    Currency,
    Inventory,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
    is_beta_prefix,
)
from discord import Color, Embed, File, Message
from PIL import UnidentifiedImageError
from discord.ext.commands import Bot, Context, BucketType, Cog
import discord.ext.commands as Jeanne
from assets.generators.profile_card import Profile
from requests import exceptions
from reactionmenu import ViewButton, ViewMenu


class Shop_Group(Cog, name="Shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @Jeanne.group(name="shop", description="Main shop command", invoke_without_command=True)
    async def shop(self, ctx:Context):...

    @shop.command(aliases=["bgs", "bg"],description="Check all the wallpapers available")
    @Jeanne.check(is_beta_prefix)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def backgrounds(self, ctx: Context):
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

    @Jeanne.group(aliases=["bg"],
        name="background", description="Main background command", invoke_without_command=True
    )
    async def background(self, ctx: Context): ...

    @background.command(description="Buy a background pic for your level card")
    @Jeanne.check(is_beta_prefix)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.cooldown(1, 60, type=BucketType.user)
    async def buy(self, ctx: Context, *, name: str):
        balance = Currency(ctx.author).get_balance
        if balance == 0:
            nomoney = Embed(
                description="You have no QP.\nPlease get QP by doing `/daily`, `/guess`, `/flip` and/or `/dice`"
            )
            await ctx.send(embed=nomoney)
            return
        if balance < 1000:
            notenough = Embed(
                description="You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess`, `/flip` and/or `/dice`"
            )
            await ctx.send(embed=notenough)
            return
        try:
            Inventory.get_wallpaper(name)
        except:
            await ctx.send(
                embed=Embed(description="Unable to find wallpaper", color=Color.red())
            )
            return
        image_url = Inventory().get_wallpaper(name)[1]
        m=await ctx.send(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )
        image = await Profile(self.bot).generate_profile(ctx.author, image_url, True)
        file = File(fp=image, filename=f"preview_profile_card.png")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.random(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
        )
        view = Confirmation(ctx.author)
        m=await m.edit(
            content=None, attachments=[file], embed=preview, view=view
        )
        await view.wait()
        if view.value == None:
            await m.edit(
                content="Timeout", view=None, embed=None, attachments=[]
            )
            return
        if view.value == True:
            await Inventory(ctx.author).add_user_wallpaper(name)
            embed1 = Embed(
                description=f"Background wallpaper bought and selected",
                color=Color.random(),
            )
            await m.edit(embed=embed1, view=None)
        else:
            await m.edit(
                content="Cancelled", view=None, embed=None, attachments=[]
            )

    @buy.error
    async def buy_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already previewed this background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.send(embed=cooldown)

    @background.command(aliases=["select"],description="Select a wallpaper")
    @Jeanne.check(is_beta_prefix)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def use(self, ctx: Context, *, name: str):

        try:
            await Inventory(ctx.author).use_wallpaper(name)
            embed = Embed(description=f"{name} has been selected", color=Color.random())
            await ctx.send(embed=embed)
        except:
            embed = Embed(
                description="This background image is not in your inventory",
                color=Color.red(),
            )
            await ctx.send(embed=embed)

    buycustom = argparse.ArgumentParser(add_help=False)
    buycustom.add_argument(
        "--name",
        type=str,
        help="NAME",
        nargs="+",
        required=True,
    )
    buycustom.add_argument(
        "--link",
        type=str,
        help="LINK",
        required=True,
    )

    @background.command(
        name="buy-custom", description="Buy a custom background pic for your level card"
    )
    @Jeanne.checks.cooldown(1, 60, type=BucketType.user)
    @Jeanne.check(is_beta_prefix)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def buycustom(self, ctx: Context, *words:str, parser=buycustom):
        balance = Currency(ctx.author).get_balance
        if balance is None or balance < 1000:
            nomoney = Embed(description="You do not have enough QP.")
            await ctx.send(embed=nomoney)
            return
        try:
            parsed_args, unknown = parser.parse_known_args(words)
            name = parsed_args.name + unknown
            name = " ".join(name)
            link:str = parsed_args.link    
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
           
        m=await ctx.send(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )
        image = await Profile(self.bot).generate_profile(ctx.author, link, True)
        if image == False:
            size_error = Embed(
                description="The image is below the 900x500 size.\nPlease enlarge the image and try again"
            )
            await m.edit(content=None, embed=size_error)
            return
        file = File(fp=image, filename=f"preview_profile_card.png")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.blue(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
            .set_footer(
                text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS!"
            )
        )
        view = Confirmation(ctx.author)
        m=await m.edit(
            content=None, embed=preview, attachments=[file], view=view
        )
        await view.wait()
        if view.value:
            await Inventory(ctx.author).add_user_custom_wallpaper(name, link)
            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await m.edit(embed=embed1, view=None, attachments=[])
        else:
            await m.edit(
                content="Cancelled", embed=None, view=None, attachments=[]
            )

    @buycustom.error
    async def buycustom_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already tried to preview this background!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.send(embed=cooldown)
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
            await Message.edit(content=None, embed=embed)

    @Jeanne.command(description="Check which backgrounds you have")
    @Jeanne.check(is_beta_prefix)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def list(self, ctx: Context):

        if Inventory(ctx.author).get_user_inventory == None:
            embed = Embed(description="Your inventory is empty", color=Color.red())
            await ctx.send(embed=embed)
            return
        a = Inventory(ctx.author).get_user_inventory
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
