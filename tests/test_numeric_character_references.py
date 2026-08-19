from __future__ import annotations

import pytest

import feedparser


def _title_feed(charref: str) -> str:
    return (
        '<rss version="2.0"><channel>'
        f"<item><title>before{charref}after</title></item>"
        "</channel></rss>"
    )


@pytest.mark.parametrize(
    "charref, expected",
    [
        # A value that overflows the Unicode range.
        ("&#xFFFFFFFF;", "before&#xffffffff;after"),
        # The first code point above the maximum (0x10FFFF).
        ("&#x110000;", "before&#x110000;after"),
        # A lone surrogate that can't be encoded as UTF-8.
        ("&#xD800;", "before&#xd800;after"),
        # The decimal spelling of an out-of-range value.
        ("&#4294967295;", "before&#4294967295;after"),
    ],
)
def test_out_of_range_charref_does_not_crash(charref, expected):
    """Out-of-range numeric character references must not abort the parse.

    Previously ``&#xFFFFFFFF;``, ``&#x110000;``, and ``&#xD800;`` raised
    ``OverflowError``, ``ValueError``, and ``UnicodeEncodeError`` respectively
    from the loose parser. See issue #591.
    """

    result = feedparser.parse(_title_feed(charref))
    assert result.entries[0].title == expected


def test_valid_charref_is_still_resolved():
    """Well-formed references keep resolving to their character."""

    result = feedparser.parse(_title_feed("&#160;"))
    assert result.entries[0].title == "before\xa0after"
