from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands.errors import GuildNotFound, NotOwner, NSFWChannelRequired, NotOwner, UserNotFound


class errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NotOwner):
            owner_only = Embed(
            title="Owner only command", description="This command failed to commit because you are not the bot owner", color=0xff0000)
            await ctx.send(embed=owner_only)
        elif isinstance(error, NSFWChannelRequired):
            no_hentai = Embed(
                title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
            no_hentai.add_field(
                name="Reason", value="Channel is not NSFW enabled")
            await ctx.send(embed=no_hentai)
        elif isinstance(error, UserNotFound):
            no_user = Embed(
                title="User does not exist", description="Please make sure the USER_ID is valid or maybe they have deleted their account.", color=0xff0000)
            await ctx.send(embed=no_user)


def setup(bot):
    bot.add_cog(errors(bot))
