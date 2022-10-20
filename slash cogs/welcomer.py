from nextcord import *
from nextcord.ext.commands import Cog, Bot
from db_functions import *

class welcomer(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member:Member):
        try:
            channel_id=get_welcomer(member.guild.id)
            server_id = fetch_welcomer(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)
            
                welcome = Embed(description=f"Hi {member} and welcome to {member.guild.name}!",color=Color.og_blurple()).set_thumbnail(url=member.display_avatar)
                                
                await channel.send(embed=welcome)
            else:
                pass
        except Exception:
            pass

    @Cog.listener()
    async def on_member_remove(self, member:Member):
        try:
            channel_id = get_leaver(member.guild.id)
            server_id= fetch_leaver(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)

                leave = Embed(description=f"{member} left the server", color=0x00FFFF).set_thumbnail(url=member.display_avatar)

                await channel.send(embed=leave)
            else:
                pass
        except:
            pass

def setup(bot:Bot):
    bot.add_cog(welcomer(bot))
