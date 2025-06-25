from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from discord import Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from typing import Optional
from discord.app_commands import locale_str as T
import languages.en.reactions as en
import languages.fr.reactions as fr


class SlashReactions(Cog, name="ReactionsSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(
        name=T("hug_name"),
        description=T("hug_desc"),
        extras={
            "en": {
                "name": "hug",
                "description": "Hug someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you hugging?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "câlin",
                "description": "Faites un câlin à quelqu'un ou à vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui câlinez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("hug_member_parm_name"))
    @Jeanne.describe(member=T("hug_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def hug(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).hug(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).hug(ctx, member)

    @Jeanne.command(
        name=T("slap_name"),
        description=T("slap_desc"),
        extras={
            "en": {
                "name": "slap",
                "description": "Slap someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you slapping?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "gifler",
                "description": "Gifle quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui giflez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("slap_member_parm_name"))
    @Jeanne.describe(member=T("slap_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def slap(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).slap(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).slap(ctx, member)

    @Jeanne.command(
        name=T("smug_name"),
        description=T("smug_desc"),
        extras={
            "en": {
                "name": "smug",
                "description": "Show a smug expression",
            },
            "fr": {
                "name": "suffisant",
                "description": "Affichez une expression suffisante",
                
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def smug(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).smug(ctx)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).smug(ctx)

    @Jeanne.command(
        name=T("poke_name"),
        description=T("poke_desc"),
        extras={
            "en": {
                "name": "poke",
                "description": "Poke someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you poking?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "pousser",
                "description": "Poussez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui poussez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("poke_member_parm_name"))
    @Jeanne.describe(member=T("poke_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def poke(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).poke(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).poke(ctx, member)

    @Jeanne.command(
        name=T("pat_name"),
        description=T("pat_desc"),
        extras={
            "en": {
                "name": "pat",
                "description": "Pat someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you patting?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "tapoter",
                "description": "Tapotez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui tapotez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("pat_member_parm_name"))
    @Jeanne.describe(member=T("pat_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def pat(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).pat(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).pat(ctx, member)

    @Jeanne.command(
        name=T("kiss_name"),
        description=T("kiss_desc"),
        extras={
            "en": {
                "name": "Kiss",
                "description": "Kiss someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you patting?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "embrasser",
                "description": "Embrassez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui embrassez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("kiss_member_parm_name"))
    @Jeanne.describe(member=T("kiss_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def kiss(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).kiss(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).kiss(ctx, member)

    @Jeanne.command(
        name=T("tickle_name"),
        description=T("tickle_desc"),
        extras={
            "en": {
                "name": "tickle",
                "description": "Tickle someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you tickling?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "chatouiller",
                "description": "Chatouillez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui chatouillez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("tickle_member_parm_name"))
    @Jeanne.describe(member=T("tickle_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def tickle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).tickle(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).tickle(ctx, member)

    @Jeanne.command(
        name=T("baka_name"),
        description=T("baka_desc"),
        extras={
            "en": {
                "name": "baka",
                "description": "Call someone or yourself a baka!",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you calling a baka?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "baka",
                "description": "Traitez quelqu'un ou vous-même de baka!",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui traitez-vous de baka?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("baka_member_parm_name"))
    @Jeanne.describe(member=T("baka_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def baka(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).baka(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).baka(ctx, member)

    @Jeanne.command(
        name=T("feed_name"),
        description=T("feed_desc"),
        extras={
            "en": {
                "name": "feed",
                "description": "Feed someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you feeding?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "nourrir",
                "description": "Nourrissez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui chatouillez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("feed_member_parm_name"))
    @Jeanne.describe(member=T("feed_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def feed(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).feed(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).feed(ctx, member)

    @Jeanne.command(
        name=T("cry_name"),
        description=T("cry_desc"),
        extras={
            "en": {
                "name": "cry",
                "description": "Show a crying expression",
            },
            "fr": {
                "name": "pleurer",
                "description": "Affichez une expression de pleurs",
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def cry(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).cry(ctx)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).cry(ctx)

    @Jeanne.command(
        name=T("bite_name"),
        description=T("bite_desc"),
        extras={
            "en": {
                "name": "bite",
                "description": "Bite someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you biting?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "mordre",
                "description": "Nourrissez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Qui mordez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("bite_member_parm_name"))
    @Jeanne.describe(member=T("bite_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def bite(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).bite(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).bite(ctx, member)

    @Jeanne.command(
        name=T("blush_name"),
        description=T("blush_desc"),
        extras={
            "en": {
                "name": "blush",
                "description": "Show a blushing expression",
            },
            "fr": {
                "name": "rougir",
                "description": "Affichez une expression rougissante",
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def blush(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).blush(ctx)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).blush(ctx)

    @Jeanne.command(
        name=T("cuddle_name"),
        description=T("cuddle_desc"),
        extras={
            "en": {
                "name": "cuddle",
                "description": "Cuddle with someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you cuddling with?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "câliner",
                "description": "Câlinez quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Avec qui câlinez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("cuddle_member_parm_name"))
    @Jeanne.describe(member=T("cuddle_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def cuddle(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).cuddle(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).cuddle(ctx, member)

    @Jeanne.command(
        name=T("dance_name"),
        description=T("dance_desc"),
        extras={
            "en": {
                "name": "dance",
                "description": "Dance with someone or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Who are you dancing with?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "danser",
                "description": "Dansez avec quelqu'un ou vous-même",
                "parameters": [
                    {
                        "name": "membre",
                        "description": "Avec qui dansez-vous?",
                        "required": False,
                    }
                ],
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.rename(member=T("dance_member_parm_name"))
    @Jeanne.describe(member=T("dance_member_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def dance(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Reactions(self.bot).dance(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Reactions(self.bot).dance(ctx, member)


async def setup(bot: Bot):
    await bot.add_cog(SlashReactions(bot))
