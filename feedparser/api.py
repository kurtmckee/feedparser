# The public API for feedparser
# Copyright 2010-2015 Kurt McKee <contactme@kurtmckee.org>
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

from __future__ import absolute_import, unicode_literals

import xml.sax

try:
    from io import BytesIO as _StringIO
except ImportError:
    try:
        from cStringIO import StringIO as _StringIO
    except ImportError:
        from StringIO import StringIO as _StringIO

try:
    import urllib.parse
except ImportError:
    from urlparse import urlparse

    class urllib(object):
        class parse(object):
            urlparse = staticmethod(urlparse)

from .datetimes import registerDateHandler, _parse_date
from .encodings import convert_to_utf8
from .exceptions import *
from .html import _BaseHTMLProcessor
from . import http
from . import mixin
from .mixin import _FeedParserMixin
from .parsers.loose import _LooseFeedParser
from .parsers.strict import _StrictFeedParser
from .sanitizer import replace_doctype
from .sgml import *
from .urls import _convert_to_idn, _makeSafeAbsoluteURI
from .util import FeedParserDict

bytes_ = type(b'')
unicode_ = type('')
try:
    unichr
    basestring
except NameError:
    unichr = chr
    basestring = str

# List of preferred XML parsers, by SAX driver name.  These will be tried first,
# but if they're not installed, Python will keep searching through its own list
# of pre-installed parsers until it finds one that supports everything we need.
PREFERRED_XML_PARSERS = ["drv_libxml2"]

# If you want feedparser to automatically resolve all relative URIs, set this
# to 1.
RESOLVE_RELATIVE_URIS = 1

# If you want feedparser to automatically sanitize all potentially unsafe
# HTML content, set this to 1.
SANITIZE_HTML = 1

_XML_AVAILABLE = True
mixin.RESOLVE_RELATIVE_URIS = RESOLVE_RELATIVE_URIS
mixin.SANITIZE_HTML = SANITIZE_HTML

SUPPORTED_VERSIONS = {
    '': 'unknown',
    'rss090': 'RSS 0.90',
    'rss091n': 'RSS 0.91 (Netscape)',
    'rss091u': 'RSS 0.91 (Userland)',
    'rss092': 'RSS 0.92',
    'rss093': 'RSS 0.93',
    'rss094': 'RSS 0.94',
    'rss20': 'RSS 2.0',
    'rss10': 'RSS 1.0',
    'rss': 'RSS (unknown version)',
    'atom01': 'Atom 0.1',
    'atom02': 'Atom 0.2',
    'atom03': 'Atom 0.3',
    'atom10': 'Atom 1.0',
    'atom': 'Atom (unknown version)',
    'cdf': 'CDF',
}

def _open_resource(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers, result):
    """URL, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.

    If the etag argument is supplied, it will be used as the value of an
    If-None-Match request header.

    If the modified argument is supplied, it can be a tuple of 9 integers
    (as returned by gmtime() in the standard Python time module) or a date
    string in any format supported by feedparser. Regardless, it MUST
    be in GMT (Greenwich Mean Time). It will be reformatted into an
    RFC 1123-compliant date and used as the value of an If-Modified-Since
    request header.

    If the agent argument is supplied, it will be used as the value of a
    User-Agent request header.

    If the referrer argument is supplied, it will be used as the value of a
    Referer[sic] request header.

    If handlers is supplied, it is a list of handlers used to build a
    urllib2 opener.

    if request_headers is supplied it is a dictionary of HTTP request headers
    that will override the values generated by FeedParser.

    :return: A :class:`StringIO.StringIO` or :class:`io.BytesIO`.
    """

    if hasattr(url_file_stream_or_string, 'read'):
        return url_file_stream_or_string.read()

    if isinstance(url_file_stream_or_string, basestring) \
       and urllib.parse.urlparse(url_file_stream_or_string)[0] in ('http', 'https', 'ftp', 'file', 'feed'):
        return http.get(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers, result)

    # try to open with native open function (if url_file_stream_or_string is a filename)
    try:
        with open(url_file_stream_or_string, 'rb') as f:
            data = f.read()
    except (IOError, UnicodeEncodeError, TypeError):
        # if url_file_stream_or_string is a unicode object that
        # cannot be converted to the encoding returned by
        # sys.getfilesystemencoding(), a UnicodeEncodeError
        # will be thrown
        # If url_file_stream_or_string is a string that contains NULL
        # (such as an XML document encoded in UTF-32), TypeError will
        # be thrown.
        pass
    else:
        return data

    # treat url_file_stream_or_string as string
    if not isinstance(url_file_stream_or_string, bytes_):
        return url_file_stream_or_string.encode('utf-8')
    return url_file_stream_or_string

