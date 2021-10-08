import discord
from discord.ext import commands
import requests
from discord import Member
from discord.ext.commands.errors import MemberNotFound


class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, *, member: Member = None):
        hug_api = requests.get("https://nekos.life/api/v2/img/hug").json()

        if member == None:
            hugs = discord.Embed(color=0xFFC0CB)
            hugs.set_image(url=hug_api["url"])
            await ctx.send(f"*Hugging {ctx.author.mention}* :people_hugging:", embed=hugs)

        else:
            hugs = discord.Embed(color=0xFFC0CB)
            hugs.set_image(url=hug_api["url"])
            await ctx.send(f"*{ctx.author.mention} hugged {member.name}* :people_hugging:", embed=hugs)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Hug failed", description="Please hug someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, *, member: Member = None):
        slap_api = requests.get("https://nekos.life/api/v2/img/slap").json()

        if member == None:
            slap = discord.Embed(color=0xFFC0CB)
            slap.set_image(url=slap_api["url"])
            await ctx.send(f"*Slapping {ctx.author.mention}*", embed=slap)

        else:
            slap = discord.Embed(color=0xFFC0CB)
            slap.set_image(url=slap_api["url"])
            await ctx.send(f"*{ctx.author.mention} slapped {member.name}*", embed=slap)

    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Slap failed", description="Please slap someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smug(self, ctx):
        smug_api = requests.get("https://nekos.life/api/v2/img/smug").json()
        smug = discord.Embed(color=0xFFC0CB)
        smug.set_image(url=smug_api["url"])
        await ctx.send(f"*{ctx.author.mention} is smugging*", embed=smug)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poke(self, ctx, *, member: Member = None):
        poke_api = requests.get("https://nekos.life/api/v2/img/poke").json()

        if member == None:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_image(url=poke_api["url"])
            await ctx.send(f"*Poking {ctx.author.mention}*", embed=poke)

        else:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_image(url=poke_api["url"])
            await ctx.send(f"*{ctx.author.mention} poked {member.name}*", embed=poke)

    @poke.error
    async def poke_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Poke failed", description="Please poke someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, *, member: Member = None):
        pat_api = requests.get("https://nekos.life/api/v2/img/pat").json()

        if member == None:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_image(url=pat_api["url"])
            await ctx.send(f"*Patting {ctx.author.mention}*", embed=poke)

        else:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_image(url=pat_api["url"])
            await ctx.send(f"*{ctx.author.mention} patted {member.name}*", embed=poke)

    @pat.error
    async def pat_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Pat failed", description="Please pat someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, *, member: Member = None):
        kiss_api = requests.get("https://nekos.life/api/v2/img/kiss").json()

        if member == None:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_image(url=kiss_api["url"])
            await ctx.send(f"*Kissing {ctx.author.mention}*", embed=poke)

        else:
            poke = discord.Embed(color=0xFFC0CB)
            poke.set_image(url=kiss_api["url"])
            await ctx.send(f"*{ctx.author.mention} kissed {member.name}*", embed=poke)

    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Kiss failed", description="Please pat someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tickle(self, ctx, *, member: Member = None):
        tickle_api = requests.get("https://nekos.life/api/v2/img/tickle").json()

        if member == None:
            tickle = discord.Embed(color=0xFFC0CB)
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(f"*Tickling {ctx.author.mention}*", embed=tickle)

        else:
            tickle = discord.Embed(color=0xFFC0CB)
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(f"*{ctx.author.mention} tickled {member.name}*", embed=tickle)

    @tickle.error
    async def tickle_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Tickle failed", description="Please tickle someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baka(self, ctx, *, member: Member = None):
        baka_api = requests.get(
            "https://nekos.life/api/v2/img/baka").json()

        if member == None:
            baka = discord.Embed(color=0xFFC0CB)
            baka.set_image(url=baka_api["url"])
            await ctx.send(f"*{ctx.author.mention}, you are a baka!*", embed=baka)

        else:
            baka = discord.Embed(color=0xFFC0CB)
            baka.set_image(url=baka_api["url"])
            await ctx.send(f"*{member.name}, {ctx.author.mention} called you a baka!*", embed=baka)

    @baka.error
    async def baka_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                title="Baka failed", description="Please call someone who is in the server a baka\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(reactions(bot))
