from assets.reaction_gifs import get_reaction_gif
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from typing import Optional


class Reactions:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _send_reaction(
        self,
        ctx: Interaction,
        action: str,
        member: Optional[Member] = None,
    ) -> None:
        reaction_embed = Embed(color=Color.random())
        reaction_embed.set_footer(text="Von Tenor archiviert")
        reaction_embed.set_image(url=get_reaction_gif(action))

        messages = {
            "baka": (
                f"*{ctx.user}*, je bent een baka!"
                if member is None
                else f"*{member.mention}*, *{ctx.user} nennt dich einen baka!*"
            ),
            "smug": f"*{ctx.user}* grinst",
            "hug": (
                f"*Umarmt {ctx.user}*"
                if member is None
                else f"*{ctx.user} umarmte {member.mention}*"
            ),
            "poke": (
                f"*{ctx.user} stupst an*"
                if member is None
                else f"*{ctx.user} sticht {member.mention}*"
            ),
            "cuddle": (
                f"*Umarmt {ctx.user}*"
                if member is None
                else f"*{ctx.user} umarmt {member.mention}*"
            ),
            "dance": (
                f"*{ctx.user} tanzt*"
                if member is None
                else f"*{ctx.user} tanzt mit {member.mention}*"
            ),
            "pat": (
                f"*Streichelt {ctx.user}*"
                if member is None
                else f"*{ctx.user} streichelt {member.mention}*"
            ),
            "blush": f"*{ctx.user} errötet*",
            "bite": (
                f"*Beißt {ctx.user}*"
                if member is None
                else f"*{ctx.user} biss {member.mention}*"
            ),
            "feed": (
                f"*Füttert {ctx.user}*"
                if member is None
                else f"*{ctx.user} füttert {member.mention}. Guten Appetit*"
            ),
            "cry": f"*{ctx.user} weint*",
            "slap": (
                f"*Schlägt {ctx.user}*"
                if member is None
                else f"*{ctx.user} schlug {member.mention}*"
            ),
            "kiss": (
                f"*Küsst {ctx.user}*"
                if member is None
                else f"*{ctx.user} küsste {member.mention}*"
            ),
            "tickle": (
                f"*Kitzelt {ctx.user}*"
                if member is None
                else f"*{ctx.user} kitzelte {member.mention}*"
            ),
        }

        msg = messages.get(action, f"*{ctx.user} führt eine Aktion aus*")
        await ctx.response.send_message(msg, embed=reaction_embed)

    async def hug(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "hug", member)

    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "slap", member)

    async def smug(self, ctx: Interaction):
        await self._send_reaction(ctx, "smug")

    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "poke", member)

    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "pat", member)

    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "kiss", member)

    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "tickle", member)

    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "baka", member)

    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "feed", member)

    async def cry(self, ctx: Interaction):
        await self._send_reaction(ctx, "cry")

    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "bite", member)

    async def blush(self, ctx: Interaction):
        await self._send_reaction(ctx, "blush")

    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "cuddle", member)

    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "dance", member)
