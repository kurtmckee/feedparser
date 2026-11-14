import time

import pytest

import feedparser
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


@pytest.mark.parametrize(
    "style, expected_style",
    (
        ("color: red", "color: red;"),
        ("color:red;margin:0", "color: red; margin: 0;"),
        ("color: red; margin: 0;", "color: red; margin: 0;"),
        ("  color : red ;  ", "color: red ;"),
        ("color: red blue", "color: red blue;"),
        ("margin: 0 0 0 0;", "margin: 0 0 0 0;"),
    ),
)
def test_valid_styles_are_accepted(style, expected_style):
    html = f'<p style="{style}">example</p>'
    expected = f'<p style="{expected_style}">example</p>'
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == expected


@pytest.mark.parametrize(
    "style",
    (
        "",
        "   ",
        "color",
        "color red",
        ":",
        ";",
        ";color: red",
        "color: red;;",
        "color: red; garbage",
        "color: red: blue",
        "color:;",
        "a" * 2000,
    ),
)
def test_invalid_or_empty_styles_are_dropped(style):
    html = f'<p style="{style}">example</p>'
    result = feedparser.sanitizer.sanitize_html(html, None, "text/html")
    assert result == "<p>example</p>"


def test_hostile_style_is_parsed_quickly():
    # A long run of word characters with no ":" passes the sanitizer's
    # gauntlet, but the declaration check used to rescan the run at every
    # offset, taking quadratic time in the length of the style attribute.
    style = "a" * 40000
    doc = (
        '<?xml version="1.0"?><rss version="2.0"><channel><title>t</title>'
        f'<item><description><![CDATA[<p style="{style}">x</p>]]>'
        "</description></item></channel></rss>"
    )

    start = time.perf_counter()
    result = feedparser.parse(doc)
    elapsed = time.perf_counter() - start

    assert elapsed < 2.0
    assert result.bozo is False
    assert result.entries[0].description == "<p>x</p>"
