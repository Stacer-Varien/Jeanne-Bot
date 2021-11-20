import discord
from discord.ext import commands
from discord.ext.commands.errors import NotOwner, NSFWChannelRequired, NotOwner


class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NotOwner):
            embed = discord.Embed(
            title="Owner only command", description="This command failed to commit because you are not the bot owner", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, NSFWChannelRequired):
            error = discord.Embed(
                title='NSFW Failed', description="NSFW material couldn't be sent in this channel", color=0xff0000)
            error.add_field(
                name="Reason", value="Channel is not NSFW enabled")
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(errors(bot))
