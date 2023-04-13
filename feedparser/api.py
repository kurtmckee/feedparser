# The public API for feedparser
# Copyright 2010-2023 Kurt McKee <contactme@kurtmckee.org>
# Copyright 2002-2008 Mark Pilgrim
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

import io
import urllib.error
import urllib.parse
import xml.sax
from typing import IO, Dict, Optional, Union

from . import http
from .encodings import MissingEncoding, convert_file_to_utf8
from .html import BaseHTMLProcessor
from .mixin import XMLParserMixin
from .parsers.json import JSONParser
from .parsers.loose import LooseXMLParser
from .parsers.strict import StrictXMLParser
from .sanitizer import replace_doctype
from .urls import make_safe_absolute_uri
from .util import FeedParserDict

# List of preferred XML parsers, by SAX driver name.  These will be tried first,
# but if they're not installed, Python will keep searching through its own list
# of pre-installed parsers until it finds one that supports everything we need.
PREFERRED_XML_PARSERS = ["drv_libxml2"]

_XML_AVAILABLE = True

SUPPORTED_VERSIONS = {
    "": "unknown",
    "rss090": "RSS 0.90",
    "rss091n": "RSS 0.91 (Netscape)",
    "rss091u": "RSS 0.91 (Userland)",
    "rss092": "RSS 0.92",
    "rss093": "RSS 0.93",
    "rss094": "RSS 0.94",
    "rss20": "RSS 2.0",
    "rss10": "RSS 1.0",
    "rss": "RSS (unknown version)",
    "atom01": "Atom 0.1",
    "atom02": "Atom 0.2",
    "atom03": "Atom 0.3",
    "atom10": "Atom 1.0",
    "atom": "Atom (unknown version)",
    "cdf": "CDF",
    "json1": "JSON feed 1",
}


def _open_resource(
    url_file_stream_or_string,
    result,
):
    """URL, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.

    :return: A seekable, readable file object.
    """

    # Some notes on the history of the implementation of _open_resource().
    #
    # parse() might need to go over the feed content twice:
    # if the strict parser fails, it tries again with the loose parser.
    #
    # In 5.2.0, this returned an open file, to be read() by parse().
    # By 6.0.8, this returned bytes directly.
    #
    # Since #296 (>6.0.8), this once again returns an open file
    # (to reduce memory usage, see convert_file_to_utf8() for details).
    # However, to accommodate parse() needing the content twice,
    # the returned file is guaranteed to be seekable.
    # (If the underlying resource is not seekable,
    # the content is read and wrapped in a io.BytesIO/StringIO.)

    if callable(getattr(url_file_stream_or_string, "read", None)):
        if callable(getattr(url_file_stream_or_string, "seekable", None)):
            if url_file_stream_or_string.seekable():
                return url_file_stream_or_string
        return _to_in_memory_file(url_file_stream_or_string.read())

    looks_like_url = isinstance(
        url_file_stream_or_string, str
    ) and urllib.parse.urlparse(url_file_stream_or_string)[0] in (
        "http",
        "https",
    )
    if looks_like_url:
        data = http.get(url_file_stream_or_string, result)
        return io.BytesIO(data)

    # try to open with native open function (if url_file_stream_or_string is a filename)
    try:
        return open(url_file_stream_or_string, "rb")
    except (OSError, TypeError, ValueError):
        # if url_file_stream_or_string is a str object that
        # cannot be converted to the encoding returned by
        # sys.getfilesystemencoding(), a UnicodeEncodeError
        # will be thrown
        # If url_file_stream_or_string is a string that contains NULL
        # (such as an XML document encoded in UTF-32), TypeError will
        # be thrown.
        pass

    # treat url_file_stream_or_string as bytes/string
    return _to_in_memory_file(url_file_stream_or_string)


def _to_in_memory_file(data):
    if isinstance(data, str):
        return io.StringIO(data)
    else:
        return io.BytesIO(data)


class LooseFeedParser(LooseXMLParser, XMLParserMixin, BaseHTMLProcessor):
    pass


class StrictFeedParser(StrictXMLParser, XMLParserMixin, xml.sax.handler.ContentHandler):
    pass


