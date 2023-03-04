from discord import 
from discord.ext.commands import Cog, Bot
from db_functions import 


class logger(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if not before.author.bot:
            logger = get_message_logger(after.guild.id)
            if logger == False:
                pass
            else:
                try: 
                    channel = await self.bot.fetch_channel(logger)
                    embed = Embed()
                    embed.description = "Message edited in {}".format(before.channel.mention)

                    embed.color = Color.random()
                    old_attachments = bool(before.attachments)
                    old_content = bool(before.content)
                    new_content = bool(after.content)
                    if old_content == True and old_attachments == False:
                        if len(before.content) > 1024:
                            before.content = before.content[:1020] + "..."
                        if len(after.content) > 1024:
                            after.content = after.content[:1020] + "..."
                        embed.add_field(name="Old message",
                                        value=before.content, inline=False)
                        if new_content == True:
                            embed.add_field(name="New message",
                                            value=after.content, inline=False)
                        else:
                            embed.add_field(name="New message",
                                            value="None (no message)", inline=False)
                    elif old_content == True and old_attachments == True:
                        if len(before.content) > 1024:
                            before.content = before.content[:1020] + "..."
                        if len(after.content) > 1024:
                            after.content = after.content[:1020] + "..."
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
                    channel = await self.bot.fetch_channel(logger)
                    embed = Embed()
                    embed.description = "Message deleted in {}".format(message.channel.mention)
                    embed.color = Color.random()
                    attachments = bool(message.attachments)
                    content = bool(message.content)
                    if content == True and attachments == False:
                        if len(message.content) > 1024:
                            message.content = message.content[:1020] + "..."
                        embed.add_field(name="Message",
                                        value=message.content, inline=False)
                    elif content == True and attachments == True:
                        if len(message.content) > 1024:
                            message.content = message.content[:1020] + "..."
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
                    await channel.send(embed=embed)
                except AttributeError:
                    pass
                        
async def setup(bot: Bot):
    await bot.add_cog(logger(bot))
