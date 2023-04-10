import io

import feedparser


def test_fileobj():
    r = feedparser.api._open_resource(io.BytesIO(b""), {}).read()
    assert r == b""


def testbytes():
    s = b"<feed><item><title>text</title></item></feed>"
    r = feedparser.api._open_resource(s, {}).read()
    assert s == r


def test_string():
    s = b"<feed><item><title>text</title></item></feed>"
    r = feedparser.api._open_resource(s, {}).read()
    assert s == r


def test_unicode_1():
    s = b"<feed><item><title>text</title></item></feed>"
    r = feedparser.api._open_resource(s, {}).read()
    assert s == r


def test_unicode_2():
    s = rb"<feed><item><title>t\u00e9xt</title></item></feed>"
    r = feedparser.api._open_resource(s, {}).read()
    assert s == r
