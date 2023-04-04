from discord import AllowedMentions, Color, Embed, Member
from discord.ext.commands import Cog, Bot
from functions import Logger, Welcomer
from collections import OrderedDict
from json import loads


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class welcomer(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        try:
            channel_id = Logger(server=member.guild.id).get_welcomer()
            server_id = Logger(
                member.guild.id,
                channel=await
                self.bot.fetch_channel(channel_id)).fetch_welcomer()

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)

                if Welcomer(member.guild).get_welcoming_msg() == None:
                    welcome = Embed(
                        description=
                        f"Hi {member} and welcome to {member.guild.name}!",
                        color=Color.random()).set_thumbnail(
                            url=member.display_avatar)
                    await channel.send(embed=welcome)
                else:
                    humans = len([
                        member for member in member.guild.members
                        if not member.bot
                    ])
                    parameters = OrderedDict([
                        ("%member%", str(member)),
                        ("%pfp%", str(member.display_avatar)),
                        ("%server%", str(member.guild.name)),
                        ("%mention%", str(member.mention)),
                        ("%name%", str(member.name)),
                        ("%members%", str(member.guild.member_count)),
                        ("%humans%", str(humans)),
                        ("%icon%", str(member.guild.icon))
                    ])

                    json = loads(
                        replace_all(
                            Welcomer(
                                member.guild).get_welcoming_msg(parameters)))

                    try:
                        content = json["content"]
                    except:
                        pass

                    try:
                        embed = Embed.from_dict(json['embeds'][0])
                        await channel.send(content=content,
                                           embed=embed,
                                           allowed_mentions=AllowedMentions(
                                               everyone=False, users=True))
                    except:
                        await channel.send(content=content)
            else:
                return
        except Exception:
            return

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            channel_id = Logger(member.guild).get_leaver(member.guild)
            server_id = Logger().fetch_leaver(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)

                if Welcomer(member.guild).get_leaving_msg() == None:
                    leave = Embed(description=f"{member} left the server",
                                  color=Color.random()).set_thumbnail(
                                      url=member.display_avatar)
                    await channel.send(embed=leave)
                else:
                    humans = len([
                        member for member in member.guild.members
                        if not member.bot
                    ])
                    parameters = OrderedDict([
                        ("%member%", str(member)),
                        ("%pfp%", str(member.display_avatar)),
                        ("%server%", str(member.guild.name)),
                        ("%mention%", str(member.mention)),
                        ("%name%", str(member.name)),
                        ("%members%", str(member.guild.member_count)),
                        ("%humans%", str(humans)),
                        ("%icon%", str(member.guild.icon))
                    ])

                    json = loads(
                        replace_all(
                            Welcomer(member.guild).get_leaving_msg(),
                            parameters))

                    try:
                        content = json["content"]
                    except:
                        return

                    try:
                        embed = Embed.from_dict(json['embeds'][0])
                        await channel.send(content=content,
                                           embed=embed,
                                           allowed_mentions=AllowedMentions(
                                               everyone=False, users=True))
                    except:
                        await channel.send(content=content)
            else:
                return
        except Exception:
            return


async def setup(bot: Bot):
    await bot.add_cog(welcomer(bot))
