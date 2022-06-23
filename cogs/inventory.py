from config import inv_db, db
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from assets.levelcard.generator import Generator
from asyncio import get_event_loop
from functools import partial
from sqlite3 import connect


class Confirm(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        def is_author():
            return ctx.user
        
        if is_author:
            self.value = True
            button.disabled=True
            self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @ui.button(label="Cancel", style=ButtonStyle.grey)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        def is_author():
            return ctx.user
        
        if is_author:
            self.value = False
            button.disabled = True
            self.stop()


class inventory(Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_card(self, args):
        image = Generator().generate_profile(**args)
        return image

    @jeanne_slash(description="Main shop command")
    async def shop(self, ctx:Interaction):
        pass

    @shop.subcommand(description="Check all the wallpapers available")
    async def background(self, ctx:Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            w=inv_db.execute("SELECT * FROM wallpapers").fetchall()

            backgrounds=Embed(title='Avaliable Background Pictures for Level Cards', color=Color.blue()).set_footer(text="To view them, click on the hyperlinked names")

            for a in w:
                backgrounds.add_field(name=f"{a[1]}", value='[Item ID: {}]({})'.format(a[0], a[2]), inline=True)


            await ctx.followup.send(embed=backgrounds)

    @shop.subcommand(description="Buy a background pic for your level card")
    async def buy_background(self, ctx:Interaction, item_id):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            balance=db.execute("SELECT amount FROM bankData WHERE user_id = ?", (ctx.user.id,)).fetchone()
            

            if balance == None:
                nomoney = Embed(description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=nomoney)
            
            elif int(balance[0]) < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=notenough)

            else:
                qp = self.bot.get_emoji(980772736861343774)
                wallpaper = inv_db.execute(
                    'SELECT * FROM wallpapers WHERE id = ?', (item_id,)).fetchone()
                        
                if wallpaper == None:
                    nonexist=Embed(description='Invalid item ID passed')
                    await ctx.followup.send(embed=nonexist)

                else:

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

                    preview=Embed(description="This is the preview of the level card.", color=Color.blue()).add_field(name="Cost", value=f"{wallpaper[3]} {qp}").set_footer(text="Is this the background you wanted?")
                    view=Confirm()
                    await ctx.followup.send(file=file, embed=preview, view=view)
                    await view.wait()

                    if view.value is None:
                        pass
                    elif view.value is True:
                        user_inv=connect("./User_Inventories/{}.db".format(ctx.user.id))
                        cur=user_inv.cursor()
                        cur.execute("CREATE TABLE IF NOT EXISTS backgrounds (item_id int, link_bg text, selected int)")
                        cur.execute("INSERT OR IGNORE INTO backgrounds (item_id, link_bg, selected) VALUES (?,?,?)", (item_id, wallpaper[2], 0,))
                        user_inv.commit()

                        db.execute("UPDATE bankData SET amount = amount - ? WHERE user_id = ?", (1000, ctx.user.id,))
                        db.commit()

                        embed1 = Embed(description="Background wallpaper bought. Don't forget to use `/use ITEM_ID` to set it",color=Color.blue())
                        await ctx.followup.send(embed=embed1)

                    elif view.value is False:
                        await ctx.followup.send("Cancelled")
    
    @jeanne_slash(description='Use a background picture')
    async def use(self, ctx:Interaction, item_id):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            user_inv = connect("./User_Inventories/{}.db".format(ctx.user.id))
            cur = user_inv.cursor()
            try:
                a=cur.execute("SELECT item_id FROM backgrounds").fetchall()

                if a == None:
                    await ctx.followup.send("Invalid item ID passed")
                
                else:
                    for b in a:
                        cur.execute("UPDATE backgrounds SET selected = ? WHERE item_id = ?", (0, b[0]))
                    
                
                    cur.execute("UPDATE backgrounds SET selected = ? WHERE item_id = ?", (1, item_id,))
                
                    user_inv.commit()

                    await ctx.followup.send("Background selected")
            except:
                await ctx.followup.send("You have no items in your inventory")




def setup(bot):
    bot.add_cog(inventory(bot))
