from __future__ import annotations

import feedparser


def _title(ref: str) -> str:
    text = (
        '<?xml version="1.0"?>'
        '<rss version="2.0"><channel><title>t</title>'
        f"<item><title>a{ref}b</title></item></channel></rss>"
    )
    result = feedparser.parse(text)
    return result.entries[0].title


def test_out_of_range_charref_stays_in_the_title():
    # These used to abort parsing: OverflowError, ValueError, UnicodeEncodeError.
    assert _title("&#xFFFFFFFF;") == "a&#xffffffff;b"
    assert _title("&#x110000;") == "a&#x110000;b"
    assert _title("&#xD800;") == "a&#xd800;b"
    assert _title("&#1114112;") == "a&#1114112;b"


def test_in_range_charref_still_decodes():
    assert _title("&#65;") == "aAb"
    assert _title("&#x41;") == "aAb"
