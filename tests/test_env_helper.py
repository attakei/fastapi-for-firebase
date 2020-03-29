import pytest
from fastapi_for_firebase import env_helper


@pytest.mark.parametrize(
    "prefix,lowering,src,dst",
    [
        ("APP_", True, {"APPS_": "sample"}, {}),
        ("APP_", True, {"APP_KEY": "sample"}, {"key": "sample"}),
        ("APP_", False, {"APP_KEY": "sample"}, {"KEY": "sample"}),
        (
            "APP_",
            True,
            {"APP_DEBUG": "1", "APP_URL": "/sample"},
            {"debug": "1", "url": "/sample"},
        ),
    ],
)
def test_filter_envmap(prefix, lowering, src, dst):
    assert env_helper.filter_envmap(prefix, src, lowering) == dst


@pytest.mark.parametrize(
    "value,convert,expect",
    [
        ("a:1,b:test", None, {"a": "1", "b": "test"}),
        ("a:1,b:2", int, {"a": 1, "b": 2}),
    ],
)
def test_parse_as_dict(value, convert, expect):
    assert env_helper.parse_as_dict(value, convert=convert) == expect
