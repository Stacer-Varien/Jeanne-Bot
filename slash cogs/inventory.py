from cgitb import text
from typing import Optional
from assets.buttons import Confirmation
from db_functions import add_user_custom_wallpaper, add_user_wallpaper, check_botbanned_user, fetch_user_inventory, fetch_wallpapers, get_balance, create_user_inventory, get_wallpaper, use_wallpaper
from discord import *
from discord.ext.commands import Cog, Bot, Context, hybrid_group
from assets.generators.level_card import Level
from asyncio import get_event_loop
from functools import partial
import requests


class inventory(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    def get_card(self, args):
        image = Level().generate_level(**args)
        return image

    @hybrid_group(description="Check what items is available in the shop", fallback='items')
    async def shop(self, ctx:Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:        
            embed = Embed(title="Available items in the shop:",
                          description="• Backgrounds", color=ctx.author.color).set_footer(text='For now, it is only one type of item that can be bought')
            await ctx.send(embed=embed)


    @shop.command(description="Check all the wallpapers available", aliases=['bgs'])
    async def background(self, ctx:Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            qp = self.bot.get_emoji(980772736861343774)
            await ctx.send(embed=fetch_wallpapers(qp))

    @hybrid_group(description='Main background command', aliases=['bg'])
    async def background(self, ctx: Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            embed = Embed(title="This is a group command. However, the available commands are:",
                          description="`background list`\n`background preview\n`background buy`\n`background buy custom\n`background use`", color=ctx.author.color)
            await ctx.send(embed=embed)

    @background.command(description="Preview the background image", aliases=['show'])
    async def preview(self, ctx: Context, item_id):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            qp = self.bot.get_emoji(980772736861343774)
            wallpaper = get_wallpaper(item_id)
            embed=Embed(title="Preview backgorund")
            embed.color=ctx.author.color
            embed.add_field(name="Name", value=wallpaper[1], inline=True)
            embed.add_field(name="Price", value=f"1000 {qp}", inline=True)
            embed.set_image(url=wallpaper[2])
            await ctx.send(embed=embed)


    @background.command(description="Buy a background pic for your level card")
    async def buy(self, ctx:Context, item_id):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            balance = get_balance(ctx.author.id)
            

            if int(balance) == 0:
                nomoney = Embed(description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.send(embed=nomoney)
            
            elif int(balance) < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.send(embed=notenough)

            else:
                qp = self.bot.get_emoji(980772736861343774)
                wallpaper=get_wallpaper(item_id)
                        
                if wallpaper == None:
                    nonexist=Embed(description='Invalid item ID passed')
                    await ctx.send(embed=nonexist)

                else:

                    args = {
                        'level_card': wallpaper[2],
             	    	'profile_image': str(ctx.author.avatar.with_format('png')),
     			        'server_level': 100,
     			        'server_user_xp': 50,
     			        'server_next_xp': 100,
                        'global_level': 100,
     			        'global_user_xp': 100,
     			        'global_next_xp': 100,
     			        'user_name': str(ctx.author),
                        }

                    func = partial(self.get_card, args)
                    image = await get_event_loop().run_in_executor(None, func)

                    file = File(fp=image, filename=f'preview_level_card.png')

                    preview=Embed(description="This is the preview of the level card.", color=Color.blue()).add_field(name="Cost", value=f"{wallpaper[3]} {qp}").set_footer(text="Is this the background you wanted?")
                    view=Confirmation()
                    await ctx.send(file=file, embed=preview, view=view)
                    await view.wait()

                    if view.value is None:
                        await ctx.send("Timeout")
                    elif view.value is True:
                        if create_user_inventory(ctx.author.id) == False:
                            pass
                        add_user_wallpaper(ctx.author.id, item_id)
                        embed1 = Embed(description=f"Background wallpaper bought and selected",color=Color.blue())
                        await ctx.send(embed=embed1)

                    elif view.value is False:
                        await ctx.send("Cancelled")
                    
    @background.command(description='Select a wallpaper', aliases=['select', 'pick'])
    async def use(self, ctx:Context, name:str):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            user_inv=fetch_user_inventory(ctx.author.id)

            if f'{name}.png' in user_inv:
                use_wallpaper(name, ctx.author.id)
                embed=Embed(description=f"{name} has been selected", color=ctx.author.color)
                await ctx.send(embed=embed)
            else:
               embed = Embed(
                   description="This background image is not in your inventory", color=Color.red())
               await ctx.send(embed=embed)

    @background.command(description="Buy a custom background pic for your level card", aliases=['buy custom', 'custom'])
    async def buy_custom(self, ctx:Context, name:str, *,link:Optional[str]=None, attachment:Optional[Attachment]=None)->None:
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            balance=get_balance(ctx.author.id)
            
            if balance == None:
                nomoney = Embed(description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.send(embed=nomoney)
            
            elif int(balance) < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.send(embed=notenough)
            
            elif attachment and link ==None:
                nothing = Embed(
                    description='There is no link or attachment...\nPlease add a valid image link or attachement')
                await ctx.send(embed=nothing)

            else:
                if not attachment:
                    link=link

                if not link:
                    link=attachment.url

                alert="""
Before you buy a custom background picture, did you make sure the image is:

    1. A valid image URL
    2. Not crossing NSFW borderline
    3. Does not contain any lewded characters and/or lolis
    4. Is not sexualised in some way
    5. Does not violate ToS and/or contains TW slurs
    6. The name you set for it also does not violate ToS and/or contains TW slurs
    7. The image's resolution is at a 9:5 ratio and at least 900x500 for better quality.

If you feel that the image fits the above or not, click one of the buttons to continue
"""
                view=Confirmation()
                confirm = Embed(description=alert, color=ctx.author.color)
                await ctx.send(embed=confirm, view=view)
                await view.wait()
                if view.value == True:
                    
                    qp = self.bot.get_emoji(980772736861343774)                    
                    if requests.get(link).status_code == 200:
                        async with ctx.typing():
                            args = {
                                'level_card': link,
                                'profile_image': str(ctx.author.avatar.with_format('png')),
                                'server_level': 100,
                                'server_user_xp': 50,
                                'server_next_xp': 100,
                                'global_level': 100,
                                'global_user_xp': 100,
                                'global_next_xp': 100,
                                'user_name': str(ctx.author),
                            }

                            func = partial(self.get_card, args)
                            image = await get_event_loop().run_in_executor(None, func)

                            file = File(fp=image, filename='preview_level_card.png')

                            preview = Embed(description="This is the preview of the level card.", color=Color.blue()).add_field(name="Cost", value=f"1000 {qp}").set_footer(
                                text="Is this the background you wanted?").set_footer(text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS!")
                            view=Confirmation()
                        await ctx.send(content=None, file=file, embed=preview, view=view)
                        await view.wait()

                        if view.value is None:
                            await ctx.send(content="Time out", view=None)
                        elif view.value is True:
                            add_user_custom_wallpaper(ctx.author.id, name, link)

                            embed1 = Embed(
                                description=f"Background wallpaper bought and selected.", color=Color.blue())
                            await ctx.send(embed=embed1, view=None)

                        elif view.value is False:
                            await ctx.send(content="Cancelled", embed=None, view=None)
                elif view.value == False:
                    check = Embed(description="Please try to sort out the image first and try again", color=Color.blue())
                    await ctx.send(view=None, embed=check)
                elif view.value == None:
                    await ctx.send(content="Time out", embed=None, view=None)
           
    @background.command(description='Check which backgrounds you have', aliases=['inv', 'inventory'])
    async def list(self, ctx: Context):
        await ctx.defer()
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            try:
                a = fetch_user_inventory(ctx.author.id)
                inv=Embed(title="List of wallpapers you have",color=Color.blue())
                inv.description = "\n".join(a)
                await ctx.send(embed=inv)
            except FileNotFoundError:
                embed=Embed(description="Your inventory is empty", color=Color.red())
                await ctx.send(embed=embed)

               
async def setup(bot:Bot):
    await bot.add_cog(inventory(bot))
