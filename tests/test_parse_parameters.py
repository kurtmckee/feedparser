import io

import pytest

import feedparser
import feedparser.encodings

feed_xml = b"""
    <rss version="2.0">
        <channel>
            <item>
                <body><script>alert("boo!")</script></body>
            </item>
            <item>
                <body><a href="/boo.html">boo</a></body>
            </item>
        </channel>
    </rss>
"""


def test_sanitize_html_default():
    d = feedparser.parse(io.BytesIO(feed_xml))
    assert d.entries[0].content[0].value == ""


def test_sanitize_html_on():
    d = feedparser.parse(io.BytesIO(feed_xml), sanitize_html=True)
    assert d.entries[0].content[0].value == ""


def test_sanitize_html_off():
    d = feedparser.parse(io.BytesIO(feed_xml), sanitize_html=False)
    assert d.entries[0].content[0].value == '<script>alert("boo!")</script>'


def test_response_headers_case_insensitive():
    d = feedparser.parse(
        io.BytesIO(feed_xml),
        response_headers={"CoNtEnT-LoCaTiOn": "http://example.com/feed"},
    )
    assert d.entries[1].content[0].value == (
        '<a href="http://example.com/boo.html">boo</a>'
    )


def test_resolve_relative_uris_default():
    d = feedparser.parse(
        io.BytesIO(feed_xml),
        response_headers={"content-location": "http://example.com/feed"},
    )
    assert d.entries[1].content[0].value == (
        '<a href="http://example.com/boo.html">boo</a>'
    )


def test_resolve_relative_uris_on():
    d = feedparser.parse(
        io.BytesIO(feed_xml),
        response_headers={"content-location": "http://example.com/feed"},
        resolve_relative_uris=True,
    )
    assert d.entries[1].content[0].value == (
        '<a href="http://example.com/boo.html">boo</a>'
    )


def test_resolve_relative_uris_off():
    d = feedparser.parse(
        io.BytesIO(feed_xml),
        response_headers={"content-location": "http://example.com/feed.xml"},
        resolve_relative_uris=False,
    )
    assert d.entries[1].content[0].value == '<a href="/boo.html">boo</a>'


length = feedparser.encodings.CONVERT_FILE_PREFIX_LEN
digits = "0123456789abcdef😀"
description = digits * int(length / len(digits) * 1.5)
optimistic_encoding_xml = f"""
    <rss version="2.0">
    <channel>
        <item>
            <guid isPermaLink="false">id</guid>
            <description>{description}</description>
        </item>
    </channel>
    </rss>
"""


class NonSeekableFileWrapper:
    def __init__(self, file):
        self.file = file

    def read(self, *args, **kwargs):
        return self.file.read(*args, **kwargs)


@pytest.mark.parametrize(
    "kwargs",
    (
        {},
        {"optimistic_encoding_detection": True},
        {"optimistic_encoding_detection": False},
    ),
)
@pytest.mark.parametrize(
    "get_content",
    (
        lambda: io.BytesIO(optimistic_encoding_xml.encode("utf-8")),
        lambda: NonSeekableFileWrapper(
            io.BytesIO(optimistic_encoding_xml.encode("utf-8"))
        ),
        lambda: optimistic_encoding_xml.encode("utf-8"),
        lambda: io.StringIO(optimistic_encoding_xml),
        lambda: NonSeekableFileWrapper(io.StringIO(optimistic_encoding_xml)),
        lambda: optimistic_encoding_xml,
    ),
    ids=lambda x: repr(x)[:100],
)
def test_optimistic_encoding_detection(get_content, kwargs):
    content = get_content()
    result = feedparser.parse(content, **kwargs)
    assert len(result.entries), result
    assert result.entries[0].description == description
