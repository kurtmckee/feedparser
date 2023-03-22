import warnings

import pytest

import feedparser


def test_issue_328_fallback_behavior():
    """Test fallback behavior. See issues 310 and 328."""

    warnings.filterwarnings("error")

    d = feedparser.util.FeedParserDict()
    d["published"] = "pub string"
    d["published_parsed"] = "pub tuple"
    d["updated"] = "upd string"
    d["updated_parsed"] = "upd tuple"
    # Ensure that `updated` doesn't map to `published` when it exists
    assert "published" in d
    assert "published_parsed" in d
    assert "updated" in d
    assert "updated_parsed" in d
    assert d["published"] == "pub string"
    assert d["published_parsed"] == "pub tuple"
    assert d["updated"] == "upd string"
    assert d["updated_parsed"] == "upd tuple"

    d = feedparser.util.FeedParserDict()
    d["published"] = "pub string"
    d["published_parsed"] = "pub tuple"
    # Ensure that `updated` doesn't actually exist
    assert "updated" not in d
    assert "updated_parsed" not in d
    # Ensure that accessing `updated` throws a DeprecationWarning
    with pytest.warns(DeprecationWarning):
        d["updated"]
    with pytest.warns(DeprecationWarning):
        d["updated_parsed"]
    # Ensure that `updated` maps to `published`
    warnings.filterwarnings("ignore")
    assert d["updated"] == "pub string"
    assert d["updated_parsed"] == "pub tuple"
    warnings.resetwarnings()
