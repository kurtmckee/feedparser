# Copyright 2010-2025 Kurt McKee <contactme@kurtmckee.org>
# Copyright 2025 Tom Most <twm@freecog.net>
# Copyright 2002-2008 Mark Pilgrim
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

import re
import urllib.parse

from .html import BaseHTMLProcessor

# If you want feedparser to allow all URL schemes, set this to ()
# List culled from Python's urlparse documentation at:
#   http://docs.python.org/library/urlparse.html
# as well as from "URI scheme" at Wikipedia:
#   https://secure.wikimedia.org/wikipedia/en/wiki/URI_scheme
# Many more will likely need to be added!
ACCEPTABLE_URI_SCHEMES = (
    "file",
    "ftp",
    "gopher",
    "h323",
    "hdl",
    "http",
    "https",
    "imap",
    "magnet",
    "mailto",
    "mms",
    "news",
    "nntp",
    "prospero",
    "rsync",
    "rtsp",
    "rtspu",
    "sftp",
    "shttp",
    "sip",
    "sips",
    "snews",
    "svn",
    "svn+ssh",
    "telnet",
    "wais",
    # Additional common-but-unofficial schemes
    "aim",
    "callto",
    "cvs",
    "facetime",
    "feed",
    "git",
    "gtalk",
    "irc",
    "ircs",
    "irc6",
    "itms",
    "mms",
    "msnim",
    "skype",
    "ssh",
    "smb",
    "svn",
    "ymsg",
)

_urifixer = re.compile("^([A-Za-z][A-Za-z0-9+-.]*://)(/*)(.*?)")


def _urljoin(base, uri):
    uri = _urifixer.sub(r"\1\3", uri)
    try:
        uri = urllib.parse.urljoin(base, uri)
    except ValueError:
        uri = ""
    return uri


def make_safe_absolute_uri(base, rel=None):
    # bail if ACCEPTABLE_URI_SCHEMES is empty
    if not ACCEPTABLE_URI_SCHEMES:
        return _urljoin(base, rel or "")
    if not base:
        return rel or ""
    if not rel:
        try:
            scheme = urllib.parse.urlparse(base)[0]
        except ValueError:
            return ""
        if not scheme or scheme in ACCEPTABLE_URI_SCHEMES:
            return base
        return ""
    uri = _urljoin(base, rel)
    if uri.strip().split(":", 1)[0] not in ACCEPTABLE_URI_SCHEMES:
        return ""
    return uri


# Matches image candidate strings within a srcset attribute value as
# described in https://html.spec.whatwg.org/multipage/images.html#srcset-attributes
_srcset_candidate = re.compile(
    r"""
    # ASCII whitespace: https://infra.spec.whatwg.org/#ascii-whitespace
    [\t\n\f\r ]*
    (
        # URL that doesn't start or end with a comma
        (?!,)
        [^\t\n\f\r ]+
        (?<!,)
    )
    (
        # Width descriptor like "1234w"
        # https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#non-negative-integers
        [\t\n\f\r ]+
        \d+w
        |
        # Pixel density descriptor like "2.0x"
        # https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#valid-floating-point-number
        [\t\n\f\r ]+
        \d+(?:\.\d+)?(?:[eE][-+]?\d+)?x
        |
    )
    [\t\n\f\r ]*
    (?:,|\Z)
    """,
    re.VERBOSE | re.ASCII,
)


def srcset_candidates(value: str) -> list[tuple[str, str]]:
    """
    Split a ``srcset`` attribute value into candidates:

    >>> srcset_candidates("/foo.jpg, /foo.2x.jpg 2x")
    [("/foo.jpg", ""), ("/foo.2x.jpg", "2x")]

    This doesn't validate the URLs, nor check for duplicate or conflicting
    descriptors. It returns an empty list when parsing fails.
    """
    pos = 0
    candidates = []
    while m := _srcset_candidate.match(value, pos):
        desc = m[2].strip("\t\n\f\r ")
        candidates.append((m[1], desc))
        pos = m.end(0)
    return candidates


class RelativeURIResolver(BaseHTMLProcessor):
    relative_uris = {
        ("a", "href"),
        ("applet", "codebase"),
        ("area", "href"),
        ("audio", "src"),
        ("blockquote", "cite"),
        ("body", "background"),
        ("del", "cite"),
        ("form", "action"),
        ("frame", "longdesc"),
        ("frame", "src"),
        ("iframe", "longdesc"),
        ("iframe", "src"),
        ("head", "profile"),
        ("img", "longdesc"),
        ("img", "src"),
        ("img", "usemap"),
        ("input", "src"),
        ("input", "usemap"),
        ("ins", "cite"),
        ("link", "href"),
        ("object", "classid"),
        ("object", "codebase"),
        ("object", "data"),
        ("object", "usemap"),
        ("q", "cite"),
        ("script", "src"),
        ("source", "src"),
        ("video", "poster"),
        ("video", "src"),
    }

    def __init__(self, baseuri, encoding, _type):
        BaseHTMLProcessor.__init__(self, encoding, _type)
        self.baseuri = baseuri

    def resolve_uri(self, uri):
        return make_safe_absolute_uri(self.baseuri, uri.strip())

    def resolve_srcset(self, srcset):
        candidates = []
        for uri, desc in srcset_candidates(srcset):
            uri = self.resolve_uri(uri)
            if desc:
                candidates.append(f"{uri} {desc}")
            else:
                candidates.append(uri)
        return ", ".join(candidates)

    def unknown_starttag(self, tag, attrs):
        attrs = self.normalize_attrs(attrs)
        for i, (key, value) in enumerate(attrs):
            if (tag, key) in self.relative_uris:
                attrs[i] = (key, self.resolve_uri(value))
            elif tag in {"img", "source"} and key == "srcset":
                attrs[i] = (key, self.resolve_srcset(value))
        super().unknown_starttag(tag, attrs)


def resolve_relative_uris(html_source, base_uri, encoding, type_):
    p = RelativeURIResolver(base_uri, encoding, type_)
    p.feed(html_source)
    return p.output()
