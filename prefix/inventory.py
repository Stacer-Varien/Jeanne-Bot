from assets.components import Confirmation, buy_function_context, use_function_context
from functions import (
    Currency,
    Inventory,
    check_botbanned_prefix,
    check_disabled_prefixed_command,
)
from discord import ButtonStyle, Color, Embed, File
from PIL import UnidentifiedImageError
from discord.ext.commands import Bot, Context, BucketType, Cog
import discord.ext.commands as Jeanne
from assets.generators.profile_card import Profile
from requests import exceptions
from reactionmenu import ViewButton, ViewMenu
from assets.argparsers import inv_parser


class InvPrefix(Cog, name="Inventory"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Jeanne.group(
        name="shop", description="Main shop command", invoke_without_command=True
    )
    async def shop(self, ctx: Context): ...

    @shop.command(
        aliases=["bgs", "bg"], description="Check all the wallpapers available"
    )
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    @Jeanne.cooldown(1, 60, type=BucketType.user)
    async def backgrounds(self, ctx: Context):
        disabled = False
        balance = Currency(ctx.author).get_balance
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
            await buy_function_context(
                self.bot, ctx, menu.last_viewed.embed.title, menu.message
            )
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

    @Jeanne.group(
        aliases=["bg"],
        name="background",
        description="Main background command",
        invoke_without_command=True,
    )
    async def background(self, ctx: Context): ...

    @backgrounds.error
    async def backgrounds_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already previewed this background!\nTry again after `{
                    round(error.retry_after, 2)} seconds`",
                color=Color.random(),
            )
            await ctx.send(embed=cooldown)

    @background.command(
        aliases=["custom"],
        name="buy-custom",
        description="Buy a custom background pic for your level card",
    )
    @Jeanne.cooldown(1, 60, type=BucketType.user)
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def buycustom(self, ctx: Context, *words: str, parser=inv_parser):
        balance = Currency(ctx.author).get_balance
        if balance is None or balance < 1000:
            nomoney = Embed(description="You do not have enough QP.")
            await ctx.send(embed=nomoney)
            return
        try:
            parsed_args,  = parser.parse_known_args(words)[0]
            name = None if parsed_args.name == None else " ".join(
                parsed_args.name)
            link: str = None if parsed_args.link == None else parsed_args.link
        except SystemExit:
            await ctx.send(
                embed=Embed(
                    description=f"You are missing some arguments or using incorrect arguments for this command",
                    color=Color.red(),
                )
            )
            return
        if link == None:
            await ctx.send(embed=Embed(description="You didn't add a link. Please try again later", color=Color.red()))
        m = await ctx.send(embed=Embed(description="Creating preview... This will take some time <a:loading:1161038734620373062>")
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
                text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS and without warning!"
            )
        )
        view = Confirmation(ctx.author)
        m = await m.edit(content=None, embed=preview, attachments=[file], view=view)
        await view.wait()
        if view.value:
            await Inventory(ctx.author).add_user_custom_wallpaper(name, link)
            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await m.edit(embed=embed1, view=None, attachments=[])
            return
        await m.edit(embed=Embed(description="Cancel"), view=None, attachments=[])

    @buycustom.error
    async def buycustom_error(self, ctx: Context, error: Jeanne.CommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            cooldown = Embed(
                description=f"You have already tried to preview this background!\nTry again after `{
                    round(error.retry_after, 2)} seconds`",
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
            await ctx.message.edit(content=None, embed=embed)

    @background.command(description="Check which backgrounds you have")
    @Jeanne.check(check_botbanned_prefix)
    @Jeanne.check(check_disabled_prefixed_command)
    async def list(self, ctx: Context):
        if Inventory(ctx.author).get_user_inventory == None:
            embed = Embed(description="Your inventory is empty",
                          color=Color.red())
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
            page_embed = Embed(title=str(wallpaper[1]), color=embed.color)
            page_embed.set_image(url=str(wallpaper[2]))
            menu.add_page(embed=page_embed)

        async def use_callback():
            await use_function_context(ctx, menu.last_viewed.embed.title, menu.message)
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


async def setup(bot: Bot):
    await bot.add_cog(InvPrefix(bot))
