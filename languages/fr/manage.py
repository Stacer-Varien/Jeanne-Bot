from typing import Literal, Optional
from json import loads
from discord import (
    AllowedMentions,
    Attachment,
    CategoryChannel,
    Color,
    Embed,
    File,
    GuildSticker,
    HTTPException,
    Interaction,
    User,
    Role,
    StageChannel,
    TextChannel,
    VerificationLevel,
    VoiceChannel,
    app_commands as Jeanne,
    abc,
    utils,
)
from PIL import ImageColor
from discord.ext.commands import Bot
from humanfriendly import format_timespan, parse_timespan, InvalidTimespan
from collections import OrderedDict
from functions import (
    Command,
    Inventory,
    Levelling,
    Manage,
)
from assets.components import (
    Confirmation,
    Levelmsg,
    RemoveManage,
    Welcomingmsg,
    Leavingmsg,
    ForumGuildlines,
    RankUpmsg,
)
from requests import get
from io import BytesIO


class Create_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def textchannel(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        topic: Optional[Jeanne.Range[str, 1, 1024]] = None,
        category: Optional[CategoryChannel] = None,
        slowmode: str = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        name = "new-channel" if name is None else name
        channel = await ctx.guild.create_text_channel(name=name)
        embed = Embed()
        embed.color = Color.random()
        embed.description = "{} a été créé".format(channel.jump_url)
        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Ajouté dans la catégorie", value=category.name, inline=True
            )
        if topic:
            await channel.edit(topic=topic)
            embed.add_field(name="Sujet", value=topic, inline=True)
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Mode lent", value=added_slowmode, inline=True)
        if nsfw_enabled:
            embed.add_field(name="NSFW", value="Oui", inline=True)
            await channel.edit(nsfw=True)
        await ctx.followup.send(embed=embed)


    async def voicechannel(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 99]] = None,
    ) -> None:
        await ctx.response.defer()
        name = "new-channel" if name is None else name
        channel = await ctx.guild.create_voice_channel(name=name)
        embed = Embed()
        embed.description = "{} a été créé".format(channel.jump_url)
        embed.color = Color.random()
        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Ajouté dans la catégorie", value=category.name, inline=True
            )
        if users:
            await channel.edit(user_limit=users)
            embed.add_field(name="Limite d'utilisateurs", value=users, inline=True)
        await ctx.followup.send(embed=embed)


    async def category(self, ctx: Interaction, name: Jeanne.Range[str, 1, 100]):
        await ctx.response.defer()
        cat = await ctx.guild.create_category(name=name)
        embed = Embed()
        embed.description = "{} a été créé".format(cat.mention)
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)


    async def stagechannel(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 10000]] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        channel: StageChannel = await ctx.guild.create_stage_channel(name=name)
        embed.description = "{} a été créé".format(channel.jump_url)
        if category:
            await channel.edit(category=category)
            embed.add_field(
                name="Déplacé dans la catégorie", value=category.mention, inline=True
            )
        if users:
            await channel.edit(user_limit=users)
            embed.add_field(name="Utilisateurs", value=users, inline=True)
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)


    async def stagechannel_error(self, ctx: Interaction):
            embed = Embed()
            embed.description = "Impossible de créer un nouveau salon de scène. Veuillez vérifier que le serveur est activé pour la communauté"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)


    async def forum(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        category: Optional[CategoryChannel] = None,
        topic: Optional[bool] = None,
    ):
        if topic:
            await ctx.response.send_modal(ForumGuildlines(name, ctx, category))
            return
        await ctx.response.defer()
        embed = Embed()
        forum = await ctx.guild.create_forum(name=name, topic=topic)
        embed.description = "{} a été créé".format(forum.jump_url)
        embed.color = Color.random()
        if category:
            await forum.edit(category=category)
            embed.add_field(
                name="Ajouté dans la catégorie", value=category.name, inline=True
            )
        await ctx.followup.send(embed=embed)


    async def forum_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            embed = Embed()
            embed.description = "Impossible de créer un nouveau forum. Veuillez vérifier que le serveur est activé pour la communauté"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)


    async def role(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, None, 100],
        color: Optional[Jeanne.Range[str, None, 6]] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        role = await ctx.guild.create_role(name=name)
        embed = Embed()
        embed.description = "Le rôle `{}` a été créé".format(name)
        if color is not None:
            try:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Couleur", value=color, inline=True)
                embed.color = role.color
            except Exception:
                embed.add_field(name="Couleur", value="Invalid color code", inline=True)
        else:
            embed.color = Color.random()
        if hoisted:
            if hoisted:
                await role.edit(hoist=True)
                embed.add_field(name="Mis en avant", value="Oui", inline=True)
            elif not hoisted:
                embed.add_field(name="Mis en avant", value="No", inline=True)
        if mentionable:
            if mentionable:
                await role.edit(mentionable=True)
                embed.add_field(name="Mentionnable", value="Oui", inline=True)
            elif not mentionable:
                embed.add_field(name="Mentionnable", value="No", inline=True)
        await ctx.followup.send(embed=embed)

    async def public(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        channel: TextChannel,
        message_id: str,
        slowmode: Optional[str] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        embed.add_field(name="Canal", value=channel.jump_url, inline=True)
        message = await channel.fetch_message(int(message_id))
        thread = await channel.create_thread(name=name, message=message)
        embed.add_field(name="Trouvé dans le message", value=message.jump_url, inline=True)
        await thread.add_user(ctx.user)
        embed.description = "{} a été créé".format(thread.jump_url)
        embed.color = Color.random()
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Mode lent", value=added_slowmode, inline=True)
        await ctx.followup.send(embed=embed)

    async def public_thread_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError, type:Literal["NotFound", "Failed"]
    ):
        if type == "NotFound":
            embed = Embed()
            embed.description = "Le message n'a pas pu être trouvé. Veuillez vérifier que vous avez ajouté l'ID de message correct"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return
        if type == "Failed":
            embed = Embed()
            embed.description = "Échec de la création du fil public. Veuillez réessayer"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    async def private(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 1, 100],
        channel: TextChannel,
        slowmode: Optional[str] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        embed.add_field(name="Canal", value=channel.jump_url, inline=True)
        thread = await channel.create_thread(name=name)
        await thread.add_user(ctx.user)
        embed.description = "{} a été créé".format(thread.jump_url)
        embed.color = Color.random()
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Mode lent", value=added_slowmode, inline=True)
        await ctx.followup.send(embed=embed)

    async def private_thread_error(
        self, ctx: Interaction):
            embed = Embed()
            embed.description = "Échec de la création du fil privé. Veuillez réessayer"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)

    async def emoji(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 2, 30],
        emoji_link: Optional[str] = None,
        emoji_image: Optional[Attachment] = None,
    ):
        await ctx.response.defer()
        embed = Embed()
        if emoji_link is None and emoji_image is None:
            embed.description = "Veuillez ajouter soit une URL d'emoji, soit une image d'emoji"
            embed.color = Color.red()
        elif emoji_link and emoji_image:
            embed.description = "Veuillez utiliser soit une URL d'emoji, soit une image d'emoji"
            embed.color = Color.red()
        else:
            emojibytes = get(emoji_link if emoji_link else emoji_image.url).content
            emote = await ctx.guild.create_custom_emoji(
                name=name.replace(" ", "_"), image=emojibytes
            )
            embed.description = "{} | {} a été créé".format(
                emote.name, str(emote)
            )
            embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    async def emoji_error(self, ctx: Interaction, error: Jeanne.errors.AppCommandError):
            a_emojis = len(
                [emote for emote in ctx.guild.emojis if emote.animated]
            )
            emojis = len(
                [emote for emote in ctx.guild.emojis if not emote.animated]
            )
            limit = 50 + (50 * ctx.guild.premium_tier)
            if HTTPException:
                embed = Embed(color=Color.red())
                if a_emojis == limit or emojis == limit:
                    embed.description = "Vous avez atteint la limite maximale d'emojis"
                else:
                    embed.description = "Il y a eu un problème lors de la création de l'emoji. Veuillez vérifier que l'emoji que vous créez est un PNG, JPEG ou GIF"
                await ctx.followup.send(embed=embed)

    async def sticker(
        self,
        ctx: Interaction,
        name: Jeanne.Range[str, 2, 30],
        emoji: str,
        sticker_link: Optional[str] = None,
        sticker_image: Optional[Attachment] = None,
    ):
        embed = Embed()
        if sticker_link is None and sticker_image is None:
            embed.description = "Veuillez ajouter soit une URL de sticker, soit une image de sticker"
            embed.color = Color.red()
        elif sticker_link and sticker_image:
            embed.description = "Veuillez utiliser soit une URL de sticker, soit une image de sticker"
            embed.color = Color.red()
        else:
            url = sticker_link if sticker_link else sticker_image.url
            stickerbytes = BytesIO(get(url).content)
            stickerfile = File(fp=stickerbytes, filename="sticker.png")
            sticker = await ctx.guild.create_sticker(
                name=name.lower(), description="None", emoji=emoji, file=stickerfile
            )
            embed.description = "{} a été créé".format(sticker.name)
            embed.color = Color.random()
            embed.set_image(url=url)
        await ctx.followup.send(embed=embed)

    async def sticker_error(
        self, ctx: Interaction
    ):
            embed = Embed(color=Color.red())
            embed.description = "Il y a eu un problème lors de la création du sticker. Veuillez vérifier que le sticker que vous créez respecte les conditions suivantes :\n\n1. 512kb ou moins\n2. Le fichier est au format PNG ou APNG\n3. L'emoji correct a été ajouté\n\nSi toutes les conditions sont remplies mais échouent toujours, cela signifie que vous avez atteint la limite des emplacements de stickers"
            await ctx.followup.send(embed=embed)


