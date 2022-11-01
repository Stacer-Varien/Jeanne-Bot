from optparse import Option
from db_functions import check_botbanned_user
from discord import *
from discord.ext.commands import Cog, Bot, hybrid_command, Context
from requests import get
from config import *
from typing import Optional



class slashreactions(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @hybrid_command(description="Hug someone or yourself")
    async def hug(self, ctx: Context, member: Optional[Member]=None)->None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            hug_api = get(hug_nekoslife).json()
            if member == None:
                msg=f"*Hugging {ctx.author}*"
            elif member == ctx.author:
                msg = f"*Hugging {ctx.author}*"
            else:
                msg=f"*{ctx.author} hugged {member.mention}*"
            hug = Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await ctx.send(msg, embed=hug)

    @hybrid_command(description="Slap someone or yourself")
    async def slap(self, ctx: Context, member: Optional[Member]=None)->None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:        
            slap_api = get(slap_nekoslife).json()

            slap = Embed(color=0xFFC0CB)
            slap.set_footer(text="Fetched from nekos.life")
            slap.set_image(url=slap_api["url"])
            if member == None:
                msg=f"*Slapping {ctx.author}*"
            elif member==ctx.author:
                msg = f"*Slapping {ctx.author}*"
            else:
                    msg=f"*{ctx.author} slapped {member.mention}*"
            await ctx.send(msg, embed=slap)

    @hybrid_command(description="Show a smuggy look")
    async def smug(self, ctx : Context):
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            smug_api = get(smug_nekoslife).json()

            smug = Embed(color=0xFFC0CB)
            smug.set_footer(text="Fetched from nekos.life")
            smug.set_image(url=smug_api["url"])
            await ctx.send(f"*{ctx.author} is smugging*", embed=smug) 

    @hybrid_command(description="Poke someone or yourself")
    async def poke(self, ctx: Context, member: Optional[Member]=None)->None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            poke_api = get(poke_nekosfun).json()
            poke = Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.fun")
            poke.set_image(url=poke_api["image"])
            if member == None:
                    msg=f"*Poking {ctx.author}*"
            elif member == ctx.author:
                msg = f"*Poking {ctx.author}*"
            else:
                    msg=f"*{ctx.author} poked {member.mention}*"
            await ctx.send(msg, embed=poke)

    @hybrid_command(description="Pat someone or yourself")
    async def pat(self, ctx: Context, member: Optional[Member]=None)->None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            pat_api = get(pat_nekoslife).json()
            pat = Embed(color=0xFFC0CB)
            pat.set_footer(text="Fetched from nekos.life")
            pat.set_image(url=pat_api["url"])
            if member == None:
                    msg=f"*Patting {ctx.author}*"
            elif member == ctx.author:
                msg = f"*Patting {ctx.author}*"
            else:
                    msg=f"*{ctx.author} patted {member.mention}*"
            await ctx.send(msg, embed=pat)

    @hybrid_command(description="Kiss someone or yourself")
    async def kiss(self, ctx: Context, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            kiss_api = get(kiss_nekosfun).json()
            if member == None:
                msg=f"*Kissing {ctx.author}*"
            if member == ctx.author:
                msg = f"*Kissing {ctx.author}*"
            else:
                msg=f"*{ctx.author} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["image"])
            await ctx.send(msg, embed=kiss)

    @hybrid_command(description="Tickle someone or yourself")
    async def tickle(self, ctx: Context, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            tickle_api = get(tickle_nekoslife).json()
            if member == None:
                msg=f"*Tickling {ctx.author}*"
            elif member == ctx.author:
                msg = f"*Tickling {ctx.author}*"
            else:
                msg=f"*{ctx.author} tickled {member.mention}*"
            tickle = Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(msg, embed=tickle)

    @hybrid_command(description="Call someone or yourself a baka!")
    async def baka(self, ctx: Context, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            baka_api = get(baka_nekosfun).json()
            if member == None:
                msg=f"*{ctx.author}, you are a baka!*"
            elif member == ctx.author:
                msg = f"*{ctx.author}, you are a baka!*"
            else:
                msg=f"*{member}, {ctx.author.mention} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.fun")
            baka.set_image(url=baka_api['image'])
            await ctx.send(msg, embed=baka)

    @hybrid_command(description="Feed someone or yourself")
    async def feed(self, ctx: Context, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.author.id) == True:
            pass
        else:
            feed_api = get(feed_nekoslife).json()
            if member == None:
                msg = f"*Feeding {ctx.author}*"
            elif member == ctx.author:
                msg = f"*Feeding {ctx.author}*"
            else:
                msg = f"*{ctx.author} fed {member.mention}*"
            feed = Embed(color=0xFFC0CB)
            feed.set_footer(text="Fetched from nekos.life")
            feed.set_image(url=feed_api["url"])
            await ctx.send(msg, embed=feed)


async def setup(bot:Bot):
    await bot.add_cog(slashreactions(bot))
