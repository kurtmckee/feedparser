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


@pytest.mark.parametrize("prefix", ["creativeCommons", "creativecommons"])
def test_stray_license_end_tag(prefix):
    result = feedparser.parse(f"</{prefix}:license>")

    assert result.bozo
    assert result.feed == {}
    assert result.entries == []


@pytest.mark.parametrize("prefix", ["creativeCommons", "ccrss"])
@pytest.mark.parametrize("level", ["feed", "entry"])
@pytest.mark.parametrize(
    "content, has_license",
    [
        ("<title>item</title></{prefix}:license>", False),
        (
            "<{prefix}:license>https://example.com/license</{prefix}:license>"
            "</{prefix}:license><title>item</title>",
            True,
        ),
        ("<title>it</{prefix}:license>em</title>", False),
    ],
)
def test_stray_license_end_tag_preserves_context(prefix, level, content, has_license):
    content = content.format(prefix=prefix)
    if level == "entry":
        content = f"<item>{content}</item>"
    result = feedparser.parse(
        f'<rss xmlns:{prefix}="http://backend.userland.com/creativeCommonsRssModule">'
        f"<channel>{content}</channel></rss>"
    )

    assert result.bozo
    context = result.feed if level == "feed" else result.entries[0]
    assert context.title == "item"
    expected_links = (
        [{"rel": "license", "href": "https://example.com/license"}]
        if has_license
        else []
    )
    assert context.get("links", []) == expected_links
