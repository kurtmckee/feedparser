# Copyright 2010-2025 Kurt McKee <contactme@kurtmckee.org>
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

import html.entities
import re
import warnings

from .sanitizer import HTMLSanitizer


class FeedParserDict(dict):
    keymap = {
        "channel": "feed",
        "items": "entries",
        "guid": "id",
        "date": "updated",
        "date_parsed": "updated_parsed",
        "description": ["summary", "subtitle"],
        "description_detail": ["summary_detail", "subtitle_detail"],
        "url": ["href"],
        "modified": "updated",
        "modified_parsed": "updated_parsed",
        "issued": "published",
        "issued_parsed": "published_parsed",
        "copyright": "rights",
        "copyright_detail": "rights_detail",
        "tagline": "subtitle",
        "tagline_detail": "subtitle_detail",
    }

    def __getitem__(self, key, _stacklevel=2):
        """
        :return: A :class:`FeedParserDict`.
        """

        if key == "category":
            try:
                return dict.__getitem__(self, "tags")[0]["term"]
            except IndexError:
                raise KeyError("object doesn't have key 'category'")
        elif key == "enclosures":
            return [
                FeedParserDict(
                    [(name, value) for (name, value) in link.items() if name != "rel"]
                )
                for link in dict.__getitem__(self, "links")
                if link["rel"] == "enclosure"
            ]
        elif key == "license":
            for link in dict.__getitem__(self, "links"):
                if link["rel"] == "license" and "href" in link:
                    return link["href"]
        elif key == "updated":
            # Temporarily help developers out by keeping the old
            # broken behavior that was reported in issue 310.
            # This fix was proposed in issue 328.
            if not dict.__contains__(self, "updated") and dict.__contains__(
                self, "published"
            ):
                warnings.warn(
                    "To avoid breaking existing software while "
                    "fixing issue 310, a temporary mapping has been created "
                    "from `updated` to `published` if `updated` doesn't "
                    "exist. This fallback will be removed in a future version "
                    "of feedparser.",
                    DeprecationWarning,
                    stacklevel=_stacklevel,
                )
                return dict.__getitem__(self, "published")
            return dict.__getitem__(self, "updated")
        elif key == "updated_parsed":
            if not dict.__contains__(self, "updated_parsed") and dict.__contains__(
                self, "published_parsed"
            ):
                warnings.warn(
                    "To avoid breaking existing software while "
                    "fixing issue 310, a temporary mapping has been created "
                    "from `updated_parsed` to `published_parsed` if "
                    "`updated_parsed` doesn't exist. This fallback will be "
                    "removed in a future version of feedparser.",
                    DeprecationWarning,
                    stacklevel=_stacklevel,
                )
                return dict.__getitem__(self, "published_parsed")
            return dict.__getitem__(self, "updated_parsed")
        else:
            realkey = self.keymap.get(key, key)
            if isinstance(realkey, list):
                for k in realkey:
                    if dict.__contains__(self, k):
                        return dict.__getitem__(self, k)
            elif dict.__contains__(self, realkey):
                return dict.__getitem__(self, realkey)
        return dict.__getitem__(self, key)

    def __contains__(self, key):
        if key in ("updated", "updated_parsed"):
            # Temporarily help developers out by keeping the old
            # broken behavior that was reported in issue 310.
            # This fix was proposed in issue 328.
            return dict.__contains__(self, key)
        try:
            self.__getitem__(key, _stacklevel=3)
        except KeyError:
            return False
        return True

    has_key = __contains__

    def get(self, key, default=None):
        """
        :return: A :class:`FeedParserDict`.
        """

        try:
            return self.__getitem__(key, _stacklevel=3)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        key = self.keymap.get(key, key)
        if isinstance(key, list):
            key = key[0]
        return dict.__setitem__(self, key, value)

    def __getattr__(self, key):
        # __getattribute__() is called first; this will be called
        # only if an attribute was not already found
        try:
            return self.__getitem__(key, _stacklevel=3)
        except KeyError:
            raise AttributeError("object has no attribute '%s'" % key)

    def __hash__(self):
        # This is incorrect behavior -- dictionaries shouldn't be hashable.
        # Note to self: remove this behavior in the future.
        return id(self)


def looks_like_html(content: str) -> bool:
    """Guess whether some text looks like HTML.

    A number of elements in several XML specifications are nominally plain text,
    but feed authors and generators may ignore the specifications they're using.

    In addition, the JSON feed spec fails to document some values' content types,
    which means that titles and descriptions might -- or might not -- be HTML.

    This function attempts to guess whether content looks like HTML
    or should be rendered as plain text in an HTML context.

    As false positives can result in silent data loss,
    this function errs on the side of caution.
    """

    # If the content doesn't have closing tags or entity references, it's just text.
    if not (re.search(r"</(\w+)>", content) or re.search(r"&#?\w+;", content)):
        return False

    # If any tags are found that are not considered safe for rendering, it's just text.
    # For example, a title like "It's time to </blink>" should be treated as text.
    # In effect, it should be escaped when rendered in an HTML context,
    # and this is suggested by treating the text as 'text/plain'.
    if not all(
        tag.lower() in HTMLSanitizer.acceptable_elements
        for tag in re.findall(r"</?(\w+)", content)
    ):
        return False

    # If any entities references are undefined, it's just text.
    # For example, a title like "U&IRGR8;)" should be treated as text.
    # In effect, it should be escaped when rendered in an HTML context,
    # and this is suggested by treating the text as 'text/plain'.
    if not all(
        entity in html.entities.entitydefs for entity in re.findall(r"&(\w+);", content)
    ):
        return False

    return True
