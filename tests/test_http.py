import responses

import feedparser


def test_error_status_body_is_not_parsed():
    # GH 460 - an HTTP error page's body (here a plain-text message, but an
    # HTML error page is just as common) isn't feed content, and used to be
    # fed straight to the XML parser, producing a confusing bozo_exception
    # that looked like a malformed feed instead of clearly surfacing the
    # HTTP failure that result["status"] already reports.
    url = "http://127.0.0.1:8097/error-status-body-is-not-parsed"
    responses.get(
        url,
        status=500,
        body="Internal Server Error",
        content_type="text/plain",
    )

    result = feedparser.parse(url)

    assert result.status == 500
    assert not result.bozo
    assert "bozo_exception" not in result
    assert result.entries == []


def test_success_status_body_is_still_parsed():
    url = "http://127.0.0.1:8097/success-status-body-is-still-parsed"
    responses.get(
        url,
        status=200,
        body=(
            b"<rss version='2.0'><channel>"
            b"<item><title>hi</title></item>"
            b"</channel></rss>"
        ),
        content_type="application/rss+xml",
    )

    result = feedparser.parse(url)

    assert result.status == 200
    assert not result.bozo
    assert len(result.entries) == 1
    assert result.entries[0].title == "hi"
