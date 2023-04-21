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
        assert eval(test_string, result, locals()), test_string
    assert result["bozo"] is False, result["bozo_exception"]
