import json
import pathlib

import pytest

import feedparser

paths = pathlib.Path("tests/json").rglob("*.json")


@pytest.mark.parametrize("path", paths, ids=lambda path: path.stem)
def test_json(path):
    text = path.read_text(encoding="utf8")
    data = json.loads(text)
    result = feedparser.parse(text, sanitize_html=False)
    for test_string in data["__tests"]:
        assert eval(test_string, None, result), test_string

    # Verify that all dicts are instances of FeedParserDict.
    dicts: list[tuple[str, dict]] = [("top level", result)]
    while dicts:
        key, value = dicts.pop()
        assert isinstance(value, feedparser.FeedParserDict), f"{key} is just a dict"
        dicts.extend(
            (k, v)
            for k, v in value.items()
            if isinstance(v, dict) and k != "namespaces" and k != "headers"
        )

    assert result["bozo"] is False, result["bozo_exception"]
