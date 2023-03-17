import datetime
import time

import feedparser


def test_301(http_server):
    f = feedparser.parse("http://localhost:8097/tests/http/http_status_301.xml")
    assert f.status == 301
    assert f.href == "http://localhost:8097/tests/http/target.xml"
    assert f.entries[0].title == "target"


def test_302(http_server):
    f = feedparser.parse("http://localhost:8097/tests/http/http_status_302.xml")
    assert f.status == 302
    assert f.href == "http://localhost:8097/tests/http/target.xml"
    assert f.entries[0].title == "target"


def test_302_no_location(http_server):
    """Confirm no AttributeErrors when an HTTP 3xx response has no Location header."""

    f = feedparser.parse(
        "http://localhost:8097/tests/http/http_status_302-no-location.xml"
    )
    assert f.status == 302


def test_303(http_server):
    f = feedparser.parse("http://localhost:8097/tests/http/http_status_303.xml")
    assert f.status == 303
    assert f.href == "http://localhost:8097/tests/http/target.xml"
    assert f.entries[0].title == "target"


def test_307(http_server):
    f = feedparser.parse("http://localhost:8097/tests/http/http_status_307.xml")
    assert f.status == 307
    assert f.href == "http://localhost:8097/tests/http/target.xml"
    assert f.entries[0].title == "target"


def test_304(http_server):
    # first retrieve the url
    u = "http://localhost:8097/tests/http/http_status_304.xml"
    f = feedparser.parse(u)
    assert f.status == 200
    assert f.entries[0].title == "title 304"
    # extract the etag and last-modified headers
    e = [v for k, v in f.headers.items() if k.lower() == "etag"][0]
    ms = f.updated
    mt = f.updated_parsed
    md = datetime.datetime(*mt[0:7])
    assert isinstance(mt, time.struct_time)
    assert isinstance(md, datetime.datetime)
    # test that sending back the etag results in a 304
    f = feedparser.parse(u, etag=e)
    assert f.status == 304
    # test that sending back last-modified (string) results in a 304
    f = feedparser.parse(u, modified=ms)
    assert f.status == 304
    # test that sending back last-modified (9-tuple) results in a 304
    f = feedparser.parse(u, modified=mt)
    assert f.status == 304
    # test that sending back last-modified (datetime) results in a 304
    f = feedparser.parse(u, modified=md)
    assert f.status == 304


def test_404(http_server):
    f = feedparser.parse("http://localhost:8097/tests/http/http_status_404.xml")
    assert f.status == 404


def test_redirect_to_304(http_server):
    # ensure that an http redirect to an http 304 doesn't
    # trigger a bozo_exception
    u = "http://localhost:8097/tests/http/http_redirect_to_304.xml"
    f = feedparser.parse(u)
    assert f.bozo == 0
    assert f.status == 302
