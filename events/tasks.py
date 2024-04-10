from discord import Color, Embed
from functions import Moderation, Reminder
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from datetime import datetime


class tasksCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.check_softbanned_members.start()
        self.check_reminders.start()

    @tasks.loop(seconds=60, reconnect=True)
    async def check_softbanned_members(self):
        for bans in Moderation().get_softban_data():
            if int(round(datetime.now().timestamp())) > int(bans[2]):
                guild = await self.bot.fetch_guild(bans[1])
                member = await self.bot.fetch_user(bans[0])
                await guild.unban(member, reason="Softban expired")
                await Moderation(guild, member).remove_softban()
                mod_channel = Moderation(guild).get_modlog_channel
                if mod_channel != None:
                    unmute = Embed(title="Member unbanned", color=0xFF0000)
                    unmute.add_field(name="Member", value=member, inline=True)
                    unmute.add_field(name="ID", value=member.id, inline=True)
                    unmute.add_field(
                        name="Reason", value="Softban expired", inline=True
                    )
                    unmute.set_thumbnail(url=member.display_avatar)
                    modlog = await guild.fetch_channel(mod_channel)
                    await modlog.send(embed=unmute)
                else:
                    continue

    @check_softbanned_members.before_loop
    async def before_check_softbanned_members(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=60, reconnect=True)
    async def check_reminders(self):
        data = Reminder().get_all_reminders
        if data == None:
            return
        for reminder in data:
            if int(round(datetime.now().timestamp())) > int(reminder[2]):
                member = await self.bot.fetch_user(reminder[0])
                id = reminder[1]
                reason = reminder[3]
                try:
                    embed = Embed(title="Reminder ended", color=Color.random())
                    embed.add_field(name="Reminder", value=reason, inline=False)
                    await member.send(embed=embed)
                except:
                    pass
                await Reminder(member).remove(id)
            else:
                continue

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()


async def setup(bot: Bot):
    await bot.add_cog(tasksCog(bot))
