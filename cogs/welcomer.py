from discord import AllowedMentions, Color, Embed, Member
from discord.ext.commands import Cog, Bot
from functions import Logger, Welcomer
from collections import OrderedDict
from json import loads


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class WelcomerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        welcomer = Welcomer(member.guild).get_welcomer()

        if welcomer is None:
            return

        if member.guild.id == int(welcomer[0]):
            channel = self.bot.get_channel(int(welcomer[1]))
            welcomemsg = Welcomer(member.guild).get_welcoming_msg()

            if welcomemsg is None or welcomemsg == 0:
                welcome = Embed(
                    description=f"Hi {member} and welcome to {member.guild.name}!",
                    color=Color.random(),
                ).set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=welcome)
            else:
                humans = sum(not member.bot for member in member.guild.members)
                parameters = {
                    "%member%": str(member),
                    "%pfp%": str(member.display_avatar.url),
                    "%server%": str(member.guild.name),
                    "%mention%": str(member.mention),
                    "%name%": str(member.name),
                    "%members%": str(member.guild.member_count),
                    "%humans%": str(humans),
                    "%icon%": str(member.guild.icon.url),
                }

                json_data: dict = loads(
                    replace_all(Welcomer(member.guild).get_welcoming_msg(), parameters)
                )

                content: str = json_data.get("content")
                embed_data = json_data.get("embeds")

                if embed_data:
                    embed = Embed.from_dict(embed_data[0])
                    await channel.send(
                        content=content,
                        embed=embed,
                        allowed_mentions=AllowedMentions(everyone=False, users=True),
                    )
                else:
                    await channel.send(content=content)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        leaver = Welcomer(member.guild).get_leaver()

        if leaver is None:
            return

        if member.guild.id == int(leaver[0]):
            channel = self.bot.get_channel(int(leaver[1]))
            leavingmsg = Welcomer(member.guild).get_leaving_msg()

            if leavingmsg is None or leavingmsg == 0:
                leave = Embed(
                    description=f"{member} left the server", color=Color.random()
                ).set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=leave)
            else:
                humans = len(
                    [member for member in member.guild.members if not member.bot]
                )
                parameters = OrderedDict(
                    [
                        ("%member%", str(member)),
                        ("%pfp%", str(member.display_avatar.url)),
                        ("%server%", str(member.guild.name)),
                        ("%mention%", str(member.mention)),
                        ("%name%", str(member.name)),
                        ("%members%", str(member.guild.member_count)),
                        ("%humans%", str(humans)),
                        ("%icon%", str(member.guild.icon.url)),
                    ]
                )

                json_data: dict = loads(
                    replace_all(Welcomer(member.guild).get_leaving_msg(), parameters)
                )

                content: str = json_data.get("content")

                try:
                    embed = Embed.from_dict(json_data["embeds"][0])
                    await channel.send(
                        content=content,
                        embed=embed,
                        allowed_mentions=AllowedMentions(everyone=False, users=True),
                    )
                except:
                    await channel.send(content=content)


async def setup(bot: Bot):
    await bot.add_cog(WelcomerCog(bot))
