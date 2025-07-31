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


class Reactions():
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
        reaction_embed.set_footer(text="Tiré de Ténor")
        random_gif = random.choice(json.loads(reaction_api.content)["results"])
        reaction_url = random_gif["media_formats"]["gif"]["url"]
        reaction_embed.set_image(url=reaction_url)

        messages = {
            "baka": (
                f"*{ctx.user}*, tu es un baka !"
                if member is None
                else f"*{member.mention}*, *{ctx.user} t'a traité de baka !*"
            ),
            "smug": f"*{ctx.user}* a un sourire narquois",
            "hug": (
                f"*{ctx.user} se fait un câlin*"
                if member is None
                else f"*{ctx.user} a fait un câlin à {member.mention}*"
            ),
            "poke": (
                f"*{ctx.user} se fait un poke*"
                if member is None
                else f"*{ctx.user} poke {member.mention}*"
            ),
            "cuddle": (
                f"*{ctx.user} se fait un câlin*"
                if member is None
                else f"*{ctx.user} fait un câlin à {member.mention}*"
            ),
            "dance": (
                f"*{ctx.user} danse*"
                if member is None
                else f"*{ctx.user} danse avec {member.mention}*"
            ),
            "pat": (
                f"*{ctx.user} se fait tapoter la tête*"
                if member is None
                else f"*{ctx.user} tapote la tête de {member.mention}*"
            ),
            "blush": f"*{ctx.user} rougit*",
            "bite": (
                f"*{ctx.user} se mord*"
                if member is None
                else f"*{ctx.user} mord {member.mention}*"
            ),
            "feed": (
                f"*{ctx.user} se nourrit*"
                if member is None
                else f"*{ctx.user} nourrit {member.mention}. Bon appétit*"
            ),
            "cry": f"*{ctx.user} pleure*",
            "slap": (
                f"*{ctx.user} se gifle*"
                if member is None
                else f"*{ctx.user} a giflé {member.mention}*"
            ),
            "kiss": (
                f"*{ctx.user} s'embrasse*"
                if member is None
                else f"*{ctx.user} a embrassé {member.mention}*"
            ),
            "tickle": (
                f"*{ctx.user} se chatouille*"
                if member is None
                else f"*{ctx.user} a chatouillé {member.mention}*"
            ),
        }

        msg = messages.get(action, f"*{ctx.user} effectue une action*")
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
