from datetime import datetime, timedelta
from typing import Optional
from discord import DMChannel, Embed, Message, TextChannel
from discord.ext.commands import Bot, Cog
from functions import DevPunishment, Levelling


class listenersCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot or isinstance(message.channel, DMChannel):
            return

        if DevPunishment(message.author).check_botbanned_user:
            return

        level_instance = Levelling(message.author, message.guild)

        user_id = message.author.id
        server_id = message.guild.id
        now_time = datetime.now()
        cooldowns=level_instance.cooldowns

        if user_id not in cooldowns:
            cooldowns[user_id] = {
                "global": {"next_time": datetime.min},
                "servers": {},
            }

        user_cooldowns = cooldowns[user_id]

        if server_id not in user_cooldowns["servers"]:
            user_cooldowns["servers"][server_id] = {"next_time": datetime.min}

        if now_time >= user_cooldowns["servers"][server_id]["next_time"]:
                if level_instance.check_xpblacklist_channel(message.channel) is None:
                    weekend_check = now_time.isoweekday() >= 6
                    xp = 15 if weekend_check else 10
                    await level_instance.add_xp(xp)
                    user_cooldowns["servers"][server_id]["next_time"] = now_time + timedelta(minutes=2)

                    if now_time >= user_cooldowns["global"]["next_time"]:
                        user_cooldowns["global"]["next_time"] = now_time + timedelta(minutes=2)

                    level_instance.save_cooldowns()

    async def send_level_message(
        self, channel: Optional[TextChannel], content: str, embed: Optional[Embed]
    ):
        if channel is not None:
            await channel.send(content=content, embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(listenersCog(bot))
    bot.loop.create_task(Levelling().cleanup_cooldowns())