LooseFeedParser = type(str('LooseFeedParser'), (
    _LooseFeedParser, _FeedParserMixin, _BaseHTMLProcessor, object
), {})
StrictFeedParser = type(str('StrictFeedParser'), (
    _StrictFeedParser, _FeedParserMixin, xml.sax.handler.ContentHandler, object
), {})

def parse(url_file_stream_or_string, etag=None, modified=None, agent=None, referrer=None, handlers=None, request_headers=None, response_headers=None):
    '''Parse a feed from a URL, file, stream, or string.

    request_headers, if given, is a dict from http header name to value to add
    to the request; this overrides internally generated values.

    :return: A :class:`FeedParserDict`.
    '''

    if not agent:
        agent = USER_AGENT
    result = FeedParserDict(
        bozo = False,
        entries = [],
        feed = FeedParserDict(),
        headers = {},
    )

    data = _open_resource(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers, result)

    if not data:
        return result

    # overwrite existing headers using response_headers
    result['headers'].update(response_headers or {})

    data = convert_to_utf8(result['headers'], data, result)
    use_strict_parser = result['encoding'] and True or False

    result['version'], data, entities = replace_doctype(data)

    # Ensure that baseuri is an absolute URI using an acceptable URI scheme.
    contentloc = result['headers'].get('content-location', '')
    href = result.get('href', '')
    baseuri = _makeSafeAbsoluteURI(href, contentloc) or _makeSafeAbsoluteURI(contentloc) or href

    baselang = result['headers'].get('content-language', None)
    if isinstance(baselang, bytes_) and baselang is not None:
        baselang = baselang.decode('utf-8', 'ignore')

    if not _XML_AVAILABLE:
        use_strict_parser = 0
    if use_strict_parser:
        # initialize the SAX parser
        feedparser = StrictFeedParser(baseuri, baselang, 'utf-8')
        saxparser = xml.sax.make_parser(PREFERRED_XML_PARSERS)
        saxparser.setFeature(xml.sax.handler.feature_namespaces, 1)
        try:
            # disable downloading external doctype references, if possible
            saxparser.setFeature(xml.sax.handler.feature_external_ges, 0)
        except xml.sax.SAXNotSupportedException:
            pass
        saxparser.setContentHandler(feedparser)
        saxparser.setErrorHandler(feedparser)
        source = xml.sax.xmlreader.InputSource()
        source.setByteStream(_StringIO(data))
        try:
            saxparser.parse(source)
        except xml.sax.SAXException as e:
            result['bozo'] = 1
            result['bozo_exception'] = feedparser.exc or e
            use_strict_parser = 0
    if not use_strict_parser and _SGML_AVAILABLE:
        feedparser = LooseFeedParser(baseuri, baselang, 'utf-8', entities)
        feedparser.feed(data.decode('utf-8', 'replace'))
    result['feed'] = feedparser.feeddata
    result['entries'] = feedparser.entries
    result['version'] = result['version'] or feedparser.version
    result['namespaces'] = feedparser.namespacesInUse
    return result