class Delete_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def channel(self, ctx: Interaction, channel: abc.GuildChannel):
        await ctx.response.defer()
        embed = Embed(
            description="{} a été supprimé".format(channel.name), color=Color.random()
        )
        await channel.delete()
        await ctx.followup.send(embed=embed)

    async def role(self, ctx: Interaction, role: Role):
        await ctx.response.defer()
        embed = Embed(
            description="{} a été supprimé".format(role.name), color=Color.random()
        )
        await role.delete()
        await ctx.followup.send(embed=embed)

    async def emoji(self, ctx: Interaction, emoji: str):
        await ctx.response.defer()
        try:
            e = emoji.strip().split(":")[-1].rstrip(">")
            emote = await ctx.guild.fetch_emoji(int(e))
        except Exception:
            emote = utils.get(ctx.guild.emojis, name=emoji.replace(" ", "_"))
        embed = Embed(
            description="{} a été supprimé".format(str(emote)), color=0x00FF68
        )
        await emote.delete()
        await ctx.followup.send(embed=embed)

    async def emoji_error(self, ctx: Interaction):
            embed = Embed(
                description="Cet emoji n'existe pas sur le serveur",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    async def sticker(self, ctx: Interaction, sticker: str):
        await ctx.response.defer()
        stick = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` a été supprimé".format(str(stick.name)), color=0x00FF68
        )
        await stick.delete()
        await ctx.followup.send(embed=embed)

    async def sticker_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
            embed = Embed(
                description="Ce sticker n'existe pas sur le serveur",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)


class Edit_Group():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def textchannel(
        self,
        ctx: Interaction,
        channel: Optional[TextChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        topic: Optional[Jeanne.Range[str, 1, 1024]] = None,
        slowmode: Optional[str] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        channel = ctx.channel if channel is None else channel
        embed = Embed()
        embed.description = "Le salon `{}` a été modifié".format(channel.name)
        embed.color = Color.green()
        if name:
            await channel.edit(name=name)
            embed.add_field(name="Nom", value=name, inline=True)
        if category:
            await channel.edit(category=category)
            embed.add_field(name="Déplacé dans la catégorie", value=category, inline=True)
        if topic:
            await channel.edit(topic=topic)
            embed.add_field(name="Sujet", value=topic, inline=True)
        if slowmode:
            try:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                added_slowmode = format_timespan(delay)
            except InvalidTimespan as e:
                added_slowmode = e
            embed.add_field(name="Mode lent", value=added_slowmode, inline=True)
        if nsfw_enabled:
            if nsfw_enabled:
                await channel.edit(nsfw=True)
                embed.add_field(name="NSFW activé", value="Oui", inline=True)
            elif not nsfw_enabled:
                await channel.edit(nsfw=False)
                embed.add_field(name="NSFW activé", value="Non", inline=True)
        await ctx.followup.send(embed=embed)

    async def voicechannel(
        self,
        ctx: Interaction,
        channel: Optional[VoiceChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        users: Optional[Jeanne.Range[int, None, 99]] = None,
    ) -> None:
        await ctx.response.defer()
        channel = ctx.channel if channel is None else channel
        embed = Embed()
        embed.description = "Le salon `{}` a été modifié".format(channel.name)
        embed.color = Color.green()
        if name:
            await channel.edit(name=name)
            embed.add_field(name="Nom", value=name, inline=True)
        if category:
            await channel.edit(category=category)
            embed.add_field(name="Déplacé dans la catégorie", value=category, inline=True)
        if users:
            if users > 99:
                users = 99
            await channel.edit(user_limit=users)
            embed.add_field(name="Utilisateurs", value=users, inline=True)

        await ctx.followup.send(embed=embed)

    async def role(
        self,
        ctx: Interaction,
        role: Role,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        color: Optional[Jeanne.Range[str, None, 6]] = None,
        hoisted: Optional[bool] = None,
        mentionable: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        embed = Embed()
        embed.description = "Le rôle `{}` a été modifié".format(role.name)
        if name:
            await role.edit(name=name)
            embed.add_field(name="Nom", value=name, inline=True)
        if color is not None:
            try:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Couleur", value=color, inline=True)
                embed.color = role.color
            except Exception:
                embed.add_field(name="Couleur", value="Code couleur invalide", inline=True)
        else:
            embed.color = Color.random()
        if hoisted:
            if hoisted:
                await role.edit(hoist=True)
                embed.add_field(name="Mis en avant", value="Oui", inline=True)
            elif not hoisted:
                await role.edit(hoist=False)
                embed.add_field(name="Mis en avant", value="Non", inline=True)
        if mentionable:
            if mentionable:
                await role.edit(mentionable=True)
                embed.add_field(name="Mentionnable", value="Oui", inline=True)
            elif not mentionable:
                await role.edit(mentionable=False)
                embed.add_field(name="Mentionnable", value="Non", inline=True)
        await ctx.followup.send(embed=embed)

    async def server(
        self,
        ctx: Interaction,
        name: Optional[Jeanne.Range[str, 2, 100]] = None,
        description: Optional[Jeanne.Range[str, None, 120]] = None,
        avatar: Optional[Attachment] = None,
        splash: Optional[Attachment] = None,
        banner: Optional[Attachment] = None,
        verification_level: Optional[VerificationLevel] = None,
    ) -> None:
        await ctx.response.defer()
        embed = Embed()
        embed.description = "{} a été modifié".format(ctx.guild.name)
        embed.color = Color.green()
        if name:
            await ctx.guild.edit(name=name)
            embed.add_field(name="Nom", value=name, inline=True)
        if description:
            if "PUBLIC" in ctx.guild.features:
                await ctx.guild.edit(description=description)
                embed.add_field(name="Description", value=description, inline=True)
            else:
                embed.add_field(
                    name="Description",
                    value="Votre serveur n'est pas public pour pouvoir modifier la description",
                    inline=True,
                )
        if avatar:
            try:
                avatar_url = avatar.url
                embed.set_thumbnail(url=avatar_url)
                avatarbytes = get(avatar_url).content
                await ctx.guild.edit(icon=avatarbytes)
            except Exception:
                embed.add_field(
                    name="Icône non ajoutée",
                    value="Un problème est survenu lors de l'ajout de l'avatar",
                    inline=True,
                )
        if splash:
            if ctx.guild.premium_tier == 0:
                embed.add_field(
                    name="Splash non ajouté",
                    value="Ce serveur n'est pas boosté au niveau 1",
                    inline=True,
                )
            else:
                try:
                    splash_url = splash.url
                    splash_bytes = get(splash_url).content
                    await ctx.guild.edit(splash=splash_bytes)
                    embed.add_field(
                        name="Nouvel écran d'accueil du serveur",
                        value=ctx.guild.splash.url,
                        inline=True,
                    )
                except Exception:
                    pass
        if banner:
            if ctx.guild.premium_tier <= 1:
                embed.add_field(
                    name="Bannière non ajoutée",
                    value="Ce serveur n'est pas boosté au niveau 2",
                    inline=True,
                )
            else:
                try:
                    bannerbytes = get(banner.url).content
                    await ctx.guild.edit(banner=bannerbytes)
                    embed.add_field(
                        name="Nouvelle bannière du serveur",
                        value=ctx.guild.banner.url,
                        inline=True,
                    )
                except Exception:
                    pass
        if verification_level:
            if verification_level.name == "none":
                await ctx.guild.edit(verification_level=VerificationLevel.none)
                embed.add_field(
                    name="Niveau de vérification",
                    value="**{}**\nAucune vérification requise".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "low":
                await ctx.guild.edit(verification_level=VerificationLevel.low)
                embed.add_field(
                    name="Niveau de vérification",
                    value="**{}**\nLes membres doivent avoir un email vérifié".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "medium":
                await ctx.guild.edit(verification_level=VerificationLevel.medium)
                embed.add_field(
                    name="Niveau de vérification",
                    value="**{}**\nLes membres doivent avoir un email vérifié et être inscrits sur Discord depuis plus de 5 minutes".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "high":
                await ctx.guild.edit(verification_level=VerificationLevel.high)
                embed.add_field(
                    name="Niveau de vérification",
                    value="**{}**\nLes membres doivent avoir un email vérifié, être inscrits sur Discord depuis plus de 5 minutes et rester sur le serveur plus de 10 minutes".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
            elif verification_level.name == "highest":
                await ctx.guild.edit(verification_level=VerificationLevel.highest)
                embed.add_field(
                    name="Niveau de vérification",
                    value="**{}**\nLes membres doivent avoir un numéro de téléphone vérifié".format(
                        verification_level.name.title()
                    ),
                    inline=True,
                )
        await ctx.followup.send(embed=embed)


class Set_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    async def welcomer(
        self,
        ctx: Interaction,
        welcoming_channel: Optional[TextChannel] = None,
        leaving_channel: Optional[TextChannel] = None,
    ) -> None:
        await ctx.response.defer()
        if (welcoming_channel is None) and (leaving_channel is None):
            error = Embed(
                description="Les deux options sont vides. Veuillez définir au moins un canal de bienvenue ou de départ.",
                color=Color.red(),
            )
            await ctx.followup.send(embed=error)
            return
        setup = Embed(description="Canaux de bienvenue définis", color=Color.random())
        if welcoming_channel:
            await Manage(ctx.guild).set_welcomer(welcoming_channel)
            setup.add_field(
                name="Canal de bienvenue des utilisateurs",
                value=welcoming_channel.mention,
                inline=True,
            )
        if leaving_channel:
            await Manage(ctx.guild).set_leaver(leaving_channel)
            setup.add_field(
                name="Canal indiquant les utilisateurs partis",
                value=leaving_channel.mention,
                inline=True,
            )
        await ctx.followup.send(embed=setup)

    async def modlog(self, ctx: Interaction, channel: TextChannel):
        await ctx.response.defer()
        await Manage(ctx.guild).set_modloger(channel)
        embed = Embed(description="Canal de modlog défini", color=Color.red())
        embed.add_field(name="Canal sélectionné", value=channel.mention, inline=True)
        await ctx.followup.send(embed=embed)

    async def welcomingmsg(
        self, ctx: Interaction, jsonscript: Optional[str] = None
    ) -> None:
        if jsonscript is None:
            await ctx.response.send_modal(Welcomingmsg(ctx))
            return
        if jsonscript is not None:
            await ctx.response.defer()
            humans = str(
                len([member for member in ctx.guild.members if not member.bot])
            )
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

            json_content = self.replace_all(jsonscript, parameters)
            json = loads(json_content)
            try:
                content = json["content"]
                embed = Embed.from_dict(json["embeds"][0])
            except Exception:
                content = json_content
            confirm = Embed(
                description="Voici un aperçu du message de bienvenue.\nÊtes-vous satisfait ?"
            )
            embed = Embed.from_dict(json["embeds"][0])
            view = Confirmation(ctx, ctx.user)
            await ctx.followup.send(
                content=content,
                embeds=[embed, confirm],
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_welcomer_msg(str(jsonscript))
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
                embed = Embed(description="Délai dépassé")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )

    async def leavingmsg(
        self, ctx: Interaction, jsonscript: Optional[str] = None
    ) -> None:
        if jsonscript is None:
            await ctx.response.send_modal(Leavingmsg(ctx))
            return
        if jsonscript is not None:
            await ctx.response.defer()
            humans = str(
                len([member for member in ctx.guild.members if not member.bot])
            )
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
            json_content = self.replace_all(jsonscript, parameters)
            json = loads(json_content)
            try:
                content = json["content"]
                embed = Embed.from_dict(json["embeds"][0])
            except Exception:
                content = json_content
            confirm = Embed(
                description="Voici un aperçu du message de départ.\nÊtes-vous satisfait ?"
            )
            embed = Embed.from_dict(json["embeds"][0])
            view = Confirmation(ctx, ctx.user)
            await ctx.followup.send(
                content=content,
                embeds=[embed, confirm],
                view=view,
                allowed_mentions=AllowedMentions(
                    everyone=False, roles=False, users=False
                ),
                ephemeral=True,
            )
            await view.wait()
            if view.value:
                await Manage(ctx.guild).set_leaving_msg(str(jsonscript))
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
                embed = Embed(description="Délai dépassé")
                await ctx.edit_original_response(
                    content=None, embeds=[embed], view=None
                )

    async def rolereward_message(
        self, ctx: Interaction, message: Optional[bool] = None
    ) -> None:
        if message :
            await ctx.response.send_modal(RankUpmsg(ctx))
            return
        await ctx.response.defer()
        await Manage(ctx.guild).add_rankup_rolereward(message)
        embed = Embed()
        embed.description = "Message de récompense de rôle par défaut défini"
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    async def levelupdate(
        self, ctx: Interaction, channel: TextChannel, levelmsg: Optional[bool] = None
    ) -> None:
        if levelmsg :
            await ctx.response.send_modal(Levelmsg(ctx, channel))
            return
        await ctx.response.defer()
        await Manage(server=ctx.guild).add_level_channel(channel)
        embed = Embed()
        embed.description = "{} publiera des mises à jour de niveau lorsqu'un membre montera de niveau".format(
            channel.mention
        )
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    async def confessionchannel(self, ctx: Interaction, channel: TextChannel) -> None:
        await ctx.response.defer()
        await Manage(ctx.guild).add_confession_channel(channel)
        embed = Embed(
            description=f"{channel.mention} recevra des confessions anonymes de la part des membres",
            color=Color.random(),
        )
        await ctx.followup.send(embed=embed)

    async def brightness(
        self, ctx: Interaction, brightness: Jeanne.Range[int, 10, 150]
    ):
        await ctx.response.defer()
        embed = Embed()
        if not Inventory(ctx.user).set_brightness(brightness):
            embed.description = "Vous n'avez pas de fond d'écran"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return
        await Inventory(ctx.user).set_brightness(brightness)
        embed.description = "La luminosité a été changée à {}%".format(brightness)
        embed.color = Color.random()
        await ctx.followup.send(embed=embed)

    async def bio(self, ctx: Interaction, bio: Jeanne.Range[str, 1, 120]):
        await ctx.response.defer()
        if len(bio) > 60 <= 120:
            bio = bio[:60] + "\n" + bio[60:120]
        embed = Embed(title="Nouvelle bio définie :", color=Color.random())
        await Inventory(ctx.user).set_bio(bio)
        embed.description = bio
        await ctx.followup.send(embed=embed)

    async def color(self, ctx: Interaction, color: Jeanne.Range[str, 1]):
        await ctx.response.defer()
        embed = Embed()
        try:
            c = ImageColor.getcolor(color, "RGB")
            await Inventory(ctx.user).set_color(color)
            embed.description = "La couleur de police et de la barre de la carte de profil a été changée en {} comme indiqué dans la couleur de l'embed".format(
                color
            )
            embed.color = int("{:02X}{:02X}{:02X}".format(*c), 16)
        except Exception:
            embed.description = "Couleur invalide"
            embed.color = Color.red()
        await ctx.followup.send(embed=embed)


class manage:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def addrole(self, ctx: Interaction, member: User, role: Role):
        await ctx.response.defer()
        await member.add_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Rôle attribué",
            value=f"`{role}` a été attribué à `{member}`",
            inline=False,
        )
        await ctx.followup.send(embed=embed)

    async def removerole(self, ctx: Interaction, member: User, role: Role):
        await ctx.response.defer()
        m = await ctx.guild.fetch_member(member.id)
        await m.remove_roles(role)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Rôle retiré",
            value=f"`{role}` a été retiré de `{member}`",
            inline=False,
        )
        await ctx.followup.send(embed=embed)

    async def remove(self, ctx: Interaction) -> None:
        await ctx.response.defer()
        embed = Embed(
            description="Cliquez sur l'un des boutons pour le supprimer",
            color=Color.random(),
        )
        view = RemoveManage(ctx, ctx.user)
        await ctx.followup.send(embed=embed, view=view)
        await view.wait()
        if view.value is None:
            embed.description = (
                "Tous les boutons ont été supprimés en raison du délai d'attente"
            )
            await ctx.edit_original_response(embed=embed, view=None)

    async def clone(
        self,
        ctx: Interaction,
        channel: Optional[abc.GuildChannel] = None,
        name: Optional[Jeanne.Range[str, 1, 100]] = None,
        category: Optional[CategoryChannel] = None,
        nsfw_enabled: Optional[bool] = None,
    ) -> None:
        await ctx.response.defer()
        channel = ctx.channel if channel is None else channel
        name = channel.name if (name is None) else name
        c = await channel.clone(name=name)
        cloned = Embed(
            description="{} a été cloné en {}".format(channel.jump_url, c.jump_url)
        )
        cloned_channel = await ctx.guild.fetch_channel(c.id)
        if category:
            if channel is CategoryChannel:
                cloned.add_field(
                    name="Déplacé dans la catégorie",
                    value="Impossible de déplacer une catégorie dans une autre catégorie",
                    inline=True,
                )
            else:
                await cloned_channel.edit(category=category)
                cloned.add_field(
                    name="Déplacé dans la catégorie", value=category.name, inline=True
                )
        if nsfw_enabled:
            await cloned_channel.edit(nsfw=nsfw_enabled)
            cloned.add_field(name="NSFW Activé", value=nsfw_enabled, inline=True)
        cloned.color = Color.random()
        await ctx.followup.send(embed=cloned)


class Rename_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def emoji(self, ctx: Interaction, emoji: str, name: Jeanne.Range[str, 2, 30]):
        await ctx.response.defer()
        try:
            e: int = emoji.strip().split(":")[-1].rstrip(">")
            emote = await ctx.guild.fetch_emoji(e)
        except Exception:
            emote = utils.get(ctx.guild.emojis, name=emoji.replace(" ", "_"))
        embed = Embed(
            description="{} a été renommé en {}".format(str(emote), name),
            color=0x00FF68,
        )
        await emote.edit(name=name.replace(" ", "_"))
        await ctx.followup.send(embed=embed)

    async def emoji_error(self, ctx: Interaction):
        embed = Embed(
            description="Cet émoji n'existe pas sur le serveur",
            color=Color.red(),
        )
        await ctx.followup.send(embed=embed)

    async def category(
        self,
        ctx: Interaction,
        category: CategoryChannel,
        name: Jeanne.Range[str, 1, 100],
    ):
        await ctx.response.defer()
        embed = Embed(colour=Color.random())
        embed.description = f"`{category.name}` a été renommé en `{name}`"
        await category.edit(name=name)
        await ctx.followup.send(embed=embed)

    async def sticker(
        self, ctx: Interaction, sticker: str, name: Jeanne.Range[str, 2, 30]
    ):
        await ctx.response.defer()
        sticker: GuildSticker = utils.get(ctx.guild.stickers, name=sticker)
        embed = Embed(
            description="`{}` a été renommé en `{}`".format(str(sticker.name), name),
            color=Color.random(),
        )
        await sticker.edit(name=name)
        await ctx.followup.send(embed=embed)

    async def sticker_error(self, ctx: Interaction):
        embed = Embed(
            description="Ce sticker n'existe pas sur le serveur",
            color=Color.red(),
        )
        await ctx.followup.send(embed=embed)


class Command_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _disable(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
    ):
        await ctx.response.defer()
        cmd = Command(ctx.guild)
        embed = Embed()
        if command.startswith(("help", "command")):
            embed.color = Color.red()
            embed.description = "WOAH ! Ne désactivez pas cette commande !"
        elif command not in [
            cmd.qualified_name
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Jeanne.Group)
        ]:
            embed.color = Color.red()
            embed.description = "Il n'existe aucune commande avec ce nom..."
        elif cmd.check_disabled(command):
            embed.color = Color.red()
            embed.description = "Cette commande est déjà désactivée"
        else:
            embed.title = "Commande désactivée"
            embed.description = f"`{command}` a été désactivée"
            embed.color = Color.random()
            await cmd.disable(command)
        await ctx.followup.send(embed=embed)

    async def _enable(
        self,
        ctx: Interaction,
        command: Jeanne.Range[str, 3],
    ):
        await ctx.response.defer()
        embed = Embed()
        cmd = Command(ctx.guild)
        if command not in [
            cmd.qualified_name
            for cmd in self.bot.tree.walk_commands()
            if not isinstance(cmd, Jeanne.Group)
        ]:
            embed.color = Color.red()
            embed.description = "Il n'existe aucune commande avec ce nom..."
        elif cmd.check_disabled(command) is None:
            embed.color = Color.red()
            embed.description = "Cette commande est déjà activée"
        else:
            embed.title = "Commande activée"
            embed.description = f"`{command}` a été activée"
            embed.color = Color.random()
            await cmd.enable(command)
        await ctx.followup.send(embed=embed)

    async def listdisabled(self, ctx: Interaction):
        await ctx.response.defer()
        cmd = Command(ctx.guild)
        embed = Embed()
        if cmd.list_all_disabled is None:
            embed.description = "Aucune commande n'est désactivée actuellement"
            embed.color = Color.red()
        else:
            embed.title = "Commandes désactivées :"
            embed.description = "\n".join(cmd.list_all_disabled)
            embed.color = Color.random()
        await ctx.followup.send(embed=embed)


class Level_Group:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _add(self, ctx: Interaction, role: Role, level: Jeanne.Range[int, 1]):
        await ctx.response.defer()
        botmember = await ctx.guild.fetch_member(self.bot.user.id)
        if role.position >= botmember.top_role.position:
            embed = Embed(color=Color.red())
            embed.description = "Ce rôle est au-dessus de moi"
            await ctx.followup.send(embed=embed)
            return
        await Manage(server=ctx.guild).add_role_reward(role, level)
        embed = Embed(color=Color.random())
        embed.description = (
            "{} sera attribué à un membre lorsqu'il atteindra le niveau {}".format(
                role.mention, level
            )
        )
        await ctx.followup.send(embed=embed)

    async def _remove(self, ctx: Interaction, role: Role):
        await ctx.response.defer()
        await Manage(server=ctx.guild).remove_role_reward(role)
        embed = Embed(color=Color.random())
        embed.description = "{} a été supprimé des récompenses de niveau".format(
            role.mention
        )
        await ctx.followup.send(embed=embed)

    async def listrolerewards(self, ctx: Interaction):
        await ctx.response.defer()
        roles = Levelling(server=ctx.guild).list_all_roles
        data = []
        for i in roles:
            role = f"<@&{i[1]}>"
            level = i[2]
            data.append(f"Niveau {level} : {role}\n")
        embed = Embed(color=Color.random())
        embed.description = "".join(data)
        embed.title = "Récompenses de niveau"
        await ctx.followup.send(embed=embed)

    async def add(self, ctx: Interaction, channel: TextChannel) -> None:
        await ctx.response.defer()
        if not Levelling(server=ctx.guild).check_xpblacklist_channel(channel):
            await Manage(server=ctx.guild).add_xpblacklist(channel)
            embed = Embed(color=Color.random())
            embed.add_field(
                name="Salon blacklisté pour l'XP",
                value=f"{channel.jump_url} a été ajouté à la blacklist XP",
                inline=False,
            )
            await ctx.followup.send(embed=embed)
            return
        embed = Embed(color=Color.red())
        embed.description = f"{channel.jump_url} est déjà blacklisté pour l'XP"
        await ctx.followup.send(embed=embed)

    async def remove(self, ctx: Interaction, channel: TextChannel) -> None:
        await ctx.response.defer()
        if not Levelling(server=ctx.guild).check_xpblacklist_channel(channel):
            embed = Embed(color=Color.red())
            embed.description = f"{channel.jump_url} n'est pas blacklisté pour l'XP"
            embed.color = Color.red()
            await ctx.followup.send(embed=embed)
            return
        await Manage(server=ctx.guild).remove_blacklist(channel)
        embed = Embed(color=Color.random())
        embed.add_field(
            name="Salon retiré de la blacklist XP",
            value=f"{channel.jump_url} a été retiré de la blacklist XP",
            inline=False,
        )
        await ctx.followup.send(embed=embed)

    async def listblacklistedchannels(self, ctx: Interaction) -> None:
        await ctx.response.defer()
        embed = Embed()
        channels = Levelling(server=ctx.guild).get_blacklisted_channels
        if channels is None:
            embed.description = "Aucun salon n'est actuellement blacklisté pour l'XP"
            embed.color = Color.red()
        else:
            embed.color = Color.random()
            embed.title = "Salons blacklistés pour l'XP :"
            blchannels = []
            for channel in channels:
                blchannel = await ctx.guild.fetch_channel(channel)
                blchannels.append(blchannel.jump_url)
            embed.description = "\n".join(blchannels)
        await ctx.followup.send(embed=embed)
