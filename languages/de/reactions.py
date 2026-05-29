import json
import random
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from requests import get
from config import (
    hug,
    slap,
    smug,
    poke,
    cry,
    pat,
    kiss,
    tickle,
    baka,
    feed,
    bite,
    blush,
    cuddle,
    dance,
)
from typing import Optional


class Reactions:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _send_reaction(
        self,
        ctx: Interaction,
        action: str,
        member: Optional[Member] = None,
        api_url: str = None,
    ) -> None:
        reaction_api = get(api_url)
        reaction_embed = Embed(color=Color.random())
        reaction_embed.set_footer(text="Abgerufen von Tenor")
        random_gif = random.choice(json.loads(reaction_api.content)["results"])
        reaction_url = random_gif["media_formats"]["gif"]["url"]
        reaction_embed.set_image(url=reaction_url)

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
        await self._send_reaction(ctx, "hug", member, hug)

    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "slap", member, slap)

    async def smug(self, ctx: Interaction):
        await self._send_reaction(ctx, "smug", api_url=smug)

    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "poke", member, poke)

    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "pat", member, pat)

    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "kiss", member, kiss)

    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "tickle", member, tickle)

    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "baka", member, baka)

    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "feed", member, feed)

    async def cry(self, ctx: Interaction):
        await self._send_reaction(ctx, "cry", api_url=cry)

    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "bite", member, bite)

    async def blush(self, ctx: Interaction):
        await self._send_reaction(ctx, "blush", api_url=blush)

    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "cuddle", member, cuddle)

    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "dance", member, dance)
