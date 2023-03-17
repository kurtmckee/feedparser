"""Test IDN support (unavailable in Jython as of Jython 2.5.2)"""

import feedparser.urls

# this is the greek test domain
hostname = "\u03c0\u03b1\u03c1\u03ac\u03b4\u03b5\u03b9\u03b3\u03bc\u03b1"
hostname += ".\u03b4\u03bf\u03ba\u03b9\u03bc\u03ae"


def test_control():
    r = feedparser.urls.convert_to_idn("http://example.test/")
    assert r == "http://example.test/"


def test_idn():
    r = feedparser.urls.convert_to_idn(f"http://{hostname}/")
    assert r == "http://xn--hxajbheg2az3al.xn--jxalpdlp/"


def test_port():
    r = feedparser.urls.convert_to_idn(f"http://{hostname}:8080/")
    assert r == "http://xn--hxajbheg2az3al.xn--jxalpdlp:8080/"
