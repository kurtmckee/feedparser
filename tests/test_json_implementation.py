import feedparser


def test_duplicate_keys():
    """Verify that the last duplicate JSON key is the one that is seen."""

    text = """
        {
            "version": "bogus",
            "version": "https://jsonfeed.org/version/1",
            "version": "https://jsonfeed.org/version/1.1"
        }
    """

    result = feedparser.parse(text)
    assert result["version"] == "json11"


def test_common_non_standard_types():
    """Verify that the JSON implementation doesn't choke on common, non-standard types."""

    text = """
        {
            "a": NaN,
            "b": Infinity,
            "c": -Infinity,
            "version": "https://jsonfeed.org/version/1.1"
        }
    """

    result = feedparser.parse(text)
    assert result["version"] == "json11"


def test_unicode_escapes():
    """Verify that Unicode escapes are handled correctly."""

    text = r"""
        {
            "title": "abc\ud83d\ude0edef"
        }
    """
    assert "ud83d" in text
    result = feedparser.parse(text)
    assert result["feed"]["title"] == "abc😎def"
