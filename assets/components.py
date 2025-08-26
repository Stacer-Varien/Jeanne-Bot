from functools import partial
from os import listdir
from discord import (
    CategoryChannel,
    File,
    Member,
    Message,
    ui,
    ButtonStyle,
    Interaction,
    User,
    SelectOption,
    AllowedMentions,
    Color,
    Embed,
    SyncWebhook,
    TextChannel,
    TextStyle,
    utils,
)
from typing import Optional
from collections import OrderedDict
from json import loads
from discord.ext.commands import Context, Bot
from assets.generators.profile_card import Profile
from config import WEBHOOK, BADGES
from functions import DevPunishment, Inventory, Levelling, Manage, Moderation, Welcomer


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Confirmation(ui.View):
    def __init__(self, ctx: Interaction, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            label_confirm = "Confirm"
            label_cancel = "Cancel"
        elif ctx.locale.value == "fr":
            label_confirm = "Confirmer"
            label_cancel = "Annuler"
        elif ctx.locale.value == "de":
            label_confirm = "Bestätigen"
            label_cancel = "Abbrechen"

        confirm_button = ui.Button(label=label_confirm, style=ButtonStyle.green)
        cancel_button = ui.Button(label=label_cancel, style=ButtonStyle.red)

        async def confirm_callback(ctx: Interaction):
            await self.confirm(ctx, confirm_button)

        async def cancel_callback(ctx: Interaction):
            await self.cancel(ctx, cancel_button)

        confirm_button.callback = confirm_callback
        cancel_button.callback = cancel_callback

        self.add_item(confirm_button)
        self.add_item(cancel_button)

    async def confirm(self, ctx: Interaction, button: ui.Button):
        self.value = True
        button.disabled = True
        self.stop()

    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = False
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Heads_or_Tails(ui.View):
    def __init__(self, ctx: Interaction, author: User):
        self.author = author
        super().__init__(timeout=30)
        self.value = None

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.heads = "Heads"
            self.tails = "Tails"
        elif ctx.locale.value == "fr":
            self.heads = "Face"
            self.tails = "Pile"
        elif ctx.locale.value == "de":
            self.heads = "Kopf"
            self.tails = "Zahl"

        heads = ui.Button(label=self.heads, style=ButtonStyle.green)
        tails = ui.Button(label=self.tails, style=ButtonStyle.red)
        heads.callback = lambda ctx: self.button_callback(ctx, self.heads)
        tails.callback = lambda ctx: self.button_callback(ctx, self.tails)
        self.add_item(heads)
        self.add_item(tails)

    async def button_callback(self, ctx: Interaction, label: str):
        self.value = label
        for child in self.children:
            child.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Welcomingmsg(ui.Modal, title="Welcoming Message"):
    def __init__(self, ctx: Interaction) -> None:
        super().__init__()

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "fr":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "de":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Fügen Sie hier ein JSON-Skript ein. Wenn Sie keines haben, geben Sie eine einfache Nachricht ein, solange sie den Parametern entspricht",
                required=True,
                min_length=1,
                max_length=4000,
            )
        self.add_item(self.jsonscript)

    async def on_submit(self, ctx: Interaction) -> None:
        humans = str(len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%members%", str(ctx.guild.member_count)),
                ("%humans%", str(humans)),
                ("%icon%", str(ctx.guild.icon)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except Exception:
            content = replace_all(self.jsonscript.value, parameters)
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            confirm = Embed(
                description="This is the preview of the welcoming message.\nAre you happy with it?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_welcomer_msg(self.jsonscript.value)
                embed = Embed(description="Welcoming message set")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "fr":
            confirm = Embed(
                description="Ceci est l'aperçu du message de bienvenue.\nÊtes-vous satisfait?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_welcomer_msg(self.jsonscript.value)
                embed = Embed(description="Message de bienvenue défini")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action annulée")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Temps écoulé")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "de":
            confirm = Embed(
                description="Dies ist die Vorschau der Willkommensnachricht.\nSind Sie damit zufrieden?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_welcomer_msg(self.jsonscript.value)
                embed = Embed(description="Willkommensnachricht festgelegt")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Aktion abgebrochen")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Zeitüberschreitung")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )


class Leavingmsg(ui.Modal, title="Leaving Message"):
    def __init__(self, ctx: Interaction) -> None:
        super().__init__()

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "fr":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insérez un script JSON ici. Si vous n'en avez pas, tapez un message simple tant qu'il respecte les paramètres",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "de":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Fügen Sie hier ein JSON-Skript ein. Wenn Sie keines haben, geben Sie eine einfache Nachricht ein, solange sie den Parametern entspricht",
                required=True,
                min_length=1,
                max_length=4000,
            )
        self.add_item(self.jsonscript)

    async def on_submit(self, ctx: Interaction) -> None:
        humans = str(len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%members%", str(ctx.guild.member_count)),
                ("%humans%", str(humans)),
                ("%icon%", str(ctx.guild.icon)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except Exception:
            content = replace_all(self.jsonscript.value, parameters)
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            confirm = Embed(
                description="This is the preview of the leaving message.\nAre you happy with it?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_leaving_msg(self.jsonscript.value)
                embed = Embed(description="Leaving message set")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "fr":
            confirm = Embed(
                description="Ceci est l'aperçu du message de départ.\nÊtes-vous satisfait?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_leaving_msg(self.jsonscript.value)
                embed = Embed(description="Message de départ défini")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action annulée")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Temps écoulé")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "de":
            confirm = Embed(
                description="Dies ist die Vorschau der Abschiedsnachricht.\nSind Sie damit zufrieden?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_leaving_msg(self.jsonscript.value)
                embed = Embed(description="Abschiedsnachricht festgelegt")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Aktion abgebrochen")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Zeitüberschreitung")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )


class Levelmsg(ui.Modal, title="Level Update Message"):
    def __init__(self, ctx: Interaction, channel: TextChannel) -> None:
        super().__init__()
        self.channel = channel

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
                required=True,
                min_length=1,
                max_length=4000,
            )

        elif ctx.locale.value == "fr":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insérez un script JSON ici. Si vous n'en avez pas, tapez un message simple tant qu'il respecte les paramètres",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "de":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Fügen Sie hier ein JSON-Skript ein. Wenn Sie keines haben, geben Sie eine einfache Nachricht ein, solange sie den Parametern entspricht",
                required=True,
                min_length=1,
                max_length=4000,
            )
        self.add_item(self.jsonscript)

    async def on_submit(self, ctx: Interaction) -> None:
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%newlevel%", str(Levelling(ctx.user, ctx.guild).get_member_level)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except Exception:
            content = replace_all(self.jsonscript.value, parameters)
        if ctx.locale.value == "en-US" or ctx.locale.value == "en-GB":
            confirm = Embed(
                description="This is the preview of the level update message whenever someone levels up in the server and will be sent to {}.\nAre you happy with it?".format(
                    self.channel.mention
                )
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(server=ctx.guild).add_level_channel(
                    self.channel, self.jsonscript.value
                )
                embed = Embed(description="Level update message set")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "fr":
            confirm = Embed(
                description="Ceci est l'aperçu du message de mise à jour de niveau chaque fois que quelqu'un monte de niveau dans le serveur et il sera envoyé dans {}.\nÊtes-vous satisfait?".format(
                    self.channel.mention
                )
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(server=ctx.guild).add_level_channel(
                    self.channel, self.jsonscript.value
                )
                embed = Embed(description="Message de mise à jour de niveau défini")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action annulée")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Temps écoulé")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "de":
            confirm = Embed(
                description="Dies ist die Vorschau der Nachricht, die gesendet wird, wenn jemand ein Level erreicht.\nSind Sie damit zufrieden?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(server=ctx.guild).add_level_channel(
                    self.channel, self.jsonscript.value
                )
                embed = Embed(description="Level update message set")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )


class RankUpmsg(ui.Modal, title="Role Reward Message"):
    def __init__(self, ctx: Interaction) -> None:
        super().__init__()

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "fr":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Insérez un script JSON ici. Si vous n'en avez pas, tapez un message simple tant qu'il respecte les paramètres",
                required=True,
                min_length=1,
                max_length=4000,
            )
        elif ctx.locale.value == "de":
            self.jsonscript = ui.TextInput(
                label="JSON",
                style=TextStyle.paragraph,
                placeholder="Fügen Sie hier ein JSON-Skript ein. Wenn Sie keines haben, geben Sie eine einfache Nachricht ein, solange sie den Parametern entspricht",
                required=True,
                min_length=1,
                max_length=4000,
            )
        self.add_item(self.jsonscript)

    async def on_submit(self, ctx: Interaction) -> None:
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%newlevel%", str(Levelling(ctx.user, ctx.guild).get_member_level)),
                ("%role%", str(ctx.user.top_role)),
                ("%rolemention%", str(ctx.user.top_role.mention)),
            ]
        )
        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except Exception:
            content = replace_all(self.jsonscript.value, parameters)
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            confirm = Embed(
                description="This is the preview of the role reward message whenever someone recieves a role reward after levelling up in the server and will be sent to the current level update channel\nAre you happy with it?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(server=ctx.guild).add_rankup_rolereward(
                    self.jsonscript.value
                )
                embed = Embed(description="Level update message set")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action cancelled")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Timeout")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "fr":
            confirm = Embed(
                description="Ceci est l'aperçu du message de récompense de rôle chaque fois que quelqu'un reçoit une récompense de rôle après avoir monté en niveau dans le serveur et sera envoyé au canal de mise à jour de niveau actuel\nÊtes-vous satisfait?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(server=ctx.guild).add_rankup_rolereward(
                    self.jsonscript.value
                )
                embed = Embed(description="Message de mise à jour du niveau défini")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Action annulée")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Temps écoulé")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
        elif ctx.locale.value == "de":
            confirm = Embed(
                description="Dies ist die Vorschau der Nachricht, die gesendet wird, wenn jemand ein Level erreicht.\nSind Sie damit zufrieden?"
            )
            view = Confirmation(ctx, ctx.user)
            try:
                embeds = [embed, confirm]
            except Exception:
                embeds = [confirm]
            await ctx.response.send_message(
                content=content,
                embeds=embeds,
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(server=ctx.guild).add_rankup_rolereward(
                    self.jsonscript.value
                )
                embed = Embed(description="Level-Update-Meldungssatz")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            elif not view.value:
                embed = Embed(description="Aktion abgebrochen")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )
            else:
                embed = Embed(description="Zeitüberschreitung")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )


