from discord import *
from discord.ext.commands import Cog, Bot
from db_functions import *


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
                    embed.description = "[Message]({}) edited in {}".format(before.jump_url, before.channel.mention)

                    embed.color = Color.random()
                    new_attachments = bool(after.attachments)

                    if len(before.content) > 1024:
                        before.content = before.content[:1020] + "..."
                    if len(after.content) > 1024:
                        after.content = after.content[:1020] + "..."
                    embed.add_field(name="Old message",
                                        value=before.content, inline=False)
                    embed.add_field(name="New message", value=after.content, inline=False)

                    if new_attachments == True:
                        old_image_urls = [x.url for x in before.attachments]
                        old_images = "\n".join(old_image_urls)
                        new_image_urls = [x.url for x in after.attachments]
                        new_images = "\n".join(new_image_urls)

                        if old_images != new_images:

                            if len(old_images) > 1024:
                                old_images = old_images[:1020] + "..."
                            if len(new_images) > 1024:
                                new_images = new_images[:1020] + "..."

                            embed.add_field(name="Old Media", value=old_images, inline=False)
                            embed.add_field(name="New Media",value=new_images, inline=False)
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
