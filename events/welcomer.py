import asyncio
from discord import Color, Embed, Guild, Member, AllowedMentions, RawMemberRemoveEvent
from discord.ext.commands import Cog, Bot
from functions import Welcomer
from collections import OrderedDict
from json import loads, JSONDecodeError


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
        try:
            welcomer_instance = Welcomer(member.guild)
            welcomer = welcomer_instance.get_welcomer
            if welcomer is None:
                return

            server = welcomer_instance.server
            if member.guild.id == server.id:
                welcomemsg = welcomer_instance.get_welcoming_msg
                if welcomemsg is None:
                    if (
                        server.preferred_locale.value == "en-GB"
                        or server.preferred_locale.value == "en-US"
                    ):
                        welcome = Embed(
                            description=f"Hi {member} and welcome to {member.guild.name}!",
                            color=Color.random(),
                        ).set_thumbnail(
                            url=(
                                member.display_avatar.url
                                if member.display_avatar
                                else ""
                            )
                        )
                        await welcomer.send(embed=welcome)
                        
                    elif server.preferred_locale.value == "fr":
                        welcome = Embed(
                            description=f"Salut {member} et bienvenue sur {member.guild.name} !",
                            color=Color.random(),
                        ).set_thumbnail(
                            url=(
                                member.display_avatar.url
                                if member.display_avatar
                                else ""
                            )
                        )
                        await welcomer.send(embed=welcome)
                        
                    elif server.preferred_locale.value == "de":
                        welcome = Embed(
                            description=f"Hallo {member} und willkommen auf {member.guild.name}!",
                            color=Color.random(),
                        ).set_thumbnail(
                            url=(
                                member.display_avatar.url
                                if member.display_avatar
                                else ""
                            )
                        )
                        await welcomer.send(embed=welcome)
                    return

                humans = sum(not m.bot for m in member.guild.members)
                parameters = OrderedDict(
                    [
                        ("%member%", str(member)),
                        (
                            "%pfp%",
                            str(
                                member.display_avatar.url
                                if member.display_avatar
                                else ""
                            ),
                        ),
                        ("%server%", str(member.guild.name)),
                        ("%mention%", str(member.mention)),
                        ("%name%", str(member.global_name or member.name)),
                        ("%members%", str(member.guild.member_count)),
                        ("%humans%", str(humans)),
                        (
                            "%icon%",
                            str(member.guild.icon.url if member.guild.icon else ""),
                        ),
                    ]
                )
                try:
                    json_data: dict = loads(self.replace_all(welcomemsg, parameters))
                    content: str = json_data.get("content")
                    embed_data = json_data.get("embeds")
                    if embed_data:
                        embed = Embed.from_dict(embed_data[0])
                        await welcomer.send(
                            content=content,
                            embed=embed,
                            allowed_mentions=AllowedMentions(
                                everyone=False, users=True
                            ),
                        )
                        return
                    await welcomer.send(content=content)
                except JSONDecodeError:
                    print("Error: Invalid JSON in welcoming message.")
        except Exception as e:
            print(f"Error in on_member_join: {e}")

    @Cog.listener()
    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent):

        member = payload.user
        server = self.bot.get_guild(payload.guild_id)
        welcomer_instance = Welcomer(server)
        leaver = welcomer_instance.get_leaver
        if leaver is None:
            return

        server_data = welcomer_instance.server
        if payload.guild_id == server_data.id:
            leavingmsg = welcomer_instance.get_leaving_msg
            if leavingmsg is None:
                if (
                    server.preferred_locale.value == "en-GB"
                    or server.preferred_locale.value == "en-US"
                ):
                    leave = Embed(
                        description=f"{member} left the server",
                        color=Color.random(),
                    ).set_thumbnail(
                        url=member.display_avatar.url if member.display_avatar else ""
                    )
                    await leaver.send(embed=leave)
                    return
                if server.preferred_locale.value == "fr":
                    leave = Embed(
                        description=f"{member} a quitté le serveur",
                        color=Color.random(),
                    ).set_thumbnail(
                        url=(member.display_avatar.url if member.display_avatar else "")
                    )
                    await leaver.send(embed=leave)
                    return
                if server.preferred_locale.value=="de":
                    leave = Embed(
                        description=f"{member} hat den Server verlassen",
                        color=Color.random(),
                    ).set_thumbnail(
                        url=(member.display_avatar.url if member.display_avatar else "")
                    )
                    await leaver.send(embed=leave)
                return

            humans = len([m for m in server.members if not m.bot])
            parameters = OrderedDict(
                [
                    ("%member%", str(member)),
                    (
                        "%pfp%",
                        str(member.display_avatar.url if member.display_avatar else ""),
                    ),
                    ("%server%", str(server.name)),
                    ("%mention%", str(member.mention)),
                    ("%name%", str(member.global_name or member.name)),
                    ("%members%", str(server.member_count)),
                    ("%humans%", str(humans)),
                    ("%icon%", str(server.icon.url if server.icon else "")),
                ]
            )
            try:
                json_data: dict = loads(self.replace_all(leavingmsg, parameters))
                content: str = json_data.get("content")
                embed_data = json_data.get("embeds")
                if embed_data:
                    embed = Embed.from_dict(embed_data[0])
                    await leaver.send(
                        content=content,
                        embed=embed,
                        allowed_mentions=AllowedMentions(everyone=False, users=True),
                    )
                else:
                    await leaver.send(content=content)
            except JSONDecodeError:
                print("Error: Invalid JSON in leaving message.")

    @Cog.listener()
    async def on_guild_join(self, server: Guild):
        try:
            print(f"Chunking guild: {server.name} ({server.id})...")
            await asyncio.wait_for(server.chunk(), timeout=60.0)
            print(f"Successfully chunked {server.name}.")
        except asyncio.TimeoutError:
            print(f"Chunking timed out for {server.name}.")
        except Exception as e:
            print(f"An error occurred while chunking {server.name}: {e}")


async def setup(bot: Bot):
    await bot.add_cog(WelcomerCog(bot))
