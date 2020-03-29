import pytest
from fastapi_for_firebase import hosting


def test_header_value__default():
    cc = hosting.CacheControl()
    assert cc.header_value == "public"


@pytest.mark.parametrize("max_age,s_maxage,expected", [
    (60, 60, "public, max-age=60, s-maxage=60"),
    (30, 0, "public, max-age=30"),
    (0, 30, "public, s-maxage=30"),
    (30, None, "public, max-age=30"),
    (None, 30, "public, s-maxage=30"),
])
def test_header_value__parameters(max_age, s_maxage, expected):
    cc = hosting.CacheControl(max_age, s_maxage)
    assert cc.header_value == expected
