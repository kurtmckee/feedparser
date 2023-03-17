import xml.sax
import zlib

import feedparser


def test_gzip_good(http_server):
    f = feedparser.parse("http://localhost:8097/tests/compression/gzip.gz")
    assert f.bozo == 0
    assert f.version == "atom10"


def test_gzip_not_compressed(http_server):
    f = feedparser.parse(
        "http://localhost:8097/tests/compression/gzip-not-compressed.gz"
    )
    assert f.bozo == 1
    assert isinstance(f.bozo_exception, IOError)
    assert f["feed"]["title"] == "gzip"


def test_gzip_struct_error(http_server):
    f = feedparser.parse("http://localhost:8097/tests/compression/gzip-struct-error.gz")
    assert f.bozo == 1
    assert isinstance(f.bozo_exception, xml.sax.SAXException)


def test_zlib_good(http_server):
    f = feedparser.parse("http://localhost:8097/tests/compression/deflate.z")
    assert f.bozo == 0
    assert f.version == "atom10"


def test_zlib_no_headers(http_server):
    f = feedparser.parse("http://localhost:8097/tests/compression/deflate-no-headers.z")
    assert f.bozo == 0
    assert f.version == "atom10"


def test_zlib_not_compressed(http_server):
    f = feedparser.parse(
        "http://localhost:8097/tests/compression/deflate-not-compressed.z"
    )
    assert f.bozo == 1
    assert isinstance(f.bozo_exception, zlib.error)
    assert f["feed"]["title"] == "deflate"
