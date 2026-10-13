from __future__ import annotations

import pytest

import feedparser
from feedparser.namespaces.georss import _parse_poslist


@pytest.mark.parametrize("value", [".", "1 invalid", "1 2 3 invalid"])
def test_invalid_polygon_poslist(value):
    assert _parse_poslist(value, "polygon") is None


@pytest.mark.parametrize("loose", [False, True])
@pytest.mark.parametrize("value", [".", "1 invalid", "1 2 3 invalid"])
def test_invalid_gml_polygon_does_not_raise(value, loose, monkeypatch):
    if loose:
        monkeypatch.setattr(feedparser.api, "_XML_AVAILABLE", False)
    data = f"""<feed xmlns="http://www.w3.org/2005/Atom"
        xmlns:georss="http://www.georss.org/georss"
        xmlns:gml="http://www.opengis.net/gml">
        <entry><title>Preserved</title><georss:where><gml:Polygon>
        <gml:exterior><gml:LinearRing><gml:posList>{value}</gml:posList>
        </gml:LinearRing></gml:exterior></gml:Polygon></georss:where>
        </entry></feed>"""
    result = feedparser.parse(data)
    assert result.entries[0].title == "Preserved"
    assert "coordinates" not in result.entries[0].get("where", {})


def test_invalid_gml_polygon_minimized_input():
    result = feedparser.parse(
        b"<gml:Polygon<gml:LinearRing<gml:posList>.</gml:posList>"
    )
    assert result.bozo


def test_valid_polygon_poslist():
    assert _parse_poslist("1 2 3 4 5 6 1 2", "polygon") == {
        "type": "Polygon",
        "coordinates": ([(2.0, 1.0), (4.0, 3.0), (6.0, 5.0), (2.0, 1.0)],),
    }
