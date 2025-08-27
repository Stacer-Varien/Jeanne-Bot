from discord import Color, Embed
from functions import DevPunishment, Moderation, Reminder
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import datetime


class tasksCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_softbanned_members.start()
        self.check_reminders.start()
        self.check_suspended_users.start()

    @tasks.loop(seconds=60, reconnect=True)
    async def check_softbanned_members(self):
        for bans in Moderation().get_softban_data():
            if int(round(datetime.now().timestamp())) > int(bans[2]):
                guild = await self.bot.fetch_guild(bans[1])
                member = await self.bot.fetch_user(bans[0])
                await guild.unban(member, reason="Softban expired")
                await Moderation(guild, member).remove_softban()
                modlog = Moderation(guild).get_modlog_channel
                if modlog is not None:
                    if guild.preferred_locale.value in ["en-GB", "en-US"]:
                        unmute = Embed(title="Member unbanned", color=0xFF0000)
                        unmute.add_field(name="Member", value=member, inline=True)
                        unmute.add_field(name="ID", value=member.id, inline=True)
                        unmute.add_field(
                            name="Reason", value="Softban expired", inline=True
                        )
                        unmute.set_thumbnail(url=member.display_avatar)

                        await modlog.send(embed=unmute)
                    elif guild.preferred_locale.value == "fr":
                        unmute = Embed(title="Membre débanni", color=0xFF0000)
                        unmute.add_field(name="Membre", value=member, inline=True)
                        unmute.add_field(name="ID", value=member.id, inline=True)
                        unmute.add_field(
                            name="Raison", value="Softban expiré", inline=True
                        )
                        unmute.set_thumbnail(url=member.display_avatar)

                        await modlog.send(embed=unmute)
                    elif guild.preferred_locale.value == "de":
                        unmute = Embed(title="Mitglied entbannt", color=0xFF0000)
                        unmute.add_field(name="Mitglied", value=member, inline=True)
                        unmute.add_field(name="ID", value=member.id, inline=True)
                        unmute.add_field(
                            name="Grund", value="Softban abgelaufen", inline=True
                        )
                        unmute.set_thumbnail(url=member.display_avatar)

                    await modlog.send(embed=unmute)
                else:
                    continue

    @tasks.loop(seconds=60, reconnect=True)
    async def check_reminders(self):
        data = Reminder().get_all_reminders
        if data is None:
            return
        for reminder in data:
            if int(round(datetime.now().timestamp())) > int(reminder[2]):
                member = await self.bot.fetch_user(reminder[0])
                reminder_id = reminder[1]
                reason = reminder[3]
                try:
                    embed = Embed(title="Reminder ended", color=Color.random())
                    embed.add_field(name="Reminder", value=reason, inline=False)
                    await member.send(embed=embed)
                except Exception:
                    pass
                await Reminder(member).remove(reminder_id)
            else:
                continue

    @tasks.loop(seconds=60, reconnect=True)
    async def check_suspended_users(self):
        data = DevPunishment().get_suspended_users()
        if data is None:
            return
        for i in data:
            current_time = int(round(datetime.now().timestamp()))
            suspended_time = int(i[2])
            user = await self.bot.fetch_user(int(i[0]))
            if current_time > suspended_time:
                await DevPunishment(user).remove_suspended_user()
            else:
                continue

    @check_softbanned_members.before_loop
    async def before_softbans(self):
        await self.bot.wait_until_ready()

    @check_reminders.before_loop
    async def before_reminders(self):
        await self.bot.wait_until_ready()

    @check_suspended_users.before_loop
    async def before_check_suspended_users(self):
        await self.bot.wait_until_ready()


async def setup(bot: Bot):
    await bot.add_cog(tasksCog(bot))
