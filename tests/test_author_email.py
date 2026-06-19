"""Exercise author email extraction."""

import time

from feedparser.mixin import email_pattern


def test_email_pattern_rejects_pathological_domain_quickly():
    """Reject an email-like author without repeatedly rescanning its domain."""
    author = "user@" + ("a-b." * 5000) + "!"

    start = time.perf_counter()
    assert email_pattern.search(author) is None
    elapsed = time.perf_counter() - start

    assert elapsed < 0.1
