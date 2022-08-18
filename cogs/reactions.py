from assets.db_functions import check_botbanned_user
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from requests import get
from config import *



class slashreactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Hug someone or yourself")
    async def hug(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to hug?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            hug_api = get(hug_nekoslife).json()
            if member == None:
                msg=f"*Hugging {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Hugging {ctx.user}*"
            else:
                msg=f"*{ctx.user} hugged {member.mention}*"
            hug = Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await ctx.response.send_message(msg, embed=hug)

    @jeanne_slash(description="Slap someone or yourself")
    async def slap(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to slap?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:        
            slap_api = get(slap_nekoslife).json()

            slap = Embed(color=0xFFC0CB)
            slap.set_footer(text="Fetched from nekos.life")
            slap.set_image(url=slap_api["url"])
            if member == None:
                msg=f"*Slapping {ctx.user}*"
            elif member==ctx.user:
                msg = f"*Slapping {ctx.user}*"
            else:
                    msg=f"*{ctx.user} slapped {member.mention}*"
            await ctx.response.send_message(msg, embed=slap)

    @jeanne_slash(description="Show a smuggy look")
    async def smug(self, ctx : Interaction):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            smug_api = get(smug_nekoslife).json()

            smug = Embed(color=0xFFC0CB)
            smug.set_footer(text="Fetched from nekos.life")
            smug.set_image(url=smug_api["url"])
            await ctx.response.send_message(f"*{ctx.user} is smugging*", embed=smug) 

    @jeanne_slash(description="Poke someone or yourself")
    async def poke(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to poke?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            poke_api = get(poke_nekosfun).json()
            poke = Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.fun")
            poke.set_image(url=poke_api["image"])
            if member == None:
                    msg=f"*Poking {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Poking {ctx.user}*"
            else:
                    msg=f"*{ctx.user} poked {member.mention}*"
            await ctx.response.send_message(msg, embed=poke)

    @jeanne_slash(description="Pat someone or yourself")
    async def pat(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to pat?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            pat_api = get(pat_nekoslife).json()
            pat = Embed(color=0xFFC0CB)
            pat.set_footer(text="Fetched from nekos.life")
            pat.set_image(url=pat_api["url"])
            if member == None:
                    msg=f"*Patting {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Patting {ctx.user}*"
            else:
                    msg=f"*{ctx.user} patted {member.mention}*"
            await ctx.response.send_message(msg, embed=pat)

    @jeanne_slash(description="Kiss someone or yourself")
    async def kiss(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to kiss?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            kiss_api = get(kiss_nekosfun).json()
            if member == None:
                msg=f"*Kissing {ctx.user}*"
            if member == ctx.user:
                msg = f"*Kissing {ctx.user}*"
            else:
                msg=f"*{ctx.user} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["image"])
            await ctx.response.send_message(msg, embed=kiss)

    @jeanne_slash(description="Tickle someone or yourself")
    async def tickle(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to tickle?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            tickle_api = get(tickle_nekoslife).json()
            if member == None:
                msg=f"*Tickling {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Tickling {ctx.user}*"
            else:
                msg=f"*{ctx.user} tickled {member.mention}*"
            tickle = Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.response.send_message(msg, embed=tickle)

    @jeanne_slash(description="Call someone or yourself a baka!")
    async def baka(self, ctx: Interaction, member: Member = SlashOption(description="Who do you calling a baka?", required=False)):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            baka_api = get(baka_nekosfun).json()
            if member == None:
                msg=f"*{ctx.user}, you are a baka!*"
            elif member == ctx.user:
                msg = f"*{ctx.user}, you are a baka!*"
            else:
                msg=f"*{member}, {ctx.user.mention} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.fun")
            baka.set_image(url=baka_api['image'])
            await ctx.response.send_message(msg, embed=baka)

    @jeanne_slash(description="Feed someone or yourself")
    async def feed(self, ctx: Interaction, *, member: Member = SlashOption(description="Who do you want to feed?", required=False)):
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


def setup(bot):
    bot.add_cog(slashreactions(bot))
