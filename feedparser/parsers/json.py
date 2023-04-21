# The JSON feed parser
# Copyright 2017 Beat Bolli
# All rights reserved.
#
# This file is a part of feedparser.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
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

from __future__ import annotations

import json
import typing

from ..datetimes import _parse_date
from ..sanitizer import sanitize_html
from ..util import FeedParserDict, looks_like_html

JSON_VERSIONS = {
    "https://jsonfeed.org/version/1": "json1",
    "https://jsonfeed.org/version/1.1": "json11",
}


def coerce_scalar(value: int | float | bool | None) -> str | None:
    """Coerce an item identifier to a string if it's a scalar.

    The JSON feed specification states that non-string IDs must be coerced to strings.
    This function attempts to follow this bad advice.

    Objects and arrays (dicts and lists in Python) are ignored.
    """

    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if str(value) == "nan":
            return "NaN"
        if str(value) == "inf":
            return "Infinity"
        if str(value) == "-inf":
            return "-Infinity"
        # Ideally, the original presentation in-JSON could be returned as a string.
        # However, floats are an imperfect data type.
        # For example, `1.0e2` in JSON is `100.0` in Python,
        # and `1.9999999999999999e2` in JSON is `200.0` in Python.
        # There's no way to return the original interpretation as a string.
        if isinstance(value, float):
            return str(value)
    return None


