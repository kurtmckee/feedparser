from __future__ import annotations

import pytest

import feedparser

# Malformed inputs that used to raise out of feedparser.parse() instead of
# being reported through the ``bozo_exception`` mechanism that parse() is
# documented to use.
CASES: list[tuple[str, bytes]] = [
    (
        "namespace declaration that expat reports as a longer name tuple",
        b'<?l?><d xmlns=":\xa0\xff\xa0o">',
    ),
    (
        "XML declaration encoding containing a NUL byte",
        b'<?encoding="\x00"?>',
    ),
    (
        "XML declaration encoding that is not valid UTF-8",
        b'<?encoding="\xff"?>',
    ),
]

IDS = [case[0] for case in CASES]
PARAMS = pytest.mark.parametrize(("description", "data"), CASES, ids=IDS)


@PARAMS
def test_malformed_input_does_not_raise(description: str, data: bytes) -> None:
    result = feedparser.parse(data)

    assert result["bozo"], description
    assert result["bozo_exception"] is not None, description


@PARAMS
def test_malformed_input_leaves_a_usable_result(description: str, data: bytes) -> None:
    result = feedparser.parse(data)

    # A failed parse still has to produce the documented result shape, so
    # callers can log the problem rather than handling an exception.
    assert result["entries"] == [], description
    assert isinstance(result["encoding"], str), description
