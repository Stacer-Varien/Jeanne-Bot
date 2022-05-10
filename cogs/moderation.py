from random import randint
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog
from nextcord.ext.application_checks import *
from nextcord.utils import utcnow
from datetime import datetime, timedelta
from humanfriendly import parse_timespan
from config import db
from assets.errormsgs import *
from nextcord.ext.application_checks.errors import *
from nextcord.ext.commands.errors import *


format = "%d %b %Y | %H:%M:%S"


class slashmoderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Warn a member")
    @has_permissions(kick_members=True)
    async def warn(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to warn?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                if reason == None:
                    reason = "Unspecified"
                
                if member == ctx.user:
                    failed=Embed(description="You can't warn yourself")
                    await ctx.followup.send(embed=failed)

                else:                    
                    warn_id = f"{randint(0,100000)}"
                    date=datetime.now().strftime('%Y-%m-%d %H:%M')

                    cursor1 = db.execute("INSERT OR IGNORE INTO warnData (guild_id, user_id, moderator_id, reason, warn_id, date) VALUES (?,?,?,?,?,?)", (ctx.guild.id, member.id, ctx.user.id, reason, warn_id, date))

                    cursor2 = db.execute("INSERT OR IGNORE INTO warnDatav2 (guild_id, user_id, warn_points) VALUES (?,?,?)", (
                        ctx.guild.id, member.id, 1))

                    if cursor1.rowcount == 0:
                        db.execute(
                            f"UPDATE warnData SET moderator_id = {ctx.user.id}, reason = {reason}, warn_id = {warn_id} and date = {date} WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}")
                    db.commit()

                    if cursor2.rowcount==0:
                        db.execute(
                            f"UPDATE warnDatav2 SET warn_points = warn_points + 1 WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}")
                    db.commit()

                    warn = Embed(title="Member warned", color=0xFF0000)
                    warn.add_field(name="Member",
                                    value=member,
                                    inline=True)
                    warn.add_field(name="ID",
                                    value=member.id,
                                    inline=True)                                    
                    warn.add_field(
                        name="Moderator", value=ctx.user, inline=True)
                    warn.add_field(name="Reason",
                                    value=reason,
                                    inline=False)
                    warn.add_field(name="Warn ID",
                                    value=warn_id,
                                    inline=True)
                    warn.add_field(name="Date",
                                    value=date,
                                    inline=True)
                    warn.set_thumbnail(url=member.display_avatar)

                    try:
                        modlog_channel_query = db.execute(
                            f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                        modlog_channel_id = modlog_channel_query.fetchone()[0]
                        modlog = ctx.guild.get_channel(modlog_channel_id)
                        await modlog.send(embed=warn)
                        warned = Embed(
                            description=f"Member has been warned. Check {modlog.mention}", color=0xFF0000)
                        await ctx.followup.send(embed=warned)
                    except:
                        await ctx.followup.send(embed=warn)

    @warn.error
    async def warn_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=warn_perm)

    @jeanne_slash(description="View warnings in the server or a member")
    async def list_warns(self, ctx: Interaction, member: Member = SlashOption(description="Who's warnings you wanna see?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member == None:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM warnDATAv2 WHERE guild_id = {ctx.guild.id}")
                record = cur.fetchall()
                if len(record) == 0:
                    await ctx.followup.send(f"No warnings up to date")
                else:
                    embed = Embed(
                        title=f"Currently warned members", colour=0xFF0000)
                    embed.description = ""
                    for i in record:
                        warned_member = await self.bot.fetch_user(i[0])
                        warn_points = i[2]

                        embed.description += f"**{warned_member}**\n**Warn points**: {warn_points}\n\n"
                    await ctx.followup.send(embed=embed)

            else:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM warnDATA user WHERE user_id = {member.id} AND guild_id = {member.guild.id}")
                record = cur.fetchall()
                if len(record) == 0:
                    await ctx.followup.send(f"{member} has no warn IDs")
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
                await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Revoke a warn by warn ID")
    @has_permissions(kick_members=True)
    async def revoke_warn(self, ctx: Interaction, warn_id=SlashOption(description="Provide the valid warn ID")):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                cur = db.cursor()
                cur.execute(
                    f"SELECT * FROM warnData WHERE guild_id = {ctx.guild.id} AND warn_id = {warn_id}")
                result = cur.fetchone()

                if result == None:
                    await ctx.followup.send("Invalid warn ID")

                else:
                    cur.execute(
                        f"SELECT user_id FROM warnData WHERE warn_id = {warn_id}")
                    result = cur.fetchone()
                    cur.execute(f"DELETE FROM warnData WHERE warn_id = {warn_id}")

                    try:
                        cur.execute(f"UPDATE warnDatav2 SET warn_points = warn_points - 1 WHERE user_id = {result[0]} AND guild_id = {ctx.guild.id}")

                        wp_query=cur.execute(f"SELECT warn_points FROM warnDatav2 WHERE user_id = {result[0]} AND guild_id = {ctx.guild.id}")
                        warnpoints=wp_query.fetchone()[0]

                        if warnpoints==0:
                            cur.execute(f"DELETE FROM warnDatav2 WHERE user_id = {result[0]} AND guild_id = {ctx.guild.id}")
                    except:
                        pass
                    
                    revoked_warn = Embed(
                        title="Warn removed!", description=f"{ctx.user} has revoked warn ID ({warn_id})")
                    try:
                        modlog_channel_query = db.execute(
                            f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                        modlog_channel_id = modlog_channel_query.fetchone()[0]
                        modlog = ctx.guild.get_channel(modlog_channel_id)
                        await modlog.send(embed=revoked_warn)
                        revoke = Embed(
                            description=f"Warn revoked. Check {modlog.mention}", color=0xFF0000)
                        await ctx.followup.send(embed=revoke)
                    except:
                        await ctx.followup.send(embed=revoked_warn)                    
                    db.commit()

    @revoke_warn.error
    async def revoke_warn_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=warn_perm)

    @jeanne_slash(description="Main ban command")
    async def ban(self, ctx: Interaction):
        pass        


    @ban.subcommand(description="Ban someone in this server")
    @has_permissions(ban_members=True)
    async def member(self, ctx:Interaction, member:Member=SlashOption(description="Who do you want to ban?", required=True), reason=SlashOption(description='What is the reason?', required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            if member == ctx.user:
                failed = Embed(description="You can't ban yourself")
                await ctx.followup.send(embed=failed)
            else:
                try:
                    banmsg = Embed(description=f"You are banned from **{ctx.guild.name}** for **{reason}**")
                    await member.send(embed=banmsg)
                except:
                    pass

                await member.ban(reason=reason)
                ban = Embed(title="Member Banned", color=0xFF0000)
                ban.add_field(name="Name", value=member, inline=True)
                ban.add_field(name="ID", value=member.id, inline=True)
                ban.add_field(name="Moderator", value=ctx.user, inline=True)
                ban.add_field(name="Reason", value=reason, inline=False)
                ban.set_thumbnail(url=member.display_avatar)

                try:
                    modlog_channel_query = db.execute(f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                    modlog_channel_id = modlog_channel_query.fetchone()[0]
                    modlog = ctx.guild.get_channel(modlog_channel_id)
                    await modlog.send(embed=ban)
                    banned = Embed(description=f"Member has been banned. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=banned)
                except:
                    await ctx.followup.send(embed=ban)

    @ban.subcommand(description="Ban someone outside the server")
    @has_permissions(ban_members=True)
    async def user(self, ctx:Interaction, user_id=SlashOption(description="What is the User ID?", required=True), reason=SlashOption(description="What is the reason", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
            user = await self.bot.fetch_user(user_id)
            guild = ctx.guild
            if reason == None:
                reason = "Unspecified"

            try:
                banned = await guild.fetch_ban(user)
            except NotFound:
                banned = False

            if banned:
                already_banned = Embed(description="User is already banned here")
                await ctx.followup.send(embed=already_banned)

            else:
                await guild.ban(user, reason=reason)
                ban = Embed(title="User Banned", color=0xFF0000)
                ban.add_field(name="Name", value=user, inline=True)
                ban.add_field(name="ID", value=user.id, inline=True)
                ban.add_field(name="Moderator", value=ctx.user, inline=True)
                ban.add_field(name="Reason", value=reason, inline=False)
                ban.set_thumbnail(url=user.display_avatar)
                
                try:
                    modlog_channel_query = db.execute(f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                    modlog_channel_id = modlog_channel_query.fetchone()[0]
                    modlog = ctx.guild.get_channel(
                    modlog_channel_id)
                    await modlog.send(embed=ban)
                    banned = Embed(description=f"User has been banned. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=banned)
                except:
                    await ctx.followup.send(embed=ban)


    @member.error
    async def ban_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=ban_perm)

    @user.error
    async def ban_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=ban_perm)

        elif isinstance(error, Exception):
            await ctx.response.defer()
            await ctx.followup.send("Invalid user ID")


    @jeanne_slash(description="Kick a member out of the server")
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Interaction, member: Member = SlashOption(description="Who do you want to kick?"), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                if member == ctx.user:
                    failed = Embed(description="You can't kick yourself out")
                    await ctx.followup.send(embed=failed)
                else:
                    try:
                        kickmsg = Embed(
                            description=f"You are kicked from **{ctx.guild.name}** for **{reason}**")
                        await member.send(embed=kickmsg)
                    except:
                        pass
                    await member.kick(reason=reason)
                    kick = Embed(title="Member Kicked", color=0xFF0000)
                    kick.add_field(name="Member",
                                    value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                                    inline=True)
                    kick.add_field(
                            name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.user}\n**>** **Reason:** {reason}", inline=True)
                    kick.set_thumbnail(url=member.display_avatar)
                    try:
                            modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                            modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                            modlog = ctx.guild.get_channel(
                                modlog_channel_id)
                            await modlog.send(embed=kick)
                            kicked = Embed(
                                description=f"Member has been kicked. Check {modlog.mention}", color=0xFF0000)
                            await ctx.followup.send(embed=kicked)
                    except:
                            await ctx.followup.send(embed=kick)

    @kick.error
    async def kick_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=kick_perm)

    @jeanne_slash(description="Bulk delete messages")
    @has_permissions(manage_messages=True)
    async def purge(self, ctx: Interaction, limit=SlashOption(description="How many messages are you deleting?", required=False), member: Member = SlashOption(description="Who's messages are you deleting?", required=False)):
        await ctx.response.defer(ephemeral=True)
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                    if limit==None:
                        limit=100
                
                    if member:
                        def is_member(m):
                            return m.author==member

                        await ctx.channel.purge(limit=int(limit), check=is_member)
                        await ctx.followup.send(f"Deleted {limit} messages from {member}")

                    elif not member:
                        await ctx.channel.purge(limit=int(limit))
                        await ctx.followup.send(f"Deleted {limit} messages")   

    @purge.error
    async def purge_error(self, ctx:Interaction, error):
        if isinstance(error, MissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=message_perm)

    @jeanne_slash(description="Change someone's nickname")
    @has_permissions(manage_nicknames=True)
    async def change_nickname(self, ctx: Interaction, member: Member = SlashOption(description="Who's nickname are you changing?", required=True), nickname=SlashOption(description="What will be their new name?", required=True)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                await member.edit(nick=nickname)
                setnick = Embed(color=0x00FF68)
                setnick.add_field(name="Nickname changed",
                                value=f"{member}'s nickname is now `{nickname}`", inline=False)
                await ctx.followup.send(embed=setnick)

    @change_nickname.error
    async def change_nickname_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=nick_perm)

    @jeanne_slash(description="Unbans a user")
    @has_permissions(ban_members=True)
    async def unban(self, ctx: Interaction, user_id=SlashOption(description="Who do you want to unban with ID?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                user = await self.bot.fetch_user(user_id)
                await ctx.guild.unban(user, reason=reason)
                unban = Embed(title="User Unbanned", color=0xFF0000)
                unban.add_field(name="Name", value=user, inline=True)
                unban.add_field(name="ID", value=user.id, inline=True)
                unban.add_field(name="Moderator", value=ctx.user, inline=True)
                unban.add_field(name="Reason", value=reason, inline=False)
                unban.set_thumbnail(url=user.display_avatar)
                try:
                    modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                    modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                    modlog = ctx.guild.get_channel(
                                modlog_channel_id)
                    await modlog.send(embed=unban)
                    unbanned = Embed(
                                description=f"Member has been unbanned. Check {modlog.mention}", color=0xFF0000)
                    await ctx.followup.send(embed=unbanned)
                except:
                        await ctx.followup.send(embed=unban)

    @unban.error
    async def unban_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=unban_perm)

        elif isinstance(error, UserNotFound):
            await ctx.response.defer()
            await ctx.followup.send("Invalid user ID")                    

    @jeanne_slash(description="Mute a member")
    @has_permissions(moderate_members=True)
    async def mute(self, ctx: Interaction, member: Member = SlashOption(description="Who are you muting?", required=True), time=SlashOption(description="How long will the member be muted?", required=False), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                    if time == None:
                        time = '28d'

                    if reason is None:
                            reason = "Unspecified"
                        
                    if member == ctx.user:
                            failed=Embed(description="You can't mute yourself")
                            await ctx.followup.send(embed=failed)

                    else:
                            timed = parse_timespan(time)
                            await member.edit(timeout=utcnow()+timedelta(seconds=timed), reason=reason)
                            mute = Embed(
                                title="Member Muted", color=0xFF0000)
                            mute.add_field(name="Member", value=member, inline=True)
                            mute.add_field(name="ID", value=member.id, inline=True)
                            mute.add_field(
                                name="Moderator", value=ctx.user, inline=True)
                            mute.add_field(
                                name="Duration", value=time, inline=True)
                            mute.add_field(
                                name="Reason", value=reason, inline=False)
                            mute.set_thumbnail(url=member.display_avatar)
                            try:
                                modlog_channel_query = db.execute(
                                    f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                                modlog_channel_id = modlog_channel_query.fetchone()[
                                    0]
                                modlog = ctx.guild.get_channel(
                                    modlog_channel_id)
                                await modlog.send(embed=mute)
                                muted = Embed(
                                    description=f"Member has been muted. Check {modlog.mention}", color=0xFF0000)
                                await ctx.followup.send(embed=muted)
                            except:
                                await ctx.followup.send(embed=mute)

    @mute.error
    async def mute_error(self, ctx:Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=mute_perm)

    @jeanne_slash()
    @has_permissions(moderate_members=True)
    async def unmute(self, ctx: Interaction, member: Member = SlashOption(description="Who are you unmuting?", required=True), reason=SlashOption(description="Give a reason", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                f"SELECT * FROM botbannedData WHERE user_id = {ctx.user.id}")
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]
            reason = botbanned_data[1]

            botbanned_user = await self.bot.fetch_user(botbanned)
            if ctx.user.id == botbanned_user.id:
                await ctx.followup.send(f"You have been botbanned for:\n{reason}", ephemeral=True)
        except:
                if reason == None:
                    reason = "Unspecified"

                if member == ctx.user:
                    failed = Embed(description="You can't unmute yourself")
                    await ctx.followup.send(embed=failed)

                else:
                    await member.edit(timeout=None, reason=reason)
                    unmute = Embed(
                        title="Member Unmuted", color=0xFF0000)
                    unmute.add_field(name="Member", value=member, inline=True)
                    unmute.add_field(name="ID", value=member.id, inline=True)
                    unmute.add_field(
                        name="Moderator", value=ctx.user, inline=True)
                    unmute.add_field(
                        name="Reason", value=reason, inline=False)
                    unmute.set_thumbnail(url=member.display_avatar)
                    try:
                        modlog_channel_query = db.execute(
                                f'SELECT channel_id FROM modlogData WHERE guild_id = {ctx.guild.id}')
                        modlog_channel_id = modlog_channel_query.fetchone()[
                                0]
                        modlog = ctx.guild.get_channel(
                                modlog_channel_id)
                        await modlog.send(embed=unmute)
                        unmuted = Embed(
                                description=f"Member has been unmuted. Check {modlog.mention}", color=0xFF0000)
                        await ctx.followup.send(embed=unmuted)
                    except:
                        await ctx.followup.send(embed=unmute)

    @unmute.error
    async def unmute_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationMissingPermissions):
            await ctx.response.defer()
            await ctx.followup.send(embed=unmute_perm)


def setup(bot):
    bot.add_cog(slashmoderation(bot))
