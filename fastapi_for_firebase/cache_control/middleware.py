"""Provide functions ad FastAPI middleware.
"""
from typing import Awaitable, Callable

from fastapi import Request, Response

from . import CacheControl


MiddlewareCallable = Callable[[Request], Awaitable[Response]]
"""Wapper to middleware ``call_next``"""


def cache_control(max_age: int = None, s_maxage: int = None) -> MiddlewareCallable:
    """Bind Cache-Control for all GET request.

    When you define FastAPI application, set this function as middleware.

    .. code-block:: python

       app = FastAPI()
       app.middleware("http")(cache_control(300, 600))

    :param max_age: max-age value
    :param s_maxage: s-maxage value
    """
    cc = CacheControl(max_age, s_maxage)

    async def _cache_control(
        request: Request, call_next: MiddlewareCallable
    ) -> Response:
        response = await call_next(request)
        if request.method == "GET":
            response.headers[cc.header_name] = cc.header_value
        return response

    return _cache_control
