import pytest

import feedparser.urls

BASE_URI = "http://d.test/d/f.ext"


@pytest.mark.parametrize(
    "uri, expected_uri, description",
    (
        ("https://s.test/", "https://s.test/", "absolute uri"),
        ("/new", "http://d.test/new", "relative uri"),
        ("x://bad.test/", "", "unacceptable uri protocol"),
        ("magnet:?xt=a", "magnet:?xt=a", "magnet uri"),
    ),
)
def test_make_safe_absolute_uri(uri, expected_uri, description):
    absolute_uri = feedparser.urls.make_safe_absolute_uri(BASE_URI, uri)
    assert absolute_uri == expected_uri, f"unexpected uri calculated for {description}"


@pytest.mark.parametrize("uri", ["http://bad]test/"])
def test_catch_value_error(monkeypatch, uri):
    """Catch ValueErrors when a URI is corrupt and malformed."""

    assert feedparser.urls.make_safe_absolute_uri(uri) == ""
    assert feedparser.urls.make_safe_absolute_uri(BASE_URI, uri) == ""

    monkeypatch.setattr(feedparser.urls, "ACCEPTABLE_URI_SCHEMES", ())
    assert feedparser.urls.make_safe_absolute_uri(BASE_URI, uri) == ""
