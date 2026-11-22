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


def test_svg_xlink_href_with_unsafe_scheme_is_stripped():
    # SVG animation elements reference their target with xlink:href; an
    # unsafe (e.g. javascript:) URI scheme must be stripped just like it
    # is for plain HTML href attributes.
    html = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<set attributeName="onmouseover" to="alert(1)" '
        'xlink:href="javascript:alert(1)" /></svg>'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert "javascript:" not in result
    assert 'xlink:href=""' in result or "xlink:href" not in result


def test_svg_a_xlink_href_with_unsafe_scheme_is_stripped():
    html = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<a xlink:href="javascript:alert(1)"><text>click</text></a></svg>'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert "javascript:" not in result


def test_svg_xlink_href_with_safe_scheme_is_kept():
    html = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<a xlink:href="https://example.org/"><text>click</text></a></svg>'
    )
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert 'xlink:href="https://example.org/"' in result
