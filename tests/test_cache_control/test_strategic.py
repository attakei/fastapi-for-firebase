from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from fastapi_for_firebase.cache_control import strategic


def get_app() -> FastAPI:
    app = FastAPI()
    app.state.cache_control_strategy = strategic.StrategyStore()
    app.state.cache_control_strategy.add_rule("long")
    return app


def test_cache_control__get():
    app = get_app()
    app.get("/", dependencies=[Depends(strategic.cache_control_strategy("long"))])(
        lambda: "OK"
    )
    response = TestClient(app).get("/")
    assert response.text == '"OK"'
    assert response.headers["Cache-Control"] == "public"


def test_cache_control__invalid_strategy():
    app = get_app()
    app.get("/", dependencies=[Depends(strategic.cache_control_strategy("invalid"))])(
        lambda: "OK"
    )
    response = TestClient(app).get("/")
    assert response.status_code == 500


def test_cache_control__post():
    app = get_app()
    app.post("/", dependencies=[Depends(strategic.cache_control_strategy("long"))])(
        lambda: "OK"
    )
    response = TestClient(app).post("/")
    assert response.text == '"OK"'
    assert "Cache-Control" not in response.headers
