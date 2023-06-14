from discord import Color, Embed, Message
from discord.ext.commands import Cog, Bot
from functions import Logger


class LoggerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if not before.guild or before.author.bot:
            return

        logger_id = Logger(after.guild).get_message_logger()

        if not logger_id:
            return

        channel = self.bot.get_channel(int(logger_id))

        embed = Embed(
            description=f"Message edited in {before.channel.mention}",
            color=Color.random(),
        )

        has_old_content = bool(before.content)
        has_new_content = bool(after.content)

        old_content = before.content[:1020] + "..." if len(before.content) >= 1024 else before.content
        new_content = after.content[:1020] + "..." if len(after.content) >= 1024 else after.content

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

        embed.set_thumbnail(url=before.author.display_avatar.url)
        embed.set_footer(text=f"Author: {before.author} | {before.author.id}")

        await channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if message.author.bot:
            return

        logger_id = Logger(message.guild).get_message_logger()

        if not logger_id:
            return

        try:
            channel = self.bot.get_channel(int(logger_id))
            embed = Embed(
                description=f"Message deleted in {message.channel.mention}",
                color=Color.random(),
            )
            attachments = bool(message.attachments)
            content = bool(message.content)

            if content:
                value = message.content[:1020] + "..." if len(message.content) >= 1024 else message.content
                embed.add_field(name="Message", value=value, inline=False)
                if attachments:
                    embed.set_image(
                        url=message.attachments[0].url.replace(
                            "cdn.discordapp.com", "media.discordapp.net"
                        )
                    )
            elif attachments:
                embed.add_field(
                    name="Image",
                    value="No messages, only media. If you can't see anything, it was a video file",
                    inline=False,
                )
                embed.set_image(
                    url=message.attachments[0].url.replace(
                        "cdn.discordapp.com", "media.discordapp.net"
                    )
                )

            embed.set_thumbnail(url=message.author.display_avatar.url)
            embed.set_footer(
                text=f"Author: {message.author} | {message.author.id}"
            )

            await channel.send(embed=embed)
        except AttributeError:
            return


async def setup(bot: Bot):
    await bot.add_cog(LoggerCog(bot))

