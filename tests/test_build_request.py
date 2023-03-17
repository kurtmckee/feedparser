import feedparser.http


def test_extra_headers():
    """Confirm that extra headers are added to the request object."""

    request = feedparser.http._build_urllib2_request(
        "http://example.com/feed",
        "agent-name",
        None,
        None,
        None,
        None,
        None,
        {"Cache-Control": "max-age=0"},
    )
    # nb, urllib2 folds the case of the headers
    assert request.get_header("Cache-control") == "max-age=0"
