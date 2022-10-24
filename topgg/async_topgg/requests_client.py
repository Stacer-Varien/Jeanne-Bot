import asyncio
import typing as T

import aiohttp

from .topgg_errors import TopGGError


class Response(aiohttp.ClientResponse):
    error: T.Optional[TopGGError]


class AsyncRequestClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def request(self, method: str, url: str, **kwargs) -> Response:
        if (data := kwargs.pop("data", None)):
            kwargs["json"] = data
        should_catch: bool = kwargs.pop("catch_errors", False)

        async with self.session.request(method, url, **kwargs) as response:
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError as err:
                if err.status == 400:
                    Error = TopGGError.subclasses.get("BadRequestError", TopGGError)
                elif err.status == 401:
                    Error = TopGGError.subclasses.get("UnauthorizedError", TopGGError)
                elif err.status == 403:
                    Error = TopGGError.subclasses.get("ForbiddenAccessError", TopGGError)
                elif err.status == 404:
                    Error = TopGGError.subclasses.get("NotFoundError", TopGGError)
                elif err.status == 429:
                    Error = TopGGError.subclasses.get("RateLimitedError", TopGGError)
                elif 600 > err.status >= 500:
                    Error = TopGGError.subclasses.get("ServerError", TopGGError)
                else:
                    Error = TopGGError               
                error = Error(err.request_info, err.history, status=err.status, message=err.message, headers=err.headers)
                if not should_catch:
                    response.error = error
                    raise error from err
                else:
                    response.error = error
            else:
                response.error = None
            finally:
                return response
            
    def get(self, url: str, params: T.Optional[dict[str, str]] = None, headers: T.Optional[dict[str, str]] = None, catch_errors: bool = False):
        return self.request("GET", url, params=params, headers=headers, catch_errors=catch_errors)
    
    def post(self, url: str, data: dict, params: T.Optional[dict[str, str]] = None, headers: T.Optional[dict[str, str]] = None, catch_errors: bool = False):
        return self.request("POST", url, params=params, headers=headers, data=data, catch_errors=catch_errors)
