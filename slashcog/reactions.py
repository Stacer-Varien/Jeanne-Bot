import discord
from discord.ext import commands
import requests
from discord import Member
from discord_slash import cog_ext, SlashContext

class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Hug someone or yourself")
    async def hug(self, ctx:SlashContext, member : Member = None):
        hug_api = requests.get("https://nekos.life/api/v2/img/hug").json()

        if member == None:
            hugs = discord.Embed(color=0xFFC0CB)
            hugs.set_footer(text="Fetched from nekos.life")
            hugs.set_image(url=hug_api["url"])
            await ctx.send(f"*Hugging {ctx.author.mention}* :people_hugging:", embed=hugs)

        else:
            hugs = discord.Embed(color=0xFFC0CB)
            hugs.set_footer(text="Fetched from nekos.life")
            hugs.set_image(url=hug_api["url"])
            await ctx.send(f"*{ctx.author.mention} hugged {member.name}* :people_hugging:", embed=hugs)

    @cog_ext.cog_slash(description="Slap someone or yourself")
    async def slap(self, ctx:SlashContext, member: Member = None):
        slap_api = requests.get("https://nekos.life/api/v2/img/slap").json()

        if member == None:
            slap = discord.Embed(color=0xFFC0CB)
            slap.set_footer(text="Fetched from nekos.life")
            slap.set_image(url=slap_api["url"])
            await ctx.send(f"*Slapping {ctx.author.mention}*", embed=slap)

        else:
            slap = discord.Embed(color=0xFFC0CB)
            slap.set_footer(text="Fetched from nekos.life")
            slap.set_image(url=slap_api["url"])
            await ctx.send(f"*{ctx.author.mention} slapped {member.name}*", embed=slap)

    @cog_ext.cog_slash(description="Show a smuggy look")
    async def smug(self, ctx:SlashContext):
        smug_api = requests.get("https://nekos.life/api/v2/img/smug").json()

        smug = discord.Embed(color=0xFFC0CB)
        smug.set_footer(text="Fetched from nekos.life")
        smug.set_image(url=smug_api["url"])
        await ctx.send(f"*Slapping {ctx.author.mention}*", embed=smug) 

    @cog_ext.cog_slash(description="Poke someone or yourself")
    async def poke(self, ctx:SlashContext, member: Member = None):
        poke_api = requests.get("https://nekos.life/api/v2/img/poke").json()

        if member == None:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.life")
            poke.set_image(url=poke_api["url"])
            await ctx.send(f"*Poking {ctx.author.mention}*", embed=poke)

        else:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_footer(text="Fetched from nekos.life")
            poke.set_image(url=poke_api["url"])
            await ctx.send(f"*{ctx.author.mention} poked {member.name}*", embed=poke)

    @cog_ext.cog_slash(description="Pat someone or yourself")
    async def pat(self, ctx:SlashContext, member: Member = None):
        pat_api = requests.get("https://nekos.life/api/v2/img/pat").json()

        if member == None:
            pat = discord.Embed(color=0xFFC0CB)
            pat.set_footer(text="Fetched from nekos.life")
            pat.set_image(url=pat_api["url"])
            await ctx.send(f"*Patting {ctx.author.mention}*", embed=pat)

        else:
            pat = discord.Embed(color=0xFFC0CB)
            pat.set_image(url=pat_api["url"])
            await ctx.send(f"*{ctx.author.mention} patted {member.name}*", embed=pat)

    @cog_ext.cog_slash(description="Kiss someone or yourself")
    async def kiss(self, ctx:SlashContext, member: Member = None):
        kiss_api = requests.get("https://nekos.life/api/v2/img/kiss").json()

        if member == None:
            kiss = discord.Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await ctx.send(f"*Kissing {ctx.author.mention}*", embed=kiss)

        else:
            kiss = discord.Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await ctx.send(f"*{ctx.author.mention} kissed {member.name}*", embed=kiss)

    @cog_ext.cog_slash(description="Tickle someone or yourself")
    async def tickle(self, ctx:SlashContext, member: Member = None):
        tickle_api = requests.get("https://nekos.life/api/v2/img/tickle").json()

        if member == None:
            tickle = discord.Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(f"*Tickling {ctx.author.mention}*", embed=tickle)

        else:
            tickle = discord.Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(f"*{ctx.author.mention} tickled {member.name}*", embed=tickle)

    @cog_ext.cog_slash(description="Call someone or yourself a baka!")
    async def baka(self, ctx:SlashContext, member: Member = None):
        tickle_api = requests.get("https://nekos.life/api/v2/img/baka").json()

        if member == None:
            baka = discord.Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=tickle_api["url"])
            await ctx.send(f"*{ctx.author.mention}*, you are a baka!", embed=baka)

        else:
            baka = discord.Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=tickle_api["url"])
            await ctx.send(f"*{member.mention}, {ctx.author.mention} called you a baka!*", embed=baka)

def setup(bot):
    bot.add_cog(reactions(bot))
