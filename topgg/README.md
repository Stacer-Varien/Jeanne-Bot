# Top.gg api

Examples

```py
# Normal Client
from topgg import TopGGClient

client = TopGGClient("Auth", 0)
client.fetch_bot_info()

# Async Client
from topgg import AsyncTopGGClient

client = AsyncTopGGClient.from_new_session("Auth", 0)
await client.fetch_bot_info()
# Or
client = AsyncTopGGClient.from_bot_session(bot, "Auth", 0)
await client.fetch_bot_info()
```
