import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_for_firebase.hosting.middleware import cache_control


@pytest.mark.parametrize(
    "max_age,s_maxage,header_value", [(30, 60, "public, max-age=30, s-maxage=60"), (30, None, "public, max-age=30")]
)
def test_cache_control__get(max_age, s_maxage, header_value):
    app = FastAPI()
    client = TestClient(app)
    app.middleware("http")(cache_control(max_age, s_maxage))
    app.get("/")(lambda: "OK")
    response = client.get("/")
    assert response.text == '"OK"'
    assert response.headers["Cache-Control"] == header_value


def test_cache_control__post():
    app = FastAPI()
    client = TestClient(app)
    app.middleware("http")(cache_control())
    app.post("/")(lambda: "OK")
    response = client.post("/")
    assert response.text == '"OK"'
    assert "Cache-Control" not in response.headers
