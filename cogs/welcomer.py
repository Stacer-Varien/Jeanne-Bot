from discord import *
from discord.ext.commands import Cog, Bot
from db_functions import *
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
            channel_id = get_welcomer(member.guild.id)
            server_id = fetch_welcomer(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)

                if get_welcoming_msg(member.guild.id) == None:
                    welcome = Embed(description=f"Hi {member} and welcome to {member.guild.name}!", color=Color.og_blurple(
                    )).set_thumbnail(url=member.display_avatar)
                    await channel.send(embed=welcome)
                else:
                    humans = len(
                        [member for member in member.guild.members if not member.bot])
                    parameters = OrderedDict([("%member%", str(member)), ("%pfp%", str(member.display_avatar)), ("%server%", str(member.guild.name)), ("%mention%", str(
                        member.mention)), ("%name%", str(member.name)), ("%members%", str(member.guild.member_count)), ("%humans%", str(humans)), ("%icon%", str(member.guild.icon))])

                    json = loads(replace_all(
                        get_welcoming_msg(member.guild.id), parameters))

                    try:
                        content = json["content"]
                    except:
                        pass

                    try:
                        embed = Embed.from_dict(json['embeds'][0])
                        await channel.send(content=content, embed=embed, allowed_mentions=AllowedMentions(everyone=False, users=True))
                    except:
                        await channel.send(content=content)
            else:
                pass
        except Exception:
            pass

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            channel_id = get_leaver(member.guild.id)
            server_id = fetch_leaver(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)

                if get_leaving_msg(member.guild.id) == None:
                    leave = Embed(description=f"{member} left the server", color=0x00FFFF).set_thumbnail(
                        url=member.display_avatar)
                    await channel.send(embed=leave)
                else:
                    humans = len(
                        [member for member in member.guild.members if not member.bot])
                    parameters = OrderedDict([("%member%", str(member)), ("%pfp%", str(member.display_avatar)), ("%server%", str(member.guild.name)), ("%mention%", str(
                        member.mention)), ("%name%", str(member.name)), ("%members%", str(member.guild.member_count)), ("%humans%", str(humans)), ("%icon%", str(member.guild.icon))])

                    json = loads(replace_all(
                        get_leaving_msg(member.guild.id), parameters))

                    try:
                        content = json["content"]
                    except:
                        pass

                    try:
                        embed = Embed.from_dict(json['embeds'][0])
                        await channel.send(content=content, embed=embed, allowed_mentions=AllowedMentions(everyone=False, users=True))
                    except:
                        await channel.send(content=content)
            else:
                pass
        except Exception:
            pass


async def setup(bot: Bot):
    await bot.add_cog(welcomer(bot))
