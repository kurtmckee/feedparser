import datetime

import pytest

import feedparser


def test_malformed_chapter_without_start():
    result = feedparser.parse("<psc:chapters<psc:chapter>")

    assert result.bozo
    assert result.feed.psc_chapters.chapters == [{"start_parsed": None}]


@pytest.mark.parametrize("feed_format", ["rss", "atom"])
@pytest.mark.parametrize("malformed", [False, True])
@pytest.mark.parametrize("start", [None, "", "invalid"])
def test_chapter_with_invalid_start_preserves_metadata(feed_format, malformed, start):
    start_attribute = "" if start is None else f' start="{start}"'
    chapters = (
        '<psc:chapters version="1.2">'
        '<psc:chapter start="00:00:00" title="First"/>'
        f'<psc:chapter{start_attribute} title="Untimed" '
        'href="https://example.com/chapter" image="https://example.com/image"/>'
        '<psc:chapter start="00:03:07.250" title="Last"/>'
        "</psc:chapters>"
    )
    if malformed:
        chapters += "</wrong>"
    if feed_format == "rss":
        document = (
            '<rss xmlns:psc="http://podlove.org/simple-chapters">'
            f"<channel><item><title>Episode</title>{chapters}</item></channel></rss>"
        )
    else:
        document = (
            '<feed xmlns="http://www.w3.org/2005/Atom" '
            'xmlns:psc="http://podlove.org/simple-chapters">'
            f"<entry><title>Episode</title>{chapters}</entry></feed>"
        )

    result = feedparser.parse(document)

    assert bool(result.bozo) == malformed
    assert result.entries[0].title == "Episode"
    parsed_chapters = result.entries[0].psc_chapters.chapters
    assert len(parsed_chapters) == 3
    assert parsed_chapters[0].start_parsed == datetime.timedelta(0)
    assert parsed_chapters[1].title == "Untimed"
    assert parsed_chapters[1].href == "https://example.com/chapter"
    assert parsed_chapters[1].image == "https://example.com/image"
    assert parsed_chapters[1].start_parsed is None
    if start is None:
        assert "start" not in parsed_chapters[1]
    else:
        assert parsed_chapters[1].start == start
    assert parsed_chapters[2].start_parsed == datetime.timedelta(
        seconds=187, milliseconds=250
    )
