from nextcord import *
from nextcord.ext.commands import Cog
from config import db

class welcomer(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        try:
            guild_id_query=db.execute(f"SELECT guild_id FROM welcomerData where guild_id = {member.guild.id}")
            channel_id_query = db.execute(
                f"SELECT channel_id FROM welcomerData where guild_id = {member.guild.id}")
            server_id=guild_id_query.fetchone()[0]
            channel_id=channel_id_query.fetchone()[0]
            server=self.bot.get_guild(server_id)
            
            if member.guild.id==server_id:
                try:
                    channel = self.bot.get_channel(channel_id)
                    try:
                        welcome = Embed(color=0x00FFFF)

                        if member.guild.icon.is_animated() is True:
                            welcome.set_author(icon_url=member.guild.icon.with_size(512))
                        else:
                            welcome.set_author(
                                name=f"Hello {member.mention} and welcome to {server.name}!", icon_url=member.guild.icon)
                        welcome.set_footer(text=f"Now there is {len(server.members)} members")
                        welcome.set_thumbnail(url=member.avatar)
                        await channel.send(embed=welcome)
                    except Exception as e:
                        raise e
                except Exception as e:
                    raise e
            else:
                pass
        except Exception as e:
            raise e

    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            guild_id_query = db.execute(
                f"SELECT guild_id FROM leaverData where guild_id = {member.guild.id}")
            channel_id_query = db.execute(
                f"SELECT channel_id FROM leaverData where guild_id = {member.guild.id}")
            server_id = guild_id_query.fetchone()[0]
            channel_id = channel_id_query.fetchone()[0]
            server = self.bot.get_guild(server_id)

            if member.guild.id == server_id:
                try:
                    channel = self.bot.get_channel(channel_id)
                    try:
                        channel = self.bot.get_channel(channel_id)
                        leave = Embed(color=0x00FFFF)

                        if member.guild.icon.is_animated() is True:
                            leave.set_author(
                                icon_url=member.guild.icon.with_size(512))
                        else:
                            leave.set_author(name=f"{member.name} left the server.", icon_url=member.guild.icon)
                        leave.set_footer(text=f"Now there is {len(server.members)} members")
                        leave.set_thumbnail(url=member.avatar)
                        await channel.send(embed=leave)
                    except Exception as e:
                        raise e
                except Exception as e:
                    raise e
            else:
                pass
        except Exception as e:
            raise e

def setup(bot):
    bot.add_cog(welcomer(bot))
