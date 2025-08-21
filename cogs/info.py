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
import languages.de.info as de


class InfoCog(Cog, name="InfoSlash"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot_version = "v5.2.1"
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
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).get_userinfo(ctx, member)
            return       
        if ctx.locale.value == "de":
            await de.Info(self.bot).get_userinfo(ctx, member)
            return
        await en.Info(self.bot).get_userinfo(ctx, member)

    @Jeanne.command(
        description=T("stats_desc"),
        extras={
            "en": {
                "name": "stats",
                "description": "See the bot's status from development to now",
            },
            "fr": {
                "name": "stats",
                "description": "Voir l'état du bot depuis le développement jusqu'à maintenant",
            },
            "de": {
                "name": "stats",
                "description": "Sehen Sie den Status des Bots von der Entwicklung bis jetzt",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def stats(self, ctx: Interaction):
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).stats(ctx, self.bot_version)
            return
        if ctx.locale.value == "de":
            await de.Info(self.bot).stats(ctx, self.bot_version)
            return
        await en.Info(self.bot).stats(ctx, self.bot_version)

    @Jeanne.command(
        description=T("userinfo_desc"),
        extras={
            "en": {
                "name": "userinfo",
                "description": "See the information of a member or yourself",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "userinfo",
                "description": "Voir les informations d'un membre ou de vous-même",
                "parameters": [
                    {"name": "member", "description": "Quel membre?", "required": False}
                ],
            },
            "de": {
                "name": "userinfo",
                "description": "Sehen Sie die Informationen eines Mitglieds oder von sich selbst",
                "parameters": [
                    {"name": "member", "description": "Welches Mitglied?", "required": False}
                ],
            },
        },
    )
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def userinfo(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        member = ctx.user if member is None else member
        await self.get_userinfo(ctx, member)

    @Jeanne.command(
        description=T("serverinfo_desc"),
        extras={
            "en": {
                "name": "serverinfo",
                "description": "Get information about this server",
            },
            "fr": {
                "name": "serverinfo",
                "description": "Obtenez des informations sur ce serveur",
            },
            "de": {
                "name": "serverinfo",
                "description": "Erhalten Sie Informationen über diesen Server",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def serverinfo(self, ctx: Interaction):
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).serverinfo(ctx)
            return
        if ctx.locale.value == "de":
            await de.Info(self.bot).serverinfo(ctx)
            return
        await en.Info(self.bot).serverinfo(ctx)

    @Jeanne.command(
        description=T("ping_desc"),
        extras={
            "en": {
                "name": "ping",
                "description": "Check how fast I respond to a command",
            },
            "fr": {
                "name": "ping",
                "description": "Vérifiez la rapidité de ma réponse à une commande",
            },
            "de": {
                "name": "ping",
                "description": "Überprüfen Sie, wie schnell ich auf einen Befehl reagiere",
            },
        },
    )
    @Jeanne.check(is_suspended)
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def ping(self, ctx: Interaction):
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).ping(ctx)
            return
        if ctx.locale.value == "de":
            await de.Info(self.bot).ping(ctx)
            return
        await en.Info(self.bot).ping(ctx)

    @Jeanne.command(
        description=T("serverbanner_desc"),
        extras={
            "en": {"name": "serverbanner", "description": "Get the server banner"},
            "fr": {
                "name": "serverbanner",
                "description": "Obtenez la bannière du serveur",
            },
            "de": {
                "name": "serverbanner",
                "description": "Holen Sie sich das Serverbanner",
            },
        },
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def serverbanner(self, ctx: Interaction):
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).serverbanner(ctx) 
            return
        if ctx.locale.value == "de":
            await de.Info(self.bot).serverbanner(ctx)
            return
        await en.Info(self.bot).serverbanner(ctx)

    @Jeanne.command(
        description=T("avatar_desc"),
        extras={
            "en": {
                "name": "avatar",
                "description": "See your avatar or another member's avatar",
                "parameters": [
                    {
                        "name": "member",
                        "description": "Which member?",
                        "required": False,
                    }
                ],
            },
            "fr": {
                "name": "avatar",
                "description": "Voir votre avatar ou l'avatar d'un autre membre",
                "parameters": [
                    {"name": "member", "description": "Quel membre?", "required": False}
                ],
            },
            "de": {
                "name": "avatar",
                "description": "Sehen Sie Ihr Avatar oder das Avatar eines anderen Mitglieds",
                "parameters": [
                    {"name": "member", "description": "Welches Mitglied?", "required": False}
                ],
            },
        },
    )
    @Jeanne.describe(member=T("member_parm_desc"))
    @Jeanne.rename(member=T("member_parm_name"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def avatar(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).avatar(ctx, member)      
            return
        if ctx.locale.value == "de":
            await de.Info(self.bot).avatar(ctx, member)
            return
        await en.Info(self.bot).avatar(ctx, member)

    @Jeanne.command(
        description=T("sticker_desc"),
        extras={
            "en": {
                "name": "sticker",
                "description": "Views a sticker",
                "parameters": [
                    {
                        "name": "sticker",
                        "description": "Insert message ID with the sticker or name of the sticker in the server",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "sticker",
                "description": "Voir un sticker",
                "parameters": [
                    {
                        "name": "sticker",
                        "description": "Insérez l'ID du message avec le sticker ou le nom du sticker dans le serveur",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "sticker",
                "description": "Siehe einen Sticker",
                "parameters": [
                    {
                        "name": "sticker",
                        "description": "Fügen Sie die Nachrichten-ID mit dem Sticker oder den Namen des Stickers im Server ein",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(
        sticker=T("sticker_parm_desc"),
    )
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def sticker(self, ctx: Interaction, sticker: str):
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).sticker(ctx, sticker)      
            return
        if ctx.locale.value == "de":
            await de.Info(self.bot).sticker(ctx, sticker)
            return
        await en.Info(self.bot).sticker(ctx, sticker)

    @sticker.error
    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, IndexError
        ):
            if ctx.locale.value == "fr":
                await fr.Info(self.bot).sticker_error(ctx, error, "NoSticker")
                return
            if ctx.locale.value == "de":
                await de.Info(self.bot).sticker_error(ctx, error, "NoSticker")
            await en.Info(self.bot).sticker_error(ctx, error, "NoSticker")
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            if ctx.locale.value == "de":
                await de.Info(self.bot).sticker_error(ctx, error, "StickerNotFound")
                return
            if ctx.locale.value == "fr":
                await fr.Info(self.bot).sticker_error(ctx, error, "StickerNotFound")
                return
            await en.Info(self.bot).sticker_error(ctx, error, "StickerNotFound")

    @Jeanne.command(
        description=T("emoji_desc"),
        extras={
            "en": {
                "name": "emoji",
                "description": "View an emoji",
                "parameters": [
                    {
                        "name": "emoji",
                        "description": "Insert the emoji name or ID",
                        "required": True,
                    }
                ],
            },
            "fr": {
                "name": "emoji",
                "description": "Voir un emoji",
                "parameters": [
                    {
                        "name": "emoji",
                        "description": "Insérez le nom ou l'ID de l'emoji",
                        "required": True,
                    }
                ],
            },
            "de": {
                "name": "emoji",
                "description": "Siehe ein Emoji",
                "parameters": [
                    {
                        "name": "emoji",
                        "description": "Fügen Sie den Namen oder die ID des Emojis ein",
                        "required": True,
                    }
                ],
            },
        },
    )
    @Jeanne.describe(emoji=T("emoji_parm_desc"))
    @Jeanne.check(check_botbanned_app_command)
    @Jeanne.check(check_disabled_app_command)
    @Jeanne.check(is_suspended)
    async def emoji(self, ctx: Interaction, emoji: str):
        if ctx.locale.value == "de":
            await de.Info(self.bot).emoji(ctx, emoji)
            return
        if ctx.locale.value == "fr":
            await fr.Info(self.bot).emoji(ctx, emoji)
            return
        await en.Info(self.bot).emoji(ctx, emoji)

    @emoji.error
    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandInvokeError) and isinstance(
            error.original, AttributeError
        ):
            if ctx.locale.value == "de":
                await de.Info(self.bot).emoji_error(ctx, error)
                return
            if ctx.locale.value == "fr":
                await fr.Info(self.bot).emoji_error(ctx, error)
                return
            await en.Info(self.bot).emoji_error(ctx, error)


async def setup(bot: Bot):
    await bot.add_cog(InfoCog(bot))
