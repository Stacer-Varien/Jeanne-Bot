import asyncio
from random import randint
from discord import (
    Color,
    Embed,
    Interaction,
    User,
    Message,
    NotFound,
    Member,
    app_commands as Jeanne,
)
from discord.ext.commands import Bot
from datetime import datetime, timedelta
from humanfriendly import format_timespan, parse_timespan
from reactionmenu import ViewButton, ViewMenu
from functions import (
    Moderation,  
)
from assets.components import Confirmation
from typing import Optional


class moderation():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def commit_ban(
        self,
        ctx: Interaction,
        member: User,
        reason: str,
        time: Optional[str] = None,
        delete_message_history: Optional[bool] = None,
    ):
        if delete_message_history :
            dmh = 604800
        else:
            dmh = 86400

        await ctx.guild.ban(
            member,
            reason="{} | {}".format(reason, ctx.user),
            delete_message_seconds=dmh,
        )
        ban = Embed(title="Gebruiker verbannen", color=0xFF0000)
        ban.add_field(name="Naam", value=member, inline=True)
        ban.add_field(name="ID", value=member.id, inline=True)
        ban.add_field(name="Moderator", value=ctx.user, inline=True)
        ban.add_field(name="Reden", value=reason, inline=False)
        if time is not None:
            try:
                a = round(parse_timespan(time))
                await Moderation(ctx.guild).softban_member(member, a)
                time = format_timespan(a)
            except Exception:
                time = "Ongeldige tijd toegevoegd. Gebruiker is permanent verbannen!"
            ban.add_field(name="Duur", value=time, inline=True)
        ban.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.edit_original_response(embed=ban, view=None)
            return
        banned = Embed(
            description=f"{member} is verbannen. Zie {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.edit_original_response(embed=banned, view=None)
        await modlog.send(embed=ban)

    async def check_banned(self, ctx: Interaction, member: User):
        try:
            banned = await ctx.guild.fetch_ban(member)
            if banned:
                already_banned = Embed(
                    description=f"{member} is hier al verbannen",
                    color=Color.red(),
                )
                await ctx.followup.send(embed=already_banned)
                return
        except NotFound:
            return False

    async def ban(
        self,
        ctx: Interaction,
        member: User,
        reason: Optional[str] = "Ongespecificeerd",
        delete_message_history: Optional[bool] = None,
        time: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        if member == ctx.guild.owner:
            failed = Embed(
                description="Je kunt de eigenaar van de server niet verbannen...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.user:
            failed = Embed(description="Je kunt jezelf niet verbannen...", color=Color.red())
            await ctx.followup.send(embed=failed)
            return

        if member not in ctx.guild.members:
            if not await self.check_banned(ctx, member):
                view = Confirmation(ctx, ctx.user)
                confirm = Embed(
                    description="Is {} degene die je wilt verbannen van je server?".format(
                        member
                    ),
                    color=Color.dark_red(),
                ).set_thumbnail(url=member.display_avatar)
                await ctx.followup.send(embed=confirm, view=view)
                await view.wait()
                if view.value is None:
                    cancelled = Embed(description="Ban geannuleerd", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)
                    return
                if view.value :
                    await self.commit_ban(
                        ctx, member, reason, None, delete_message_history
                    )
                    return

                if not view.value:
                    cancelled = Embed(description="Ban geannuleerd", color=Color.red())
                    await ctx.edit_original_response(embed=cancelled, view=None)
                    return
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="De positie van {} is hoger dan die van jou...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        await self.commit_ban(ctx, member, reason, time, delete_message_history)

    async def ban_user_error(self, ctx: Interaction):
        embed = Embed()
        embed.description = "Ongeldige gebruikers-ID opgegeven\nProbeer het opnieuw"
        embed.color = Color.red()
        await ctx.followup.send(embed=embed)

    async def warn(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="De positie van {} is hoger dan die van jou...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.guild.owner:
            failed = Embed(
                description="Je kunt de eigenaar van de server niet waarschuwen...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.user:
            failed = Embed(description="Je kunt jezelf niet waarschuwen")
            await ctx.followup.send(embed=failed)
            return
        reason = reason if reason else "Niet gespecificeerd"
        warn_id = randint(0, 100000)
        date = round(datetime.now().timestamp())
        await Moderation(ctx.guild).warn_user(
            member, ctx.user.id, reason, warn_id, date
        )
        warn = Embed(title="Lid gewaarschuwd", color=0xFF0000)
        warn.add_field(name="Lid", value=member, inline=True)
        warn.add_field(name="ID", value=member.id, inline=True)
        warn.add_field(name="Moderator", value=ctx.user, inline=True)
        warn.add_field(name="Reden", value=reason, inline=False)
        warn.add_field(name="Waarschuwing ID", value=warn_id, inline=True)
        warn.add_field(name="Datum", value="<t:{}:F>".format(date), inline=True)
        warn.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.followup.send(embed=warn)
            return

        warned = Embed(
            description=f"{member} is gewaarschuwd. Zie {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=warned)
        await modlog.send(embed=warn)

    async def listwarns(self, ctx: Interaction, member: Optional[str]):
        await ctx.response.defer()
        if member is not None:
            mem = ctx.guild.get_member(int(member))
        record = (
            Moderation(ctx.guild).fetch_warnings_user(mem)
            if member is not None
            else Moderation(ctx.guild).fetch_warnings_server
        )
        if record is None:
            await ctx.followup.send("Niemand heeft waarschuwing-ID's")
            return

        menu = ViewMenu(
            ctx,
            menu_type=ViewMenu.TypeEmbed,
            disable_items_on_timeout=True,
            style="Page $/&",
        )
        unique_names = set()
        for i in range(0, len(record), 5):
            embed_title = (
                f"Waarschuwingen van {mem}"
                if member is not None
                else "Momenteel gewaarschuwde leden"
            )
            embed_color = 0xFF0000 if member else Color.red()

            embed = Embed(title=embed_title, colour=embed_color)

            embed.set_thumbnail(url=mem.display_avatar if member else ctx.guild.icon)
            for j in record[i : i + 5]:
                mod = await self.bot.fetch_user(j[2])
                user = await self.bot.fetch_user(j[0])
                reason = j[3]
                warn_id = j[4]
                points = Moderation(ctx.guild).warnpoints(user)
                date = f"<t:{j[5]}:F>"

                if member is None:
                    if user not in unique_names:
                        unique_names.add(user)
                        embed.add_field(
                            name=f"{user} | {user.id}",
                            value=f"- **Punten:** {points}",
                            inline=False,
                        )
                else:
                    embed.add_field(
                        name=f"**Waarschuwing ID:** {warn_id}",
                        value=f"- **Moderator:** {mod}\n- **Reden:** {reason}\n- **Datum:** {date}",
                        inline=False,
                    )
                    embed.set_footer(text=f"Totaal waarschuwingpunten: {points}")

            menu.add_page(embed=embed)
        if len(record) < 5:
            await ctx.followup.send(embed=embed)
            return

        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()

    async def listwarns_error(self, ctx: Interaction):
        embed = Embed(
                description="Dit lid heeft geen waarschuwingen of bestaat niet in deze server",
                color=Color.red(),
            )
        await ctx.followup.send(embed=embed)

    async def clearwarn(self, ctx: Interaction, member: Member, warn_id: int):
        await ctx.response.defer()
        mod = Moderation(ctx.guild)
        result = mod.check_warn_id(member, warn_id)
        if result is None:
            await ctx.followup.send("Ongeldige waarschuwing ID")
            return
        await mod.revoke_warn(member, warn_id)
        revoked_warn = Embed(
            title="Waarschuwing verwijderd",
            description=f"{ctx.user} heeft waarschuwing ID ({warn_id}) ingetrokken",
        )
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.followup.send(embed=revoked_warn)
            return

        revoke = Embed(
            description=f"Waarschuwing ingetrokken. Zie {modlog.mention}", color=0xFF0000
        )
        await modlog.send(embed=revoke)
        await ctx.followup.send(embed=revoked_warn)

    async def kick(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        if member == ctx.user:
            failed = Embed(description="Je kunt jezelf niet kicken")
            await ctx.followup.send(embed=failed)
            return
        if ctx.user.top_role.position < member.top_role.position:
            failed = Embed(
                description="De positie van {} is hoger dan die van jou...".format(member),
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.guild.owner:
            failed = Embed(
                description="Je kunt de eigenaar van de server niet kicken...",
                color=Color.red(),
            )
            await ctx.followup.send(embed=failed)
            return
        if member == ctx.user:
            failed = Embed(description="Je kunt jezelf niet kicken")
            await ctx.followup.send(embed=failed)
            return
        reason = reason if reason else "Niet gespecificeerd"
        try:
            kickmsg = Embed(
                description=f"Je bent gekickt uit **{ctx.guild.name}** voor **{reason}**"
            )
            await member.send(embed=kickmsg)
        except Exception:
            pass
        await ctx.guild.kick(member, reason="{} | {}".format(reason, ctx.user))
        kick = Embed(title="Lid gekickt", color=0xFF0000)
        kick.add_field(name="Lid", value=member, inline=True)
        kick.add_field(name="ID", value=member.id, inline=True)
        kick.add_field(name="Moderator", value=ctx.user, inline=True)
        kick.add_field(name="Reden", value=reason, inline=True)
        kick.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.followup.send(embed=kick)
            return

        kicked = Embed(
            description=f"{member} is gekickt. Zie {modlog.mention}",
            color=0xFF0000,
        )
        await modlog.send(embed=kick)
        await ctx.followup.send(embed=kicked)

    async def prune(
        self,
        ctx: Interaction,
        limit: Optional[int] = None,
        member: Optional[Member] = None,
    ) -> None:
        await ctx.response.defer()
        limit = (limit + 1) if limit else 101
        if member:

            def is_member(m: Message):
                return m.author == member

            await ctx.channel.purge(limit=limit, check=is_member)
            return
        await ctx.channel.purge(limit=limit)

    async def changenickname(
        self,
        ctx: Interaction,
        member: Member,
        nickname: Optional[str],
    ):
        await ctx.response.defer()
        if (not nickname) or (nickname is None):
            await member.edit(nick=None)
            setnick = Embed(color=0x00FF68)
            setnick.add_field(
                name="Bijnaam gewijzigd",
                value=f"De bijnaam van {member} is verwijderd",
                inline=False,
            )
            await ctx.followup.send(embed=setnick)
            return
        if member.nick is None:
            embed = Embed(color=Color.red())
            embed.description = f"{member} heeft geen bijnaam"
            await ctx.followup.send(embed=embed)
            return
        await member.edit(nick=nickname)
        setnick = Embed(color=0x00FF68)
        setnick.add_field(
            name="Bijnaam gewijzigd",
            value=f"De bijnaam van {member} is nu `{nickname}`",
            inline=False,
        )
        await ctx.followup.send(embed=setnick)

    async def unban(
        self,
        ctx: Interaction,
        user_id: str,
        reason: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        reason = reason if reason else "Ongespecificeerd"
        user = await self.bot.fetch_user(int(user_id))
        await ctx.guild.unban(user, reason="{} | {}".format(reason, ctx.user))
        unban = Embed(title="Gebruiker unbanned", color=0xFF0000)
        unban.add_field(name="Naam", value=user, inline=True)
        unban.add_field(name="ID", value=user.id, inline=True)
        unban.add_field(name="Moderator", value=ctx.user, inline=True)
        unban.add_field(name="Reden", value=reason, inline=False)
        unban.set_thumbnail(url=user.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.followup.send(embed=unban)
            return

        unbanned = Embed(
            description=f"{user} is unbanned. Zie {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=unbanned)
        await modlog.send(embed=unban)

    async def unban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        embed = Embed()
        embed.color = Color.red()
        embed.description = str(error.original)
        await ctx.followup.send(embed=embed)

    async def timeout(
        self,
        ctx: Interaction,
        member: Member,
        time: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        if member == ctx.user:
            failed = Embed(description="Je kunt jezelf geen timeout geven")
            await ctx.followup.send(embed=failed)
            return
        if member not in ctx.guild.members:
            failed = Embed(description="Deze persoon is niet in deze server")
            await ctx.followup.send(embed=failed)
            return
        reason = reason if reason else "Niet gespecificeerd"
        if not time or (parse_timespan(time) > 2332800.0):
            time = 2332800.0
        timed = parse_timespan(str(time))
        await member.edit(
            timed_out_until=(datetime.now().astimezone() + timedelta(seconds=timed)),
            reason="{} | {}".format(reason, ctx.user),
        )
        mute = Embed(title="Lid Timeout", color=0xFF0000)
        mute.add_field(name="Lid", value=member, inline=True)
        mute.add_field(name="ID", value=member.id, inline=True)
        mute.add_field(name="Moderator", value=ctx.user, inline=True)
        mute.add_field(name="Duur", value=format_timespan(timed), inline=True)
        mute.add_field(name="Reden", value=reason, inline=False)
        mute.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.followup.send(embed=mute)
            return

        muted = Embed(
            description=f"{member} heeft een timeout gekregen. Zie {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=muted)
        await modlog.send(embed=mute)

    async def timeout_error(self, ctx: Interaction):
        embed = Embed()
        embed.description = "Ongeldige tijd toegevoegd. Probeer het opnieuw"
        embed.color = Color.red()
        await ctx.followup.send(embed=embed)

    async def timeoutremove(
        self,
        ctx: Interaction,
        member: Member,
        reason: Optional[str] = None,
    ) -> None:
        await ctx.response.defer()
        reason = reason if reason else "Ongespecificeerd"
        if member == ctx.user:
            failed = Embed(
                description="Je kunt jezelf geen timeout verwijderen", color=Color.red()
            )
            await ctx.followup.send(embed=failed)
            return
        if not member.is_timed_out():
            failed = Embed(
                description="Dit lid heeft geen timeout", color=Color.red()
            )
            await ctx.followup.send(embed=failed)
            return
        await member.edit(
            timed_out_until=None, reason="{} | {}".format(reason, ctx.user)
        )
        unmute = Embed(title="Gebruiker timeout verwijderd", color=0xFF0000)
        unmute.add_field(name="Gebruiker", value=member, inline=True)
        unmute.add_field(name="ID", value=member.id, inline=True)
        unmute.add_field(name="Moderator", value=ctx.user, inline=True)
        unmute.add_field(name="Reden", value=reason, inline=False)
        unmute.set_thumbnail(url=member.display_avatar)
        modlog = Moderation(ctx.guild).get_modlog_channel
        if modlog is None:
            await ctx.followup.send(embed=unmute)
            return

        unmuted = Embed(
            description=f"{member} heeft geen timeout meer. Zie {modlog.mention}",
            color=0xFF0000,
        )
        await ctx.followup.send(embed=unmuted)
        await modlog.send(embed=unmute)

    async def massban(self, ctx: Interaction, user_ids: str, reason: str):
        await ctx.response.defer()
        ids_str = user_ids.split()[:100]
        ids = list(map(int, ids_str))
        if len(ids) < 5:
            embed = Embed(
                description=f"Er zijn te weinig ID's. Voeg er meer toe en probeer het opnieuw na <t:{round((datetime.now() + timedelta(minutes=30)).timestamp())}:R>"
            )
            await ctx.followup.send(embed=embed)
            return
        banned_ids = {entry.user.id async for entry in ctx.guild.bans()}
        author_id = ctx.user.id
        guild_owner_id = ctx.guild.owner.id
        to_ban_ids = [
            user_id
            for user_id in ids
            if user_id not in banned_ids
            and user_id != author_id
            and user_id != guild_owner_id
        ]
        if not to_ban_ids:
            embed = Embed(description="Geen gebruikers kunnen worden verbannen.", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        view = Confirmation(ctx, ctx.user)
        alert = Embed(
            title="Gevonden gebruikers:",
            description="\n".join(
                [f"{self.bot.get_user(i).global_name}" for i in to_ban_ids]
            ),
            color=Color.red(),
        )
        alert.set_footer(
            text="LET OP: De ontwikkelaar is **NIET** op welke manier dan ook verantwoordelijk als je een fout maakt, zelfs niet bij misbruik.\n\nWil je doorgaan?"
        )
        await ctx.followup.send(embed=alert, view=view)
        await view.wait()
        if view.value :

            em = Embed(
                description="Gebruikers worden nu verbannen <a:loading:1161038734620373062>",
                color=Color.red(),
            )
            to_ban: list[User] = []
            for i in to_ban_ids:
                try:
                    user = await self.bot.fetch_user(i)
                    to_ban.append(user)
                except Exception:
                    continue
            await ctx.edit_original_response(embed=em, view=None)
            ban_results = await ctx.guild.bulk_ban(to_ban, reason=reason)

            if len(ban_results) > 0:
                embed = Embed(
                    title="Lijst van verbannen gebruikers",
                    color=Color.red(),
                )
                banned_users = []
                for i in ban_results.banned:
                    u = await self.bot.fetch_user(i.id)
                    banned_users.append(f"{u.global_name} | `{i.id}`")
                embed.description = "\n".join(banned_users)
                embed.add_field(name="Reden", value=reason, inline=False)
                if ban_results.failed:
                    failed_banned_users = []
                    for i in ban_results.failed:
                        u = await self.bot.fetch_user(i.id)
                        failed_banned_users.append(f"{u.global_name} | `{i.id}`")
                    embed.add_field(
                        name="Niet gelukt te verbannen",
                        value="\n".join(failed_banned_users),
                        inline=False,
                    )
            else:
                embed = Embed(description="Geen gebruikers zijn verbannen.", color=Color.red())
            modlog = Moderation(ctx.guild).get_modlog_channel
            if modlog is None:
                await ctx.edit_original_response(embed=embed)
                return

            await ctx.edit_original_response(
                embed=Embed(
                    description=f"Succesvol {len(ban_results.banned)} gebruiker(s) verbannen. Zie {modlog.mention}",
                    color=Color.red(),
                )
            )
            await modlog.send(embed=embed)
        elif (not view.value) or (view.value is None):
            cancelled = Embed(description="Massaban geannuleerd", color=Color.red())
            await ctx.edit_original_response(embed=cancelled, view=None)

    async def massban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
                description=f"Een massaban-commando is hier al gebruikt in deze server.\nProbeer het opnieuw na <t:{reset_hour}:R>",
                color=0xFF0000,
            )
        await ctx.response.send_message(embed=cooldown)

    async def massunban(self, ctx: Interaction, user_ids: str, reason: str):
        await ctx.response.defer()
        ids = user_ids.split()[:25]
        if len(ids) < 5:
            embed = Embed(
                description=f"Er zijn te weinig ID's. Voeg er meer toe en probeer het opnieuw na <t:{round((datetime.now() + timedelta(minutes=30)).timestamp())}:R>"
            )
            await ctx.followup.send(embed=embed)
            return
        banned_ids = {entry.user.id async for entry in ctx.guild.bans()}
        author_id = ctx.user.id
        guild_owner_id = ctx.guild.owner.id
        to_ban_ids = [
            user_id
            for user_id in ids
            if user_id not in banned_ids
            and user_id != str(author_id)
            and user_id != str(guild_owner_id)
        ]
        if not to_ban_ids:
            embed = Embed(description="Geen gebruikers kunnen worden unbanned.", color=Color.red())
            await ctx.followup.send(embed=embed)
            return
        view = Confirmation(ctx, ctx.user)
        alert = Embed(
            title="LET OP",
            description="De ontwikkelaar is **NIET** op welke manier dan ook verantwoordelijk als je een fout maakt, zelfs niet bij misbruik.\n\nWil je doorgaan?",
            color=Color.red(),
        )
        await ctx.followup.send(embed=alert, view=view)
        await view.wait()
        if view.value :
            em = Embed(
                description="Gebruikers worden nu unbanned <a:loading:1161038734620373062>",
                color=Color.red(),
            )
            await ctx.edit_original_response(embed=em, view=None)
            unban_count = 0
            failed_ids = []
            unbanned = []
            for user_id in to_ban_ids:
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    await ctx.guild.unban(user, reason=reason)
                    unbanned.append(f"{user} | `{user.id}`")
                    unban_count += 1
                    await asyncio.sleep(0.5)
                except Exception:
                    failed_ids.append(user_id)
                    continue
            if unban_count > 0:
                embed = Embed(
                    title="Lijst van unbanned gebruikers",
                    color=Color.red(),
                )
                embed.description = "\n".join(unbanned)
                embed.add_field(name="Reden", value=reason, inline=False)
                if failed_ids:
                    embed.add_field(
                        name="Niet gelukt te unbannen",
                        value="\n".join(failed_ids),
                        inline=False,
                    )
            else:
                embed = Embed(description="Geen gebruikers zijn unbanned.", color=Color.red())
            modlog = Moderation(ctx.guild).get_modlog_channel
            if modlog is None:
                await ctx.edit_original_response(embed=embed)
                return

            await ctx.edit_original_response(
                embed=Embed(
                    description=f"Succesvol {unban_count} gebruiker(s) unbanned. Zie {modlog.mention}",
                    color=Color.red(),
                )
            )
            await modlog.send(embed=embed)
        elif (not view.value) or (view.value is None):
            cancelled = Embed(description="Massunban geannuleerd", color=Color.red())
            await ctx.edit_original_response(embed=cancelled, view=None)

    async def massunban_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        reset_hour_time = datetime.now() + timedelta(seconds=error.retry_after)
        reset_hour = round(reset_hour_time.timestamp())
        cooldown = Embed(
                description=f"Een massunban-commando is hier al gebruikt in deze server.\nProbeer het opnieuw na <t:{reset_hour}:R>",
                color=0xFF0000,
            )
        await ctx.response.send_message(embed=cooldown)
