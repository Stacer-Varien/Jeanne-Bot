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

    @Jeanne.command(
        name=T("hug_name"),
        description=T("hug_desc"),
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
