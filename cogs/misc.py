import discord
from discord.ext import commands


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite me!",
            url="https://discord.com/oauth2/authorize?client_id=831993597166747679&scope=bot&permissions=469888182",
            description="Invite me to your server! Doing that will make me and my creator happy",
            color=0x00bfff)
        embed.add_field(name="Or if you want to join the support server:",
                        value="https://discord.gg/Xn3EvGcMrF",
                        inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, text):
        message = ctx.message
        await message.delete()
        await ctx.send(text)

    @commands.group(name='saye')
    @commands.has_permissions(administrator=True)
    async def sayembed(self, ctx, *, text):
        message = ctx.message
        say = discord.Embed(description=f"{text}", color=0xADD8E6)
        await message.delete()
        await ctx.send(embed=say)


def setup(bot):
    bot.add_cog(misc(bot))
