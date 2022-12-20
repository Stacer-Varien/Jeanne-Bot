from discord import *
from discord.ext.commands import Cog, Bot
import random
from db_functions import *


class logger(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if not after.author.bot:
            logger = get_message_logger(after.guild.id)
            if logger == False:
                pass
            else:
                try:
                    embed = Embed()
                    embed.description = "Message edited"
                    colors = [Color.red(), Color.blue(),
                              Color.green(), Color.gold()]
                    embed.color = random.choice(colors)
                    old_attachments = bool(before.attachments)
                    old_content = bool(before.content)
                    new_content = bool(after.content)
                    if old_content == True and old_attachments == False:
                        embed.add_field(name="Old message",
                                        value=before.content, inline=False)
                        if new_content == True:
                            embed.add_field(name="New message",
                                            value=after.content, inline=False)
                        else:
                            embed.add_field(name="New message",
                                            value="None (no message)", inline=False)
                    elif old_content == True and old_attachments == True:
                        embed.add_field(name="Old message",
                                        value=before.content, inline=False)
                        if new_content == True:
                            embed.add_field(name="New message",
                                            value=after.content, inline=False)
                        else:
                            embed.add_field(name="New message",
                                            value="None (no message)", inline=False)
                    elif old_attachments == True and old_content == False:
                        embed.add_field(name="Old message",
                                        value=before.content, inline=False)
                        if new_content == True:
                            embed.add_field(name="New message",
                                            value=after.content, inline=False)
                        else:
                            embed.add_field(name="New message",
                                            value="None (no message)", inline=False)
                    embed.set_thumbnail(url=before.author.display_avatar)
                    embed.set_footer(text="Author: {} | {}".format(
                        before.author, before.author.id))
                    channel = await self.bot.fetch_channel(logger)
                    await channel.send(embed=embed)
                except AttributeError:
                    pass

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if not message.author.bot:
            logger = get_message_logger(message.guild.id)
            if logger == False:
                pass
            else:
                try:
                    embed = Embed()
                    embed.description = "Message deleted"
                    colors = [Color.red(), Color.blue(),
                              Color.green(), Color.gold()]
                    embed.color = random.choice(colors)
                    attachments = bool(message.attachments)
                    content = bool(message.content)
                    if content == True and attachments == False:
                        embed.add_field(name="Message",
                                        value=message.content, inline=False)
                    elif content == True and attachments == True:
                        embed.add_field(name="Message",
                                        value=message.content, inline=False)
                        embed.set_image(url=message.attachments[0].url.replace(
                            'cdn.discordapp.com', 'media.discordapp.net'))
                    elif attachments == True and content == False:
                        embed.add_field(name="Image",
                                        value="No messages, only media. If you can't see anything, it was a video file", inline=False)
                        embed.set_image(url=message.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net'))
                    embed.set_thumbnail(url=message.author.display_avatar)
                    embed.set_footer(text="Author: {} | {}".format(
                        message.author, message.author.id))
                    channel = await self.bot.fetch_channel(logger)
                    await channel.send(embed=embed)
                except AttributeError:
                    pass

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if not self.bot.user.id:
            logger = get_member_logger(before.guild.id)
            if logger == None:
                pass
            else:
                embed = Embed()
                if before.nick != after.nick:
                    embed.description = "Nickname changed"
                    embed.add_field(name="Old Nickname",
                                    value=before.nick, inline=True)
                    embed.add_field(name="New Nickname",
                                    value=after.nick, inline=True)

                elif before.guild_avatar != after.guild_avatar:
                    embed.description = "Avatar change"
                    embed.set_thumbnail(url=after.guild_avatar)

                colors = [Color.red(), Color.blue(),
                          Color.green(), Color.gold()]
                embed.color = random.choice(colors)
                embed.set_footer(
                    text="Member: {} | `{}`".format(before, before.id))
                channel = await self.bot.fetch_channel(logger)
                await channel.send(embed=embed)
                        
async def setup(bot: Bot):
    await bot.add_cog(logger(bot))
