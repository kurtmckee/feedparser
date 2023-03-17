import feedparser.sanitizer


def test_style_attr_is_enabled():
    html = """<p style="margin: 15em;">example</p>"""
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == html


def test_style_attr_can_be_disabled():
    html = """<p style="margin: 15em;">example</p>"""
    expected = """<p>example</p>"""
    original_attrs = feedparser.sanitizer.HTMLSanitizer.acceptable_attributes
    feedparser.sanitizer.HTMLSanitizer.acceptable_attributes = set()
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    feedparser.sanitizer.HTMLSanitizer.acceptable_attributes = original_attrs
    assert result == expected
