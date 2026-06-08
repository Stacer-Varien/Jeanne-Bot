from assets.reaction_gifs import get_reaction_gif
from discord import Color, Embed, Interaction, Member
from discord.ext.commands import Bot
from typing import Optional


class Reactions():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _send_reaction(
        self,
        ctx: Interaction,
        action: str,
        member: Optional[Member] = None,
    ) -> None:
        reaction_embed = Embed(color=Color.random())
        reaction_embed.set_footer(text="Archivé depuis Tenor")
        reaction_embed.set_image(url=get_reaction_gif(action))

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
