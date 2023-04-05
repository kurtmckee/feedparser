"""
Unconditionally substitute text for variables in .rst sources.

The feedparser documentation references example feed files
which are hosted on Read the Docs.

This extension helps ensure that the documentation points at the correct doc URL.
"""

import os


READTHEDOCS_CANONICAL_URL = os.getenv(
    "READTHEDOCS_CANONICAL_URL",
    "https://domain.example/",
).rstrip("/")


def substitute(app, docname, source: list[str]):
    source[0] = source[0].replace(
        "$READTHEDOCS_CANONICAL_URL",
        READTHEDOCS_CANONICAL_URL,
    )


def setup(app):
    app.connect("source-read", substitute)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
