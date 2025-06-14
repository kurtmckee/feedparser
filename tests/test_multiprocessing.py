from concurrent.futures import ProcessPoolExecutor

import pytest

import feedparser

base_feed_str = b"""<?xml version='1.0' encoding='UTF-8'?>
<rss version="2.0">
<channel>
<title>Foo</title>
<link>https://foo.com/</link>
<item><title>Title 1</title><link>https://foo.com/1</link><pubDate>Thu, 05 Jun 2025 18:27:58 -0000</pubDate></item>
</channel>
</rss>
"""


def _parse_and_return_full(raw_feed: bytes):
    return feedparser.parse(raw_feed)


@pytest.mark.parametrize(
    "feed, expected_title, expected_bozo_exception, expected_items",
    [
        (
            base_feed_str,
            "Foo",
            None,
            [
                dict(
                    title="Title 1",
                    link="https://foo.com/1",
                    published="Thu, 05 Jun 2025 18:27:58 -0000",
                )
            ],
        ),
        (
            b"\n" + base_feed_str,
            "Foo",
            "XML or text declaration not at start of entity",
            [
                dict(
                    title="Title 1",
                    link="https://foo.com/1",
                    published="Thu, 05 Jun 2025 18:27:58 -0000",
                )
            ],
        ),
    ],
    ids=["correct_feed", "leading_newline_feed"],
)
def test_multiprocessing_parse(
    feed, expected_title, expected_bozo_exception, expected_items
):
    with ProcessPoolExecutor(1) as pool:
        future = pool.submit(_parse_and_return_full, feed)
        result = future.result()

    assert result["feed"]["title"] == expected_title
    if expected_bozo_exception:
        assert expected_bozo_exception in result.get("bozo_exception")
    else:
        assert result.get("bozo_exception") is None
    for observed, expected in zip(result["entries"], expected_items, strict=True):
        assert observed["published"] == expected["published"]
        assert observed["link"] == expected["link"]
        assert observed["title"] == expected["title"]
