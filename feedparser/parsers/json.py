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
from ..util import FeedParserDict

JSON_VERSIONS = {
    "https://jsonfeed.org/version/1": "json1",
    "https://jsonfeed.org/version/1.1": "json11",
}


def coerce_scalar_id(value: bool | float | int | None) -> str:
    """Coerce an item identifier to a string if it's a scalar.

    The JSON feed specification states that non-string IDs must be coerced to strings.
    This function attempts to follow this bad advice.

    Objects and arrays (dicts and lists in Python) are ignored.
    """

    if isinstance(value, bool):
        return str(value).lower()
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
        # There's no way to return the original text as a string.
        if isinstance(value, float):
            return str(value)
    if isinstance(value, int):
        return str(value)

    return "null"


class JSONParser:
    def __init__(self, baseuri=None, baselang=None, encoding=None):
        self.baseuri = baseuri or ""
        self.lang = baselang or None
        self.encoding = encoding or "utf-8"  # character encoding
        self.sanitize_html = False

        self.version = None
        self.feeddata: FeedParserDict[str, typing.Any] = FeedParserDict()
        self.namespacesInUse = []
        self.entries = []

    def feed(self, file) -> None:
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
            self.feeddata["title"] = title
            self.feeddata["title_detail"] = FeedParserDict(
                value=title,
                type="text/plain",
            )

        # Handle `description`, if it exists.
        description = data.get("description")
        if isinstance(description, str):
            description = description.strip()
            self.feeddata["subtitle"] = description
            self.feeddata["subtitle_detail"] = FeedParserDict(
                value=description,
                type="text/plain",
            )

        # Handle `feed_url`, if it exists.
        feed_url = data.get("feed_url")
        if isinstance(feed_url, str):
            feed_url = feed_url.strip()
            # The feed URL is also...sigh...the feed ID.
            self.feeddata["id"] = feed_url
            link_data = FeedParserDict(
                href=feed_url,
                rel="self",
            )
            if "title" in self.feeddata:
                link_data["title"] = self.feeddata["title"]
            self.feeddata.setdefault("links", [])
            self.feeddata["links"].append(link_data)

        # Handle `home_page_url`, if it exists.
        home_page_url = data.get("home_page_url")
        if isinstance(home_page_url, str):
            home_page_url = home_page_url.strip()
            self.feeddata["link"] = home_page_url
            link_data = FeedParserDict(
                href=home_page_url,
                rel="alternate",
            )
            self.feeddata.setdefault("links", [])
            self.feeddata["links"].append(link_data)

        # Handle `icon`, if it exists.
        icon = data.get("icon")
        if isinstance(icon, str):
            self.feeddata["image"] = FeedParserDict(href=icon.strip())

        # Handle `favicon`, if it exists.
        favicon = data.get("favicon")
        if isinstance(favicon, str):
            self.feeddata["icon"] = favicon.strip()

        # Handle `user_comment`, if it exists.
        user_comment = data.get("user_comment")
        if isinstance(user_comment, str):
            user_comment = user_comment.strip()
            self.feeddata["info"] = user_comment
            self.feeddata["info_detail"] = FeedParserDict(
                value=user_comment,
                type="text/plain",
            )

        # Handle `next_url`, if it exists.
        next_url = data.get("next_url")
        if isinstance(next_url, str):
            next_url = next_url.strip()
            link_data = FeedParserDict(
                href=next_url,
                rel="next",
            )
            self.feeddata.setdefault("links", [])
            self.feeddata["links"].append(link_data)

        # Handle `expired`, if it exists.
        expired = data.get("expired", ...)
        if expired is not ...:
            # The spec states that only boolean true means "expired".
            self.feeddata["expired"] = expired is True

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
                        FeedParserDict(
                            url=url.strip(),
                            type=type_.strip(),
                        )
                    )

        author_singular = data.get("author")
        if isinstance(author_singular, dict):
            parsed_author = self._parse_author(author_singular)
            if parsed_author:
                self.feeddata["authors"] = [parsed_author]
                # "or", instead of ".get(..., <default>)"
                self.feeddata["author"] = (
                    parsed_author.get("name")
                    or parsed_author.get("email")
                    or parsed_author.get("href")
                    or parsed_author.get["avatar"]
                )
                self.feeddata["author_detail"] = parsed_author

        items = data.get("items")
        if isinstance(items, list):
            for item in items:
                if not isinstance(item, dict):
                    continue
                entry = self._parse_entry(item)
                if entry:
                    self.entries.append(entry)

    def _parse_entry(
        self, item: dict[str, typing.Any]
    ) -> FeedParserDict[str, typing.Any]:
        entry = FeedParserDict()

        # Handle `id`, if it exists and is a scalar value.
        id_ = item.get("id")
        if isinstance(id_, str):
            entry["id"] = id_.strip()
        elif isinstance(id_, (bool, float, int)) or id_ is None:
            entry["id"] = coerce_scalar_id(id_)

        # Handle `title`, if it exists.
        title = item.get("title")
        if isinstance(title, str):
            title = title.strip()
            entry["title"] = title
            entry["title_detail"] = FeedParserDict(
                value=title,
                type="text/plain",
            )

        # Handle `url`, if it exists.
        url = item.get("url")
        if isinstance(url, str):
            url = url.strip()
            link_data = FeedParserDict(
                rel="self",
                href=url,
            )
            if "title" in entry:
                link_data["title"] = entry["title"]
            entry["link"] = url
            entry.setdefault("links", [])
            entry["links"].append(link_data)

        # Handle `external_url`, if it exists.
        external_url = item.get("external_url")
        if isinstance(external_url, str):
            external_url = external_url.strip()
            link_data = FeedParserDict(
                rel="related",
                href=external_url,
            )
            entry.setdefault("links", [])
            entry["links"].append(link_data)

        # Handle `content_text`, if it exists.
        content_text = item.get("content_text")
        if isinstance(content_text, str):
            content_text = content_text.strip()
            entry.setdefault("content", [])
            entry["content"].append(
                FeedParserDict(
                    value=content_text,
                    type="text/plain",
                )
            )

        # Handle `content_html`, if it exists.
        content_html = item.get("content_html")
        if isinstance(content_html, str):
            # JSON Feed fails to allow for content type declarations,
            # so it's impossible to know whether the content is HTML or XHTML.
            # "text/html" is chosen for lack of actual information.
            content_html = content_html.strip()
            content_type = "text/html"
            if self.sanitize_html:
                content_html = sanitize_html(content_html, self.encoding, content_type)
            entry.setdefault("content", [])
            entry["content"].append(
                FeedParserDict(
                    value=content_html,
                    type=content_type,
                )
            )

        # Handle `summary`, if it exists.
        summary = item.get("summary")
        if isinstance(summary, str):
            summary = summary.strip()
            entry["summary"] = summary
            entry["summary_detail"] = FeedParserDict(
                value=summary,
                type="text/plain",
            )

        # Handle `image`, if it exists.
        image = item.get("image")
        if isinstance(image, str):
            image = image.strip()
            entry.setdefault("images", [])
            entry["images"].append(
                FeedParserDict(
                    href=image,
                    role="main",
                )
            )

        # Handle `banner_image`, if it exists.
        banner_image = item.get("banner_image")
        if isinstance(banner_image, str):
            banner_image = banner_image.strip()
            entry.setdefault("images", [])
            entry["images"].append(
                FeedParserDict(
                    href=banner_image,
                    role="banner",
                )
            )

        # Handle `date_published`, if it exists.
        date_published = item.get("date_published")
        if isinstance(date_published, str):
            date_published = date_published.strip()
            entry["published"] = date_published
            entry["published_parsed"] = _parse_date(date_published)

        # Handle `date_modified`, if it exists.
        date_modified = item.get("date_modified")
        if isinstance(date_modified, str):
            date_modified = date_modified.strip()
            entry["updated"] = date_modified
            entry["updated_parsed"] = _parse_date(date_modified)

        # Handle `author`, if it exists.
        author_singular = item.get("author")
        if isinstance("author", dict):
            parsed_author = self._parse_author(author_singular)
            if parsed_author:
                entry["author"] = (
                    parsed_author.get("name")
                    or parsed_author.get("email")
                    or parsed_author.get("url")
                    or parsed_author["avatar"]
                )
                entry["author_detail"] = parsed_author

        # Handle `tags`, if it exists.
        tags = item.get("tags")
        if isinstance(tags, list):
            normalized_tags = self._parse_tags(tags)
            entry.setdefault("tags", [])
            entry["tags"].extend(normalized_tags)

        # Handle `attachments`, if it exists.
        attachments = item.get("attachments")
        if isinstance(attachments, list):
            parsed_attachments = self._parse_attachments(attachments)
            if parsed_attachments:
                entry["enclosures"] = parsed_attachments

        return entry

    @staticmethod
    def _parse_tags(tags: list[typing.Any]) -> list[FeedParserDict]:
        """Parse a list of tags, keeping only non-empty strings."""

        normalized_tags = []
        for tag in tags:
            if not isinstance(tag, str):
                continue
            tag = tag.strip()
            if not tag:
                continue
            normalized_tags.append(
                FeedParserDict(
                    label=tag,
                    term=tag,
                )
            )

        return normalized_tags

    @staticmethod
    def _parse_author(info: dict[str, str]) -> FeedParserDict[str, str]:
        parsed_author: FeedParserDict[str, str] = FeedParserDict()

        name = info.get("name")
        if isinstance(name, str):
            parsed_author["name"] = name.strip()

        url = info.get("url")
        if isinstance(url, str):
            url = url.strip()
            parsed_author["href"] = url
            # URLs can be email addresses.
            # However, the "mailto:" URI supports options like:
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
    def _parse_attachments(
        attachments: list[dict[str, typing.Any]]
    ) -> list[FeedParserDict[str, str | int | float]]:
        """Parse a list of attachments."""

        parsed_attachments = []
        for attachment in attachments:
            url = attachment.get("url")
            if not isinstance(url, str):
                continue
            url = url.strip()
            if not url:
                continue
            parsed_attachment = FeedParserDict(href=url)
            parsed_attachments.append(parsed_attachment)

            mime_type = attachment.get("mime_type")
            if isinstance(mime_type, str):
                mime_type = mime_type.strip()
                if mime_type:
                    parsed_attachment["type"] = mime_type

            size_in_bytes = attachment.get("size_in_bytes")
            if isinstance(size_in_bytes, int):
                parsed_attachment["length"] = size_in_bytes

            duration = attachment.get("duration_in_seconds")
            if isinstance(duration, (int, float)):
                parsed_attachment["duration"] = duration

        return parsed_attachments