class ModuleMenu(ui.Select):
    def __init__(
        self, ctx: Interaction, user: User, reason: str, duration: int
    ) -> None:
        self.modules = [
            "cogs.utilities",
            "cogs.fun",
            "cogs.image",
            "cogs.help",
            "cogs.hentai",
            "cogs.levelling",
            "cogs.currency",
            "cogs.reactions",
            "cogs.manage",
            "cogs.inventory",
            "cogs.moderation",
            "cogs.info",
        ]
        options = [SelectOption(label=module, value=module) for module in self.modules]
        super().__init__(
            placeholder="Select a module", max_values=12, min_values=1, options=options
        )
        self.reason = reason
        self.user = user
        self.duration = duration

    async def callback(self, ctx: Interaction):
        selected_modules = [i for i in self.values]
        await DevPunishment(self.user).suspend(
            duration=self.duration, reason=self.reason, modules=selected_modules
        )
        await ctx.message.edit(
            content="User has been suspended from the following modules: {}".format(
                ", ".join(selected_modules)
            ),
            view=None,
            embed=None,
            delete_after=5,
        )


class ModuleSelect(ui.View):
    def __init__(self, user: User, reason: str, duration: int):
        super().__init__(timeout=60)
        self.add_item(ModuleMenu(user, reason, duration))


