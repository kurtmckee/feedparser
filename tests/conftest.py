from __future__ import annotations

import pytest
import responses


@pytest.fixture
def use_loose_parser(monkeypatch):
    import feedparser.api

    monkeypatch.setattr(feedparser.api, "_XML_AVAILABLE", False)
    yield


@pytest.fixture(scope="session", autouse=True)
def mock_responses():
    responses.start()
