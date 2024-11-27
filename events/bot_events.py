import asyncio
from datetime import datetime, timedelta
from discord import Color, Embed, SyncWebhook
from discord.ext.commands import Cog, AutoShardedBot as Bot
from config import STATUS_WEBHOOK

class ShardEvents(Cog):
    def __init__(self, bot:Bot) -> None:
        self.bot=bot
        self.webhook=SyncWebhook.from_url(STATUS_WEBHOOK)

    @Cog.listener()
    async def on_shard_connect(self, shard_id:int):
        if self.bot.is_ws_ratelimited():
            embed=Embed(color=Color.yellow())
            embed.title="A shard is being ratelimited"
            embed.add_field(name="Affected shard", value=shard_id, inline=True)
            embed.add_field(name="Retrying after", value=f"<t:{round(datetime.now()+ timedelta(seconds=60))}:R>", inline=True)
            embed.set_thumbnail(url="https://files.catbox.moe/0sv1zq.png")
            self.webhook.send(embed=embed)
            await asyncio.sleep(60)

    @Cog.listener()
    async def on_shard_resumed(self, shard_id:int):
        embed=Embed(color=Color.green())
        embed.description=f"Shard {shard_id} resumed!"
        embed.set_thumbnail(url="https://files.catbox.moe/lerkqk.png")
        self.webhook.send(embed=embed)

    @Cog.listener()
    async def on_shard_disconnect(self, shard_id:int):
        if self.bot.is_ws_ratelimited():
            embed=Embed(color=Color.yellow())
            embed.title="A shard is ratelimited"
            embed.add_field(name="Affected shard", value=shard_id, inline=True)
            embed.add_field(name="Retrying after", value=f"<t:{round(datetime.now()+ timedelta(seconds=60))}:R>", inline=True)
            embed.set_thumbnail(url="https://files.catbox.moe/0sv1zq.png")
            self.webhook.send(embed=embed)
            await asyncio.sleep(60)
        else:
            embed = Embed(color=Color.red())
            embed.description = f"Shard {shard_id} disconnected!"
            embed.set_thumbnail(url="https://files.catbox.moe/pkiq8r.png")
            self.webhook.send(embed=embed)



async def setup(bot:Bot):
    await bot.add_cog(ShardEvents(bot))
