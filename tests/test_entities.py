from __future__ import annotations

import pathlib
import typing

import pytest

import feedparser

from .helpers import everything_is_unicode, get_file_contents, get_test_data

tests: list[tuple[typing.Any, ...]] = []
for path_ in pathlib.Path("tests/entities").rglob("*.xml"):
    data_, text_ = get_file_contents(str(path_))
    tests.append((path_, data_, text_, *get_test_data(str(path_), text_)))


@pytest.mark.parametrize("info", tests)
def test_entities_strict(info):
    path, data, text, description, eval_string, _ = info
    result = feedparser.parse(text)
    assert result["bozo"] == 1
    assert eval(eval_string, globals(), result), description
    assert everything_is_unicode(result)


@pytest.mark.parametrize("info", tests)
def test_entities_loose(info, use_loose_parser):
    path, data, text, description, eval_string, _ = info
    result = feedparser.parse(text)
    assert result["bozo"] is False
    assert eval(eval_string, globals(), result), description
    assert everything_is_unicode(result)
