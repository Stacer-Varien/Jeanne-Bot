from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands.errors import MemberNotFound, NotOwner, UserNotFound, GuildNotFound, NSFWChannelRequired, CommandOnCooldown


class errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, NotOwner):
            embed = Embed(
            title="Owner only command", description="This command failed to commit because you are not the bot owner", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, GuildNotFound):
            embed = Embed(
                description="Bot is not in this server", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, UserNotFound):
            no_user = Embed(
                title="User does not exist", description="Please make sure the USER_ID is valid or maybe they have deleted their account.", color=0xff0000)
            await ctx.send(embed=no_user)
        elif isinstance(error, CommandOnCooldown):
            embed = Embed(
                title="Command On Cooldown", description=f"This command is on cooldown. Please wait at least {error.retry_after: .2f} seconds to use it again.", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, NSFWChannelRequired):
            error = Embed(
                title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
            error.add_field(
                name="Reason", value="Channel is not NSFW enabled")
            await ctx.send(embed=error)
        elif isinstance(error, MemberNotFound):
            embed = Embed(description="Member is not in this server")
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(errors(bot))
