from asyncio import sleep
from random import randint
from nextcord import Member, Embed, NotFound, Interaction, slash_command as jeanne_slash, Interaction, SlashOption
from nextcord.ext.commands import Cog
from nextcord.ext.commands.errors import MissingPermissions, UserNotFound
from nextcord.utils import utcnow
from datetime import timedelta
from humanfriendly import parse_timespan
from sqlite3 import connect
from assets.errormsgs import kick_perm, ban_perm, warn_perm, unban_perm, failed_unban, failed_ban, nick_perm, mute_perm, message_perm, unmute_perm


format = "%d %b %Y | %H:%M:%S"
db = connect("database.db")


class slashmoderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Warn a member")
    async def warn(self, interaction: Interaction, member: Member, reason=SlashOption(description="Give a reason", required=False)):
        if interaction.permissions.kick_members is True:
            if reason == None:
                reason = "Unspecified"

            warn_id = f"{randint(0,100000)}"

            cursor = db.execute("INSERT OR IGNORE INTO warnData (guild_id, user_id, moderator_id, reason, warn_id) VALUES (?,?,?,?,?)",
                                (interaction.guild.id, member.id, interaction.user.id, reason, warn_id))
            if cursor.rowcount == 0:
                db.execute(
                    f"UPDATE warnData SET moderator_id = {interaction.user.id}, reason = {reason} AND warn_id = {warn_id} WHERE guild_id = {interaction.guild.id} AND user_id = {member.id}")
            db.commit()

            embed = Embed(title="Member warned", color=0xFF0000)
            embed.add_field(name="Member",
                            value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                            inline=True)
            embed.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}\n**>** **Warn ID:** {warn_id}", inline=True)
            embed.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=warn_perm)

    @jeanne_slash(description="View warnings in the server or a member")
    async def list_warns(self, interaction: Interaction, member: Member = SlashOption(required=None)):
        if member == None:
            cur = db.cursor()
            cur.execute(
                f"SELECT * FROM warnDATA user WHERE(guild_id = {interaction.guild.id})")
            record = cur.fetchall()
            await interaction.response.defer()
            if len(record) == 0:
                await interaction.followup.send(f"No warnings up to date")
                return
            embed = Embed(
                title=f"Current warnings in server", colour=0xFF0000)
            embed.description = ""
            for i in record:
                warned_member = await self.bot.fetch_user(i[0])
                moderator = await self.bot.fetch_user(i[2])
                warn_id = i[4]
                embed.description += f"**{warned_member}**\n**Warn ID**:{warn_id}\n\n"
            await interaction.followup.send(embed=embed)

        else:
            cur = db.cursor()
            cur.execute(
                f"SELECT * FROM warnDATA user WHERE(user_id = {member.id} AND guild_id = {member.guild.id})")
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
                embed.description += f"**Warn ID**:{warn_id}\n**Moderator:** {moderator}\n**Reason:** {reason}\n\n"
            await interaction.response.defer()
            await interaction.followup.send(embed=embed)

    @jeanne_slash(description="Revoke a warn by warn ID")
    async def revoke_warn(self, interaction: Interaction, warn_id):
        if interaction.permissions.kick_members is True:
            cur = db.cursor()
            cur.execute(
                f"SELECT * FROM warnData WHERE guild_id = {interaction.guild.id} AND warn_id = {warn_id}")
            result = cur.fetchone()

            if result == None:
                await interaction.followup.send("Invalid warn ID")

            else:
                cursor1 = db.cursor()
                cursor1.execute(
                    f"SELECT user_id FROM warnData WHERE warn_id = '{warn_id}'")
                result = cursor1.fetchone()
                cur.execute(f"DELETE FROM warnData WHERE warn_id = {warn_id}")
                embed = Embed(
                    title="Warn removed!", description=f"{interaction.user} has revoked warn ID ({warn_id})")
                await interaction.response.send_message(embed=embed)
                db.commit()
        else:
            await interaction.response.send_message(embed=warn_perm)

    @jeanne_slash(description="Ban a member in the server")
    async def memberban(self, interaction: Interaction, member: Member, reason=SlashOption(description="Give a reason", required=False)):
        if interaction.permissions.ban_members is True:
            if reason == None:
                reason = "Unspecified"

            try:
                banmsg = Embed(
                    description=f"You are banned from **{interaction.guild.name}** for **{reason}**")
                await member.send(embed=banmsg)
            except:
                pass
            ban = Embed(title="Member Banned", color=0xFF0000)
            ban.add_field(name="Member",
                          value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                          inline=True)
            ban.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
            ban.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=ban)
            await member.ban(reason=reason)
        else:
            await interaction.response.send_message(embed=ban_perm)

    @jeanne_slash(description="Ban a user before they join your server")
    async def outsideban(self, interaction: Interaction, user_id, reason=SlashOption(description="Give a reason", required=False)):
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
                await interaction.response.send_message(embed=already_banned)

            else:
                ban = Embed(title="Member Banned", color=0xFF0000)
                ban.add_field(name="Member",
                              value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                              inline=True)
                ban.add_field(
                    name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
                ban.set_thumbnail(url=user.display_avatar)
                await interaction.response.send_message(embed=ban)
                await guild.ban(user, reason=reason)
        else:
            try:
                await interaction.response.send_message(embed=ban_perm)
            except UserNotFound:
                await interaction.response.send_message(embed=failed_ban)

    @jeanne_slash(description="Kick a member out of the server")
    async def kick(self, interaction: Interaction, member: Member, reason=SlashOption(description="Give a reason", required=False)):
        if interaction.permissions.kick_members is True:
            try:
                kickmsg = Embed(
                    description=f"You are kicked from **{interaction.guild.name}** for **{reason}**")
                await member.send(embed=kickmsg)
            except:
                pass
            kick = Embed(title="Member Kicked", color=0xFF0000)
            kick.add_field(name="Member",
                           value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                           inline=True)
            kick.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
            kick.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=kick)
            await member.kick(reason=reason)
        else:
            await interaction.response.send_message(embed=kick_perm)

    @jeanne_slash(description="Bulk delete messages")
    async def purge(self, interaction: Interaction, limit=SlashOption(required=False), member: Member = SlashOption(required=False)):
        if interaction.permissions.manage_messages is True:
            if limit==None:
                limit=100
            msg = []
            try:
                limit = int(limit)
            except:
                return await interaction.response.send_message("Please pass in an integer as limit")
            if not member:
                await interaction.channel.purge(limit=limit)
                await interaction.response.send_message(f"{limit} messages deleted", ephemeral=True)
            async for m in interaction.channel.history():
                if len(msg) == limit:
                    break
                if m.author == member:
                    msg.append(m)
            await interaction.channel.delete_messages(msg)
        else:
            await interaction.response.send_message(embed=message_perm)

    @jeanne_slash(description="Change someone's nickname")
    async def change_nickname(self, interaction: Interaction, member: Member, nickname=None):
        if interaction.permissions.manage_nicknames is True:
            await member.edit(nick=nickname)
            setnick = Embed(color=0x00FF68)
            setnick.add_field(name="Nickname changed",
                              value=f"{member}'s nickname is now `{nickname}`", inline=False)
            await interaction.response.send_message(embed=setnick)
        else:
            await interaction.response.send_message(embed=nick_perm)

    @jeanne_slash(description="Unbans a user")
    async def unban(self, interaction: Interaction, user_id, reason=SlashOption(description="Give a reason", required=False)):
        if interaction.permissions.ban_members is True:
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user, reason=reason)
            embed = Embed(title="User Unbanned", color=0xFF0000)
            embed.add_field(name="Member",
                            value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                            inline=True)
            embed.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
            embed.set_thumbnail(url=user.display_avatar)
            await interaction.response.send_message(embed=embed)
        else:
            try:
                await interaction.response.send_message(embed=unban_perm)
            except MissingPermissions:
                await interaction.response.send_message(embed=failed_unban)

    @jeanne_slash(description="Mute a member")
    async def mute(self, interaction: Interaction, member: Member = SlashOption(required=True), time=SlashOption(description="How long is the member muted", required=False), reason=SlashOption(description="Give a reason", required=False)):
        if interaction.permissions.moderate_members is True:
            if time is None:
                time = f'{28}d'

            if reason is None:
                reason = "Unspecified"

            time = parse_timespan(time)
            await member.edit(timeout=utcnow()+timedelta(seconds=time), reason=reason)
            embed = Embed(
                title="Member Muted", color=0xFF0000)
            embed.add_field(name="Member",
                            value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                            inline=True)
            embed.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
            embed.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=mute_perm)

    @jeanne_slash()
    async def unmute(self, interaction: Interaction, member: Member, reason=SlashOption(description="Give a reason", required=False)):
        if interaction.permissions.moderate_members is True:
            if reason == None:
                reason = "Unspecified"
            await member.edit(timeout=None, reason=reason)
            embed = Embed(
                title="Member Unmuted", color=0xFF0000)
            embed.add_field(name="Member",
                            value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                            inline=True)
            embed.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {interaction.user}\n**>** **Reason:** {reason}", inline=True)
            embed.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
        else:
            interaction.response.send_message(embed=unmute_perm)


def setup(bot):
    bot.add_cog(slashmoderation(bot))
