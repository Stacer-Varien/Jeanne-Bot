from assets.components import Confirmation
from functions import Botban, Currency, Inventory
from discord import Color, Embed, File, Interaction, app_commands as Jeanne
from discord.ext.commands import Bot, GroupCog
from assets.generators.level_card import Level
from asyncio import get_event_loop
from functools import partial


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(description="Check all the wallpapers available")
    async def backgrounds(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return
        await ctx.followup.send(embed=Inventory().fetch_wallpapers())


class Background_Group(GroupCog, name="background"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    def get_card(self, args):
        image = Level().generate_level(**args)
        return image

    @Jeanne.command(description="Preview the inbuild background image")
    @Jeanne.describe(item_id="Which background you are checking?")
    async def preview(self, ctx: Interaction, item_id: str):
        if Botban(ctx.user).check_botbanned_user():
            return

        await ctx.response.defer()
        wallpaper = Inventory().get_wallpaper(item_id)
        embed = Embed(title="Preview background")
        embed.color = Color.random()
        embed.add_field(name="Name", value=wallpaper[1], inline=True)
        embed.add_field(name="Price", value="1000 <:quantumpiece:980772736861343774>", inline=True)
        embed.set_image(url=wallpaper[2])
        await ctx.followup.send(embed=embed)

    @preview.error
    async def preview_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError):
            if TypeError:
                embed = Embed()
                embed.description = "Invalid item ID given"
                embed.color = Color.red()
                await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Buy a background pic for your level card")
    @Jeanne.describe(item_id="Which background you are buying?")
    async def buy(self, ctx: Interaction, item_id: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return

        balance: int = Currency(ctx.user).get_balance()

        if balance == 0:
            nomoney = Embed(
                description="You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=nomoney)

        elif balance < 1000:
            notenough = Embed(
                description="You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=notenough)

        else:
            qp = self.bot.get_emoji(980772736861343774)
            wallpaper = Inventory().get_wallpaper(item_id)

            if wallpaper == None:
                nonexist = Embed(description="Invalid item ID passed")
                await ctx.followup.send(embed=nonexist)

            else:
                loading = self.bot.get_emoji(1012677456811016342)
                qp = self.bot.get_emoji(980772736861343774)
                await ctx.followup.send(
                    "Creating preview... This will take some time {}".format(loading)
                )
                args = {
                    "bg_image": wallpaper[2],
                    "profile_image": str(ctx.user.avatar.with_format("png")),
                    "server_level": 100,
                    "server_user_xp": 50,
                    "server_next_xp": 100,
                    "global_level": 100,
                    "global_user_xp": 100,
                    "global_next_xp": 100,
                    "user_name": str(ctx.user),
                }

                func = partial(self.get_card, args)
                image = await get_event_loop().run_in_executor(None, func)

                file = File(fp=image, filename=f"preview_level_card.png")

                preview = (
                    Embed(
                        description="This is the preview of the level card.",
                        color=Color.random(),
                    )
                    .add_field(name="Cost", value=f"{wallpaper[3]} {qp}")
                    .set_footer(text="Is this the background you wanted?")
                )
                view = Confirmation(ctx.user)
                await ctx.edit_original_response(
                    content=None, attachments=[file], embed=preview, view=view
                )
                await view.wait()

                if view.value == None:
                    await ctx.edit_original_response(
                        content="Timeout", view=None, embed=None
                    )
                elif view.value == True:
                    Inventory(ctx.user).add_user_wallpaper(item_id)
                    embed1 = Embed(
                        description=f"Background wallpaper bought and selected",
                        color=Color.random(),
                    )
                    await ctx.edit_original_response(embed=embed1, view=None)

                else:
                    await ctx.edit_original_response(
                        content="Cancelled", view=None, embed=None
                    )

    @Jeanne.command(description="Select a wallpaper")
    @Jeanne.describe(name="What is the name of the background?")
    async def use(self, ctx: Interaction, name: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return

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

    @Jeanne.command(description="Buy a custom background pic for your level card")
    @Jeanne.describe(name="What will you name it?", link="Add an image link")
    async def buycustom(self, ctx: Interaction, name: str, link: str):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return

        balance = Currency(ctx.user).get_balance()

        if balance == None:
            nomoney = Embed(
                description="You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=nomoney)

        elif int(balance) < 1000:
            notenough = Embed(
                description="You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`"
            )
            await ctx.followup.send(embed=notenough)

        else:
            loading = self.bot.get_emoji(1012677456811016342)
            qp = self.bot.get_emoji(980772736861343774)
            await ctx.followup.send(
                "Creating preview... This will take some time {}".format(loading)
            )

            args = {
                "bg_image": link,
                "profile_image": str(ctx.user.avatar.with_format("png")),
                "server_level": 100,
                "server_user_xp": 50,
                "server_next_xp": 100,
                "global_level": 100,
                "global_user_xp": 100,
                "global_next_xp": 100,
                "user_name": str(ctx.user),
            }

            func = partial(self.get_card, args)
            image = await get_event_loop().run_in_executor(None, func)

            file = File(fp=image, filename="preview_level_card.png")

            preview = (
                Embed(
                    description="This is the preview of the level card.",
                    color=Color.blue(),
                )
                .add_field(name="Cost", value=f"1000 {qp}")
                .set_footer(text="Is this the background you wanted?")
                .set_footer(
                    text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS!"
                )
            )
            view = Confirmation(ctx.user)
            await ctx.edit_original_response(
                content=None, embed=preview, attachments=[file], view=view
            )
            await view.wait()

            if view.value == None:
                await ctx.edit_original_response(
                    content="Time out", embed=None, view=None
                )
            elif view.value == True:
                Inventory(ctx.user).add_user_custom_wallpaper(name, link)

                embed1 = Embed(
                    description="Background wallpaper bought and selected",
                    color=Color.random(),
                )
                await ctx.edit_original_response(embed=embed1, view=None)

            else:
                await ctx.edit_original_response(
                    content="Cancelled", embed=None, view=None
                )

    @Jeanne.command(description="Check which backgrounds you have")
    async def list(self, ctx: Interaction):
        await ctx.response.defer()
        if Botban(ctx.user).check_botbanned_user():
            return

        if Inventory(ctx.user).fetch_user_inventory() == None:
            embed = Embed(description="Your inventory is empty", color=Color.red())
            await ctx.followup.send(embed=embed)
        else:
            a = Inventory(ctx.user).fetch_user_inventory()
            inv = Embed(title="List of wallpapers you have", color=Color.random())
            inv.description = ""
            for data in a:
                inv.description += f"[{data[1]}]({data[2]})\n"
            await ctx.followup.send(embed=inv)


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))