def parse(
    url_file_stream_or_string,
    response_headers: Optional[Dict[str, str]] = None,
    resolve_relative_uris: Optional[bool] = None,
    sanitize_html: Optional[bool] = None,
    optimistic_encoding_detection: Optional[bool] = None,
) -> FeedParserDict:
    """Parse a feed from a URL, file, stream, or string.

    :param url_file_stream_or_string:
        File-like object, URL, file path, or string. Both byte and text strings
        are accepted. If necessary, encoding will be derived from the response
        headers or automatically detected.

        Note that strings may trigger network I/O or filesystem access
        depending on the value. Wrap an untrusted string in
        a :class:`io.StringIO` or :class:`io.BytesIO` to avoid this. Do not
        pass untrusted strings to this function.

        When a URL is not passed the feed location to use in relative URL
        resolution should be passed in the ``Content-Location`` response header
        (see ``response_headers`` below).
    :param response_headers:
        A mapping of HTTP header name to HTTP header value. Multiple values may
        be joined with a comma. If a HTTP request was made, these headers
        override any matching headers in the response. Otherwise this specifies
        the entirety of the response headers.
    :param resolve_relative_uris:
        Should feedparser attempt to resolve relative URIs absolute ones within
        HTML content?  Defaults to the value of
        :data:`feedparser.RESOLVE_RELATIVE_URIS`, which is ``True``.
    :param sanitize_html:
        Should feedparser skip HTML sanitization? Only disable this if you know
        what you are doing!  Defaults to the value of
        :data:`feedparser.SANITIZE_HTML`, which is ``True``.
    :param optimistic_encoding_detection:
        Should feedparser use only a prefix of the feed to detect encodings
        (uses less memory, but the wrong encoding may be detected in rare cases).
        Defaults to the value of
        :data:`feedparser.OPTIMISTIC_ENCODING_DETECTION`, which is ``True``.

    """

    result = FeedParserDict(
        bozo=False,
        entries=[],
        feed=FeedParserDict(),
        headers={},
    )

    try:
        file = _open_resource(
            url_file_stream_or_string,
            result,
        )
    except urllib.error.URLError as error:
        result.update(
            {
                "bozo": True,
                "bozo_exception": error,
            }
        )
        return result

    # at this point, the file is guaranteed to be seekable;
    # we read 1 byte/character to see if it's empty and return early
    # (this preserves the behavior in 6.0.8)
    initial_file_offset = file.tell()
    if not file.read(1):
        return result
    file.seek(initial_file_offset)

    # overwrite existing headers using response_headers
    result["headers"].update(response_headers or {})

    try:
        _parse_file_inplace(
            file,
            result,
            resolve_relative_uris=resolve_relative_uris,
            sanitize_html=sanitize_html,
            optimistic_encoding_detection=optimistic_encoding_detection,
        )
    finally:
        if not hasattr(url_file_stream_or_string, "read"):
            # the file does not come from the user, close it
            file.close()

    return result


