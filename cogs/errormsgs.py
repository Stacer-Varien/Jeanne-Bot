import discord
from discord.ext import commands
from discord.ext.commands.errors import NotOwner, UserNotFound, GuildNotFound, NSFWChannelRequired, CommandOnCooldown


class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, NotOwner):
            embed = discord.Embed(
            title="Owner only command", description="This command failed to commit because you are not the bot owner", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, GuildNotFound):
            embed = discord.Embed(
                description="Bot is not in this server", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, UserNotFound):
            no_user = discord.Embed(
                title="User does not exist", description="Please make sure the USER_ID is valid or maybe they have deleted their account.", color=0xff0000)
            await ctx.send(embed=no_user)
        elif isinstance(error, CommandOnCooldown):
            embed = discord.Embed(
                title="Command On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, NSFWChannelRequired):
            error = discord.Embed(
                title='NSFW Failed', description="NSFW material couldn't be sent in this channel", color=0xff0000)
            error.add_field(
                name="Reason", value="Channel is not NSFW enabled")
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(errors(bot))
