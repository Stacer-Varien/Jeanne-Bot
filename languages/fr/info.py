from humanfriendly import format_timespan
from assets.components import RolesButton
from time import time
from datetime import timedelta
from sys import version_info as py_version
from discord.ext.commands import Bot
from discord import (
    ButtonStyle,
    Color,
    Embed,
    Interaction,
    Member,
    Message,
    PartialEmoji,
    StickerItem,
    app_commands as Jeanne,
    utils,
    ui,
)
from discord import __version__ as discord_version
from typing import Optional

start_time = time()


class stat_buttons(ui.View):
    def __init__(self):
        super().__init__()
        invite = "https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1429553343542&scope=bot%20applications.commands"
        votetopgg = "https://top.gg/bot/831993597166747679"
        orleans_url = "https://discord.gg/jh7jkuk2pp"
        website = "https://jeannebot.gitbook.io/jeannebot/"
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Invitez-moi", url=invite)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Votez pour moi", url=votetopgg)
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link, label="Serveur de support", url=orleans_url
            )
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="Site Web de Jeanne",
                url=website,
            )
        )


class Info:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_userinfo(self, ctx: Interaction, member: Member):
        await ctx.response.defer()
        user = await self.bot.fetch_user(member.id)
        has_roles = [role.mention for role in member.roles][1:][::-1]
        bot_check = "Oui" if member.bot else "Non"
        joined_date = round(member.joined_at.timestamp())
        create_date = round(member.created_at.timestamp())
        userinfo = Embed(title=f"Informations de {member.name}", color=member.color)
        userinfo.add_field(name="Nom", value=member, inline=True)
        userinfo.add_field(name="Nom Global", value=member.global_name, inline=True)
        if member.nick != member.global_name:
            userinfo.add_field(name="Surnom", value=member.nick, inline=True)
        userinfo.add_field(name="ID", value=member.id, inline=True)
        userinfo.add_field(name="Est un bot ?", value=bot_check, inline=True)
        userinfo.add_field(
            name="Compte créé", value=f"<t:{create_date}:F>", inline=True
        )
        userinfo.add_field(
            name="Rejoint le serveur", value=f"<t:{joined_date}:F>", inline=True
        )
        userinfo.add_field(name="Nombre de rôles", value=len(member.roles), inline=True)
        userinfo.set_thumbnail(url=member.display_avatar)
        if user.banner:
            userinfo.set_image(url=user.banner)
        view = RolesButton(member, userinfo, has_roles)
        await ctx.followup.send(embeds=[userinfo], view=view)
        await view.wait()
        if view.value is None:
            await ctx.edit_original_response(embeds=[userinfo], view=None)

    async def stats(self, ctx: Interaction):
        await ctx.response.defer()
        embed = Embed(title="Statistiques du bot", color=Color.random())
        embed.add_field(
            name="Développeur",
            value=f"• **Nom :** {self.bot.application.owner}\n• **ID :** {self.bot.application.owner.id}",
            inline=True,
        )
        embed.add_field(name="ID du bot", value=self.bot.user.id, inline=True)
        embed.add_field(
            name="Date de création",
            value="<t:{}:F>".format(round(self.bot.user.created_at.timestamp())),
            inline=True,
        )
        embed.add_field(
            name="Version",
            value=f"• **Version Python :** {py_version.major}.{py_version.minor}.{py_version.micro}\n• **Version Discord.PY :** {discord_version}\n• **Bot :** {self.bot_version}",
            inline=True,
        )
        embed.add_field(
            name="Comptes",
            value=f"• **Nombre de serveurs :** {len(self.bot.guilds)} serveurs\n• **Shards :** {self.bot.shard_count}\n• **Nombre d'utilisateurs :** {len(self.bot.users())}\n• **Membres en cache :** {len(set(self.bot.get_all_members()))}",
            inline=True,
        )
        current_time = time()
        difference = int(round(current_time - start_time))
        uptime = timedelta(seconds=difference).total_seconds()
        embed.add_field(
            name="Temps de fonctionnement", value=format_timespan(uptime), inline=True
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.followup.send(embed=embed, view=stat_buttons())

    async def serverinfo(self, ctx: Interaction):
        await ctx.response.defer()
        emojis = [str(x) for x in ctx.guild.emojis]
        humans = len([member for member in ctx.guild.members if not member.bot])
        bots = len([bot for bot in ctx.guild.members if bot.bot == True])
        date = round(ctx.guild.created_at.timestamp())
        serverinfo = Embed(color=Color.random())
        serverinfo.add_field(name="ID", value=ctx.guild.id, inline=True)
        serverinfo.add_field(
            name="Propriétaire",
            value=f"• **Nom :** {ctx.guild.owner}\n• **ID :** {ctx.guild.owner_id}",
            inline=True,
        )
        serverinfo.add_field(
            name="Date de création", value=f"<t:{date}:F>", inline=True
        )
        serverinfo.add_field(
            name="Membres",
            value=f"• **Humains :** {humans}\n• **Bots :** {bots}\n• **Total :** {ctx.guild.member_count}",
            inline=True,
        )
        serverinfo.add_field(
            name="Statut des boosts",
            value=f"• **Boosters :** {len(ctx.guild.premium_subscribers)}\n• **Boosts :** {ctx.guild.premium_subscription_count}\n• **Niveau :** {ctx.guild.premium_tier}",
            inline=True,
        )
        verification_level = (
            ctx.guild.verification_level.name.capitalize()
            if ctx.guild.verification_level.name != "none"
            else None
        )
        serverinfo.add_field(
            name="Niveau de vérification",
            value=verification_level,
            inline=True,
        )
        serverinfo.add_field(
            name="Comptes",
            value=f"**Tous les canaux :** {len(ctx.guild.channels)} | **Canaux textuels :** {len(ctx.guild.text_channels)} |  **Canaux vocaux :** {len(ctx.guild.voice_channels)} |  **Canaux de scène :** {len(ctx.guild.stage_channels)} |  **Catégories :** {len(ctx.guild.categories)} |  **Forums :** {len(ctx.guild.forums)} |  **Rôles :** {len(ctx.guild.roles)} | **Émojis :** {len(emojis)} | **Stickers :** {len(ctx.guild.stickers)}",
            inline=False,
        )
        f = []
        for i in ctx.guild.features:
            f.append(i.replace("_", " ").title())
        serverinfo.add_field(name="Features", value=" | ".join(f), inline=False)
        icon = ctx.guild.icon.url if ctx.guild.icon != None else None
        splash = (
            ctx.guild.splash.url
            if ctx.guild.splash != None and ctx.guild.premium_tier == 1
            else None
        )
        serverinfo.set_thumbnail(url=icon)
        serverinfo.set_image(url=splash)
        serverinfo.set_footer(text=f"ID du shard : {ctx.guild.shard_id}")
        if len(emojis) == 0:
            await ctx.followup.send(embed=serverinfo)
            return
        emojie = Embed(
            title="Émojis", description="".join(emojis[:80]), color=Color.random()
        )
        e = [serverinfo, emojie]
        await ctx.followup.send(embeds=e)

    async def ping(self, ctx: Interaction):
        await ctx.response.defer()
        start_time = time()
        test = Embed(description="Test de ping", color=Color.random())
        await ctx.followup.send(embed=test)
        ping = Embed(color=Color.random())
        ping.add_field(
            name="Latence du bot",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=False,
        )
        end_time = time()
        ping.add_field(
            name="Latence de l'API",
            value=f"{round((end_time - start_time) * 1000)}ms",
            inline=False,
        )
        await ctx.edit_original_response(embed=ping)

    async def serverbanner(self, ctx: Interaction):
        await ctx.response.defer()
        if ctx.guild.premium_subscription_count < 2:
            nobanner = Embed(
                description="Le serveur n'est pas boosté au niveau 2", color=Color.red()
            )
            await ctx.followup.send(embed=nobanner)
            return
        if ctx.guild.banner == None:
            embed = Embed(
                description="Le serveur n'a pas de bannière", color=Color.red()
            )
            await ctx.followup.send(embed=embed)
            return
        embed = Embed(colour=Color.random())
        embed.set_footer(text=f"Bannière de {ctx.guild.name}")
        embed.set_image(url=ctx.guild.banner.url)
        await ctx.followup.send(embed=embed)

    async def avatar(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        await ctx.response.defer()
        member = ctx.user if member is None else member
        serverav = member.guild_avatar if ctx.guild else None
        color = Color.random()
        embeds = []

        normav = Embed(
            description=f"**Avatar de {member}**",
            color=color,
        )
        normav.set_image(url=member.display_avatar)
        embeds.append(normav)

        if serverav:
            guildav = Embed(
                description=f"**Avatar serveur de {member}**",
                color=color,
            )
            guildav.set_image(url=serverav)
            embeds.append(guildav)

        await ctx.followup.send(embeds=embeds)

    async def sticker(self, ctx: Interaction, sticker: str):
        await ctx.response.defer()
        try:
            m: Message = await ctx.channel.fetch_message(int(sticker))
            s: StickerItem = m.stickers[0]
        except (ValueError, IndexError, AttributeError):
            s: StickerItem = utils.get(ctx.guild.stickers, name=sticker)
            if not s:
                embed = Embed(
                    description="Cet autocollant n'existe pas sur le serveur",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=embed)
                return

        q = await self.bot.fetch_sticker(s.id)
        embed = Embed(color=Color.random())
        embed.add_field(name="Nom de l'autocollant", value=q.name, inline=False)
        embed.add_field(name="ID de l'autocollant", value=q.id, inline=False)
        embed.set_image(url=q.url)
        if "apng" in q.format:
            embed.add_field(
                name="URL de l'autocollant animé", value=q.url, inline=False
            )
        await ctx.followup.send(embed=embed)

    async def sticker_error(
        self, ctx: Interaction, error: Jeanne.AppCommandError, type: str
    ):
        if type == "NoSticker":
            embed = Embed(
                description="Aucun autocollant dans ce message",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)
            return
        if type == "StickerNotFound":
            embed = Embed(
                description="Cet autocollant n'existe pas sur le serveur",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    async def emoji(self, ctx: Interaction, emoji: str):
        await ctx.response.defer()
        try:
            emote = PartialEmoji.from_str(emoji)
            if not emote.id:
                raise ValueError("Invalid emoji format")
            embed = Embed(color=Color.random())
            embed.add_field(name="Nom", value=emote.name, inline=False)
            embed.add_field(name="ID", value=emote.id, inline=False)
            embed.set_image(url=emote.url)
            await ctx.followup.send(embed=embed)
        except ValueError:
            embed = Embed(
                description="Échec de récupération de l'émoji. Assurez-vous que l'émoji est valide.",
                color=Color.red(),
            )
            await ctx.followup.send(embed=embed)

    async def emoji_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        embed = Embed(
            description="Échec de récupération de l'émoji",
            color=Color.red(),
        )
        await ctx.followup.send(embed=embed)
