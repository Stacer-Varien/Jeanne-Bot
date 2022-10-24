from __future__ import annotations

import aiohttp


class TopGGError(aiohttp.ClientResponseError):
    subclasses: dict[str, type[TopGGError]] = {}

    def __init_subclass__(cls) -> None:
        TopGGError.subclasses[cls.__name__] = cls
        return super().__init_subclass__()


class BadRequestError(TopGGError):
    ...


class UnauthorizedError(TopGGError):
    ...


class ForbiddenAccessError(TopGGError):
    ...


class NotFoundError(TopGGError):
    ...


class RateLimitError(TopGGError):
    ...


class ServerError(TopGGError):
    ...
