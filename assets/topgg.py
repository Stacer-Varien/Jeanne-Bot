import requests
import typing as T
import json


def to_sjson(data: dict):
    return json.dumps(data, indent=4)


def build_url(*args: T.Union[str, int]) -> str:
    return (
        f"/{'/'.join([str(o) for o in args])}"
        if not args[0] == "https" or args[0] == "https"
        else f"https://{'/'.join([str(o) for o in args[1:]])}"
    )


class _RequestsClient:
    def __init__(self):
        self._session = requests.session()

    def __get__(self, obj: object, owner: type = None):
        self.__obj__ = obj
        self.__owner__ = owner
        return self

    def request(self, method, url, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = to_sjson(kwargs["data"])

        response = self._session.request(method, url, **kwargs)

        if 300 > response.status_code >= 200:
            return response
        elif response.status_code == 429:
            raise requests.exceptions.ConnectionError(
                "429: You are being rate limited")
        elif response.status_code == 400:
            raise requests.exceptions.HTTPError("400: Bad request")
        elif response.status_code == 401:
            raise requests.exceptions.InvalidHeader("401: Unauthorized")
        elif response.status_code == 403:
            raise requests.exceptions.ConnectionError("403: Forbidden")
        elif response.status_code == 404:
            raise requests.exceptions.ConnectionError("404: Not Found")
        elif response.status_code >= 500:
            raise requests.exceptions.HTTPError(
                f"{response.status_code}: Server Error")
        else:
            raise response.raise_for_status()

    def __set_name__(self, obj: object, name: str):
        self.__public_name__ = name
        self.__private_name__ = "_" + name

    def close(self):
        return self._session.close()

    def __set__(self, obj, value):
        if value == "closed":
            self.close()
        else:
            raise ValueError


class TopGGClient:

    request_client = _RequestsClient()

    def __init__(self, auth: str, bot_id: int) -> None:
        self._bot_id = bot_id
        self._headers = {"Authorization": auth,
                         "Content-Type": "application/json"}

    @property
    def base_url(self):
        return "https://top.gg/api"

    def get(
        self,
        endpoint_url: str,
        params: T.Optional[dict[str, T.Any]] = None,
    ) -> requests.Response:

        return self.request_client.request(
            "GET",
            f"{self.base_url}{endpoint_url}",
            params=params,
            headers=self._headers,
            allow_redirects=False,
        )

    def post(
        self,
        endpoint_url: str,
        params: T.Optional[dict[str, T.Any]] = None,
        data: T.Optional[dict] = None,
    ) -> requests.Response:

        return self.request_client.request(
            "POST",
            f"{self.base_url}{endpoint_url}",
            params,
            data=data,
            allow_redirects=False,
            headers=self._headers,
        )

    def fetch_bot_info(self):
        return self.get(build_url("bots", self._bot_id)).json()

    def fetch_bot_stats(self):
        return self.get(build_url("bots", self._bot_id, "stats")).json()

    def fetch_weekend_status(self):
        return self.get(build_url("weekend")).json()

    def fetch_bot_votes(self):
        return self.get(build_url("bots", self._bot_id, "votes")).json()

    def fetch_user_info(self, user_id: int):
        return self.get(build_url("users", user_id)).json()

    def fetch_user_vote(self, user_id: int):
        return self.get(
            build_url("bots", self._bot_id, "check"), params={"userId": user_id}
        ).json()

    def post_server_count(
        self,
        guild_count: int,
        shard_id: T.Optional[int] = None,
        shard_count: T.Optional[int] = None,
    ):
        data = {"server_count": guild_count}
        if shard_id:
            data["shard_id"] = shard_id
        if shard_count:
            data["shard_count"] = shard_count

        return self.post(build_url("bots", self._bot_id, "stats"), data=data)

    def close(self):
        self.request_client.close()
