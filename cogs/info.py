from functions import (
    check_botbanned_app_command,
    check_disabled_app_command,
    is_suspended,
)
from discord.app_commands import locale_str as T
from discord.ext.commands import Cog, Bot
from discord import (
    Interaction,
    Member,
    app_commands as Jeanne,
)
from typing import Optional
import languages.en.info as en
import languages.fr.info as fr


class InfoCog(Cog, name="InfoSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot_version = "v5.0b"
        self.userinfo_context = Jeanne.ContextMenu(
            name="Userinfo", callback=self.userinfo_callback
        )
        self.bot.tree.add_command(self.userinfo_context)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.userinfo_context.name, type=self.userinfo_context.type
        )

    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def userinfo_callback(self, ctx: Interaction, member: Member):
        await self.get_userinfo(ctx, member)

    async def get_userinfo(self, ctx: Interaction, member: Member):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).get_userinfo(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).get_userinfo(ctx, member)

    @Jeanne.command(description="See the bot's status from development to now")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def stats(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).stats(ctx)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).stats(ctx)

    @Jeanne.command(description="See the information of a member or yourself")
    @Jeanne.describe(member="Which member?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def userinfo(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        member = ctx.user if member is None else member
        await self.get_userinfo(ctx, member)

    @Jeanne.command(description="Get information about this server")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def serverinfo(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).serverinfo(ctx)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).serverinfo(ctx)

    @Jeanne.command(
        name=T("ping_name", default="ping"),
        description=T("ping_desc", default="Check how fast I respond to a command"),
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def ping(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).ping(ctx)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).ping(ctx)

    @Jeanne.command(description="See the server's banner")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def serverbanner(self, ctx: Interaction):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).serverbanner(ctx)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).serverbanner(ctx)

    @Jeanne.command(description="See your avatar or another member's avatar")
    @Jeanne.describe(member="Which member?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def avatar(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).avatar(ctx, member)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).avatar(ctx, member)

    @Jeanne.command(description="View a sticker")
    @Jeanne.describe(
        sticker="Insert message ID with the sticker or name of the sticker in the server"
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def sticker(self, ctx: Interaction, sticker: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).sticker(ctx, sticker)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).sticker(ctx, sticker)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Info(self.bot).sticker_error(ctx, error, "NoSticker")
            elif ctx.locale.value == "fr":
                await fr.Info(self.bot).sticker_error(ctx, error, "NoSticker")
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Info(self.bot).sticker_error(ctx, error, "StickerNotFound")
            elif ctx.locale.value == "fr":
                await fr.Info(self.bot).sticker_error(ctx, error, "StickerNotFound")

    @Jeanne.command(description="View an emoji")
    @Jeanne.describe(emoji="What is the name of the emoji?")
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def emoji(self, ctx: Interaction, emoji: str):
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            await en.Info(self.bot).emoji(ctx, emoji)
        elif ctx.locale.value == "fr":
            await fr.Info(self.bot).emoji(ctx, emoji)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
                await en.Info(self.bot).emoji_error(ctx, error)
            elif ctx.locale.value == "fr":
                await fr.Info(self.bot).emoji_error(ctx, error)


async def setup(bot: Bot):
    await bot.add_cog(InfoCog(bot))
