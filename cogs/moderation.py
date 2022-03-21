from random import randint
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.ext.commands.errors import MissingPermissions, UserNotFound
from nextcord.utils import utcnow
from datetime import datetime, timedelta
from humanfriendly import parse_timespan
from config import db
from assets.errormsgs import *


format = "%d %b %Y | %H:%M:%S"


class slashmoderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Warn a member")
    async def warn(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to warn?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.kick_members is True:
                if reason == None:
                    reason = "Unspecified"
                
                if member == interaction.user:
                    failed=Embed(description="You can't warn yourself")
                    await interaction.followup.send(embed=failed)

                elif member.top_role.id == interaction.user.top_role.id:
                    failed = Embed(description="You can't warn someone who has the same role as you")
                    await interaction.followup.send(embed=failed)

                elif member.top_role > interaction.user.top_role:
                    failed = Embed(
                        description="You can't warn someone who has a higher role than you")
                    await interaction.followup.send(embed=failed)

                elif member.top_role < interaction.user.top_role:
                    
                    warn_id = f"{randint(0,100000)}"
                    date=datetime.now().strftime('%Y-%m-%d %H:%M')

                    cursor1 = db.execute("INSERT OR IGNORE INTO warnData (guild_id, user_id, moderator_id, reason, warn_id, date) VALUES (?,?,?,?,?,?)", (interaction.guild.id, member.id, interaction.user.id, reason, warn_id, date))

                    cursor2 = db.execute("INSERT OR IGNORE INTO warnDatav2 (guild_id, user_id, warn_points) VALUES (?,?,?)", (
                        interaction.guild.id, member.id, 1))

                    if cursor1.rowcount == 0:
                        db.execute(
                            f"UPDATE warnData SET moderator_id = {interaction.user.id}, reason = {reason}, warn_id = {warn_id} and date = {date} WHERE guild_id = {interaction.guild.id} AND user_id = {member.id}")
                    db.commit()

                    if cursor2.rowcount==0:
                        db.execute(
                            f"UPDATE warnDatav2 SET warn_points = warn_points + 1 WHERE guild_id = {interaction.guild.id} AND user_id = {member.id}")
                    db.commit()

                    warn = Embed(title="Member warned", color=0xFF0000)
                    warn.add_field(name="Member",
                                    value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                                    inline=True)
                    warn.add_field(
                        name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}\n**>** **Warn ID:** {warn_id}\n**>** **Date:** {date}", inline=True)
                    warn.set_thumbnail(url=member.display_avatar)

                    try:
                        modlog_channel_query = db.execute(
                            f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                        modlog_channel_id = modlog_channel_query.fetchone()[0]
                        modlog = interaction.guild.get_channel(modlog_channel_id)
                        await modlog.send(embed=warn)
                        warned = Embed(
                            description=f"Member has been warned. Check {modlog.mention}", color=0xFF0000)
                        await interaction.followup.send(embed=warned)
                    except:
                        await interaction.followup.send(embed=warn)

            elif interaction.permissions.kick_members is False:
                await interaction.followup.send(embed=warn_perm)

    @jeanne_slash(description="View warnings in the server or a member")
    async def list_warns(self, interaction: Interaction, member: Member = SlashOption(description="Who's warnings you wanna see?", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member == None:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM warnDATAv2 WHERE guild_id = {interaction.guild.id}")
                record = cur.fetchall()
                if len(record) == 0:
                    await interaction.followup.send(f"No warnings up to date")
                else:
                    embed = Embed(
                        title=f"Currently warned members", colour=0xFF0000)
                    embed.description = ""
                    for i in record:
                        warned_member = await self.bot.fetch_user(i[0])
                        warn_points = i[2]

                        embed.description += f"**{warned_member}**\n**Warn points**: {warn_points}\n\n"
                    await interaction.followup.send(embed=embed)

            else:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM warnDATA user WHERE user_id = {member.id} AND guild_id = {member.guild.id}")
                record = cur.fetchall()
                if len(record) == 0:
                    await interaction.followup.send(f"{member} has no warn IDs")
                    return
                embed = Embed(
                    title=f"{member}'s warnings", colour=0xFF0000)
                embed.description = ""
                embed.set_thumbnail(url=member.display_avatar)
                for i in record:
                    moderator = await self.bot.fetch_user(i[2])
                    reason = i[3]
                    warn_id = i[4]
                    date = i[5]

                    if date==None:
                        date="Unspecified due to new update"

                    embed.add_field(name=f"`{warn_id}`", value=f"**Moderator:** {moderator}\n**Reason:** {reason}\n**Date:** {date}", inline=False)
                await interaction.followup.send(embed=embed)

    @jeanne_slash(description="Revoke a warn by warn ID")
    async def revoke_warn(self, interaction: Interaction, warn_id=SlashOption(description="Provide the valid warn ID")):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.kick_members is True:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM warnData WHERE guild_id = {interaction.guild.id} AND warn_id = {warn_id}")
                result = cur.fetchone()

                if result == None:
                    await interaction.followup.send("Invalid warn ID")

                else:
                    cur.execute(
                        f"SELECT user_id FROM warnData WHERE warn_id = {warn_id}")
                    result = cur.fetchone()
                    cur.execute(f"DELETE FROM warnData WHERE warn_id = {warn_id}")

                    try:
                        cur.execute(f"UPDATE warnDatav2 SET warn_points = warn_points - 1 WHERE user_id = {result[0]} AND guild_id = {interaction.guild.id}")
                    except:
                        pass
                    
                    revoked_warn = Embed(
                        title="Warn removed!", description=f"{interaction.user} has revoked warn ID ({warn_id})")
                    try:
                        modlog_channel_query = db.execute(
                            f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                        modlog_channel_id = modlog_channel_query.fetchone()[0]
                        modlog = interaction.guild.get_channel(modlog_channel_id)
                        await modlog.send(embed=revoked_warn)
                        revoke = Embed(
                            description=f"Member has been warned. Check {modlog.mention}", color=0xFF0000)
                        await interaction.followup.send(embed=revoke)
                    except:
                        await interaction.followup.send(embed=revoked_warn)                    
                    db.commit()
            elif interaction.permissions.kick_members is False:
                await interaction.followup.send(embed=warn_perm)

    @jeanne_slash(description="Ban a member in the server")
    async def memberban(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to ban?"), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:        
            if interaction.permissions.ban_members is True:
                if reason == None:
                    reason = "Unspecified"

                if member == interaction.user:
                    failed = Embed(description="You can't ban yourself")
                    await interaction.followup.send(embed=failed)
                else:
                    try:
                        banmsg = Embed(
                            description=f"You are banned from **{interaction.guild.name}** for **{reason}**")
                        await member.send(embed=banmsg)
                    except:
                        pass
                    try:
                        await member.ban(reason=reason)
                        ban = Embed(title="Member Banned", color=0xFF0000)
                        ban.add_field(name="Member",
                                    value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                                    inline=True)
                        ban.add_field(
                            name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
                        ban.set_thumbnail(url=member.display_avatar)
                        try:
                            modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                            modlog_channel_id = modlog_channel_query.fetchone()[0]
                            modlog = interaction.guild.get_channel(
                                modlog_channel_id)
                            await modlog.send(embed=ban)
                            banned = Embed(
                                description=f"Member has been banned. Check {modlog.mention}", color=0xFF0000)
                            await interaction.followup.send(embed=banned)
                        except:
                            await interaction.followup.send(embed=ban)
                    except (Forbidden, MissingPermissions):
                        failed=Embed(description="Failed to ban member\nPlease check if you have permission to ban, I have permission to ban or my role is higher than the member")
                        await interaction.followup.send(embed=failed)
            elif interaction.permissions.ban_members is False:
                await interaction.followup.send(embed=ban_perm)

    @jeanne_slash(description="Ban a user before they join your server")
    async def outsideban(self, interaction: Interaction, user_id=SlashOption(description="Who do you want to ban with ID?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.ban_members is True:
                user = await self.bot.fetch_user(user_id)
                guild = interaction.guild
                if reason == None:
                    reason = "Unspecified"

                try:
                    banned = await guild.fetch_ban(user)
                except NotFound:
                    banned = False

                if banned:
                    already_banned = Embed(
                        description="User is already banned here")
                    await interaction.followup.send(embed=already_banned)

                else:
                    try:
                        await guild.ban(user, reason=reason)
                        ban = Embed(title="Member Banned", color=0xFF0000)
                        ban.add_field(name="Member",
                                    value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                                    inline=True)
                        ban.add_field(
                            name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
                        ban.set_thumbnail(url=user.display_avatar)
                        try:
                            modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                            modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                            modlog = interaction.guild.get_channel(
                                modlog_channel_id)
                            await modlog.send(embed=ban)
                            banned = Embed(
                                description=f"User has been banned. Check {modlog.mention}", color=0xFF0000)
                            await interaction.followup.send(embed=banned)
                        except:
                            await interaction.followup.send(embed=ban)
                    except (Forbidden, MissingPermissions):
                        failed = Embed(
                            description="Failed to ban member\nPlease check if you have permission to ban or I have permission to ban")
                        await interaction.followup.send(embed=failed)
            else:
                try:
                    await interaction.followup.send(embed=ban_perm)
                except UserNotFound:
                    await interaction.followup.send(embed=failed_ban)

    @jeanne_slash(description="Kick a member out of the server")
    async def kick(self, interaction: Interaction, member: Member = SlashOption(description="Who do you want to kick?"), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.kick_members is True:
                if member == interaction.user:
                    failed = Embed(description="You can't kick yourself out")
                    await interaction.followup.send(embed=failed)
                else:
                    try:
                        kickmsg = Embed(
                            description=f"You are kicked from **{interaction.guild.name}** for **{reason}**")
                        await member.send(embed=kickmsg)
                    except:
                        pass
                    try:
                        await member.kick(reason=reason)
                        kick = Embed(title="Member Kicked", color=0xFF0000)
                        kick.add_field(name="Member",
                                    value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                                    inline=True)
                        kick.add_field(
                            name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
                        kick.set_thumbnail(url=member.display_avatar)
                        try:
                            modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                            modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                            modlog = interaction.guild.get_channel(
                                modlog_channel_id)
                            await modlog.send(embed=kick)
                            kicked = Embed(
                                description=f"Member has been kicked. Check {modlog.mention}", color=0xFF0000)
                            await interaction.followup.send(embed=kicked)
                        except:
                            await interaction.followup.send(embed=kick)
                    except (Forbidden, MissingPermissions):
                        failed = Embed(
                            description="Failed to kick member\nPlease check if you have permission to kick, I have permission to kick or my role is higher than the member")
                        await interaction.followup.send(embed=failed)
                
            elif interaction.permissions.kick_members is False:
                await interaction.followup.send(embed=kick_perm)

    @jeanne_slash(description="Bulk delete messages")
    async def purge(self, interaction: Interaction, limit=SlashOption(description="How many messages are you deleting?", required=False), member: Member = SlashOption(description="Who's messages are you deleting?", required=False)):
        await interaction.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.manage_messages is True:
                if int(limit) > 100:
                    await interaction.followup.send("That is over the API limit")
                else:
                    if int(limit)==None:
                        limit=100
                    
                    elif int(limit) < 100:
                        limit=limit
                
                    if member:
                        def is_member(m):
                            return m.author==member

                        await interaction.channel.purge(limit=int(limit), check=is_member)
                        await interaction.followup.send(f"Deleted {limit} messages from {member}")

                    elif not member:
                        await interaction.channel.purge(limit=int(limit))
                        await interaction.followup.send(f"Deleted {limit} messages")   
            elif interaction.permissions.manage_messages is False:
                await interaction.followup.send(embed=message_perm)

    @jeanne_slash(description="Change someone's nickname")
    async def change_nickname(self, interaction: Interaction, member: Member = SlashOption(description="Who's nickname are you changing?", required=True), nickname=SlashOption(description="What will be their new name?", required=True)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.manage_nicknames is True:
                await member.edit(nick=nickname)
                setnick = Embed(color=0x00FF68)
                setnick.add_field(name="Nickname changed",
                                value=f"{member}'s nickname is now `{nickname}`", inline=False)
                await interaction.followup.send(embed=setnick)
            elif interaction.permissions.manage_nicknames is False:
                await interaction.followup.send(embed=nick_perm)

    @jeanne_slash(description="Unbans a user")
    async def unban(self, interaction: Interaction, user_id=SlashOption(description="Who do you want to unban with ID?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.ban_members is True:
                user = await self.bot.fetch_user(user_id)
                await interaction.guild.unban(user, reason=reason)
                unban = Embed(title="User Unbanned", color=0xFF0000)
                unban.add_field(name="Member",
                                value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                                inline=True)
                unban.add_field(
                    name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
                unban.set_thumbnail(url=user.display_avatar)
                try:
                    modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                    modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                    modlog = interaction.guild.get_channel(
                                modlog_channel_id)
                    await modlog.send(embed=unban)
                    unbanned = Embed(
                                description=f"Member has been unbanned. Check {modlog.mention}", color=0xFF0000)
                    await interaction.followup.send(embed=unbanned)
                except:
                        await interaction.followup.send(embed=unban)
            else:
                try:
                    await interaction.followup.send(embed=unban_perm)
                except MissingPermissions:
                    await interaction.followup.send(embed=failed_unban)

    @jeanne_slash(description="Mute a member")
    async def mute(self, interaction: Interaction, member: Member = SlashOption(description="Who are you muting?", required=True), time=SlashOption(description="How long will the member be muted?", required=False), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.moderate_members is True:
                    if time is None:
                        time = '28d'

                    if reason is None:
                            reason = "Unspecified"
                        
                    if member == interaction.user:
                            failed=Embed(description="You can't mute yourself")
                            await interaction.followup.send(embed=failed)

                    else:
                            timed = parse_timespan(time)
                            await member.edit(timeout=utcnow()+timedelta(seconds=timed), reason=reason)
                            mute = Embed(
                                title="Member Muted", color=0xFF0000)
                            mute.add_field(name="Member",
                                            value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                                            inline=True)
                            mute.add_field(
                                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}\n**>** **Duration:** {time}", inline=True)
                            mute.set_thumbnail(url=member.display_avatar)
                            try:
                                modlog_channel_query = db.execute(
                                    f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                                modlog_channel_id = modlog_channel_query.fetchone()[
                                    0]
                                modlog = interaction.guild.get_channel(
                                    modlog_channel_id)
                                await modlog.send(embed=mute)
                                muted = Embed(
                                    description=f"Member has been muted. Check {modlog.mention}", color=0xFF0000)
                                await interaction.followup.send(embed=muted)
                            except:
                                await interaction.followup.send(embed=mute)
            elif interaction.permissions.moderate_members is False:
                await interaction.followup.send(embed=mute_perm)

    @jeanne_slash()
    async def unmute(self, interaction: Interaction, member: Member = SlashOption(description="Who are you unmuting?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await interaction.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {interaction.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if interaction.user.id == botbanned_user.id:
                await interaction.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if interaction.permissions.moderate_members is True:
                if reason == None:
                    reason = "Unspecified"

                if member == interaction.user:
                    failed = Embed(description="You can't unmute yourself")
                    await interaction.followup.send(embed=failed)

                else:
                    await member.edit(timeout=None, reason=reason)
                    unmute = Embed(
                        title="Member Unmuted", color=0xFF0000)
                    unmute.add_field(name="Member",
                                    value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                                    inline=True)
                    unmute.add_field(
                        name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
                    unmute.set_thumbnail(url=member.display_avatar)
                    try:
                        modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {interaction.guild.id}')
                        modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                        modlog = interaction.guild.get_channel(
                                modlog_channel_id)
                        await modlog.send(embed=unmute)
                        unmuted = Embed(
                                description=f"Member has been unmuted. Check {modlog.mention}", color=0xFF0000)
                        await interaction.followup.send(embed=unmuted)
                    except:
                        await interaction.followup.send(embed=unmute)
            elif interaction.permissions.moderate_members is False:
                interaction.followup.send(embed=unmute_perm)


def setup(bot):
    bot.add_cog(slashmoderation(bot))