def _parse_file_inplace(
    file: Union[IO[bytes], IO[str]],
    result: dict,
    *,
    resolve_relative_uris: Optional[bool] = None,
    sanitize_html: Optional[bool] = None,
    optimistic_encoding_detection: Optional[bool] = None,
) -> None:
    # Avoid a cyclic import.
    import feedparser

    if sanitize_html is None:
        sanitize_html = bool(feedparser.SANITIZE_HTML)
    if resolve_relative_uris is None:
        resolve_relative_uris = bool(feedparser.RESOLVE_RELATIVE_URIS)
    if optimistic_encoding_detection is None:
        optimistic_encoding_detection = bool(feedparser.OPTIMISTIC_ENCODING_DETECTION)

    stream_factory = convert_file_to_utf8(
        result["headers"], file, result, optimistic_encoding_detection
    )
    # We're done with file, all access must happen through stream_factory.
    del file

    # Some notes about the stream_factory.get_{text,binary}_file() methods:
    #
    # Calling them a second time will raise io.UnsupportedOperation
    # if the underlying file was not seekable.
    #
    # Calling close() on the returned file is ignored
    # (that is, the underlying file is *not* closed),
    # because the SAX parser closes the file when done;
    # we don't want that, since we might try again with the loose parser.

    use_json_parser = False
    if result["content-type"] in {"application/json", "application/feed+json"}:
        use_json_parser = True
    use_strict_parser = bool(result["encoding"])

    result["version"], stream_factory.prefix, entities = replace_doctype(
        stream_factory.prefix
    )

    # Ensure that baseuri is an absolute URI using an acceptable URI scheme.
    contentloc = result["headers"].get("content-location", "")
    href = result.get("href", "")
    baseuri = (
        make_safe_absolute_uri(href, contentloc)
        or make_safe_absolute_uri(contentloc)
        or href
    )

    baselang = result["headers"].get("content-language", None)
    if isinstance(baselang, bytes) and baselang is not None:
        baselang = baselang.decode("utf-8", "ignore")

    if not _XML_AVAILABLE:
        use_strict_parser = False

    feed_parser: Union[JSONParser, StrictFeedParser, LooseFeedParser]

    if use_strict_parser and not use_json_parser:
        # Initialize the SAX parser.
        feed_parser = StrictFeedParser(baseuri, baselang, "utf-8")
        feed_parser.resolve_relative_uris = resolve_relative_uris
        feed_parser.sanitize_html = sanitize_html
        saxparser = xml.sax.make_parser(PREFERRED_XML_PARSERS)
        saxparser.setFeature(xml.sax.handler.feature_namespaces, 1)
        try:
            # Disable downloading external doctype references, if possible.
            saxparser.setFeature(xml.sax.handler.feature_external_ges, 0)
        except xml.sax.SAXNotSupportedException:
            pass
        saxparser.setContentHandler(feed_parser)
        saxparser.setErrorHandler(feed_parser)
        source = xml.sax.xmlreader.InputSource()

        # If an encoding was detected, decode the file on the fly;
        # otherwise, pass it as-is and let the SAX parser deal with it.
        try:
            source.setCharacterStream(stream_factory.get_text_file())
        except MissingEncoding:
            source.setByteStream(stream_factory.get_binary_file())

        try:
            saxparser.parse(source)
        except xml.sax.SAXException as e:
            result["bozo"] = 1
            result["bozo_exception"] = feed_parser.exc or e
            use_strict_parser = False

    # The loose XML parser will be tried if the strict XML parser was not used
    # (or if it failed to parse the feed).
    if not use_strict_parser and not use_json_parser:
        feed_parser = LooseFeedParser(baseuri, baselang, "utf-8", entities)
        feed_parser.resolve_relative_uris = resolve_relative_uris
        feed_parser.sanitize_html = sanitize_html

        # If an encoding was detected, use it; otherwise, assume utf-8 and do your best.
        # Will raise io.UnsupportedOperation if the underlying file is not seekable.
        data = stream_factory.get_text_file("utf-8", "replace").read()

        # As of 6.0.8, LooseFeedParser.feed() can be called exactly once
        # with the entire data (it does some re.sub() and str.replace() on it).
        #
        # SGMLParser (of which LooseFeedParser is a subclass)
        # *can* be fed in a streaming fashion,
        # by calling feed() repeatedly with chunks of text.
        #
        # When/if LooseFeedParser will support being fed chunks,
        # replace the read() call above with read(size)/feed() calls in a loop.

        feed_parser.feed(data)

        # If parsing with the loose XML parser resulted in no information,
        # flag that the JSON parser should be tried.
        if not (feed_parser.entries or feed_parser.feeddata or feed_parser.version):
            use_json_parser = True

    if use_json_parser:
        result["version"] = None
        feed_parser = JSONParser(baseuri, baselang, "utf-8")
        try:
            feed_parser.feed(stream_factory.get_file())
        except Exception as e:
            result["bozo"] = 1
            result["bozo_exception"] = e

    result["feed"] = feed_parser.feeddata
    result["entries"] = feed_parser.entries
    result["version"] = result["version"] or feed_parser.version
    if isinstance(feed_parser, JSONParser):
        result["namespaces"] = {}
    else:
        result["namespaces"] = feed_parser.namespaces_in_use
