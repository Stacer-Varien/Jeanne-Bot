from functions import Botban, Command
from discord import Color, Embed, Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from requests import get
from config import (
    hug_nekoslife,
    slap_nekoslife,
    smug_nekoslife,
    poke_nekosfun,
    cry_purrbot,
    pat_nekoslife,
    kiss_nekosfun,
    tickle_nekoslife,
    baka_nekosfun,
    feed_nekoslife,
    bite_purrbot,
    blush_purrbot,
    cuddle_purrbot,
    dance_purrbot,
)
from typing import Optional


class SlashReactions(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _send_reaction(
        self,
        ctx: Interaction,
        action: str,
        member: Optional[Member] = None,
        api_url: str = None,
    ) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(getattr(self, action).qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        reaction_api = get(api_url).json()
        reaction_embed = Embed(color=Color.random())
        reaction_embed.set_footer(
            text=(
                "Fetched from nekos.life"
                if "nekos.life" in api_url
                else "Fetched from PurrBot.site"
            )
        )
        reaction_embed.set_image(
            url=(
                reaction_api["url"]
                if "nekos.life" in api_url
                else reaction_api["image"]
            )
        )
        other_actions = ["baka", "smug", "hug"]
        if action == "baka":
            msg = (
                f"*{ctx.user}*, you are a baka!"
                if member is None
                else f"*{member.mention}*, *{ctx.user} called you a baka!"
            )
            return

        if action == "smug":
            msg = f"*{ctx.user}* is smugging"
            return

        if action == "hug":
            msg = (
                f"*Hugging {ctx.user}*"
                if member is None
                else f"*{ctx.user} hugged {member.mention}*"
            )

        if action not in other_actions:
            msg = (
                f"*{action.capitalize()}ing {ctx.user}*"
                if member is None
                else f"*{ctx.user} {action}ed {member.mention}*"
            )

        await ctx.response.send_message(msg, embed=reaction_embed)

    @Jeanne.command(description="Hug someone or yourself")
    @Jeanne.describe(member="Who are you hugging?")
    async def hug(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "hug", member, hug_nekoslife)

    @Jeanne.command(description="Slap someone or yourself")
    @Jeanne.describe(member="Who are you slapping?")
    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "slap", member, slap_nekoslife)

    @Jeanne.command(description="Show a smuggy look")
    async def smug(self, ctx: Interaction):
        await self._send_reaction(ctx, "smug", api_url=smug_nekoslife)

    @Jeanne.command(description="Poke someone or yourself")
    @Jeanne.describe(member="Who are you poking?")
    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "poke", member, poke_nekosfun)

    @Jeanne.command(description="Pat someone or yourself")
    @Jeanne.describe(member="Who are you patting?")
    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "pat", member, pat_nekoslife)

    @Jeanne.command(description="Kiss someone or yourself")
    @Jeanne.describe(member="Who are you kissing?")
    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "kiss", member, kiss_nekosfun)

    @Jeanne.command(description="Tickle someone or yourself")
    @Jeanne.describe(member="Who are you tickling?")
    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "tickle", member, tickle_nekoslife)

    @Jeanne.command(description="Call someone or yourself a baka!")
    @Jeanne.describe(member="Who are you calling a baka?")
    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "baka", member, baka_nekosfun)

    @Jeanne.command(description="Feed someone or yourself")
    @Jeanne.describe(member="Who are you feeding?")
    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "feed", member, feed_nekoslife)

    @Jeanne.command(description="Make yourself cry")
    async def cry(self, ctx: Interaction):
        await self._send_reaction(ctx, "cry", api_url=cry_purrbot)

    @Jeanne.command(description="Bite someone or yourself")
    @Jeanne.describe(member="Who are you biting?")
    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "bite", member, bite_purrbot)

    @Jeanne.command(description="Make yourself blush")
    async def blush(self, ctx: Interaction):
        await self._send_reaction(ctx, "blush", api_url=blush_purrbot)

    @Jeanne.command(description="Cuddle with someone or yourself")
    @Jeanne.describe(member="Who are you cuddling?")
    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "cuddle", member, cuddle_purrbot)

    @Jeanne.command(description="Dance with someone or yourself")
    @Jeanne.describe(member="Who are you dancing with?")
    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "dance", member, dance_purrbot)


async def setup(bot: Bot):
    await bot.add_cog(SlashReactions(bot))
