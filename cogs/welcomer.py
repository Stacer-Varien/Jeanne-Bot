from nextcord import *
from nextcord.ext.commands import Cog
from config import db

class welcomer(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        try:
            guild_id_query = db.execute(
                f"SELECT guild_id FROM welcomerData where channel_id = {channel_id}")
            server_id = guild_id_query.fetchone()[0]

            server = self.bot.get_guild(server_id)

            if member.guild.id == server.id:
                channel_id_query = db.execute(
                    "SELECT channel_id FROM welcomerData where guild_id = ?", (member.guild.id))
                channel_id = channel_id_query.fetchone()[0]
                channel = self.bot.get_channel(channel_id)
            
                welcome = Embed(description=f"Hi {member} and welcome to {server.name}!",color=member.color).set_thumbnail(url=member.display_avatar)
                                
                await channel.send(embed=welcome)
            else:
                pass
        except Exception as e:
            print(e)

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
                channel = self.bot.get_channel(channel_id)

                leave = Embed(description=f"{member} left the server", color=0x00FFFF).set_thumbnail(url=member.display_avatar)

                await channel.send(embed=leave)
            else:
                pass
        except:
            pass

def setup(bot):
    bot.add_cog(welcomer(bot))
