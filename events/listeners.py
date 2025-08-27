from collections import OrderedDict
from datetime import datetime
from json import loads
from discord import AllowedMentions, DMChannel, Embed, Message
from discord.ext.commands import Bot, Cog
from functions import BetaTest, DevPunishment, Levelling
# from topgg import DBLClient
# from config import TOPGG


class listenersCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        # self.topggpy = DBLClient(bot=self.bot, token=TOPGG)

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
                if level_instance.check_xpblacklist_channel(message.channel) is None:
                    try:
                        now_time = round(datetime.now().timestamp())
                        if now_time > level_instance.get_next_time_global:
                            #temporary paused voting rewards
                            # get_vote = await self.topggpy.get_user_vote(
                            #    int(message.author.id)
                            # )

                            check = await BetaTest(self.bot).check(message.author)
                            weekend_check = datetime.now().isoweekday() >= 6
                            xp = 15 if weekend_check else 10
                            # if not get_vote:
                            #    xp = 10 if weekend_check else 5
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
                                        str(
                                            (role_reward.name if role_reward else None)
                                        ),
                                    ),
                                    (
                                        "%rolemention%",
                                        str(
                                            (
                                                role_reward.mention
                                                if role_reward
                                                else None
                                            )
                                        ),
                                    ),
                                ]
                            )

                            if update is None:
                                if message.guild.preferred_locale.value in ["en-GB", "en-US"]:
                                    msg = "{} has leveled up to `{}`".format(
                                        message.author,
                                        Levelling(
                                            message.author, message.guild
                                        ).get_member_level,
                                    )
                                elif message.guild.preferred_locale.value == "fr":
                                    msg = "{} a atteint le niveau `{}`".format(
                                        message.author,
                                        Levelling(
                                            message.author, message.guild
                                        ).get_member_level,
                                    )
                                elif message.guild.preferred_locale.value == "de":
                                    msg = "{} hat das Level `{}` erreicht".format(
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
                            else:
                                json = loads(self.replace_all(update, parameters))
                                msg = json["content"]
                                embed = Embed.from_dict(json["embeds"][0])

                                await channel.send(content=msg, embed=embed)
                            if role_reward:
                                await message.author.add_roles(role_reward)
                                if levelup is None:
                                    if message.guild.preferred_locale.value in ["en-GB", "en-US"]:
                                        msg = "CONGRATS {}! You were role awarded {}".format(
                                            message.author,
                                            role_reward.name,
                                        )
                                    elif message.guild.preferred_locale.value == "fr":
                                        msg = "FÉLICITATIONS {}! Tu as reçu le rôle {}".format(
                                            message.author,
                                            role_reward.name,
                                        )
                                    elif message.guild.preferred_locale.value == "de":
                                        msg = "HERZLICHEN GLÜCKWUNSCH {}! Du hast die Rolle {} erhalten".format(
                                            message.author,
                                            role_reward.name,
                                        )

                                    await channel.send(
                                        msg,
                                        allowed_mentions=AllowedMentions(
                                            roles=False, everyone=False, users=True
                                        ),
                                    )
                                else:
                                    json = loads(self.replace_all(levelup, parameters))
                                    msg = json["content"]
                                    embed = Embed.from_dict(json["embeds"][0])

                                    await channel.send(content=msg, embed=embed)
                            return
                    except AttributeError:
                        
                        return
        except Exception:
            return


async def setup(bot: Bot):
    await bot.add_cog(listenersCog(bot))

