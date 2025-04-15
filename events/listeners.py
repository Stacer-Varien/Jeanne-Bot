from datetime import datetime, timedelta
from typing import Optional
from discord import DMChannel, Embed, Message, TextChannel, AllowedMentions
from discord.ext.commands import Bot, Cog
from config import TOPGG
from functions import BetaTest, DevPunishment, Levelling
from topgg import DBLClient
from collections import OrderedDict
from json import loads


class listenersCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.topggpy = DBLClient(
            bot=self.bot, token=TOPGG, autopost=True, post_shard_count=True
        )

    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @staticmethod
    async def send_level_message(channel: Optional[TextChannel], content: str, embed: Optional[Embed]):
        if channel is not None:
            await channel.send(
                content=content,
                embed=embed,
                allowed_mentions=AllowedMentions(
                    roles=False, everyone=False, users=True
                ),
            )

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
        cooldowns = level_instance.cooldowns

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
                voted = await self.topggpy.get_user_vote(message.author.id)
                checkbeta = await BetaTest(self.bot).check(message.author)
                weekend_check = datetime.isoweekday(datetime.now()) < 5
                if voted:
                    xp = 15 if weekend_check else 10
                    if checkbeta:
                        xp += 5
                else:
                    xp = 10 if weekend_check else 5
                    if checkbeta:
                        xp += 5

                lvl = await level_instance.add_xp(xp)
                user_cooldowns["servers"][server_id]["next_time"] = (
                    now_time + timedelta(minutes=2)
                )

                if now_time >= user_cooldowns["global"]["next_time"]:
                    user_cooldowns["global"]["next_time"] = now_time + timedelta(
                        minutes=2
                    )

                level_instance.save_cooldowns()
                if lvl is None:
                    return
                channel, update, levelup = lvl
                role_reward = message.guild.get_role(level_instance.get_role_reward)
                parameters = OrderedDict(
                    [
                        ("%member%", str(message.author)),
                        ("%pfp%", str(message.author.display_avatar)),
                        ("%server%", str(message.guild.name)),
                        ("%mention%", str(message.author.mention)),
                        ("%name%", str(message.author.name)),
                        (
                            "%newlevel%",
                            str(
                                Levelling(
                                    message.author, message.guild
                                ).get_member_level
                            ),
                        ),
                        (
                            "%role%",
                            str((role_reward.name if role_reward else None)),
                        ),
                        (
                            "%rolemention%",
                            str((role_reward.mention if role_reward else None)),
                        ),
                    ]
                )
                try:
                    await message.author.add_roles(role_reward)
                    if levelup == "0":
                        msg = "CONGRATS {}! You were role awarded {}".format(
                            message.author,
                            (role_reward.name if role_reward else None),
                        )

                        await self.send_level_message(channel, msg, None)
                    elif levelup is None:
                        pass
                    else:
                        json = loads(self.replace_all(levelup, parameters))
                        msg = json["content"]
                        embed = Embed.from_dict(json["embeds"][0])

                        await self.send_level_message(channel, msg, embed)
                except:
                    if update == "0":
                        msg = "{} has leveled up to `level {}`".format(
                            message.author,
                            Levelling(
                                message.author, message.guild
                            ).get_member_level,
                        )

                        await self.send_level_message(channel, msg, None)
                    elif update is None:
                        pass
                    else:
                        json = loads(self.replace_all(update, parameters))
                        msg = json["content"]
                        embed = Embed.from_dict(json["embeds"][0])

                        await self.send_level_message(channel, msg, embed)


async def setup(bot: Bot):
    await bot.add_cog(listenersCog(bot))
    bot.loop.create_task(Levelling().cleanup_cooldowns())
