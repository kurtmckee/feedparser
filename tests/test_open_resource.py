import io
import unittest.mock
import urllib.error
import urllib.request

import pytest

import feedparser


def test_fileobj():
    r = feedparser.api._open_resource(
        io.BytesIO(b""), "", "", "", "", [], {}, {}
    ).read()
    assert r == b""


def test_feed(http_server):
    f = feedparser.parse("feed://localhost:8097/tests/http/target.xml")
    assert f.href == "http://localhost:8097/tests/http/target.xml"


def test_feed_http(http_server):
    f = feedparser.parse("feed:http://localhost:8097/tests/http/target.xml")
    assert f.href == "http://localhost:8097/tests/http/target.xml"


def testbytes():
    s = b"<feed><item><title>text</title></item></feed>"
    r = feedparser.api._open_resource(s, "", "", "", "", [], {}, {}).read()
    assert s == r


def test_string():
    s = b"<feed><item><title>text</title></item></feed>"
    r = feedparser.api._open_resource(s, "", "", "", "", [], {}, {}).read()
    assert s == r


def test_unicode_1():
    s = b"<feed><item><title>text</title></item></feed>"
    r = feedparser.api._open_resource(s, "", "", "", "", [], {}, {}).read()
    assert s == r


def test_unicode_2():
    s = rb"<feed><item><title>t\u00e9xt</title></item></feed>"
    r = feedparser.api._open_resource(s, "", "", "", "", [], {}, {}).read()
    assert s == r


def test_http_client_ascii_unicode_encode_error():
    """Confirm that a Unicode character doesn't cause a UnicodeEncodeError crash."""
    url = "https://0.0.0.0/ô"
    with pytest.raises(urllib.error.URLError):
        feedparser.api._open_resource(url, "", "", "", "", [], {}, {})


def test_http_client_basic_auth_type_error():
    """Confirm an in-URL username/password doesn't cause a TypeError."""
    url = "https://username@password@0.0.0.0/feed"
    with pytest.raises(urllib.error.URLError):
        feedparser.api._open_resource(url, "", "", "", "", [], {}, {})


def test_http_client_urllib_error():
    """Confirm urllib.error.URLError is caught correctly.

    urllib.request.AbstractHTTPHandler.do_open() may explicitly raise
    urllib.error.URLError in e.g. Python 3.9.
    """

    exception = urllib.error.URLError("bogus")

    with unittest.mock.patch(
        "urllib.request.AbstractHTTPHandler.do_open",
        unittest.mock.Mock(side_effect=exception),
    ):
        result = feedparser.parse("https://bogus.example")
    assert result["bozo"] is True
    assert result["bozo_exception"] is exception
