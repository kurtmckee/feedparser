import pytest

from feedparser.urls import srcset_candidates


def test_empty():
    assert srcset_candidates("") == []
    assert srcset_candidates("    \n") == []


def test_default():
    assert srcset_candidates("/1x.jpg") == [("/1x.jpg", "")]


def test_pixel_density_descriptor_one():
    assert srcset_candidates("/1x.jpg 1x") == [("/1x.jpg", "1x")]


def test_pixel_density_descriptor_two():
    assert srcset_candidates("/1x.jpg 1x,/2x.jpg\t2.0x") == [
        ("/1x.jpg", "1x"),
        ("/2x.jpg", "2.0x"),
    ]


def test_pixel_density_descriptor_three():
    assert srcset_candidates("/1x.jpg, /2x.jpg  2x  , /3x.jpg 3x  ") == [
        ("/1x.jpg", ""),
        ("/2x.jpg", "2x"),
        ("/3x.jpg", "3x"),
    ]


@pytest.mark.parametrize(
    "pd", ["1x", "1.0x", "9.5x", "36x", "39.95x", "100x", "1e1x", "2E2x"]
)
def test_pixel_density_descriptor_floats(pd):
    """A pixel density descriptor allows all the valid float formats."""
    assert [("/foo.jpg", pd)] == srcset_candidates("/foo.jpg " + pd)


def test_url_comma():
    """A URL containing a comma is not broken."""
    assert srcset_candidates(" /,.jpg 6x,\n /,,,,.webp \t1e100x") == [
        ("/,.jpg", "6x"),
        ("/,,,,.webp", "1e100x"),
    ]


def test_width_one():
    assert srcset_candidates("/a.png 600w") == [("/a.png", "600w")]


def test_width_two():
    assert srcset_candidates("a.jpg 123w, b.jpg 1234w") == [
        ("a.jpg", "123w"),
        ("b.jpg", "1234w"),
    ]


@pytest.mark.parametrize("pd", ["1.5w", "9000X", "-23w", "-60x"])
def test_invalid(pd):
    assert srcset_candidates("/x.gif " + pd) == []