class JSONParser:
    ITEM_FIELDS = (
        ("title", "title"),
        ("url", "link"),
        ("summary", "summary"),
        ("external_url", "source"),
    )

    def __init__(self, baseuri=None, baselang=None, encoding=None):
        self.baseuri = baseuri or ""
        self.lang = baselang or None
        self.encoding = encoding or "utf-8"  # character encoding
        self.sanitize_html = False

        self.version = None
        self.feeddata = FeedParserDict()
        self.namespacesInUse = []
        self.entries = []

    def feed(self, file):
        data = json.load(file)

        # If the file parses as JSON, assume it's a JSON feed.
        self.version = "json"
        try:
            self.version = JSON_VERSIONS[data["version"].strip()]
        except (AttributeError, KeyError, TypeError):
            pass

        # Handle `title`, if it exists.
        title = data.get("title")
        if isinstance(title, str):
            title = title.strip()
            is_html = looks_like_html(title)
            content_type = "text/html" if is_html else "text/plain"
            if is_html and self.sanitize_html:
                title = sanitize_html(title, encoding=None, _type=content_type)
            self.feeddata["title"] = title
            self.feeddata["title_detail"] = {
                "value": title,
                "type": content_type,
            }

        # Handle `description`, if it exists.
        description = data.get("description")
        if isinstance(description, str):
            description = description.strip()
            is_html = looks_like_html(description)
            content_type = "text/html" if is_html else "text/plain"
            if is_html and self.sanitize_html:
                description = sanitize_html(
                    description, encoding=None, _type=content_type
                )
            self.feeddata["subtitle"] = description
            self.feeddata["subtitle_detail"] = {
                "value": description,
                "type": content_type,
            }

        # Handle `feed_url`, if it exists.
        feed_url = data.get("feed_url")
        if isinstance(feed_url, str):
            feed_url = feed_url.strip()
            # The feed URL is also...sigh...the feed ID.
            self.feeddata["id"] = feed_url
            self.feeddata.setdefault("links", []).append(
                {
                    "href": feed_url,
                    "rel": "self",
                }
            )
            if "title" in self.feeddata:
                self.feeddata["links"][-1]["title"] = self.feeddata["title"]

        # Handle `home_page_url`, if it exists.
        home_page_url = data.get("home_page_url")
        if isinstance(home_page_url, str):
            home_page_url = home_page_url.strip()
            self.feeddata["link"] = home_page_url
            self.feeddata.setdefault("links", []).append(
                {
                    "href": home_page_url,
                    "rel": "alternate",
                }
            )

        # Handle `icon`, if it exists.
        icon = data.get("icon")
        if isinstance(icon, str):
            self.feeddata["image"] = {"href": icon.strip()}

        # Handle `favicon`, if it exists.
        favicon = data.get("favicon")
        if isinstance(favicon, str):
            self.feeddata["icon"] = favicon.strip()

        # Handle `user_comment`, if it exists.
        user_comment = data.get("user_comment")
        if isinstance(user_comment, str):
            user_comment = user_comment.strip()
            is_html = looks_like_html(user_comment)
            content_type = "text/html" if is_html else "text/plain"
            if is_html and self.sanitize_html:
                user_comment = sanitize_html(
                    user_comment, encoding=None, _type=content_type
                )
            self.feeddata["info"] = user_comment
            self.feeddata["info_detail"] = {
                "value": user_comment,
                "type": content_type,
            }

        # Handle `next_url`, if it exists.
        next_url = data.get("next_url")
        if isinstance(next_url, str):
            next_url = next_url.strip()
            self.feeddata.setdefault("links", []).append(
                {
                    "href": next_url,
                    "rel": "next",
                }
            )

        # Handle `expired`, if it exists.
        expired = data.get("expired", ...)
        if expired is not ...:
            # The spec claims that only boolean true means "finished".
            self.feeddata["complete"] = expired is True

        # Handle `hubs`, if it exists.
        hubs = data.get("hubs", ...)
        if hubs is not ...:
            self.feeddata["hubs"] = []
            if isinstance(hubs, list):
                for hub in hubs:
                    if not isinstance(hub, dict):
                        continue
                    url = hub.get("url")
                    type_ = hub.get("type")
                    if not (isinstance(url, str) and isinstance(type_, str)):
                        continue
                    self.feeddata["hubs"].append(
                        {
                            "url": url.strip(),
                            "type": type_.strip(),
                        }
                    )

        author_singular = data.get("author")
        if isinstance(author_singular, dict):
            parsed_author = self._parse_author(author_singular)
            if parsed_author:
                self.feeddata["authors"] = [parsed_author]
                self.feeddata["author_detail"] = parsed_author
                if "name" in parsed_author:
                    self.feeddata["author"] = parsed_author["name"]

        items = data.get("items")
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    entry = self.parse_entry(item)
                    if entry:
                        self.entries.append(entry)

    def parse_entry(self, item: dict[str, typing.Any]) -> dict[str, str]:
        entry = FeedParserDict()

        # Handle `id`, if it exists.
        id_ = item.get("id")
        if isinstance(id_, str):
            entry["id"] = id_.strip()
        elif isinstance(id_, (int, float, bool, bool)) or id_ is None:
            entry["id"] = coerce_scalar(id_)

        for src, dst in self.ITEM_FIELDS:
            if src in item:
                entry[dst] = item[src]

        if "content_text" in item:
            entry["content"] = c = FeedParserDict()
            c["value"] = item["content_text"]
            c["type"] = "text"
        elif "content_html" in item:
            entry["content"] = c = FeedParserDict()
            c["value"] = sanitize_html(
                item["content_html"], self.encoding, "application/json"
            )
            c["type"] = "html"

        if "date_published" in item:
            entry["published"] = item["date_published"]
            entry["published_parsed"] = _parse_date(item["date_published"])
        if "date_updated" in item:
            entry["updated"] = item["date_modified"]
            entry["updated_parsed"] = _parse_date(item["date_modified"])

        if "tags" in item:
            entry["category"] = item["tags"]

        if "author" in item:
            self._parse_author(item["author"])

        if "attachments" in item:
            entry["enclosures"] = [
                self.parse_attachment(a) for a in item["attachments"]
            ]

        return entry

    @staticmethod
    def _parse_author(info: dict[str, str]) -> dict[str, str]:
        parsed_author: dict[str, str] = {}

        name = info.get("name")
        if isinstance(name, str):
            parsed_author["name"] = name.strip()

        url = info.get("url")
        if isinstance(url, str):
            url = url.strip()
            parsed_author["href"] = url
            # URLs can be email addresses.
            # However, only a "mailto:" URI supports options like:
            #
            #   mailto:user@domain.example?subject=Feed
            #
            # Caution is required when converting the URL to an email.
            if url.startswith("mailto:"):
                parsed_author["email"], _, _ = url[7:].partition("?")

        avatar = info.get("avatar")
        if isinstance(avatar, str):
            parsed_author["image"] = avatar.strip()

        return parsed_author

    @staticmethod
    def parse_attachment(attachment):
        enc = FeedParserDict()
        enc["href"] = attachment["url"]
        enc["type"] = attachment["mime_type"]
        if "size_in_bytes" in attachment:
            enc["length"] = attachment["size_in_bytes"]
        return enc
