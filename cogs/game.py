from typing import Literal
from discord import Interaction, app_commands as Jeanne, embed, Member
from discord.ext.commands import Bot, Cog, GroupCog


class SummonCog(GroupCog, name="summon"):
    def __init__(self, bot:Bot) -> None:
        self.bot=bot
    
    @Jeanne.command(name="servant", description="Summon a servant from a group")
    @Jeanne.describe(group="Which group are you summoning your servant from?", amount="How much QP are you using?")
    async def servant(self, ctx:Interaction, group:Literal["Apocrypha"], amount:Jeanne.Range[int, 1000, 5000]):
        await ctx.response.defer()


class FateGame(Cog):
    def __init__(self, bot:Bot) -> None:
        self.bot=bot
    
    summon_group=Jeanne.Group(name="summon", description="...")


async def setup(bot:Bot):
    await bot.add_cog(FateGame(bot))