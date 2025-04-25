from random import choice
from discord import Color, Embed, Interaction, Member, app_commands as Jeanne
from discord.ext.commands import Cog, Bot
from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from assets.images import get_animeme_pic
from typing import Optional
import languages.en.fun as en
import languages.fr.fun as fr
from discord.app_commands import locale_str as T


class fun(Cog, name="FunSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Jeanne.command(name=T("8ball_name"), description=T("8ball_desc"))
    @Jeanne.describe(question=T("question_parm_desc"))
    @Jeanne.rename(question=T("question_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def _8ball(self, ctx: Interaction, question: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en._8ball(ctx, question)
        elif ctx.locale.value == "fr":
            await fr._8ball(ctx, question)

    @Jeanne.command(name=T("reverse_name"), description=T("reverse_desc"))
    @Jeanne.describe(text=T("text_parm_desc"))
    @Jeanne.rename(text=T("text_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def reverse(self, ctx: Interaction, text: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.reverse(ctx, text)
        if ctx.locale.value == "fr":
            await fr.reverse(ctx, text)

    @Jeanne.command(description=T("animeme_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def animeme(self, ctx: Interaction):
        await ctx.response.defer()
        embed, file = get_animeme_pic()
        await ctx.followup.send(embed=embed, file=file)

    @Jeanne.command(name=T("combine_name"), description=T("combine_desc"))
    @Jeanne.describe(
        first_word=T("first_word_parm_desc"), second_word=T("second_word_parm_desc")
    )
    @Jeanne.rename(
        first_word=T("first_word_parm_name"), second_word=T("second_word_parm_name")
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    async def combine(self, ctx: Interaction, first_word: str, second_word: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.combine(ctx, first_word, second_word)
        if ctx.locale.value == "fr-FR":
            await fr.combine(ctx, first_word, second_word)

    @Jeanne.command(name=T("choose_name"), description=T("choose_desc"))
    @Jeanne.describe(choices=T("choose_parm_desc"))
    @Jeanne.rename(choices=T("choose_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def choose(self, ctx: Interaction, choices: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.choose(ctx, choices)
        if ctx.locale.value == "fr":
            await fr.choose(ctx, choices)

    @Jeanne.command(name=T("simprate_name"), description=T("simprate_desc"))
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def simprate(self, ctx: Interaction, member: Optional[Member] = None):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.simprate(ctx, member)
        if ctx.locale.value == "fr":
            await fr.simprate(ctx, member)

    @Jeanne.command(name=T("gayrate_name"), description=T("gayrate_desc"))
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def gayrate(self, ctx: Interaction, member: Optional[Member] = None):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.gayrate(ctx, member)
        if ctx.locale.value == "fr":
            await fr.gayrate(ctx, member)


async def setup(bot: Bot):
    await bot.add_cog(fun(bot))
