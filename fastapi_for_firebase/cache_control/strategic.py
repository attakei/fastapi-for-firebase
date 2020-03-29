"""Strategic cache-control.

Module usage
------------

1. Plan your cache-control storategy. (ex: "long" caches content until 3600 seconds)
2. Set storategy store to your app.state and add rules.
3. Set cache strategy as Depends to your path routing.

.. code-block: python

   app = FastAPI()
   strategy = StrategyStore()
   strategy.add_rule("long", 3600)
   strategy.add_rule("short", 300, 600)
   app.state.cache_control_strategy = strategy

   @app.get("/", dependencies=[Depends(cache_control_strategy("long"))]
   async def hello():
       return "hello world"
"""
from dataclasses import dataclass, field
from typing import Callable, Dict

from fastapi import Request, Response

from . import CacheControl


@dataclass
class StrategyStore(object):
    """Name-based cache-control strategy
    """

    rules: Dict[str, CacheControl] = field(default_factory=dict)

    def get_rule(self, name: str) -> CacheControl:
        return self.rules[name]

    def add_rule(self, name: str, max_age: int = None, s_maxage: int = None):
        if name in self.rules:
            raise Exception(f"Rule '{name}' is already exists.")
        self.rules[name] = CacheControl(max_age, s_maxage)


def cache_control_strategy(name: str) -> Callable:
    """Dependency Injection using cache-control strategy.

    Currently spec
    --------------

    - app.state must have "cache_control_strategy" attribute.
    - strategy object must be set all rule before request.
    """

    async def _cache_control_strategy(request: Request, response: Response):
        if request.method == "GET":
            store: StrategyStore = request.app.state.cache_control_strategy
            cc = store.get_rule(name)
            response.headers[cc.header_name] = cc.header_value

    return _cache_control_strategy
