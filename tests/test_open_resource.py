import io

import feedparser


def test_fileobj():
    method, filelike = feedparser.api._open_resource(io.BytesIO(b""), {})
    r = filelike.read()
    assert r == b""
    assert method == "seekable"


def testbytes():
    s = b"<feed><item><title>text</title></item></feed>"
    method, filelike = feedparser.api._open_resource(s, {})
    r = filelike.read()
    assert s == r
    assert method == "raw_data"


def test_string():
    s = b"<feed><item><title>text</title></item></feed>"
    method, filelike = feedparser.api._open_resource(s, {})
    r = filelike.read()
    assert s == r
    assert method == "raw_data"


def test_unicode_1():
    s = b"<feed><item><title>text</title></item></feed>"
    method, filelike = feedparser.api._open_resource(s, {})
    r = filelike.read()
    assert s == r
    assert method == "raw_data"


def test_unicode_2():
    s = rb"<feed><item><title>t\u00e9xt</title></item></feed>"
    method, filelike = feedparser.api._open_resource(s, {})
    r = filelike.read()
    assert s == r
    assert method == "raw_data"