class BotReportMenu(ui.Select):
    def __init__(self, ctx: Interaction) -> None:
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            options = [
                SelectOption(label="ToS Violator", value="violator"),
                SelectOption(label="Exploit", value="exploit"),
                SelectOption(label="Bug and/or Fault", value="bugorfault"),
                SelectOption(label="Illicit NSFW Content", value="illicit"),
                SelectOption(label="Translation Error", value="translation_error"),
                SelectOption(label="Other", value="other"),
            ]
            placeholder = "Select type of the report"
        elif ctx.locale.value == "fr":
            options = [
                SelectOption(label="Violation des CGU", value="violator"),
                SelectOption(label="Exploitation", value="exploit"),
                SelectOption(label="Bug et/ou défaut", value="bugorfault"),
                SelectOption(label="Contenu NSFW illicite", value="illicit"),
                SelectOption(label="Erreur de traduction", value="translation_error"),
                SelectOption(label="Autre", value="other"),
            ]
            placeholder = "Sélectionnez le type du rapport"
        elif ctx.locale.value == "de":
            options = [
                SelectOption(label="ToS-Verletzer", value="violator"),
                SelectOption(label="Ausnutzung", value="exploit"),
                SelectOption(label="Fehler und/oder Mangel", value="bugorfault"),
                SelectOption(label="Illegale NSFW-Inhalte", value="illicit"),
                SelectOption(label="Übersetzungsfehler", value="translation_error"),
                SelectOption(label="Sonstiges", value="other"),
            ]
            placeholder = "Wählen Sie den Typ des Berichts"

        super().__init__(
            placeholder=placeholder,
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, ctx: Interaction):

        await ctx.response.send_modal(ReportModal(self.options[0].label))
        try:
            await ctx.message.delete()
        except Exception:
            pass


class BotReportSelect(ui.View):
    def __init__(self, ctx: Interaction):
        self.value = None
        super().__init__(timeout=60)
        self.add_item(BotReportMenu(ctx))


