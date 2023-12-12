from typing import Literal
from discord import Color, Interaction, app_commands as Jeanne, Embed, Member
from discord.ext.commands import Bot, Cog, GroupCog

from functions import Botban, Command


class SummonCog(GroupCog, name="summon"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Jeanne.command(name="servant", description="Summon a servant from a group")
    @Jeanne.describe(
        group="Which group are you summoning your servant from?",
        amount="How much QP are you using?",
    )
    async def servant(
        self,
        ctx: Interaction,
        group: Literal["Apocrypha"],
        amount: Jeanne.Range[int, 1000, 5000],
    ):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.servant.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        server = await self.bot.fetch_guild(740584420645535775)
        author = await server.fetch_member(ctx.user.id)
        role = server.get_role(1130430961587335219)
        try:
            if role in author.roles:
                ...
        except:
            await ctx.response.send_message(
                embed=Embed(
                    description="Uh Oh!\n\nIt seems you are trying something that is meant for beta users.\nIf you wish to join the beta programme, join [Orleans](https://discord.gg/Vfa796yvNq) and ask the bot developer.",
                    color=Color.red(),
                ),
                ephemeral=True,
            )

        await ctx.response.defer()


class FateGame(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    summon_group = Jeanne.Group(name="summon", description="...")


async def setup(bot: Bot):
    await bot.add_cog(FateGame(bot))
