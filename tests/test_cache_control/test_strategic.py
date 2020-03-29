from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from fastapi_for_firebase.cache_control import strategic


def test_cache_control__get():
    app = FastAPI()
    app.state.cache_control_strategy = strategic.StrategyStore()
    app.state.cache_control_strategy.add_rule("long")
    app.get("/", dependencies=[Depends(strategic.cache_control_strategy("long"))])(
        lambda: "OK"
    )
    response = TestClient(app).get("/")
    assert response.text == '"OK"'
    assert response.headers["Cache-Control"] == "public"


def test_cache_control__post():
    app = FastAPI()
    app.state.cache_control_strategy = strategic.StrategyStore()
    app.state.cache_control_strategy.add_rule("long")
    app.post("/", dependencies=[Depends(strategic.cache_control_strategy("long"))])(
        lambda: "OK"
    )
    response = TestClient(app).post("/")
    assert response.text == '"OK"'
    assert "Cache-Control" not in response.headers
