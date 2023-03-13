from discord import Color, Embed, Message
from discord.ext.commands import Cog, Bot
from db_functions import Logger


class logger(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if not before.guild:
            return

        if before.author.bot:
            return

        if not (logger_id := Logger(before.guild).get_message_logger()):
            return

        channel = await self.bot.fetch_channel(logger_id)

        embed = Embed()
        embed.description = f"Message edited in {before.channel.mention}"
        embed.color = Color.random()

        has_old_content = before.content != ""
        has_new_content = after.content != ""

        old_content = (before.content if len(before.content) < 1024 else
                       before.content[:1020] + "...")
        new_content = (after.content if len(after.content) < 1024 else
                       after.content[:1020] + "...")

        embed.add_field(
            name="Old message",
            value=old_content if has_old_content else "None (no message)",
            inline=False,
        )
        embed.add_field(
            name="New message",
            value=new_content if has_new_content else "None (no message)",
            inline=False,
        )

        embed.set_thumbnail(url=before.author.display_avatar)
        embed.set_footer(text=f"Author: {before.author} | {before.author.id}")

        await channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if not message.author.bot:
            logger = Logger(message.guild).get_message_logger()
            if logger == False:
                return

            try:
                    channel = await self.bot.fetch_channel(logger)
                    embed = Embed()
                    embed.description = "Message deleted in {}".format(
                        message.channel.mention)
                    embed.color = Color.random()
                    attachments = bool(message.attachments)
                    content = bool(message.content)
                    if content == True and attachments == False:
                        if len(message.content) > 1024:
                            message.content = message.content[:1020] + "..."
                        embed.add_field(name="Message",
                                        value=message.content,
                                        inline=False)
                    elif content == True and attachments == True:
                        if len(message.content) > 1024:
                            message.content = message.content[:1020] + "..."
                        embed.add_field(name="Message",
                                        value=message.content,
                                        inline=False)
                        embed.set_image(url=message.attachments[0].url.replace(
                            'cdn.discordapp.com', 'media.discordapp.net'))
                    elif attachments == True and content == False:
                        embed.add_field(
                            name="Image",
                            value=
                            "No messages, only media. If you can't see anything, it was a video file",
                            inline=False)
                        embed.set_image(url=message.attachments[0].url.replace(
                            'cdn.discordapp.com', 'media.discordapp.net'))
                    embed.set_thumbnail(url=message.author.display_avatar)
                    embed.set_footer(text="Author: {} | {}".format(
                        message.author, message.author.id))
                    await channel.send(embed=embed)
            except AttributeError:
                    return


async def setup(bot: Bot):
    await bot.add_cog(logger(bot))
