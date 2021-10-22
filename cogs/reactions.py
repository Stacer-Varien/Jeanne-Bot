import discord
from discord.ext import commands
import requests
from discord import Member, Embed
from discord.ext.commands.errors import MemberNotFound


class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, *, member: Member = None):
            hug_api = requests.get("https://nekos.life/api/v2/img/hug").json()
            if member == None:
                msg=f"*Hugging {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} hugged {member.mention}*"
            hug = Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await ctx.send(msg, embed=hug)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Hug failed", description="Please hug someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, *, member: Member = None):
        slap_api = requests.get("https://nekos.life/api/v2/img/slap").json()

        slap = Embed(color=0xFFC0CB)
        slap.set_footer(text="Fetched from nekos.life")
        slap.set_image(url=slap_api["url"])
        if member == None:
                msg=f"Slapping {ctx.author.mention}"
        else:
                msg=f"*{ctx.author.mention} slapped {member.mention}*"
        await ctx.send(msg, embed=slap)

    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Slap failed", description="Please slap someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smug(self, ctx):
        smug_api = requests.get("https://nekos.life/api/v2/img/smug").json()
        smug = Embed(color=0xFFC0CB)
        smug.set_footer(text="Fetched from nekos.life")
        smug.set_image(url=smug_api["url"])
        await ctx.send(f"*{ctx.author.mention} is smugging*", embed=smug)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poke(self, ctx, *, member: Member = None):
        poke_api = requests.get("https://nekos.life/api/v2/img/poke").json()
        poke = Embed(color=0xFFC0CB)
        poke.set_footer(text="Fetched from nekos.life")
        poke.set_image(url=poke_api["url"])
        if member == None:
                msg=f"*Poking {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} poked {member.mention}*"
        await ctx.send(msg, embed=poke)

    @poke.error
    async def poke_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Poke failed", description="Please poke someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, *, member: Member = None):
        pat_api = requests.get("https://nekos.life/api/v2/img/pat").json()
        pat = Embed(color=0xFFC0CB)
        pat.set_footer(text="Fetched from nekos.life")
        pat.set_image(url=pat_api["url"])
        if member == None:
                msg=f"*Patting {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} patted {member.mention}*"
        await ctx.send(msg, embed=pat)

    @pat.error
    async def pat_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Pat failed", description="Please pat someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, *, member: Member = None):
            kiss_api = requests.get("https://nekos.life/api/v2/img/kiss").json()
            if member == None:
                msg=f"Kissing {ctx.author.mention}"
            else:
                msg=f"*{ctx.author.mention} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await ctx.send(msg, embed=kiss)

    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Kiss failed", description="Please pat someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tickle(self, ctx, *, member: Member = None):
            tickle_api = requests.get("https://nekos.life/api/v2/img/tickle").json()
            if member == None:
                msg=f"*Kissing {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} kissed {member.mention}*"
            tickle = Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(msg, embed=tickle)

    @tickle.error
    async def tickle_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Tickle failed", description="Please tickle someone who is in the server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baka(self, ctx, *, member: Member = None):
            baka_api = requests.get("https://nekos.life/api/v2/img/baka").json()
            if member == None:
                msg=f"*{ctx.author.mention}, you are a baka!*"
            else:
                msg=f"*{member.mention}, {ctx.author.mention} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=baka_api["url"])
            await ctx.send(msg, embed=baka)

    @baka.error
    async def baka_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Baka failed", description="Please call someone who is in the server a baka\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @feed.error
    async def feed_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = Embed(
                title="Feed failed", description="Please feed someone who is in this server\nIf you were trying to mention a role or used `@everyone` or `@here`, then good luck mention spamming", color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(reactions(bot))
