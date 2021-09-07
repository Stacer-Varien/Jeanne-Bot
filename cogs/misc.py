import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite me!",
            description="Click on one of these URLs to invite me to you server or join my creator's servers",
            color=0x00bfff)
        embed.add_field(name="Bot Invite",
                        value="[Click here](https://discord.com/oauth2/authorize?client_id=831993597166747679&scope=bot&permissions=469888182)",
                        inline=True)
        embed.add_field(name="Top.gg",
                        value="[Click here](https://top.gg/bot/831993597166747679)",
                        inline=True)
        embed.add_field(name="DiscordBotList",
                        value="[Click here](https://discordbotlist.com/bots/nero-3694)", inline=True)
        embed.add_field(name="HAZE server",
                        value="[Click here](https://discord.gg/VVxGUmqQhF)", inline=True)
        embed.add_field(name="NERO Support Server",
                        value="[Click here](https://discord.gg/Xn3EvGcMrF)", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, text):
        message = ctx.message
        await message.delete()
        await ctx.send(text)
    
    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Command failed", description="It looks like I cannot say your message message", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Administrator", inline=False)
            await ctx.send(embed=embed)

        elif ctx.author==ctx.owner:
            embed = discord.Embed(
                description="I don't care if you created me. You will not use this command", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.group(name='saye')
    @commands.has_permissions(administrator=True)
    async def sayembed(self, ctx, *, text):
        message = ctx.message
        say = discord.Embed(description=f"{text}", color=0xADD8E6)
        await message.delete()
        await ctx.send(embed=say)

    @sayembed.error
    async def sayembed_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Command failed", description="It looks like I cannot say your message message", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Administrator", inline=False)
            await ctx.send(embed=embed)

        elif ctx.author==ctx.owner:
            embed = discord.Embed(
                description="I don't care if you created me. You will not use this command", color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))
