"""Strategic cache-control.

Module usage:

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
import os
from dataclasses import dataclass, field
from typing import Callable, Dict

from fastapi import HTTPException, Request, Response

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


def store_from_env(prefix: str = None) -> StrategyStore:
    """Create strategy-store from environment variables.

    1. Find prefixed key from environment-variables.
    2. Create rule from environment.
    3. Create store and register these rules.

    :param prefix: Using prefix of environment variables.
    """
    prefix = "CACHE_CONTROL_" if prefix is None else prefix
    plen = len(prefix)
    strategy = StrategyStore()
    filtered = {
        k[plen:].lower(): v for k, v in os.environ.items() if k.startswith(prefix)
    }
    for name, values in filtered.items():
        value_dict = {}
        for pair in values.split(","):
            k, v = pair.split(":")
            value_dict[k] = int(v)
        strategy.add_rule(name, **value_dict)
    return strategy


def cache_control_strategy(name: str) -> Callable:
    """Dependency Injection using cache-control strategy.

    If stategy is not exists. raise http-500.

    Currently spec:

    - app.state must have "cache_control_strategy" attribute.
    - strategy object must be set all rule before request.
    """

    async def _cache_control_strategy(request: Request, response: Response):
        if request.method == "GET":
            try:
                store: StrategyStore = request.app.state.cache_control_strategy
                cc = store.get_rule(name)
                response.headers[cc.header_name] = cc.header_value
            except KeyError:
                raise HTTPException(status_code=500, detail="invalid-cache-control")

    return _cache_control_strategy
