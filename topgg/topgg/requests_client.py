import typing as T
from abc import ABC

import requests

from .errors import (BadRequestError, ForbiddenAccessError, NotFoundError,
                     RateLimitError, ServerError, TopGGError,
                     UnauthorizedError)
from .topgg_types import JsonObject


class TopGGClient(ABC):
    base_url: str
    close: T.Callable[[], None]
    connect: T.Callable[[], None]
    on_error: T.Callable[[T.Callable], bool]


class RequestsResponse:
    def __init__(self, response: requests.Response):
        self.__response = response

    @property
    def status(self) -> int:
        return self.__response.status_code

    def json(self):
        return self.__response.json()

    def raise_from_status(self):
        code = self.status

        if 300 > code >= 200:
            return
        elif code == 400:
            error = BadRequestError(400, self.__response.text)
        elif code == 401:
            error = UnauthorizedError(401, self.__response.text)
        elif code == 403:
            error = ForbiddenAccessError(403, self.__response.text)
        elif code == 404:
            error = NotFoundError(404, self.__response.text)
        elif code == 429:
            error = RateLimitError(429, self.__response.text)
        elif 600 > code >= 500:
            error = ServerError(code, self.__response.text)
        else:
            error = TopGGError(code, self.__response.text)

        raise error


class RequestsClient:
    def __init__(self, session: requests.Session):
        self.session = session

    def __get__(self, owner, ownertype=None):
        return self

    def request(self, method, url, **kwargs):
        self.__owner__ = kwargs.pop("owner")
        response = RequestsResponse(
            self.session.request(method, url, **kwargs))
        response.raise_from_status()
        return response

    def get(self,
            url: str,
            *, params: T.Optional[dict] = None,
            headers: T.Optional[dict] = None,
            owner=None
            ) -> RequestsResponse:

        return self.request("GET", url, params=params, headers=headers, allow_redirects=False, owner=owner)

    def post(self,
            url: str,
            *, params: T.Optional[dict] = None,
            headers: T.Optional[dict] = None,
            data: T.Optional[JsonObject] = None,
            owner=None
            ) -> RequestsResponse:

        return self.request("POST", url, params=params, headers=headers, data=data.encode(4) if data else None, allow_redirects=False, owner=owner)

    def close(self):
        self.session.close()

    @classmethod
    def connect(cls):
        return cls(requests.Session())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()
