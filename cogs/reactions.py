from config import db
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
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait=await ctx.followup.send("Sending hug")
            await wait.delete()
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
            await ctx.channel.send(msg, embed=hug)

    @jeanne_slash(description="Slap someone or yourself")
    async def slap(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to slap?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:        
            wait = await ctx.followup.send("Sending slap")
            await wait.delete()
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
            await ctx.channel.send(msg, embed=slap)

    @jeanne_slash(description="Show a smuggy look")
    async def smug(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Showing smug")
            await wait.delete()
            smug_api = get(smug_nekoslife).json()

            smug = Embed(color=0xFFC0CB)
            smug.set_footer(text="Fetched from nekos.life")
            smug.set_image(url=smug_api["url"])
            await ctx.followup.send(f"*{ctx.user} is smugging*", embed=smug) 

    @jeanne_slash(description="Poke someone or yourself")
    async def poke(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to poke?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Sending poke")
            await wait.delete()
            poke_api = get(poke_nekoslife).json()
            poke = Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.life")
            poke.set_image(url=poke_api["url"])
            if member == None:
                    msg=f"*Poking {ctx.user}*"
            elif member == ctx.user:
                msg = f"*Poking {ctx.user}*"
            else:
                    msg=f"*{ctx.user} poked {member.mention}*"
            await ctx.channel.send(msg, embed=poke)

    @jeanne_slash(description="Pat someone or yourself")
    async def pat(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to pat?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Sending headpat")
            await wait.delete()
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
            await ctx.channel.send(msg, embed=pat)

    @jeanne_slash(description="Kiss someone or yourself")
    async def kiss(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to kiss?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Giving kiss")
            await wait.delete()
            kiss_api = get(kiss_nekoslife).json()
            if member == None:
                msg=f"*Kissing {ctx.user}*"
            if member == ctx.user:
                msg = f"*Kissing {ctx.user}*"
            else:
                msg=f"*{ctx.user} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await ctx.channel.send(msg, embed=kiss)

    @jeanne_slash(description="Tickle someone or yourself")
    async def tickle(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to tickle?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Giving tickle")
            await wait.delete()
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
            await ctx.channel.send(msg, embed=tickle)

    @jeanne_slash(description="Call someone or yourself a baka!")
    async def baka(self, ctx: Interaction, member: Member = SlashOption(description="Who do you calling a baka?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Shouting baka")
            await wait.delete()
            baka_api = get(baka_nekoslife).json()
            if member == None:
                msg=f"*{ctx.user}, you are a baka!*"
            if member == ctx.user:
                msg = f"*{ctx.user}, you are a baka!*"
            else:
                msg=f"*{member.mention}, {ctx.user} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=baka_api["url"])
            await ctx.channel.send(msg, embed=baka)

    @jeanne_slash(description="Feed someone or yourself")
    async def feed(self, ctx: Interaction, *, member: Member = SlashOption(description="Who do you want to feed?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                    f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned=botbanned_data[0]

            if ctx.user.id==botbanned:
                pass
        except:
            wait = await ctx.followup.send("Giving food")
            await wait.delete()
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
            await ctx.channel.send(msg, embed=feed)


def setup(bot):
    bot.add_cog(slashreactions(bot))
