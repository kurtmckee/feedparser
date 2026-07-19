from __future__ import annotations

import feedparser
from feedparser.mixin import EMAIL_PATTERN_MAX_LENGTH


def _feed(author: str) -> str:
    return (
        '<?xml version="1.0"?>'
        '<rss version="2.0"><channel><title>t</title>'
        f"<item><title>x</title><author>{author}</author></item>"
        "</channel></rss>"
    )


def test_normal_author_email_still_extracted():
    result = feedparser.parse(_feed("Example editor (me@example.com)"))
    detail = result.entries[0].author_detail
    assert detail["name"] == "Example editor"
    assert detail["email"] == "me@example.com"


def test_bare_email_still_extracted():
    result = feedparser.parse(_feed("me@example.com"))
    assert result.entries[0].author_detail["email"] == "me@example.com"


def test_oversized_author_skips_email_match():
    # A hostile feed can supply an author value crafted so the email pattern
    # backtracks quadratically. Values longer than the bound are left alone
    # instead of being fed to the regex, so parsing stays fast.
    hostile = "a@" + "a." * 16000 + "!"
    assert len(hostile) > EMAIL_PATTERN_MAX_LENGTH

    result = feedparser.parse(_feed(hostile))

    assert result.bozo is False
    # The oversized value is kept verbatim as the name and no email is split
    # out of it.
    assert "email" not in result.entries[0].author_detail
    assert result.entries[0].author_detail["name"] == hostile
