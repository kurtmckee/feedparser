import io

import feedparser


def test_empty_bytestring_sets_bozo():
    result = feedparser.parse(io.BytesIO(b""))
    assert result["bozo"] is True
    assert isinstance(result["bozo_exception"], feedparser.EmptyDocument)
    assert result["entries"] == []
    assert result["feed"] == {}


def test_empty_string_sets_bozo():
    result = feedparser.parse(io.StringIO(""))
    assert result["bozo"] is True
    assert isinstance(result["bozo_exception"], feedparser.EmptyDocument)


def test_nonempty_feed_does_not_set_bozo_via_empty_document():
    result = feedparser.parse(b"<feed><entry><title>t</title></entry></feed>")
    exc = result.get("bozo_exception")
    assert not isinstance(exc, feedparser.EmptyDocument)
