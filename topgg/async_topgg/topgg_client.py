from abc import ABC

from .requests_client import AsyncRequestClient, T, aiohttp, asyncio


class HTTP(ABC):
    _HTTPClient__session: aiohttp.ClientSession


class State(ABC):
    http: HTTP


class User(ABC):
    _state: State


class Bot(ABC):
    user: User


class AsyncTopGGClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        auth: str,
        bot_id: int,
        catch_errors: bool = False,
    ) -> None:
        self.bot_id = bot_id
        self._headers = {"Authorization": auth, "Content-Type": "application/json"}
        self.requests_client = AsyncRequestClient(session)
        self.catch_errors = catch_errors

    @property
    def base_url(self):
        return "https://top.gg/api"

    @classmethod
    def from_bot_session(
        cls, bot: Bot, auth: str, bot_id: int, catch_errors: bool = False
    ):
        return AsyncTopGGClient(
            session=bot.user._state.http._HTTPClient__session, auth=auth, bot_id=bot_id, catch_errors=catch_errors
        )

    @classmethod
    def from_new_session(cls, auth: str, bot_id: int, catch_errors: bool = False):
        try:
            return AsyncTopGGClient(
                session=aiohttp.ClientSession(loop=asyncio.get_running_loop()),
                auth=auth,
                bot_id=bot_id,
                catch_errors=catch_errors,
            )
        except RuntimeError:
            return AsyncTopGGClient(
                session=aiohttp.ClientSession(loop=asyncio.get_event_loop()),
                auth=auth,
                bot_id=bot_id,
                catch_errors=catch_errors,
            )

    async def fetch_bot_info(self) -> dict:
        return await (
            await self.requests_client.get(
                f"{self.base_url}/bots/{self.bot_id}",
                headers=self._headers,
                catch_errors=self.catch_errors,
            )
        ).json()

    async def fetch_bot_stats(self) -> dict:
        return await (
            await self.requests_client.get(
                f"{self.base_url}/bots/{self.bot_id}/stats",
                headers=self._headers,
                catch_errors=self.catch_errors,
            )
        ).json()

    async def fetch_bot_votes(self) -> dict:
        return await (
            await self.requests_client.get(
                f"{self.base_url}/bots/{self.bot_id}/votes",
                headers=self._headers,
                catch_errors=self.catch_errors,
            )
        ).json()

    async def fetch_bot_vote(self, user_id: int) -> dict:
        return await (
            await self.requests_client.get(
                f"{self.base_url}/bots/{self.bot_id}/check",
                params={"userId": user_id},
                headers=self._headers,
                catch_errors=self.catch_errors,
            )
        ).json()

    async def fetch_weekend_status(self) -> dict:
        return await (
            await self.requests_client.get(
                f"{self.base_url}/weekend",
                headers=self._headers,
                catch_errors=self.catch_errors,
            )
        ).json()

    async def fetch_user(self, user_id: int) -> dict:
        return await (
            await self.requests_client.get(
                f"{self.base_url}/users/{user_id}",
                headers=self._headers,
                catch_errors=self.catch_errors,
            )
        ).json()

    async def post_server_count(
        self, server_count: int, shard_id: T.Optional[int] = None, shard_count: T.Optional[int] = None
    ):
        data = dict(server_count=server_count)
        if shard_id:
            data.update(shard_id=shard_id)
        if shard_count:
            data.update(shard_count=shard_count)
        await self.requests_client.post(
            f"{self.base_url}/bots/{self.bot_id}/stats",
            data,
            headers=self._headers,
            catch_errors=self.catch_errors,
        )
