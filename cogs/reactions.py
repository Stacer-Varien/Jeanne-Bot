from db_functions import check_botbanned_user
from discord import *
from discord.ext.commands import Cog, Bot
from requests import get
from config import *
from typing import Optional


class slashreactions(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Hug someone or yourself")
    @app_commands.describe(member="Who are you hugging?")
    async def hug(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            hug_api = get(hug_nekoslife).json()
            if member == None:
                msg = f"*Hugging {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Hugging {ctx.user}*"
            else:
                msg = f"*{ctx.user} hugged {member.mention}*"
            hug = Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await ctx.response.send_message(msg, embed=hug)

    @app_commands.command(description="Slap someone or yourself")
    @app_commands.describe(member="Who are you slapping?")
    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            slap_api = get(slap_nekoslife).json()

            slap = Embed(color=0xFFC0CB)
            slap.set_footer(text="Fetched from nekos.life")
            slap.set_image(url=slap_api["url"])
            if member == None:
                msg = f"*Slapping {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Slapping {ctx.user}*"
            else:
                msg = f"*{ctx.user} slapped {member.mention}*"
            await ctx.response.send_message(msg, embed=slap)

    @app_commands.command(description="Show a smuggy look")
    async def smug(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            smug_api = get(smug_nekoslife).json()

            smug = Embed(color=0xFFC0CB)
            smug.set_footer(text="Fetched from nekos.life")
            smug.set_image(url=smug_api["url"])
            await ctx.response.send_message(f"*{ctx.user} is smugging*", embed=smug)

    @app_commands.command(description="Poke someone or yourself")
    @app_commands.describe(member="Who are you poking?")
    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            poke_api = get(poke_nekosfun).json()
            poke = Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.fun")
            poke.set_image(url=poke_api["image"])
            if member == None:
                msg = f"*Poking {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Poking {ctx.user}*"
            else:
                msg = f"*{ctx.user} poked {member.mention}*"
            await ctx.response.send_message(msg, embed=poke)

    @app_commands.command(description="Pat someone or yourself")
    @app_commands.describe(member="Who are you patting?")
    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            pat_api = get(pat_nekoslife).json()
            pat = Embed(color=0xFFC0CB)
            pat.set_footer(text="Fetched from nekos.life")
            pat.set_image(url=pat_api["url"])
            if member == None:
                msg = f"*Patting {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Patting {ctx.user}*"
            else:
                msg = f"*{ctx.user} patted {member.mention}*"
            await ctx.response.send_message(msg, embed=pat)

    @app_commands.command(description="Kiss someone or yourself")
    @app_commands.describe(member="Who are you kissing?")
    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            kiss_api = get(kiss_nekosfun).json()
            if member == None:
                msg = f"*Kissing {ctx.user}*"
            if member == ctx.user:
                msg = f"*Kissing {ctx.user}*"
            else:
                msg = f"*{ctx.user} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["image"])
            await ctx.response.send_message(msg, embed=kiss)

    @app_commands.command(description="Tickle someone or yourself")
    @app_commands.describe(member="Who are you tickling?")
    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            tickle_api = get(tickle_nekoslife).json()
            if member == None:
                msg = f"*Tickling {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Tickling {ctx.user}*"
            else:
                msg = f"*{ctx.user} tickled {member.mention}*"
            tickle = Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.response.send_message(msg, embed=tickle)

    @app_commands.command(description="Call someone or yourself a baka!")
    @app_commands.describe(member="Who are you calling a baka?")
    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            baka_api = get(baka_nekosfun).json()
            if member == None:
                msg = f"*{ctx.user}, you are a baka!*"
            elif member == ctx.user:
                msg = f"*{ctx.user}, you are a baka!*"
            else:
                msg = f"*{member}, {ctx.user.mention} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.fun")
            baka.set_image(url=baka_api['image'])
            await ctx.response.send_message(msg, embed=baka)

    @app_commands.command(description="Feed someone or yourself")
    @app_commands.describe(member="Who are you feeding?")
    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            feed_api = get(feed_nekoslife).json()
            if member == None:
                msg = f"*Feeding {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Feeding {ctx.user}*"
            else:
                msg = f"*{ctx.user} fed {member.mention}*"
            feed = Embed(color=0xFFC0CB)
            feed.set_footer(text="Fetched from nekos.life")
            feed.set_image(url=feed_api["url"])
            await ctx.response.send_message(msg, embed=feed)

    @app_commands.command(description="Make yourself cry")
    async def cry(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            cry_api = get(cry_purrbot).json()

            cry = Embed(color=0xFFC0CB)
            cry.set_footer(text="Fetched from PurrBot.site")
            cry.set_image(url=cry_api["link"])
            await ctx.response.send_message(f"*{ctx.user} is crying*", embed=cry)

    @app_commands.command(description="Bite someone or yourself")
    @app_commands.describe(member="Who are you biting?")
    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            bite_api = get(bite_purrbot).json()
            if member == None:
                msg = f"*Biting {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Biting {ctx.user}*"
            else:
                msg = f"*{ctx.user} bit {member.mention}*"
            bite = Embed(color=0xFFC0CB)
            bite.set_footer(text="Fetched from PurrBot.site")
            bite.set_image(url=bite_api["link"])
            await ctx.response.send_message(msg, embed=bite)

    @app_commands.command(description="Make yourself blush")
    async def blush(self, ctx: Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            blush_api = get(blush_purrbot).json()

            blush = Embed(color=0xFFC0CB)
            blush.set_footer(text="Fetched from PurrBot.site")
            blush.set_image(url=blush_api["link"])
            await ctx.response.send_message(f"*{ctx.user} is blushing*", embed=blush)

    @app_commands.command(description="Cuddle with someone or yourself")
    @app_commands.describe(member="Who are you cuddling?")
    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            cuddle_api = get(cuddle_purrbot).json()
            if member == None:
                msg = f"*Cuddling with {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Cuddling with {ctx.user}*"
            else:
                msg = f"*{ctx.user} cuddled with {member.mention}*"
            cuddle = Embed(color=0xFFC0CB)
            cuddle.set_footer(text="Fetched from PurrBot.site")
            cuddle.set_image(url=cuddle_api["link"])
            await ctx.response.send_message(msg, embed=cuddle)

    @app_commands.command(description="Dance with someone or yourself")
    @app_commands.describe(member="Who are you dancing with?")
    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            dance_api = get(dance_purrbot).json()
            if member == None:
                msg = f"*{ctx.user} is dancing*"
            elif member == ctx.user:
                msg = f"*{ctx.user} is dancing*"
            else:
                msg = f"*{ctx.user} is dancing with {member.mention}*"
            dance = Embed(color=0xFFC0CB)
            dance.set_footer(text="Fetched from PurrBot.site")
            dance.set_image(url=dance_api["link"])
            await ctx.response.send_message(msg, embed=dance)

async def setup(bot: Bot):
    await bot.add_cog(slashreactions(bot))
