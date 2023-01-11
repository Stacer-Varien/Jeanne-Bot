from assets.buttons import Confirmation
from db_functions import add_user_custom_wallpaper, add_user_wallpaper, check_botbanned_user, fetch_user_inventory, fetch_wallpapers, get_balance, create_user_inventory, get_wallpaper, use_wallpaper
from discord import *
from discord.ext.commands import Bot, GroupCog
from assets.generators.level_card import Level
from asyncio import get_event_loop
from functools import partial


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(description="Check all the wallpapers available")
    async def backgrounds(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            
            qp = self.bot.get_emoji(980772736861343774)
            await ctx.followup.send(embed=fetch_wallpapers(qp))

class Background_Group(GroupCog, name="background"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    def get_card(self, args):
        image = Level().generate_level(**args)
        return image

    @app_commands.command(description="Preview the inbuild background image")
    @app_commands.describe(item_id="Which background you are checking?")
    async def preview(self, ctx: Interaction, item_id: str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            qp = self.bot.get_emoji(980772736861343774)
            wallpaper = get_wallpaper(item_id)
            embed = Embed(title="Preview background")
            embed.color = Color.random()
            embed.add_field(name="Name", value=wallpaper[1], inline=True)
            embed.add_field(name="Price", value=f"1000 {qp}", inline=True)
            embed.set_image(url=wallpaper[2])
            await ctx.followup.send(embed=embed)

    @app_commands.command(description="Buy a background pic for your level card")
    @app_commands.describe(item_id="Which background you are buying?")
    async def buy(self, ctx: Interaction, item_id: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            balance: int = get_balance(ctx.user.id)

            if balance == 0:
                nomoney = Embed(
                    description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=nomoney)

            elif balance < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=notenough)

            else:
                qp = self.bot.get_emoji(980772736861343774)
                wallpaper = get_wallpaper(item_id)

                if wallpaper == None:
                    nonexist = Embed(description='Invalid item ID passed')
                    await ctx.followup.send(embed=nonexist)

                else:
                    loading = self.bot.get_emoji(1012677456811016342)
                    qp = self.bot.get_emoji(980772736861343774)
                    await ctx.followup.send("Creating preview... This will take some time {}".format(loading))
                    args = {
                        'bg_image': wallpaper[2],
             	    	'profile_image': str(ctx.user.avatar.with_format('png')),
             			        'server_level': 100,
             			        'server_user_xp': 50,
             			        'server_next_xp': 100,
                        'global_level': 100,
             			        'global_user_xp': 100,
             			        'global_next_xp': 100,
             			        'user_name': str(ctx.user),
                    }

                    func = partial(self.get_card, args)
                    image = await get_event_loop().run_in_executor(None, func)

                    file = File(fp=image, filename=f'preview_level_card.png')

                    preview = Embed(description="This is the preview of the level card.", color=Color.random()).add_field(
                        name="Cost", value=f"{wallpaper[3]} {qp}").set_footer(text="Is this the background you wanted?")
                    view = Confirmation(ctx.user)
                    await ctx.edit_original_response(content=None, attachments=[file], embed=preview, view=view)
                    await view.wait()

                    if view.value == None:
                        await ctx.edit_original_response(content="Timeout", view=None, embed=None)
                    elif view.value:
                        if create_user_inventory(ctx.user.id) == False:
                            pass
                        add_user_wallpaper(ctx.user.id, item_id)
                        embed1 = Embed(
                            description=f"Background wallpaper bought and selected", color=Color.random())
                        await ctx.edit_original_response(embed=embed1, view=None)

                    else:
                        await ctx.edit_original_response(content="Cancelled", view=None, embed=None)

    @app_commands.command(description='Select a wallpaper')
    @app_commands.describe(name="What is the name of the background?")
    async def use(self, ctx: Interaction, name: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            user_inv = fetch_user_inventory(ctx.user.id)

            if f'{name}.png' in user_inv:
                use_wallpaper(name, ctx.user.id)
                embed = Embed(
                    description=f"{name} has been selected", color=Color.random())
                await ctx.followup.send(embed=embed)
            else:
               embed = Embed(
                   description="This background image is not in your inventory", color=Color.red())
               await ctx.followup.send(embed=embed)

    @app_commands.command(description="Buy a custom background pic for your level card")
    @app_commands.describe(name="What will you name it?", link="Add an image link")
    async def buycustom(self, ctx: Interaction, name: str, link: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            balance = get_balance(ctx.user.id)

            if balance == None:
                nomoney = Embed(
                    description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=nomoney)

            elif int(balance) < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=notenough)

            else:
                loading = self.bot.get_emoji(1012677456811016342)
                qp = self.bot.get_emoji(980772736861343774)
                await ctx.followup.send("Creating preview... This will take some time {}".format(loading))

                args = {'bg_image': link, 'profile_image': str(ctx.user.avatar.with_format('png')), 'server_level': 100, 'server_user_xp': 50,
                        'server_next_xp': 100, 'global_level': 100, 'global_user_xp': 100, 'global_next_xp': 100, 'user_name': str(ctx.user), }

                func = partial(self.get_card, args)
                image = await get_event_loop().run_in_executor(None, func)

                file = File(
                    fp=image, filename='preview_level_card.png')

                preview = Embed(description="This is the preview of the level card.", color=Color.blue()).add_field(name="Cost", value=f"1000 {qp}").set_footer(
                    text="Is this the background you wanted?").set_footer(text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS!")
                view = Confirmation(ctx.user)
                await ctx.edit_original_response(content=None, embed=preview, attachments=[file], view=view)
                await view.wait()
                
                if view.value == None:
                    await ctx.edit_original_response(content="Time out", embed=None, view=None)
                if view.value:
                    if create_user_inventory(ctx.user.id) == False:
                        pass
                    else:
                        create_user_inventory(ctx.user.id)
                    add_user_custom_wallpaper(ctx.user.id, name, link)

                    embed1 = Embed(
                        description="Background wallpaper bought and selected", color=Color.random())
                    await ctx.edit_original_response(embed=embed1, view=None)

                else:
                    await ctx.edit_original_response(content="Cancelled", embed=None, view=None)


    @app_commands.command(description='Check which backgrounds you have')
    async def list(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            try:
                a = fetch_user_inventory(ctx.user.id)
                inv = Embed(title="List of wallpapers you have",
                            color=Color.random())
                inv.description = a
                await ctx.followup.send(embed=inv)
            except FileNotFoundError:
                embed = Embed(
                    description="Your inventory is empty", color=Color.red())
                await ctx.followup.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))
