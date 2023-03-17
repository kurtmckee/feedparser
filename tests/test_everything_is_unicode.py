import pytest

from .helpers import everything_is_unicode


def test_everything_is_unicode():
    assert everything_is_unicode({"a": "a", "b": ["b", {"c": "c"}], "d": {"e": "e"}})


@pytest.mark.parametrize(
    "example",
    (
        {"a": b"a"},
        {"a": [b"a"]},
        {"a": {"b": b"b"}},
        {"a": [{"b": b"b"}]},
    ),
)
def test_not_everything_is_unicode(example):
    assert not everything_is_unicode(example)
