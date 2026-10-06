from __future__ import annotations

import datetime
import pathlib
import typing

import pytest

import feedparser

from .helpers import (
    everything_is_unicode,
    get_file_contents,
    get_http_test_data,
    get_test_data,
)

tests: list[tuple[typing.Any, ...]] = []
http_tests: list[tuple[typing.Any, ...]] = []
for path_ in pathlib.Path("tests/illformed").rglob("*.xml"):
    data_, text_ = get_file_contents(str(path_))
    if "http" in str(path_):
        info_ = (path_, data_, text_, *get_http_test_data(str(path_), data_, text_))
        http_tests.append(info_)
    else:
        info_ = (path_, data_, text_, *get_test_data(str(path_), text_))
        tests.append(info_)


@pytest.mark.parametrize("info", tests)
def test_strict_parser(info):
    path, data, text, description, eval_string, skip_unless = info
    try:
        eval(skip_unless, globals(), {})
    except (ModuleNotFoundError, ValueError):
        pytest.skip(description)
    result = feedparser.parse(data)
    assert eval(eval_string, {"datetime": datetime}, result), description
    assert everything_is_unicode(result)


@pytest.mark.parametrize("info", http_tests)
def test_http_conditions(info):
    path, data, text, url, description, eval_string, skip_unless = info
    result = feedparser.parse(url)
    assert result["bozo"] is True
    assert eval(eval_string, {"datetime": datetime}, result), description
    assert everything_is_unicode(result)


@pytest.mark.parametrize("dimension", ["height", "width"])
def test_stray_dimension_end_tag(dimension):
    result = feedparser.parse(f"</{dimension}>")

    assert result.bozo
    assert result.feed == {}
    assert result.entries == []


@pytest.mark.parametrize("dimension", ["height", "width"])
@pytest.mark.parametrize(
    "image_content, expected_dimension",
    [
        ("<title>logo</title></{dimension}>", None),
        ("<{dimension}>42</{dimension}></{dimension}><title>logo</title>", 42),
        ("<title>lo</{dimension}>go</title>", None),
    ],
)
def test_stray_dimension_end_tag_in_image(dimension, image_content, expected_dimension):
    image_content = image_content.format(dimension=dimension)
    result = feedparser.parse(
        f"<rss><channel><image>{image_content}</image>"
        "<title>feed title</title></channel></rss>"
    )

    assert result.bozo
    assert result.feed.title == "feed title"
    assert result.feed.image.title == "logo"
    if expected_dimension is None:
        assert dimension not in result.feed.image
    else:
        assert result.feed.image[dimension] == expected_dimension
