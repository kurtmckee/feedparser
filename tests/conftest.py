from __future__ import annotations

import pytest
import responses


# TODO: tag=bad-layout
#
#       The `sys.path` must be modified to guarantee that
#       the repository's root directory IS NOT present
#       at the start of the import path list.
#
#       If the path appears at the beginning of `sys.path`,
#       it will breaks imports because of the namespace package
#       feedparser-sgmllib.
#
#       After migrating to a `src/` layout, remove this code block.
#
# ---- 8< ----
def rewrite_sys_path():
    import pathlib
    import sys

    root = str(pathlib.Path(__file__).parent.parent.absolute())
    if sys.path[0] == root:
        sys.path.pop(0)


rewrite_sys_path()
# ---- >8 ----


@pytest.fixture
def use_loose_parser(monkeypatch):
    import feedparser.api

    monkeypatch.setattr(feedparser.api, "_XML_AVAILABLE", False)
    yield


@pytest.fixture(scope="session", autouse=True)
def mock_responses():
    responses.start()
