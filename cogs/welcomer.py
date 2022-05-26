from nextcord import *
from nextcord.ext.commands import Cog
from config import db

class welcomer(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        try:
            channel_id_query = db.execute(
                f"SELECT channel_id FROM welcomerData where guild_id = {member.guild.id}")
            channel_id = channel_id_query.fetchone()[0]

            guild_id_query = db.execute(
                f"SELECT guild_id FROM welcomerData where channel_id = {channel_id}")
            server_id = guild_id_query.fetchone()[0]

            server = self.bot.get_guild(server_id)

            try:
                    channel = self.bot.get_channel(channel_id)
                    try:
                        welcome = Embed(color=member.color)

                        if member.avatar !=None:
                            if member.guild.icon.is_animated() is True:
                                welcome.set_author(name=f"Hello {member} and welcome to {server.name}!", icon_url=member.guild.icon.with_size(512)).set_thumbnail(url=member.avatar)

                            elif member.guild.icon.is_animated() is False:
                                welcome.set_author(name=f"Hello {member} and welcome to {server.name}!", icon_url=member.guild.icon).set_thumbnail(url=member.avatar)

                        elif member.avatar == None:
                            if member.guild.icon.is_animated() is True:
                                welcome.set_author(name=f"Hello {member} and welcome to {server.name}!", icon_url=member.guild.icon.with_size(512))

                            elif member.guild.icon.is_animated() is False:
                                welcome.set_author(name=f"Hello {member} and welcome to {server.name}!", icon_url=member.guild.icon)
                                
                        await channel.send(embed=welcome)

                    except:
                        pass
            except:
                    pass
            else:
                pass
        except:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            channel_id_query = db.execute(
                f"SELECT channel_id FROM leaverData where guild_id = {member.guild.id}")
            channel_id = channel_id_query.fetchone()[0]

            guild_id_query = db.execute(
                f"SELECT guild_id FROM leaverData where channel_id = {channel_id}")
            server_id = guild_id_query.fetchone()[0]

            if member.guild.id == server_id:
                try:
                    channel = self.bot.get_channel(channel_id)
                    try:
                        channel = self.bot.get_channel(channel_id)
                        leave = Embed(color=0x00FFFF)

                        if member.avatar != None:
                            if member.guild.icon.is_animated() is True:
                                leave.set_author(name=f"{member} left the server", icon_url=member.guild.icon.with_size(
                                    512)).set_thumbnail(url=member.avatar)

                            elif member.guild.icon.is_animated() is False:
                                leave.set_author(name=f"{member} left the server", icon_url=member.guild.icon).set_thumbnail(
                                    url=member.avatar)

                        elif member.avatar == None:
                            if member.guild.icon.is_animated() is True:
                                leave.set_author(
                                    name=f"{member} left the server", icon_url=member.guild.icon.with_size(512))

                            elif member.guild.icon.is_animated() is False:
                                leave.set_author(
                                    name=f"{member} left the server", icon_url=member.guild.icon)

                        await channel.send(embed=leave)
                    except:
                        pass
                except:
                    pass
            else:
                pass
        except:
            pass

def setup(bot):
    bot.add_cog(welcomer(bot))
