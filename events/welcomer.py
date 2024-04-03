from discord import Color, Embed, Member, AllowedMentions
from discord.ext.commands import Cog, Bot
from functions import Welcomer
from collections import OrderedDict
from json import loads



class WelcomerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @staticmethod
    def replace_all(text: str, dic: dict):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @Cog.listener()
    async def on_member_join(self, member: Member):
        welcomer = Welcomer(member.guild).get_welcomer
        if welcomer is None:
            return
        if member.guild.id == self.bot.get_channel(welcome).guild.id:
            channel = await self.bot.fetch_channel(int(welcomer[2]))
            welcomemsg = Welcomer(member.guild).get_welcoming_msg
            if welcomemsg is None:
                welcome = Embed(
                    description=f"Hi {member} and welcome to {member.guild.name}!",
                    color=Color.random(),
                ).set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=welcome)
                return
            humans = sum(not member.bot for member in member.guild.members)
            parameters = OrderedDict(
                [
                    ("%member%", str(member)),
                    ("%pfp%", str(member.display_avatar)),
                    ("%server%", str(member.guild.name)),
                    ("%mention%", str(member.mention)),
                    ("%name%", str(member.global_name)),
                    ("%members%", str(member.guild.member_count)),
                    ("%humans%", str(humans)),
                    ("%icon%", str(member.guild.icon)),
                ]
            )
            json_data: dict = loads(self.replace_all(welcomemsg, parameters))
            content: str = json_data.get("content")
            embed_data = json_data.get("embeds")
            if embed_data:
                embed = Embed.from_dict(embed_data[0])
                await channel.send(
                    content=content,
                    embed=embed,
                    allowed_mentions=AllowedMentions(everyone=False, users=True),
                )
                return
            await channel.send(content=content)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        leaver = Welcomer(member.guild).get_leaver
        if leaver is None:
            return
        if member.guild.id == int(leaver[0]):
            channel = await self.bot.fetch_channel(int(leaver[1]))
            leavingmsg = Welcomer(member.guild).get_leaving_msg
            if leavingmsg is None:
                leave = Embed(
                    description=f"{member} left the server", color=Color.random()
                ).set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=leave)
                return
            humans = len([member for member in member.guild.members if not member.bot])
            parameters = OrderedDict(
                [
                    ("%member%", str(member)),
                    ("%pfp%", str(member.display_avatar)),
                    ("%server%", str(member.guild.name)),
                    ("%mention%", str(member.mention)),
                    ("%name%", str(member.global_name)),
                    ("%members%", str(member.guild.member_count)),
                    ("%humans%", str(humans)),
                    ("%icon%", str(member.guild.icon)),
                ]
            )
            json_data: dict = loads(self.replace_all(leavingmsg, parameters))
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
