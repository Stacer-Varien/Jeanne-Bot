class TopGGError(Exception):
    def __init__(self, code: int, msg: object):
        super().__init__(msg)
        self.status = code
        self.message = msg
        self.type = type(self)

    def json(self):
        import json
        return json.loads(self.message)


class NotFoundError(TopGGError):
    ...


class UnauthorizedError(TopGGError):
    ...


class RateLimitError(TopGGError):
    ...


class BadRequestError(TopGGError):
    ...


class ForbiddenAccessError(TopGGError):
    ...


class ServerError(TopGGError):
    ...
