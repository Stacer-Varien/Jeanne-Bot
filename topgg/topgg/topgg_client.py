from __future__ import annotations

import types

from .errors import TopGGError
from .requests_client import JsonObject, RequestsClient, T


def is_connected(client: TopGGClient):
    if client._session_client is None:
        return False
    return True


client_not_connected = Exception("Client not connected")


class TopGGClient:
    def __init__(self, auth: str, bot_id: int):
        self.connect()
        self._headers = {"Authorization": auth, "Content-Type": "application/json"}
        self._bot_id = bot_id
    
    def __enter__(self):
        if not is_connected(self):
            self.connect()
        return self

    def connect(self):
        self._session_client = RequestsClient.connect()

    def close(self):
        if is_connected(self):
            self._session_client.close()
            self._session_client = None

    @property
    def base_url(self):
        return "https://top.gg/api"

    def fetch_weekend_status(self) -> dict:
        if is_connected(self):
            return self._session_client.get(f"{self.base_url}/weekend", headers=self._headers, owner=self).json()
        else:
            raise client_not_connected

    def fetch_bot_info(self) -> dict:
        if is_connected(self):
            return self._session_client.get(f"{self.base_url}/bots/{self._bot_id}", headers=self._headers, owner=self).json()
        else:
            raise client_not_connected

    def fetch_bot_stats(self) -> dict:
        if is_connected(self):
            return self._session_client.get(f"{self.base_url}/bots/{self._bot_id}/stats", headers=self._headers, owner=self).json()
        else:
            raise client_not_connected

    def fetch_bot_votes(self) -> dict:
        if is_connected(self):
            return self._session_client.get(f"{self.base_url}/bots/{self._bot_id}/votes", headers=self._headers, owner=self).json()
        else:
            raise client_not_connected

    def fetch_bot_vote(self, user_id: int) -> dict:
        if is_connected(self):
            return self._session_client.get(f"{self.base_url}/bots/{self._bot_id}/check", params={"userId": user_id}, headers=self._headers, owner=self).json()
        else:
            raise client_not_connected

    def fetch_user(self, user_id: int) -> dict:
        if is_connected(self):
            return self._session_client.get(f"{self.base_url}/users/{user_id}", headers=self._headers, owner=self).json()
        else:
            raise client_not_connected

    def post_server_count(self, server_count: int, shard_id: T.Optional[int] = None, shard_count: T.Optional[int] = None):
        if is_connected(self):
            data = JsonObject(server_count=server_count)
            data.update(shard_id=shard_id or None)
            data.update(shard_count=shard_count or 0)

            return self._session_client.post(f"{self.base_url}/bots/{self._bot_id}/stats", headers=self._headers, data=data, owner=self)
        else:
            raise client_not_connected

    def __exit__(self, err_t: T.Optional[type[BaseException]], err: T.Optional[BaseException], err_tb: T.Optional[types.TracebackType]):
        self.close()


def topgg_client(auth: str, bot_id: int):
    def inner(func: T.Callable[[TopGGClient, TopGGError], bool]):
        client = TopGGClient(auth, bot_id)
        client.on_error(func)
        return client
    return inner