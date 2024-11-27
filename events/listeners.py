from collections import OrderedDict
from datetime import datetime
from json import loads
from typing import Optional
from discord import AllowedMentions, DMChannel, Embed, Message, TextChannel
from discord.ext.commands import Bot, Cog
from functions import BetaTest, DevPunishment, Levelling
from topgg import DBLClient
from config import TOPGG


class listenersCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @Cog.listener()
    async def on_message(self, message: Message):
        if DevPunishment(message.author).check_botbanned_user:
            return

        try:
            if not message.author.bot and not isinstance(message.channel, DMChannel):
                level_instance = Levelling(message.author, message.guild)
                if level_instance.check_xpblacklist_channel(message.channel) == (
                    False or None
                ):
                    try:
                        now_time = round(datetime.now().timestamp())
                        if now_time> level_instance.get_next_time_global:
                            get_vote = await self.topggpy.get_user_vote(message.author.id)

                            check = await BetaTest(self.bot).check(message.author)
                            weekend_check = (
                                True if (datetime.isoweekday(datetime.now()) < 5) else False
                            )
                            if get_vote == True:
                                xp = 15 if weekend_check else 10
                                if check:
                                    xp += 5
                            else:
                                xp = 10 if weekend_check else 5
                                if check:
                                    xp += 5
                            lvl = await level_instance.add_xp(xp)
                            if lvl is None:
                                return
                            channel, update, levelup = lvl
                            role_reward = message.guild.get_role(
                                level_instance.get_role_reward
                            )
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

                                    await channel.send(
                                        msg,
                                        allowed_mentions=AllowedMentions(
                                            roles=False, everyone=False, users=True
                                        ),
                                    )
                                elif levelup is None:
                                    pass
                                else:
                                    json = loads(self.replace_all(levelup, parameters))
                                    msg = json["content"]
                                    embed = Embed.from_dict(json["embeds"][0])

                                    await channel.send(content=msg, embed=embed)
                            except:
                                if update == "0":
                                    msg = "{} has leveled up to `level {}`".format(
                                        message.author,
                                        Levelling(
                                            message.author, message.guild
                                        ).get_member_level,
                                    )

                                    await channel.send(
                                        msg,
                                        allowed_mentions=AllowedMentions(
                                            roles=False, everyone=False, users=True
                                        ),
                                    )
                                elif update is None:
                                    pass
                                else:
                                    json = loads(self.replace_all(update, parameters))
                                    msg = json["content"]
                                    embed = Embed.from_dict(json["embeds"][0])

                                    await channel.send(content=msg, embed=embed)
                            return
                    except AttributeError:
                        return
        except:
            return

    async def send_level_message(
        self, channel: Optional[TextChannel], content: str, embed: Optional[Embed]
    ):
        if channel is not None:
            await channel.send(content=content, embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(listenersCog(bot))
