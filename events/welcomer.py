from discord import Color, Embed, Guild, Member, AllowedMentions, RawMemberRemoveEvent
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
        server = Welcomer(member.guild).server
        if member.guild.id == server.id:
            welcomemsg = Welcomer(member.guild).get_welcoming_msg
            if welcomemsg is None:
                welcome = Embed(
                    description=f"Hi {member} and welcome to {member.guild.name}!",
                    color=Color.random(),
                ).set_thumbnail(url=member.display_avatar.url)
                await welcomer.send(embed=welcome)
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
                await welcomer.send(
                    content=content,
                    embed=embed,
                    allowed_mentions=AllowedMentions(everyone=False, users=True),
                )
                return
            await welcomer.send(content=content)
        await member.guild.chunk()

    @Cog.listener()
    async def on_raw_member_remove(self,payload:RawMemberRemoveEvent):
        member=payload.user
        server=await self.bot.fetch_guild(payload.guild_id)
        leaver = Welcomer(server).get_leaver
        if leaver is None:
            return
        server = Welcomer(server).server
        if payload.guild_id == server.id:
            leavingmsg = Welcomer(server).get_leaving_msg
            if leavingmsg is None:
                leave = Embed(
                    description=f"{member} left the server", color=Color.random()
                ).set_thumbnail(url=member.display_avatar.url)
                await leaver.send(embed=leave)
                return
            humans = len([member for member in server.members if not member.bot])
            parameters = OrderedDict(
                [
                    ("%member%", str(member)),
                    ("%pfp%", str(member.display_avatar)),
                    ("%server%", str(server.name)),
                    ("%mention%", str(member.mention)),
                    ("%name%", str(member.global_name)),
                    ("%members%", str(server.member_count)),
                    ("%humans%", str(humans)),
                    ("%icon%", str(server.icon)),
                ]
            )
            json_data: dict = loads(self.replace_all(leavingmsg, parameters))
            content: str = json_data.get("content")
            try:
                embed = Embed.from_dict(json_data["embeds"][0])
                await leaver.send(
                    content=content,
                    embed=embed,
                    allowed_mentions=AllowedMentions(everyone=False, users=True),
                )
            except:
                await leaver.send(content=content)

    @Cog.listener()
    async def on_guild_join(server:Guild):
        await server.chunk()

async def setup(bot: Bot):
    await bot.add_cog(WelcomerCog(bot))
