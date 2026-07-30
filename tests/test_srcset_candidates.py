# Copyright 2025 Tom Most <twm@freecog.net>
# All rights reserved.
#
# This file is a part of feedparser.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
