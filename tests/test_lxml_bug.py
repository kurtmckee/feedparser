import io

import pytest

import feedparser

try:
    import lxml.etree
except ImportError:
    lxml = None


@pytest.mark.skipif(lxml is None, reason="lxml is unavailable for testing")
def test_lxml_etree_bug():
    doc = b"<feed>&illformed_charref</feed>"
    # Importing lxml.etree currently causes libxml2 to
    # throw SAXException instead of SAXParseException.
    feedparser.parse(io.BytesIO(doc))
    raise AssertionError("what is this testing?")
