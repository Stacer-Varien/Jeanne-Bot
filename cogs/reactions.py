from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,  
)
from discord import Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from config import (
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
from discord.app_commands import locale_str as T
import languages.en.reactions as en
import languages.fr.reactions as fr

class SlashReactions(Cog, name="ReactionsSlash"):
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

        messages = {
            "baka": (
                f"*{ctx.user}*, you are a baka!"
                if member is None
                else f"*{member.mention}*, *{ctx.user} called you a baka!*"
            ),
            "smug": f"*{ctx.user}* is smirking",
            "hug": (
                f"*Hugging {ctx.user}*"
                if member is None
                else f"*{ctx.user} hugged {member.mention}*"
            ),
            "poke": (
                f"*Poking {ctx.user}*"
                if member is None
                else f"*{ctx.user} is poking {member.mention}*"
            ),
            "cuddle": (
                f"*Cuddling {ctx.user}*"
                if member is None
                else f"*{ctx.user} is cuddling with {member.mention}*"
            ),
            "dance": (
                f"*{ctx.user} is dancing*"
                if member is None
                else f"*{ctx.user} is dancing with {member.mention}*"
            ),
            "pat": (
                f"*Patting {ctx.user}*"
                if member is None
                else f"*{ctx.user} patted {member.mention}*"
            ),
            "blush": f"*{ctx.user} is blushing*",
            "bite": (
                f"*Biting {ctx.user}*"
                if member is None
                else f"*{ctx.user} bit {member.mention}*"
            ),
            "feed": (
                f"*Feeding {ctx.user}*"
                if member is None
                else f"*{ctx.user} is feeding {member.mention}. Eat up*"
            ),
            "cry": f"*{ctx.user} is crying*",
            "slap": (
                f"*Slapping {ctx.user}*"
                if member is None
                else f"*{ctx.user} slapped {member.mention}*"
            ),
            "kiss": (
                f"*Kissing {ctx.user}*"
                if member is None
                else f"*{ctx.user} kissed {member.mention}*"
            ),
            "tickle": (
                f"*Tickling {ctx.user}*"
                if member is None
                else f"*{ctx.user} tickled {member.mention}*"
            ),
        }

        msg = messages.get(action, f"*{ctx.user} is performing an action*")
        await ctx.response.send_message(msg, embed=reaction_embed)

    @Jeanne.command(description="Hug someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you hugging?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def hug(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "hug", member, hug)

    @Jeanne.command(description="Slap someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you slapping?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await self._send_reaction(ctx, "slap", member, slap)

    @Jeanne.command(description="Show a smug expression")
    @Jeanne.check(is_suspended)  
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def smug(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).smug(ctx)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).hug(ctx)

    @Jeanne.command(description="Poke someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you poking?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).poke(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).poke(ctx, member)

    @Jeanne.command(description="Pat someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you patting?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).pat(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).pat(ctx, member)

    @Jeanne.command(description="Kiss someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you kissing?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).kiss(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).kiss(ctx, member)

    @Jeanne.command(description="Tickle someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you tickling?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).tickle(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).tickle(ctx, member)

    @Jeanne.command(description="Call someone or yourself a baka!")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you calling a baka?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).baka(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).baka(ctx, member)

    @Jeanne.command(description="Feed someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you feeding?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).feed(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).feed(ctx, member)

    @Jeanne.command(description="Show a crying expression")
    @Jeanne.check(is_suspended)  
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def cry(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).cry(ctx)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).cry(ctx)

    @Jeanne.command(description="Bite someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you biting?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).bite(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).bite(ctx, member)

    @Jeanne.command(description="Show a blushing expression")
    @Jeanne.check(is_suspended)  
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def blush(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).blush(ctx)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).blush(ctx)

    @Jeanne.command(description="Cuddle with someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you cuddling with?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).cuddle(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).cuddle(ctx, member)

    @Jeanne.command(description="Dance with someone or yourself")
    @Jeanne.check(is_suspended)  
    @Jeanne.describe(member="Who are you dancing with?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).dance(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).dance(ctx, member)


async def setup(bot: Bot):
    await bot.add_cog(SlashReactions(bot))
