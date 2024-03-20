import json
import random
from functions import (
    Botban,
    Command,
    check_botbanned_app_command,
    check_disabled_app_command,
)
from discord import Color, Embed, Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
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
        reaction_api = get(api_url)
        reaction_embed = Embed(color=Color.random())
        reaction_embed.set_footer(text="Fetched from Tenor")
        random_gif = random.choice(json.loads(reaction_api.content)["results"])
        reaction_url = random_gif["media_formats"]["gif"]["url"]
        reaction_embed.set_image(url=reaction_url)
        other_actions = ["baka", "smug", "hug", "poke", "tickle", "dance", "cuddle"]
        if action == "baka":
            msg = (
                f"*{ctx.user}*, you are a baka!"
                if member is None
                else f"*{member.mention}, {ctx.user} called you a baka!*"
            )
        elif action == "smug":
            msg = f"*{ctx.user}* is smugging"
        elif action == "hug":
            msg = (
                f"*Hugging {ctx.user}*"
                if member is None
                else f"*{ctx.user} hugged {member.mention}*"
            )
        elif action == "poke":
            msg = (
                f"*Poking {ctx.user}*"
                if member is None
                else f"*{ctx.user} is poking {member.mention}*"
            )
        elif action == "cuddle":
            msg = (
                f"*Cuddling {ctx.user}*"
                if member is None
                else f"*{ctx.user} is cuddling with {member.mention}*"
            )
        elif action == "dance":
            msg = (
                f"*Dancing {ctx.user}*"
                if member is None
                else f"*{ctx.user} is dancing with {member.mention}*"
            )
        elif action not in other_actions:
            msg = (
                f"*{action.capitalize()}ing {ctx.user}*"
                if member is None
                else f"*{ctx.user} {action}ed {member.mention}*"
            )
        await ctx.response.send_message(msg, embed=reaction_embed)

    @Jeanne.command(description="Hug someone or yourself")
    @Jeanne.describe(member="Who are you hugging?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def hug(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "hug", member, hug)

    @Jeanne.command(description="Slap someone or yourself")
    @Jeanne.describe(member="Who are you slapping?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "slap", member, slap)

    @Jeanne.command(description="Show a smuggy look")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def smug(self, ctx: Interaction):
        await self._send_reaction(ctx, "smug", api_url=smug)

    @Jeanne.command(description="Poke someone or yourself")
    @Jeanne.describe(member="Who are you poking?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "poke", member, poke)

    @Jeanne.command(description="Pat someone or yourself")
    @Jeanne.describe(member="Who are you patting?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "pat", member, pat)

    @Jeanne.command(description="Kiss someone or yourself")
    @Jeanne.describe(member="Who are you kissing?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "kiss", member, kiss)

    @Jeanne.command(description="Tickle someone or yourself")
    @Jeanne.describe(member="Who are you tickling?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "tickle", member, tickle)

    @Jeanne.command(description="Call someone or yourself a baka!")
    @Jeanne.describe(member="Who are you calling a baka?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "baka", member, baka)

    @Jeanne.command(description="Feed someone or yourself")
    @Jeanne.describe(member="Who are you feeding?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "feed", member, feed)

    @Jeanne.command(description="Show a crying expression")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def cry(self, ctx: Interaction):
        await self._send_reaction(ctx, "cry", api_url=cry)

    @Jeanne.command(description="Bite someone or yourself")
    @Jeanne.describe(member="Who are you biting?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "bite", member, bite)

    @Jeanne.command(description="Show a blushing expression")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def blush(self, ctx: Interaction):
        await self._send_reaction(ctx, "blush", api_url=blush)

    @Jeanne.command(description="Cuddle with someone or yourself")
    @Jeanne.describe(member="Who are you cuddling with?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "cuddle", member, cuddle)

    @Jeanne.command(description="Dance with someone or yourself")
    @Jeanne.describe(member="Who are you dancing with?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "dance", member, dance)


async def setup(bot: Bot):
    await bot.add_cog(SlashReactions(bot))
