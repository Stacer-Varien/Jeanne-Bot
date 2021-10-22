import discord, requests
from discord.ext import commands
from discord import Member, Embed
from discord_slash import cog_ext, SlashContext

class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Hug someone or yourself")
    async def hug(self, ctx:SlashContext, member : Member = None):
            hug_api = requests.get("https://nekos.life/api/v2/img/hug").json()
            if member == None:
                msg=f"*Hugging {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} hugged {member.mention}*"
            hug = discord.Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await ctx.send(msg, embed=hug)

    @cog_ext.cog_slash(description="Slap someone or yourself")
    async def slap(self, ctx:SlashContext, member: Member = None):
        slap_api = requests.get("https://nekos.life/api/v2/img/slap").json()

        slap = discord.Embed(color=0xFFC0CB)
        slap.set_footer(text="Fetched from nekos.life")
        slap.set_image(url=slap_api["url"])
        if member == None:
                msg=f"*Slapping {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} slapped {member.mention}*"
        await ctx.send(msg, embed=slap)

    @cog_ext.cog_slash(description="Show a smuggy look")
    async def smug(self, ctx:SlashContext):
        smug_api = requests.get("https://nekos.life/api/v2/img/smug").json()

        smug = discord.Embed(color=0xFFC0CB)
        smug.set_footer(text="Fetched from nekos.life")
        smug.set_image(url=smug_api["url"])
        await ctx.send(f"*{ctx.author.mention} is smugging*", embed=smug) 

    @cog_ext.cog_slash(description="Poke someone or yourself")
    async def poke(self, ctx:SlashContext, member: Member = None):
        poke_api = requests.get("https://nekos.life/api/v2/img/poke").json()
        poke = discord.Embed(color=0xFFC0CB)
        poke.set_footer(text="Fetched from nekos.life")
        poke.set_image(url=poke_api["url"])
        if member == None:
                msg=f"*Poking {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} poked {member.mention}*"
        await ctx.send(msg, embed=poke)

    @cog_ext.cog_slash(description="Pat someone or yourself")
    async def pat(self, ctx:SlashContext, member: Member = None):
        pat_api = requests.get("https://nekos.life/api/v2/img/pat").json()
        pat = discord.Embed(color=0xFFC0CB)
        pat.set_footer(text="Fetched from nekos.life")
        pat.set_image(url=pat_api["url"])
        if member == None:
                msg=f"*Patting {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} patted {member.mention}*"
        await ctx.send(msg, embed=pat)

    @cog_ext.cog_slash(description="Kiss someone or yourself")
    async def kiss(self, ctx:SlashContext, member: Member = None):
            kiss_api = requests.get("https://nekos.life/api/v2/img/kiss").json()
            if member == None:
                msg=f"*Kissing {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} kissed {member.mention}*"
            kiss = discord.Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await ctx.send(msg, embed=kiss)

    @cog_ext.cog_slash(description="Tickle someone or yourself")
    async def tickle(self, ctx:SlashContext, member: Member = None):
            tickle_api = requests.get("https://nekos.life/api/v2/img/tickle").json()
            if member == None:
                msg=f"*Tickling {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} kissed {member.mention}*"
            tickle = discord.Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(msg, embed=tickle)

    @cog_ext.cog_slash(description="Call someone or yourself a baka!")
    async def baka(self, ctx:SlashContext, member: Member = None):
            baka_api = requests.get("https://nekos.life/api/v2/img/baka").json()
            if member == None:
                msg=f"*{ctx.author.mention}, you are a baka!*"
            else:
                msg=f"*{member.mention}, {ctx.author.mention} called you a baka!*"
            baka = discord.Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=baka_api["url"])
            await ctx.send(msg, embed=baka)

    @cog_ext.cog_slash(description="Feed someone or yourself")
    async def feed(self, ctx, *, member: Member = None):
        feed_api = requests.get("https://nekos.life/api/v2/img/feed").json()
        if member == None:
            msg = f"*Feeding {ctx.author.mention}*"
        else:
            msg = f"*{ctx.author.mention} fed {member.mention}*"
        feed = Embed(color=0xFFC0CB)
        feed.set_footer(text="Fetched from nekos.life")
        feed.set_image(url=feed_api["url"])
        await ctx.send(msg, embed=feed)


def setup(bot):
    bot.add_cog(reactions(bot))