class ReportModal(ui.Modal, title="Bot Report"):
    def __init__(self, ctx: Interaction, type_of_report: str):
        self.type = type_of_report
        super().__init__()

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if self.type == "Translation Error":
                self.lang = ui.TextInput(
                    label="Language",
                    required=True,
                    min_length=2,
                    max_length=2000,
                    placeholder="Type the language here",
                )
                self.incorrect = ui.TextInput(
                    label="Incorrect Translation",
                    required=True,
                    min_length=2,
                    max_length=2000,
                    placeholder="Type the incorrect translation here",
                )
                self.correct = ui.TextInput(
                    label="Correct Translation",
                    required=True,
                    min_length=2,
                    max_length=2000,
                    placeholder="Type the correct translation here",
                )
                self.add_item(self.lang)
                self.add_item(self.incorrect)
                self.add_item(self.correct)
            else:
                self.report = ui.TextInput(
                    label="Problem",
                    placeholder="Type the problem here",
                    required=True,
                    min_length=10,
                    max_length=2000,
                    style=TextStyle.paragraph,
                )
                self.steps = ui.TextInput(
                    label="Steps of how you got this problem",
                    placeholder="Type the steps here",
                    required=False,
                    min_length=10,
                    max_length=1024,
                    style=TextStyle.paragraph,
                )
        elif ctx.locale.value == "fr":
            if self.type == "Translation Error":
                self.lang = ui.TextInput(
                    label="Langue",
                    required=True,
                    min_length=2,
                    max_length=2000,
                    placeholder="Tapez la langue ici",
                )
                self.incorrect = ui.TextInput(
                    label="Traduction incorrecte",
                    required=True,
                    min_length=2,
                    max_length=2000,
                    placeholder="Tapez la traduction incorrecte ici",
                )
                self.correct = ui.TextInput(
                    label="Traduction correcte",
                    required=True,
                    min_length=2,
                    max_length=2000,
                    placeholder="Tapez la traduction correcte ici",
                )
                self.add_item(self.lang)
                self.add_item(self.incorrect)
                self.add_item(self.correct)
            else:
                self.report = ui.TextInput(
                    label="Problème",
                    placeholder="Tapez le problème ici",
                    required=True,
                    min_length=10,
                    max_length=2000,
                    style=TextStyle.paragraph,
                )
                self.steps = ui.TextInput(
                    label="Étapes pour reproduire le problème",
                    placeholder="Tapez les étapes ici",
                    required=False,
                    min_length=10,
                    max_length=1024,
                    style=TextStyle.paragraph,
                )
        elif ctx.locale.value == "de":
            self.report = ui.TextInput(
                label="Problem",
                placeholder="Beschreiben Sie das Problem hier",
                required=True,
                min_length=10,
                max_length=2000,
                style=TextStyle.paragraph,
            )
            self.steps = ui.TextInput(
                label="Schritte zur Reproduktion des Problems",
                placeholder="Geben Sie die Schritte hier ein",
                required=False,
                min_length=10,
                max_length=1024,
                style=TextStyle.paragraph,
            )
        self.add_item(self.report)
        self.add_item(self.steps)

    async def on_submit(self, ctx: Interaction) -> None:
        if self.type == "Translation Error":
            report = Embed(title=self.type, color=Color.brand_red())
            report.add_field(name="Language", value=self.lang.value, inline=False)
            report.add_field(
                name="Incorrect Translation", value=self.incorrect.value, inline=False
            )
            report.add_field(
                name="Correct Translation", value=self.correct.value, inline=False
            )
        else:
            report = Embed(title=self.type, color=Color.brand_red())
            report.description = self.report.value
            if self.steps.value is not None or self.steps.value == "":
                report.add_field(name="Steps", value=self.steps.value, inline=False)
        report.set_footer(text="Reporter {}| `{}`".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            embed = Embed(
                description="Thank you for submitting your bot report. The developer will look into it but will not tell you the results.\n\nPlease know that your user ID has been logged if you are trolling around."
            )
        elif ctx.locale.value == "fr":
            embed = Embed(
                description="Merci d'avoir soumis votre rapport sur le bot. Le développeur l'examinera mais ne vous communiquera pas les résultats.\n\nVeuillez noter que votre identifiant utilisateur a été enregistré si vous envoyez de faux rapports."
            )
        elif ctx.locale.value == "de":
            embed = Embed(
                description="Vielen Dank für die Einreichung Ihres Bot-Berichts. Der Entwickler wird sich darum kümmern, Ihnen jedoch keine Ergebnisse mitteilen.\n\nBitte beachten Sie, dass Ihre Benutzer-ID protokolliert wurde, wenn Sie trollen."
            )

        await ctx.response.send_message(embed=embed, ephemeral=True)


class ForumGuildlines(ui.Modal, title=str):
    def __init__(self, name: str, ctx: Interaction, category: CategoryChannel = None):
        self.title = (
            "Forum Guideline"
            if (ctx.locale.value == "en-GB" or ctx.locale.value == "en-US")
            else "Directives du forum"
        )
        self.name = name
        self.category = category
        super().__init__(title=self.title)

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.guidelines = ui.TextInput(
                label="Guidelines",
                placeholder="Type here. Markdown supported",
                required=True,
                min_length=1,
                max_length=4000,
                style=TextStyle.paragraph,
            )
        elif ctx.locale.value == "fr":
            self.guidelines = ui.TextInput(
                label="Directives",
                placeholder="Tapez ici. Markdown pris en charge",
                required=True,
                min_length=1,
                max_length=4000,
                style=TextStyle.paragraph,
            )
        self.add_item(self.guidelines)

    async def on_submit(self, ctx: Interaction) -> None:
        embed = Embed()
        forum = await ctx.guild.create_forum(
            name=self.name, topic=self.guidelines.value
        )
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            embed.description = "{} has been created".format(forum.jump_url)
            embed.color = Color.random()
            if self.category:
                await forum.edit(category=self.category)
                embed.add_field(
                    name="Added into category", value=self.category.name, inline=True
                )
            await ctx.response.send_message(embed=embed)
        elif ctx.locale.value == "fr":
            embed.description = "{} a été créé".format(forum.jump_url)
            embed.color = Color.random()
            if self.category:
                await forum.edit(category=self.category)
                embed.add_field(
                    name="Ajouté dans la catégorie",
                    value=self.category.name,
                    inline=True,
                )
            await ctx.response.send_message(embed=embed)
        elif ctx.locale.value == "de":
            embed.description = "{} wurde erstellt".format(forum.jump_url)
            embed.color = Color.random()
            if self.category:
                await forum.edit(category=self.category)
                embed.add_field(
                    name="In Kategorie hinzugefügt",
                    value=self.category.name,
                    inline=True,
                )
            await ctx.response.send_message(embed=embed)


class ReportContentM(ui.Modal, title="Illicit Content Report"):
    def __init__(self, ctx: Interaction, link: str):
        self.link = link
        super().__init__()

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            self.illegalcontent = ui.TextInput(
                label="Reason",
                style=TextStyle.short,
                placeholder="Why are you reporting this link?",
                required=True,
                min_length=4,
                max_length=256,
            )
        elif ctx.locale.value == "fr":
            self.illegalcontent = ui.TextInput(
                label="Raison",
                style=TextStyle.short,
                placeholder="Pourquoi signalez-vous ce lien?",
                required=True,
                min_length=4,
                max_length=256,
            )
        elif ctx.locale.value == "de":
            self.illegalcontent = ui.TextInput(
                label="Grund",
                style=TextStyle.short,
                placeholder="Warum melden Sie diesen Link?",
                required=True,
                min_length=4,
                max_length=256,
            )

        self.add_item(self.illegalcontent)

    async def on_submit(self, ctx: Interaction) -> None:
        report = Embed(title="Illicit Content Reported", color=Color.brand_red())
        report.add_field(name="Link", value=self.link, inline=False)
        report.add_field(name="Reason", value=self.illegalcontent.value, inline=False)
        report.set_footer(text=f"Reporter: {ctx.user} | ID: `{ctx.user.id}`")
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            embed = Embed(
                description="Thank you for submitting the report. Your user ID has been logged for accountability."
            )

        elif ctx.locale.value == "fr":
            embed = Embed(
                description="Merci d'avoir soumis le rapport. Votre identifiant utilisateur a été enregistré à des fins de responsabilité."
            )
        elif ctx.locale.value == "de":
            embed = Embed(
                description="Vielen Dank für die Einreichung des Berichts. Ihre Benutzer-ID wurde zur Rechenschaftspflicht protokolliert."
            )
        await ctx.response.send_message(embed=embed, ephemeral=True)


class ReportContentPlus(ui.View):
    def __init__(
        self,
        ctx: Interaction,
        link1: Optional[str] = None,
        link2: Optional[str] = None,
        link3: Optional[str] = None,
        link4: Optional[str] = None,
    ):
        super().__init__(timeout=60)
        self.links = [link1, link2, link3, link4]
        self.value = None
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            labels = [
                "Report 1st Content",
                "Report 2nd Content",
                "Report 3rd Content",
                "Report 4th Content",
            ]
        elif ctx.locale.value == "fr":
            labels = [
                "Signaler le 1er contenu",
                "Signaler le 2ème contenu",
                "Signaler le 3ème contenu",
                "Signaler le 4ème contenu",
            ]
        elif ctx.locale.value == "de":
            labels = [
                "Inhalt 1 melden",
                "Inhalt 2 melden",
                "Inhalt 3 melden",
                "Inhalt 4 melden",
            ]
        for idx, (label, link) in enumerate(zip(labels, self.links)):
            if link:
                row = 1 if idx < 2 else 2
                button = ui.Button(label=label, style=ButtonStyle.grey, row=row)
                button.callback = self._make_callback(idx)
                self.add_item(button)

    def _make_callback(self, idx):
        async def callback(interaction: Interaction):
            self.value = f"report{idx+1}"
            for child in self.children:
                child.disabled = True
            await interaction.response.send_modal(
                ReportContentM(interaction, self.links[idx])
            )
            await interaction.edit_original_response(view=self)

        return callback


class ReportContent(ui.View):
    def __init__(self, ctx: Interaction, link: str):
        super().__init__(timeout=180)
        self.link = link
        self.value = None

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            label = "Report Content"
        elif ctx.locale.value == "fr":
            label = "Signaler le contenu"
        elif ctx.locale.value == "de":
            label = "Inhalt melden"

        report_button = ui.Button(label=label, style=ButtonStyle.grey)

        async def report1(interaction: Interaction):
            self.value = "report"
            await interaction.response.send_modal(
                ReportContentM(interaction, self.link)
            )

        report_button.callback = report1

        self.add_item(report_button)


class RemoveManage(ui.View):
    def __init__(self, ctx: Interaction, author: User):
        super().__init__(timeout=180)
        self.value = None
        self.author = author

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            labels = [
                "Welcoming Channel",
                "Greeting Message",
                "Leaving Channel",
                "Leaving Message",
                "Level Update Channel",
                "Level Update Message",
                "Role Reward Message",
                "Modlog",
            ]

        elif ctx.locale.value == "fr":
            labels = [
                "Canal de bienvenue",
                "Message de bienvenue",
                "Canal de départ",
                "Message de départ",
                "Canal de mise à jour de niveau",
                "Message de mise à jour de niveau",
                "Message de récompense de rôle",
                "Modlog",
            ]
        elif ctx.locale.value == "de":
            labels = [
                "Willkommenskanal",
                "Willkommensnachricht",
                "Verlassen-Kanal",
                "Verlassen-Nachricht",
                "Level-Update-Kanal",
                "Level-Update-Nachricht",
                "Rollenbelohnungsnachricht",
                "Modlog",
            ]

        welcomer_button = ui.Button(label=labels[0], style=ButtonStyle.gray, row=1)
        greeting_button = ui.Button(label=labels[1], style=ButtonStyle.gray, row=1)
        leaving_buttion = ui.Button(label=labels[2], style=ButtonStyle.gray, row=1)
        bye_button = ui.Button(label=labels[3], style=ButtonStyle.gray, row=1)
        levelup_button = ui.Button(label=labels[4], style=ButtonStyle.gray, row=2)
        levelupdate_button = ui.Button(label=labels[5], style=ButtonStyle.gray, row=2)
        rolereward_button = ui.Button(label=labels[6], style=ButtonStyle.gray, row=2)
        modlog_button = ui.Button(label=labels[7], style=ButtonStyle.gray, row=2)

        async def welcomer_callback(ctx: Interaction):
            await self.welcomer(ctx, welcomer_button)

        async def greeting_callback(ctx: Interaction):
            await self.welcomemsg(ctx, greeting_button)

        async def leaving_callback(ctx: Interaction):
            await self.leaving(ctx, leaving_buttion)

        async def bye_callback(ctx: Interaction):
            await self.leavingmsg(ctx, bye_button)

        async def levelup_callback(ctx: Interaction):
            await self.level(ctx, levelup_button)

        async def levelupdate_callback(ctx: Interaction):
            await self.levelupdate(ctx, levelupdate_button)

        async def rolereward_callback(ctx: Interaction):
            await self.rolereward(ctx, rolereward_button)

        async def modlog_callback(ctx: Interaction):
            await self.modlog(ctx, modlog_button)

        welcomer_button.callback = welcomer_callback
        greeting_button.callback = greeting_callback
        leaving_buttion.callback = leaving_callback
        bye_button.callback = bye_callback
        levelup_button.callback = levelup_callback
        levelupdate_button.callback = levelupdate_callback
        rolereward_button.callback = rolereward_callback
        modlog_button.callback = modlog_callback

        self.add_item(welcomer_button)
        self.add_item(greeting_button)
        self.add_item(leaving_buttion)
        self.add_item(bye_button)
        self.add_item(levelup_button)
        self.add_item(levelupdate_button)
        self.add_item(rolereward_button)
        self.add_item(modlog_button)

    async def welcomer(self, ctx: Interaction, button: ui.Button):
        self.value = "welcomer"
        Embed()
        check = Welcomer(ctx.guild).get_welcomer
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.label = "No welcoming channel found"
                button.style = ButtonStyle.danger
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            await Manage(ctx.guild).remove_welcomer()
            button.label = "Welcomer Channel Removed"
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.label = "Aucun canal de bienvenue trouvé"
                button.style = ButtonStyle.danger
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            await Manage(ctx.guild).remove_welcomer()
            button.label = "Canal de bienvenue supprimé"
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.label = "Kein Willkommenskanal gefunden"
                button.style = ButtonStyle.danger
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            await Manage(ctx.guild).remove_welcomer()
            button.label = "Willkommenskanal entfernt"
            await ctx.response.edit_message(view=self)

    async def welcomemsg(self, ctx: Interaction, button: ui.Button):
        self.value = "welcomemsg"
        check = Welcomer(ctx.guild).get_welcoming_msg
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No welcoming message set"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Welcoming Message Removed"
            await Manage(ctx.guild).remove_welcomemsg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun message de bienvenue défini"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Message de bienvenue supprimé"
            await Manage(ctx.guild).remove_welcomemsg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Willkommensnachricht gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Willkommensnachricht entfernt"
            await Manage(ctx.guild).remove_welcomemsg()
            await ctx.response.edit_message(view=self)

    async def leaving(self, ctx: Interaction, button: ui.Button):
        self.value = "leaver"
        check = Welcomer(ctx.guild).get_leaver
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No leaving channel found"
                await ctx.response.edit_message(view=self)
            else:
                button.style = ButtonStyle.green
                button.label = "Leaving Channel Removed"
                await Manage(ctx.guild).remove_leaver()
                await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun canal de départ trouvé"
                await ctx.response.edit_message(view=self)
            else:
                button.style = ButtonStyle.green
                button.label = "Canal de départ supprimé"
                await Manage(ctx.guild).remove_leaver()
                await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Verlassen-Kanal gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Verlassen-Kanal entfernt"
            await Manage(ctx.guild).remove_leaver()
            await ctx.response.edit_message(view=self)

    async def leavingmsg(self, ctx: Interaction, button: ui.Button):
        self.value = "leavingmsg"
        check = Welcomer(ctx.guild).get_leaving_msg
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No leaving message set"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Leaving Message Removed"
            await Manage(ctx.guild).remove_leavingmsg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun message de départ défini"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Message de départ supprimé"
            await Manage(ctx.guild).remove_leavingmsg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Verlassen-Nachricht gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Verlassen-Nachricht entfernt"
            await Manage(ctx.guild).remove_leavingmsg()
            await ctx.response.edit_message(view=self)

    async def level(self, ctx: Interaction, button: ui.Button):
        self.value = "levelup"
        check = Levelling(server=ctx.guild).get_levelup_channel
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No level update channel found"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Level Update Channel Removed"
            await Manage(ctx.guild).remove_levelup()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun canal de mise à jour de niveau trouvé"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Canal de mise à jour de niveau supprimé"
            await Manage(ctx.guild).remove_levelup()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Level-Update-Kanal gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Level-Update-Kanal entfernt"
            await Manage(ctx.guild).remove_levelup()
            await ctx.response.edit_message(view=self)

    async def levelupdate(self, ctx: Interaction, button: ui.Button):
        self.value = "levelnotif"
        check = Levelling(server=ctx.guild).get_levelup_msg
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No level update message set"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Level Update Message Removed"
            await Manage(ctx.guild).remove_levelup_msg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun message de mise à jour de niveau défini"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Message de mise à jour de niveau supprimé"
            await Manage(ctx.guild).remove_levelup_msg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Level-Update-Nachricht gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Level-Update-Nachricht entfernt"
            await Manage(ctx.guild).remove_levelup_msg()
            await ctx.response.edit_message(view=self)

    async def rolereward(self, ctx: Interaction, button: ui.Button):
        self.value = "rolereward"
        check = Levelling(server=ctx.guild).get_rank_up_update
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No role reward message set"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Role Reward Message Removed"
            await Manage(ctx.guild).remove_rolereward_msg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun message de récompense de rôle défini"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Message de récompense de rôle supprimé"
            await Manage(ctx.guild).remove_rolereward_msg()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Rollenbelohnungsnachricht gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Rollenbelohnungsnachricht entfernt"
            await Manage(ctx.guild).remove_rolereward_msg()
            await ctx.response.edit_message(view=self)

    async def modlog(self, ctx: Interaction, button: ui.Button):
        self.value = "modlog"
        check = Moderation(ctx.guild).get_modlog_channel
        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "No modlog found"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Modlog Removed"
            await Manage(ctx.guild).remove_modloger()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "fr":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Aucun modlog trouvé"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Modlog supprimé"
            await Manage(ctx.guild).remove_modloger()
            await ctx.response.edit_message(view=self)
        elif ctx.locale.value == "de":
            if check is None:
                button.style = ButtonStyle.danger
                button.label = "Kein Modlog gefunden"
                await ctx.response.edit_message(view=self)
                return
            button.style = ButtonStyle.green
            button.label = "Modlog entfernt"
            await Manage(ctx.guild).remove_modloger()
            await ctx.response.edit_message(view=self)

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class RolesButton(ui.View):
    def __init__(self, ctx: Interaction, member: User, Uinfo: Embed, Roles: list[str]):
        super().__init__(timeout=60)
        self.value = None
        self.member = member
        self.Roles = Roles
        self.Uinfo = Uinfo

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            label = "Roles"
        elif ctx.locale.value == "fr":
            label = "Rôles"
        elif ctx.locale.value == "de":
            label = "Rollen"

        roles_button = ui.Button(label=label, style=ButtonStyle.blurple)

        async def roles_callback(ctx: Interaction):
            await self.roles(ctx, roles_button)

        roles_button.callback = roles_callback
        self.add_item(roles_button)

    async def roles(self, ctx: Interaction, button: ui.Button):
        self.value = "roles"
        roles = Embed(
            title="{}'s roles".format(self.member),
            description=" ".join(self.Roles) + " @everyone",
            color=self.member.color,
        )
        await ctx.response.edit_message(embeds=[self.Uinfo, roles], view=None)
        self.stop()


class Guess_Buttons(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

        for i in range(1, 11):
            button = ui.Button(label=str(i), style=ButtonStyle.grey)
            button.callback = partial(self.button_callback, number=i)
            self.add_item(button)

    async def button_callback(self, ctx: Interaction, number: int):
        self.value = number
        for child in self.children:
            child.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Dice_Buttons(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

        for i in range(1, 7):
            row = 0 if i <= 3 else 1
            button = ui.Button(label=str(i), style=ButtonStyle.grey, row=row)
            button.callback = partial(self.button_callback, number=i)
            self.add_item(button)

    async def button_callback(self, ctx: Interaction, number: int):
        self.value = number
        for child in self.children:
            child.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


async def buy_function_context(bot: Bot, ctx: Context, name: str, message: Message):
    image_url = Inventory().get_wallpaper(name)[2]
    if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
        m = await message.edit(
            embed=Embed(
                description="Creating preview... This will take some time <a:loading:1161038734620373062>"
            ),
            view=None,
        )
        image = await Profile(bot).generate_profile(
            ctx, ctx.author, image_url, True, True, "southafrica"
        )
        file = File(fp=image, filename="preview_profile_card.png")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.random(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
        )
        view = Confirmation(ctx.author)
        m = await m.edit(attachments=[file], embed=preview, view=view)
        await view.wait()

        if view.value:
            await Inventory(ctx.author).add_user_wallpaper(name)
            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await m.edit(embed=embed1, view=None)
            return
        await m.edit(embed=Embed(description="Cancel"), view=None, attachments=[])
    elif ctx.locale.value == "fr":
        m = await message.edit(
            embed=Embed(
                description="Création de l'aperçu... Cela prendra un certain temps <a:loading:1161038734620373062>"
            ),
            view=None,
        )
        image = await Profile(bot).generate_profile(
            ctx, ctx.author, image_url, True, True, "southafrica"
        )
        file = File(fp=image, filename="preview_profile_card.png")
        preview = (
            Embed(
                description="Ceci est l'aperçu de la carte de profil.",
                color=Color.random(),
            )
            .add_field(name="Coût", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Est-ce le fond que vous vouliez?")
        )
        view = Confirmation(ctx.author)
        m = await m.edit(attachments=[file], embed=preview, view=view)
        await view.wait()

        if view.value:
            await Inventory(ctx.author).add_user_wallpaper(name)
            embed1 = Embed(
                description="Fond d'écran acheté et sélectionné",
                color=Color.random(),
            )
            await m.edit(embed=embed1, view=None)
            return
        await m.edit(embed=Embed(description="Annulé"), view=None, attachments=[])
    elif ctx.locale.value == "de":
        m = await message.edit(
            embed=Embed(
                description="Erstelle eine Vorschau... Dies wird einige Zeit in Anspruch nehmen <a:loading:1161038734620373062>"
            ),
            view=None,
        )
        image = await Profile(bot).generate_profile(
            ctx, ctx.author, image_url, True, True, "southafrica"
        )
        file = File(fp=image, filename="preview_profile_card.png")
        preview = (
            Embed(
                description="Dies ist die Vorschau der Profilkarte.",
                color=Color.random(),
            )
            .add_field(name="Kosten", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Ist das der Hintergrund, den Sie wollten?")
        )
        view = Confirmation(ctx.author)
        m = await m.edit(attachments=[file], embed=preview, view=view)
        await view.wait()

        if view.value:
            await Inventory(ctx.author).add_user_wallpaper(name)
            embed1 = Embed(
                description="Hintergrundbild gekauft und ausgewählt",
                color=Color.random(),
            )
            await m.edit(embed=embed1, view=None)
            return
        await m.edit(embed=Embed(description="Abgebrochen"), view=None, attachments=[])


async def use_function_context(ctx: Context, name: str, message: Message):
    await Inventory(ctx.author).use_wallpaper(name)
    if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
        description = f"{name} has been selected"
    elif ctx.locale.value == "fr":
        description = f"{name} a été sélectionné"
    elif ctx.locale.value == "de":
        description = f"{name} wurde ausgewählt"
    embed = Embed(description=description, color=Color.random())
    await message.edit(embed=embed, view=None)


async def buy_function_app(bot: Bot, ctx: Interaction, name: str):
    image_url = Inventory().get_wallpaper(name)[2]
    if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
        await ctx.edit_original_response(
            "Creating preview... This will take some time <a:loading:1161038734620373062>"
        )
        image = await Profile(bot).generate_profile(
            ctx, ctx.user, image_url, True, True, "southafrica"
        )
        file = File(fp=image, filename="preview_profile_card.png")
        preview = (
            Embed(
                description="This is the preview of the profile card.",
                color=Color.random(),
            )
            .add_field(name="Cost", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Is this the background you wanted?")
        )
        view = Confirmation(ctx, ctx.user)
        await ctx.edit_original_response(
            content=None, attachments=[file], embed=preview, view=view
        )
        await view.wait()
        if view.value is None:
            await ctx.edit_original_response(
                content="Timeout", view=None, embed=None, attachments=[]
            )
            return
        if view.value:
            await Inventory(ctx.user).add_user_wallpaper(name)
            embed1 = Embed(
                description="Background wallpaper bought and selected",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None)
        else:
            await ctx.edit_original_response(
                content="Cancelled", view=None, embed=None, attachments=[]
            )
    elif ctx.locale.value == "fr":
        await ctx.edit_original_response(
            "Création de l'aperçu... Cela prendra un certain temps <a:loading:1161038734620373062>"
        )
        image = await Profile(bot).generate_profile(
            ctx, ctx.user, image_url, True, True, "southafrica"
        )
        file = File(fp=image, filename="preview_profile_card.png")
        preview = (
            Embed(
                description="Ceci est l'aperçu de la carte de profil.",
                color=Color.random(),
            )
            .add_field(name="Coût", value="1000 <:quantumpiece:1161010445205905418>")
            .set_footer(text="Est-ce le fond que vous vouliez?")
        )
        view = Confirmation(ctx, ctx.user)
        await ctx.edit_original_response(
            content=None, attachments=[file], embed=preview, view=view
        )
        await view.wait()
        if view.value is None:
            await ctx.edit_original_response(
                content="Temps écoulé", view=None, embed=None, attachments=[]
            )
            return
        if view.value:
            await Inventory(ctx.user).add_user_wallpaper(name)
            embed1 = Embed(
                description="Fond d'écran acheté et sélectionné",
                color=Color.random(),
            )
            await ctx.edit_original_response(embed=embed1, view=None)
        else:
            await ctx.edit_original_response(
                content="Annulé", view=None, embed=None, attachments=[]
            )
    elif ctx.locale.value == "de":
        await ctx.edit_original_response(
            content="Abgebrochen", view=None, embed=None, attachments=[]
        )


async def use_function_app(ctx: Interaction, name: str):
    await Inventory(ctx.user).use_wallpaper(name)
    if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
        embed = Embed(description=f"{name} has been selected", color=Color.random())
        await ctx.edit_original_response(embed=embed, view=None)
    elif ctx.locale.value == "fr":
        embed = Embed(description=f"{name} a été sélectionné", color=Color.random())
        await ctx.edit_original_response(embed=embed, view=None)
    elif ctx.locale.value == "de":
        embed = Embed(description=f"{name} wurde ausgewählt", color=Color.random())
        await ctx.edit_original_response(embed=embed, view=None)


class TopicButton(ui.View):
    def __init__(
        self, ctx: Interaction, author: Member, name: str, category: CategoryChannel
    ):
        self.value = None
        self.author = author
        self.name = name
        self.category = category
        super().__init__(timeout=180)

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            label = "Add Guidelines"
        elif ctx.locale.value == "fr":
            label = "Ajouter des directives"
        elif ctx.locale.value == "de":
            label = "Richtlinien hinzufügen"

        guidelines_button = ui.Button(label=label)

        async def guidelines_callback(ctx: Interaction):
            await self.guidelines(guidelines_button, ctx)

        guidelines_button.callback = guidelines_callback
        self.add_item(guidelines_button)

    async def guidelines(self, button: ui.Button, ctx: Interaction):
        self.value = "guidelines"
        await ctx.response.send_modal(ForumGuildlines(self.name, ctx, self.category))

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class WelcomerSetButtons(ui.View):
    def __init__(self, ctx: Interaction, author: Member, message: Message):
        self.value = None
        self.author = author
        self.message = message
        super().__init__(timeout=180)

        if ctx.locale.value == "en-GB" or ctx.locale.value == "en-US":
            set_welcome_msg_label = "Set Welcoming Message"
            set_leaving_msg_label = "Set Leaving Message"
        elif ctx.locale.value == "fr":
            set_welcome_msg_label = "Définir le message de bienvenue"
            set_leaving_msg_label = "Définir le message d'adieu"
        elif ctx.locale.value == "de":
            set_welcome_msg_label = "Willkommensnachricht festlegen"
            set_leaving_msg_label = "Verabschiedungsnachricht festlegen"

        set_welcome_msg_button = ui.Button(
            label=set_welcome_msg_label, style=ButtonStyle.gray, row=1
        )
        set_leaving_msg_button = ui.Button(
            label=set_leaving_msg_label, style=ButtonStyle.gray, row=2
        )

        async def setwelcomemsg_callback(ctx: Interaction):
            await self.setwelcomemsg(set_welcome_msg_button, ctx)

        async def setleavingmsg_callback(ctx: Interaction):
            await self.setleavingmsg(set_leaving_msg_button, ctx)

        set_welcome_msg_button.callback = setwelcomemsg_callback
        set_leaving_msg_button.callback = setleavingmsg_callback

        self.add_item(set_welcome_msg_button)
        self.add_item(set_leaving_msg_button)

    async def setwelcomemsg(self, button: ui.Button, ctx: Interaction):
        self.value = "welcomemsg"
        await self.message.edit(view=self)
        await ctx.response.send_modal(Welcomingmsg(ctx))

    async def setleavingmsg(self, button: ui.Button, ctx: Interaction):
        self.value = "leavingmsg"
        await self.message.edit(view=self)
        await ctx.response.send_modal(Leavingmsg(ctx))

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Country_Badge_Buttons(ui.View):
    def __init__(self, bot: Bot, author: User):
        super().__init__(timeout=60)
        self.bot = bot
        self.author = author
        self.value = None

        folder_path = BADGES
        files = listdir(folder_path)
        badges = [i for i in files if i.endswith((".png"))]
        server = self.bot.get_guild(913051824095916142)
        for i in badges:
            emoji = utils.find(lambda m: m.name == i[:-4], server.emojis)
            button = ui.Button(label=emoji.name, style=ButtonStyle.green, emoji=emoji)
            button.callback = partial(self.button_callback, cbadge=emoji.name)
            self.add_item(button)

    async def button_callback(self, ctx: Interaction, cbadge: str):
        self.value = cbadge
        for child in self.children:
            child.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class DevWarningReasonM(ui.Modal, title="Reason of Warn/Suspension"):
    def __init__(self, user: User, type: str):
        self.user = user
        self.type = type
        super().__init__()

    explaination = ui.TextInput(
        label="Reason",
        style=TextStyle.long,
        required=True,
        min_length=4,
        max_length=1024,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        embed = Embed(title="Warning from Developer", color=Color.brand_red())
        embed.add_field(name="Reason of Warn", value=self.type, inline=False)
        embed.add_field(name="Explanation", value=self.explaination.value, inline=False)
        warnings = ...
        if warnings == 1:
            embed.set_footer(
                text="This is your first warning. There is no serious punishment for it and it will last for 90 days if you are on good behaviour."
            )
        if warnings == 2:
            embed.set_footer(
                text="This is your second warning. You will be given a 7 day suspension from using Jeanne. This warning will last for 180 days if you are on good behaviour."
            )
        if warnings == 3:
            embed.set_footer(
                text="This is your third and last warning! You are PERMANENTLY BANNED from using Jeanne!"
            )
            await DevPunishment(self.user).add_botbanned_user(
                f"Received 3 warnings due to this final warning\n**{self.type}**\n{self.explaination}"
            )

        try:
            await self.user.send(embed=embed)
            confirm = Embed(
                description=f"Warning sent to {self.user} | `{self.user.id}`"
            )
            await ctx.response.send_message(embed=confirm, ephemeral=True)
        except Exception:
            confirm = Embed(
                description=f"Warning given to {self.user} | `{self.user.id}` but not sent as their DMs are closed"
            )
            await ctx.response.send_message(embed=confirm, ephemeral=True)


class DevWarningMenu(ui.Select):
    def __init__(self) -> None:
        options = [
            SelectOption(label="Multiple False Reports", value="falsereports"),
            SelectOption(label="Violating Bot ToS", value="violate"),
            SelectOption(label="Attempting to appeal", value="appeal"),
            SelectOption(label="Other", value="other"),
        ]
        super().__init__(
            placeholder="Select type",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, ctx: Interaction, user: User):

        await ctx.response.send_modal(DevWarningReasonM(user, self.options[0].label))
        try:
            await ctx.message.delete()
        except Exception:
            pass
