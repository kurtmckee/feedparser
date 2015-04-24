from __future__ import absolute_import

"""Universal feed parser

Handles RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom 0.3, and Atom 1.0 feeds

Visit https://code.google.com/p/feedparser/ for the latest version
Visit http://packages.python.org/feedparser/ for the latest documentation

Required: Python 2.4 or later
Recommended: iconv_codec <http://cjkpython.i18n.org/>
"""

__version__ = "5.2.0"
__license__ = """
Copyright 2010-2015 Kurt McKee <contactme@kurtmckee.org>
Copyright 2002-2008 Mark Pilgrim
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

__author__ = "Mark Pilgrim <http://diveintomark.org/>"
__contributors__ = ["Jason Diamond <http://injektilo.org/>",
                    "John Beimler <http://john.beimler.org/>",
                    "Fazal Majid <http://www.majid.info/mylos/weblog/>",
                    "Aaron Swartz <http://aaronsw.com/>",
                    "Kevin Marks <http://epeus.blogspot.com/>",
                    "Sam Ruby <http://intertwingly.net/>",
                    "Ade Oshineye <http://blog.oshineye.com/>",
                    "Martin Pool <http://sourcefrog.net/>",
                    "Kurt McKee <http://kurtmckee.org/>",
                    "Bernd Schlapsi <https://github.com/brot>",]

# HTTP "User-Agent" header to send to servers when downloading feeds.
# If you are embedding feedparser in a larger application, you should
# change this to your application name and URL.
USER_AGENT = "UniversalFeedParser/%s +https://code.google.com/p/feedparser/" % __version__

# HTTP "Accept" header to send to servers when downloading feeds.  If you don't
# want to send an Accept header, set this to None.
ACCEPT_HEADER = "application/atom+xml,application/rdf+xml,application/rss+xml,application/x-netcdf,application/xml;q=0.9,text/xml;q=0.2,*/*;q=0.1"

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

# ---------- Python 3 modules (make it work if possible) ----------
try:
    # Python 3.1 introduces bytes.maketrans and simultaneously
    # deprecates string.maketrans; use bytes.maketrans if possible
    _maketrans = bytes.maketrans
except (NameError, AttributeError):
    import string
    _maketrans = string.maketrans

# base64 support for Atom feeds that contain embedded binary data
try:
    import base64, binascii
except ImportError:
    base64 = binascii = None
else:
    # Python 3.1 deprecates decodestring in favor of decodebytes
    _base64decode = getattr(base64, 'decodebytes', base64.decodestring)

# _s2bytes: convert a UTF-8 str to bytes if the interpreter is Python 3
# _l2bytes: convert a list of ints to bytes if the interpreter is Python 3
try:
    if bytes is str:
        # In Python 2.5 and below, bytes doesn't exist (NameError)
        # In Python 2.6 and above, bytes and str are the same type
        raise NameError
except NameError:
    # Python 2
    def _s2bytes(s):
        return s
    def _l2bytes(l):
        return ''.join(map(chr, l))
else:
    # Python 3
    def _s2bytes(s):
        return bytes(s, 'utf8')
    def _l2bytes(l):
        return bytes(l)

# ---------- required modules (should come with any Python distribution) ----------
import cgi
import codecs
import copy
import datetime
import itertools
import re
import struct
import time
import types
import urllib
import urllib2
import urlparse
import warnings

from htmlentitydefs import name2codepoint, codepoint2name, entitydefs

try:
    from io import BytesIO as _StringIO
except ImportError:
    try:
        from cStringIO import StringIO as _StringIO
    except ImportError:
        from StringIO import StringIO as _StringIO

# ---------- optional modules (feedparser will work without these, but with reduced functionality) ----------

# gzip is included with most Python distributions, but may not be available if you compiled your own
try:
    import gzip
except ImportError:
    gzip = None
try:
    import zlib
except ImportError:
    zlib = None

# If a real XML parser is available, feedparser will attempt to use it.  feedparser has
# been tested with the built-in SAX parser and libxml2.  On platforms where the
# Python distribution does not come with an XML parser (such as Mac OS X 10.2 and some
# versions of FreeBSD), feedparser will quietly fall back on regex-based parsing.
try:
    import xml.sax
    from xml.sax.saxutils import escape as _xmlescape
except ImportError:
    _XML_AVAILABLE = 0
    def _xmlescape(data,entities={}):
        data = data.replace('&', '&amp;')
        data = data.replace('>', '&gt;')
        data = data.replace('<', '&lt;')
        for char, entity in entities:
            data = data.replace(char, entity)
        return data
else:
    try:
        xml.sax.make_parser(PREFERRED_XML_PARSERS) # test for valid parsers
    except xml.sax.SAXReaderNotAvailable:
        _XML_AVAILABLE = 0
    else:
        _XML_AVAILABLE = 1

# iconv_codec provides support for more character encodings.
# It's available from http://cjkpython.i18n.org/
try:
    import iconv_codec
except ImportError:
    pass

# chardet library auto-detects character encodings
# Download from http://chardet.feedparser.org/
try:
    import chardet
except ImportError:
    chardet = None

from .datetimes import registerDateHandler, _parse_date
from .html import _BaseHTMLProcessor, _cp1252
from .http import _build_urllib2_request, _FeedURLHandler
from .sanitizer import _sanitizeHTML, _HTMLSanitizer
from .sgml import *
from .urls import _urljoin, _convert_to_idn, _makeSafeAbsoluteURI, _resolveRelativeURIs

# ---------- don't touch these ----------
class ThingsNobodyCaresAboutButMe(Exception): pass
class CharacterEncodingOverride(ThingsNobodyCaresAboutButMe): pass
class CharacterEncodingUnknown(ThingsNobodyCaresAboutButMe): pass
class NonXMLContentType(ThingsNobodyCaresAboutButMe): pass
class UndeclaredNamespace(Exception): pass

SUPPORTED_VERSIONS = {'': u'unknown',
                      'rss090': u'RSS 0.90',
                      'rss091n': u'RSS 0.91 (Netscape)',
                      'rss091u': u'RSS 0.91 (Userland)',
                      'rss092': u'RSS 0.92',
                      'rss093': u'RSS 0.93',
                      'rss094': u'RSS 0.94',
                      'rss20': u'RSS 2.0',
                      'rss10': u'RSS 1.0',
                      'rss': u'RSS (unknown version)',
                      'atom01': u'Atom 0.1',
                      'atom02': u'Atom 0.2',
                      'atom03': u'Atom 0.3',
                      'atom10': u'Atom 1.0',
                      'atom': u'Atom (unknown version)',
                      'cdf': u'CDF',
                      }

class FeedParserDict(dict):
    keymap = {'channel': 'feed',
              'items': 'entries',
              'guid': 'id',
              'date': 'updated',
              'date_parsed': 'updated_parsed',
              'description': ['summary', 'subtitle'],
              'description_detail': ['summary_detail', 'subtitle_detail'],
              'url': ['href'],
              'modified': 'updated',
              'modified_parsed': 'updated_parsed',
              'issued': 'published',
              'issued_parsed': 'published_parsed',
              'copyright': 'rights',
              'copyright_detail': 'rights_detail',
              'tagline': 'subtitle',
              'tagline_detail': 'subtitle_detail'}
    def __getitem__(self, key):
        '''
        :return: A :class:`FeedParserDict`.
        '''
        if key == 'category':
            try:
                return dict.__getitem__(self, 'tags')[0]['term']
            except IndexError:
                raise KeyError, "object doesn't have key 'category'"
        elif key == 'enclosures':
            norel = lambda link: FeedParserDict([(name,value) for (name,value) in link.items() if name!='rel'])
            return [norel(link) for link in dict.__getitem__(self, 'links') if link['rel']==u'enclosure']
        elif key == 'license':
            for link in dict.__getitem__(self, 'links'):
                if link['rel']==u'license' and 'href' in link:
                    return link['href']
        elif key == 'updated':
            # Temporarily help developers out by keeping the old
            # broken behavior that was reported in issue 310.
            # This fix was proposed in issue 328.
            if not dict.__contains__(self, 'updated') and \
                dict.__contains__(self, 'published'):
                warnings.warn("To avoid breaking existing software while "
                    "fixing issue 310, a temporary mapping has been created "
                    "from `updated` to `published` if `updated` doesn't "
                    "exist. This fallback will be removed in a future version "
                    "of feedparser.", DeprecationWarning)
                return dict.__getitem__(self, 'published')
            return dict.__getitem__(self, 'updated')
        elif key == 'updated_parsed':
            if not dict.__contains__(self, 'updated_parsed') and \
                dict.__contains__(self, 'published_parsed'):
                warnings.warn("To avoid breaking existing software while "
                    "fixing issue 310, a temporary mapping has been created "
                    "from `updated_parsed` to `published_parsed` if "
                    "`updated_parsed` doesn't exist. This fallback will be "
                    "removed in a future version of feedparser.",
                    DeprecationWarning)
                return dict.__getitem__(self, 'published_parsed')
            return dict.__getitem__(self, 'updated_parsed')
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
        if key in ('updated', 'updated_parsed'):
            # Temporarily help developers out by keeping the old
            # broken behavior that was reported in issue 310.
            # This fix was proposed in issue 328.
            return dict.__contains__(self, key)
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        else:
            return True

    has_key = __contains__

    def get(self, key, default=None):
        '''
        :return: A :class:`FeedParserDict`.
        '''
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        key = self.keymap.get(key, key)
        if isinstance(key, list):
            key = key[0]
        return dict.__setitem__(self, key, value)

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
            return value
        return self[key]

    def __getattr__(self, key):
        # __getattribute__() is called first; this will be called
        # only if an attribute was not already found
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError, "object has no attribute '%s'" % key

    def __hash__(self):
        return id(self)

class _FeedParserMixin:
    namespaces = {
        '': '',
        'http://backend.userland.com/rss': '',
        'http://blogs.law.harvard.edu/tech/rss': '',
        'http://purl.org/rss/1.0/': '',
        'http://my.netscape.com/rdf/simple/0.9/': '',
        'http://example.com/newformat#': '',
        'http://example.com/necho': '',
        'http://purl.org/echo/': '',
        'uri/of/echo/namespace#': '',
        'http://purl.org/pie/': '',
        'http://purl.org/atom/ns#': '',
        'http://www.w3.org/2005/Atom': '',
        'http://purl.org/rss/1.0/modules/rss091#': '',

        'http://webns.net/mvcb/':                                'admin',
        'http://purl.org/rss/1.0/modules/aggregation/':          'ag',
        'http://purl.org/rss/1.0/modules/annotate/':             'annotate',
        'http://media.tangent.org/rss/1.0/':                     'audio',
        'http://backend.userland.com/blogChannelModule':         'blogChannel',
        'http://web.resource.org/cc/':                           'cc',
        'http://backend.userland.com/creativeCommonsRssModule':  'creativeCommons',
        'http://purl.org/rss/1.0/modules/company':               'co',
        'http://purl.org/rss/1.0/modules/content/':              'content',
        'http://my.theinfo.org/changed/1.0/rss/':                'cp',
        'http://purl.org/dc/elements/1.1/':                      'dc',
        'http://purl.org/dc/terms/':                             'dcterms',
        'http://purl.org/rss/1.0/modules/email/':                'email',
        'http://purl.org/rss/1.0/modules/event/':                'ev',
        'http://rssnamespace.org/feedburner/ext/1.0':            'feedburner',
        'http://freshmeat.net/rss/fm/':                          'fm',
        'http://xmlns.com/foaf/0.1/':                            'foaf',
        'http://www.w3.org/2003/01/geo/wgs84_pos#':              'geo',
        'http://www.georss.org/georss':                          'georss',
        'http://www.opengis.net/gml':                            'gml',
        'http://postneo.com/icbm/':                              'icbm',
        'http://purl.org/rss/1.0/modules/image/':                'image',
        'http://www.itunes.com/DTDs/PodCast-1.0.dtd':            'itunes',
        'http://example.com/DTDs/PodCast-1.0.dtd':               'itunes',
        'http://purl.org/rss/1.0/modules/link/':                 'l',
        'http://search.yahoo.com/mrss':                          'media',
        # Version 1.1.2 of the Media RSS spec added the trailing slash on the namespace
        'http://search.yahoo.com/mrss/':                         'media',
        'http://madskills.com/public/xml/rss/module/pingback/':  'pingback',
        'http://prismstandard.org/namespaces/1.2/basic/':        'prism',
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#':           'rdf',
        'http://www.w3.org/2000/01/rdf-schema#':                 'rdfs',
        'http://purl.org/rss/1.0/modules/reference/':            'ref',
        'http://purl.org/rss/1.0/modules/richequiv/':            'reqv',
        'http://purl.org/rss/1.0/modules/search/':               'search',
        'http://purl.org/rss/1.0/modules/slash/':                'slash',
        'http://schemas.xmlsoap.org/soap/envelope/':             'soap',
        'http://purl.org/rss/1.0/modules/servicestatus/':        'ss',
        'http://hacks.benhammersley.com/rss/streaming/':         'str',
        'http://purl.org/rss/1.0/modules/subscription/':         'sub',
        'http://purl.org/rss/1.0/modules/syndication/':          'sy',
        'http://schemas.pocketsoap.com/rss/myDescModule/':       'szf',
        'http://purl.org/rss/1.0/modules/taxonomy/':             'taxo',
        'http://purl.org/rss/1.0/modules/threading/':            'thr',
        'http://purl.org/rss/1.0/modules/textinput/':            'ti',
        'http://madskills.com/public/xml/rss/module/trackback/': 'trackback',
        'http://wellformedweb.org/commentAPI/':                  'wfw',
        'http://purl.org/rss/1.0/modules/wiki/':                 'wiki',
        'http://www.w3.org/1999/xhtml':                          'xhtml',
        'http://www.w3.org/1999/xlink':                          'xlink',
        'http://www.w3.org/XML/1998/namespace':                  'xml',
        'http://podlove.org/simple-chapters':                    'psc',
    }
    _matchnamespaces = {}

    can_be_relative_uri = set(['link', 'id', 'wfw_comment', 'wfw_commentrss', 'docs', 'url', 'href', 'comments', 'icon', 'logo'])
    can_contain_relative_uris = set(['content', 'title', 'summary', 'info', 'tagline', 'subtitle', 'copyright', 'rights', 'description'])
    can_contain_dangerous_markup = set(['content', 'title', 'summary', 'info', 'tagline', 'subtitle', 'copyright', 'rights', 'description'])
    html_types = [u'text/html', u'application/xhtml+xml']

    def __init__(self, baseuri=None, baselang=None, encoding=u'utf-8'):
        if not self._matchnamespaces:
            for k, v in self.namespaces.items():
                self._matchnamespaces[k.lower()] = v
        self.feeddata = FeedParserDict() # feed-level data
        self.encoding = encoding # character encoding
        self.entries = [] # list of entry-level data
        self.version = u'' # feed type/version, see SUPPORTED_VERSIONS
        self.namespacesInUse = {} # dictionary of namespaces defined by the feed

        # the following are used internally to track state;
        # this is really out of control and should be refactored
        self.infeed = 0
        self.inentry = 0
        self.incontent = 0
        self.intextinput = 0
        self.inimage = 0
        self.inauthor = 0
        self.incontributor = 0
        self.inpublisher = 0
        self.insource = 0

        # georss
        self.ingeometry = 0

        self.sourcedata = FeedParserDict()
        self.contentparams = FeedParserDict()
        self._summaryKey = None
        self.namespacemap = {}
        self.elementstack = []
        self.basestack = []
        self.langstack = []
        self.baseuri = baseuri or u''
        self.lang = baselang or None
        self.svgOK = 0
        self.title_depth = -1
        self.depth = 0
        # psc_chapters_flag prevents multiple psc_chapters from being
        # captured in a single entry or item. The transition states are
        # None -> True -> False. psc_chapter elements will only be
        # captured while it is True.
        self.psc_chapters_flag = None
        if baselang:
            self.feeddata['language'] = baselang.replace('_','-')

        # A map of the following form:
        #     {
        #         object_that_value_is_set_on: {
        #             property_name: depth_of_node_property_was_extracted_from,
        #             other_property: depth_of_node_property_was_extracted_from,
        #         },
        #     }
        self.property_depth_map = {}

    def _normalize_attributes(self, kv):
        k = kv[0].lower()
        v = k in ('rel', 'type') and kv[1].lower() or kv[1]
        # the sgml parser doesn't handle entities in attributes, nor
        # does it pass the attribute values through as unicode, while
        # strict xml parsers do -- account for this difference
        if isinstance(self, _LooseFeedParser):
            v = v.replace('&amp;', '&')
            if not isinstance(v, unicode):
                v = v.decode('utf-8')
        return (k, v)

    def unknown_starttag(self, tag, attrs):
        # increment depth counter
        self.depth += 1

        # normalize attrs
        attrs = map(self._normalize_attributes, attrs)

        # track xml:base and xml:lang
        attrsD = dict(attrs)
        baseuri = attrsD.get('xml:base', attrsD.get('base')) or self.baseuri
        if not isinstance(baseuri, unicode):
            baseuri = baseuri.decode(self.encoding, 'ignore')
        # ensure that self.baseuri is always an absolute URI that
        # uses a whitelisted URI scheme (e.g. not `javscript:`)
        if self.baseuri:
            self.baseuri = _makeSafeAbsoluteURI(self.baseuri, baseuri) or self.baseuri
        else:
            self.baseuri = _urljoin(self.baseuri, baseuri)
        lang = attrsD.get('xml:lang', attrsD.get('lang'))
        if lang == '':
            # xml:lang could be explicitly set to '', we need to capture that
            lang = None
        elif lang is None:
            # if no xml:lang is specified, use parent lang
            lang = self.lang
        if lang:
            if tag in ('feed', 'rss', 'rdf:RDF'):
                self.feeddata['language'] = lang.replace('_','-')
        self.lang = lang
        self.basestack.append(self.baseuri)
        self.langstack.append(lang)

        # track namespaces
        for prefix, uri in attrs:
            if prefix.startswith('xmlns:'):
                self.trackNamespace(prefix[6:], uri)
            elif prefix == 'xmlns':
                self.trackNamespace(None, uri)

        # track inline content
        if self.incontent and not self.contentparams.get('type', u'xml').endswith(u'xml'):
            if tag in ('xhtml:div', 'div'):
                return # typepad does this 10/2007
            # element declared itself as escaped markup, but it isn't really
            self.contentparams['type'] = u'application/xhtml+xml'
        if self.incontent and self.contentparams.get('type') == u'application/xhtml+xml':
            if tag.find(':') <> -1:
                prefix, tag = tag.split(':', 1)
                namespace = self.namespacesInUse.get(prefix, '')
                if tag=='math' and namespace=='http://www.w3.org/1998/Math/MathML':
                    attrs.append(('xmlns',namespace))
                if tag=='svg' and namespace=='http://www.w3.org/2000/svg':
                    attrs.append(('xmlns',namespace))
            if tag == 'svg':
                self.svgOK += 1
            return self.handle_data('<%s%s>' % (tag, self.strattrs(attrs)), escape=0)

        # match namespaces
        if tag.find(':') <> -1:
            prefix, suffix = tag.split(':', 1)
        else:
            prefix, suffix = '', tag
        prefix = self.namespacemap.get(prefix, prefix)
        if prefix:
            prefix = prefix + '_'

        # special hack for better tracking of empty textinput/image elements in illformed feeds
        if (not prefix) and tag not in ('title', 'link', 'description', 'name'):
            self.intextinput = 0
        if (not prefix) and tag not in ('title', 'link', 'description', 'url', 'href', 'width', 'height'):
            self.inimage = 0

        # call special handler (if defined) or default handler
        methodname = '_start_' + prefix + suffix
        try:
            method = getattr(self, methodname)
            return method(attrsD)
        except AttributeError:
            # Since there's no handler or something has gone wrong we explicitly add the element and its attributes
            unknown_tag = prefix + suffix
            if len(attrsD) == 0:
                # No attributes so merge it into the encosing dictionary
                return self.push(unknown_tag, 1)
            else:
                # Has attributes so create it in its own dictionary
                context = self._getContext()
                context[unknown_tag] = attrsD

    def unknown_endtag(self, tag):
        # match namespaces
        if tag.find(':') <> -1:
            prefix, suffix = tag.split(':', 1)
        else:
            prefix, suffix = '', tag
        prefix = self.namespacemap.get(prefix, prefix)
        if prefix:
            prefix = prefix + '_'
        if suffix == 'svg' and self.svgOK:
            self.svgOK -= 1

        # call special handler (if defined) or default handler
        methodname = '_end_' + prefix + suffix
        try:
            if self.svgOK:
                raise AttributeError()
            method = getattr(self, methodname)
            method()
        except AttributeError:
            self.pop(prefix + suffix)

        # track inline content
        if self.incontent and not self.contentparams.get('type', u'xml').endswith(u'xml'):
            # element declared itself as escaped markup, but it isn't really
            if tag in ('xhtml:div', 'div'):
                return # typepad does this 10/2007
            self.contentparams['type'] = u'application/xhtml+xml'
        if self.incontent and self.contentparams.get('type') == u'application/xhtml+xml':
            tag = tag.split(':')[-1]
            self.handle_data('</%s>' % tag, escape=0)

        # track xml:base and xml:lang going out of scope
        if self.basestack:
            self.basestack.pop()
            if self.basestack and self.basestack[-1]:
                self.baseuri = self.basestack[-1]
        if self.langstack:
            self.langstack.pop()
            if self.langstack: # and (self.langstack[-1] is not None):
                self.lang = self.langstack[-1]

        self.depth -= 1

    def handle_charref(self, ref):
        # called for each character reference, e.g. for '&#160;', ref will be '160'
        if not self.elementstack:
            return
        ref = ref.lower()
        if ref in ('34', '38', '39', '60', '62', 'x22', 'x26', 'x27', 'x3c', 'x3e'):
            text = '&#%s;' % ref
        else:
            if ref[0] == 'x':
                c = int(ref[1:], 16)
            else:
                c = int(ref)
            text = unichr(c).encode('utf-8')
        self.elementstack[-1][2].append(text)

    def handle_entityref(self, ref):
        # called for each entity reference, e.g. for '&copy;', ref will be 'copy'
        if not self.elementstack:
            return
        if ref in ('lt', 'gt', 'quot', 'amp', 'apos'):
            text = '&%s;' % ref
        elif ref in self.entities:
            text = self.entities[ref]
            if text.startswith('&#') and text.endswith(';'):
                return self.handle_entityref(text)
        else:
            try:
                name2codepoint[ref]
            except KeyError:
                text = '&%s;' % ref
            else:
                text = unichr(name2codepoint[ref]).encode('utf-8')
        self.elementstack[-1][2].append(text)

    def handle_data(self, text, escape=1):
        # called for each block of plain text, i.e. outside of any tag and
        # not containing any character or entity references
        if not self.elementstack:
            return
        if escape and self.contentparams.get('type') == u'application/xhtml+xml':
            text = _xmlescape(text)
        self.elementstack[-1][2].append(text)

    def handle_comment(self, text):
        # called for each comment, e.g. <!-- insert message here -->
        pass

    def handle_pi(self, text):
        # called for each processing instruction, e.g. <?instruction>
        pass

    def handle_decl(self, text):
        pass

    def parse_declaration(self, i):
        # override internal declaration handler to handle CDATA blocks
        if self.rawdata[i:i+9] == '<![CDATA[':
            k = self.rawdata.find(']]>', i)
            if k == -1:
                # CDATA block began but didn't finish
                k = len(self.rawdata)
                return k
            self.handle_data(_xmlescape(self.rawdata[i+9:k]), 0)
            return k+3
        else:
            k = self.rawdata.find('>', i)
            if k >= 0:
                return k+1
            else:
                # We have an incomplete CDATA block.
                return k

    def mapContentType(self, contentType):
        contentType = contentType.lower()
        if contentType == 'text' or contentType == 'plain':
            contentType = u'text/plain'
        elif contentType == 'html':
            contentType = u'text/html'
        elif contentType == 'xhtml':
            contentType = u'application/xhtml+xml'
        return contentType

    def trackNamespace(self, prefix, uri):
        loweruri = uri.lower()
        if not self.version:
            if (prefix, loweruri) == (None, 'http://my.netscape.com/rdf/simple/0.9/'):
                self.version = u'rss090'
            elif loweruri == 'http://purl.org/rss/1.0/':
                self.version = u'rss10'
            elif loweruri == 'http://www.w3.org/2005/atom':
                self.version = u'atom10'
        if loweruri.find(u'backend.userland.com/rss') <> -1:
            # match any backend.userland.com namespace
            uri = u'http://backend.userland.com/rss'
            loweruri = uri
        if loweruri in self._matchnamespaces:
            self.namespacemap[prefix] = self._matchnamespaces[loweruri]
            self.namespacesInUse[self._matchnamespaces[loweruri]] = uri
        else:
            self.namespacesInUse[prefix or ''] = uri

    def resolveURI(self, uri):
        return _urljoin(self.baseuri or u'', uri)

    def decodeEntities(self, element, data):
        return data

    def strattrs(self, attrs):
        return ''.join([' %s="%s"' % (t[0],_xmlescape(t[1],{'"':'&quot;'})) for t in attrs])

    def push(self, element, expectingText):
        self.elementstack.append([element, expectingText, []])

    def pop(self, element, stripWhitespace=1):
        if not self.elementstack:
            return
        if self.elementstack[-1][0] != element:
            return

        element, expectingText, pieces = self.elementstack.pop()

        if self.version == u'atom10' and self.contentparams.get('type', u'text') == u'application/xhtml+xml':
            # remove enclosing child element, but only if it is a <div> and
            # only if all the remaining content is nested underneath it.
            # This means that the divs would be retained in the following:
            #    <div>foo</div><div>bar</div>
            while pieces and len(pieces)>1 and not pieces[-1].strip():
                del pieces[-1]
            while pieces and len(pieces)>1 and not pieces[0].strip():
                del pieces[0]
            if pieces and (pieces[0] == '<div>' or pieces[0].startswith('<div ')) and pieces[-1]=='</div>':
                depth = 0
                for piece in pieces[:-1]:
                    if piece.startswith('</'):
                        depth -= 1
                        if depth == 0:
                            break
                    elif piece.startswith('<') and not piece.endswith('/>'):
                        depth += 1
                else:
                    pieces = pieces[1:-1]

        # Ensure each piece is a str for Python 3
        for (i, v) in enumerate(pieces):
            if not isinstance(v, unicode):
                pieces[i] = v.decode('utf-8')

        output = u''.join(pieces)
        if stripWhitespace:
            output = output.strip()
        if not expectingText:
            return output

        # decode base64 content
        if base64 and self.contentparams.get('base64', 0):
            try:
                output = _base64decode(output)
            except binascii.Error:
                pass
            except binascii.Incomplete:
                pass
            except TypeError:
                # In Python 3, base64 takes and outputs bytes, not str
                # This may not be the most correct way to accomplish this
                output = _base64decode(output.encode('utf-8')).decode('utf-8')

        # resolve relative URIs
        if (element in self.can_be_relative_uri) and output:
            # do not resolve guid elements with isPermalink="false"
            if not element == 'id' or self.guidislink:
                output = self.resolveURI(output)

        # decode entities within embedded markup
        if not self.contentparams.get('base64', 0):
            output = self.decodeEntities(element, output)

        # some feed formats require consumers to guess
        # whether the content is html or plain text
        if not self.version.startswith(u'atom') and self.contentparams.get('type') == u'text/plain':
            if self.lookslikehtml(output):
                self.contentparams['type'] = u'text/html'

        # remove temporary cruft from contentparams
        try:
            del self.contentparams['mode']
        except KeyError:
            pass
        try:
            del self.contentparams['base64']
        except KeyError:
            pass

        is_htmlish = self.mapContentType(self.contentparams.get('type', u'text/html')) in self.html_types
        # resolve relative URIs within embedded markup
        if is_htmlish and RESOLVE_RELATIVE_URIS:
            if element in self.can_contain_relative_uris:
                output = _resolveRelativeURIs(output, self.baseuri, self.encoding, self.contentparams.get('type', u'text/html'))

        # sanitize embedded markup
        if is_htmlish and SANITIZE_HTML:
            if element in self.can_contain_dangerous_markup:
                output = _sanitizeHTML(output, self.encoding, self.contentparams.get('type', u'text/html'))

        if self.encoding and not isinstance(output, unicode):
            output = output.decode(self.encoding, 'ignore')

        # address common error where people take data that is already
        # utf-8, presume that it is iso-8859-1, and re-encode it.
        if self.encoding in (u'utf-8', u'utf-8_INVALID_PYTHON_3') and isinstance(output, unicode):
            try:
                output = output.encode('iso-8859-1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

        # map win-1252 extensions to the proper code points
        if isinstance(output, unicode):
            output = output.translate(_cp1252)

        # categories/tags/keywords/whatever are handled in _end_category or _end_tags or _end_itunes_keywords
        if element in ('category', 'tags', 'itunes_keywords'):
            return output

        if element == 'title' and -1 < self.title_depth <= self.depth:
            return output

        # store output in appropriate place(s)
        if self.inentry and not self.insource:
            if element == 'content':
                self.entries[-1].setdefault(element, [])
                contentparams = copy.deepcopy(self.contentparams)
                contentparams['value'] = output
                self.entries[-1][element].append(contentparams)
            elif element == 'link':
                if not self.inimage:
                    # query variables in urls in link elements are improperly
                    # converted from `?a=1&b=2` to `?a=1&b;=2` as if they're
                    # unhandled character references. fix this special case.
                    output = output.replace('&amp;', '&')
                    output = re.sub("&([A-Za-z0-9_]+);", "&\g<1>", output)
                    self.entries[-1][element] = output
                    if output:
                        self.entries[-1]['links'][-1]['href'] = output
            else:
                if element == 'description':
                    element = 'summary'
                old_value_depth = self.property_depth_map.setdefault(self.entries[-1], {}).get(element)
                if old_value_depth is None or self.depth <= old_value_depth:
                    self.property_depth_map[self.entries[-1]][element] = self.depth
                    self.entries[-1][element] = output
                if self.incontent:
                    contentparams = copy.deepcopy(self.contentparams)
                    contentparams['value'] = output
                    self.entries[-1][element + '_detail'] = contentparams
        elif (self.infeed or self.insource):# and (not self.intextinput) and (not self.inimage):
            context = self._getContext()
            if element == 'description':
                element = 'subtitle'
            context[element] = output
            if element == 'link':
                # fix query variables; see above for the explanation
                output = re.sub("&([A-Za-z0-9_]+);", "&\g<1>", output)
                context[element] = output
                context['links'][-1]['href'] = output
            elif self.incontent:
                contentparams = copy.deepcopy(self.contentparams)
                contentparams['value'] = output
                context[element + '_detail'] = contentparams
        return output

    def pushContent(self, tag, attrsD, defaultContentType, expectingText):
        self.incontent += 1
        if self.lang:
            self.lang=self.lang.replace('_','-')
        self.contentparams = FeedParserDict({
            'type': self.mapContentType(attrsD.get('type', defaultContentType)),
            'language': self.lang,
            'base': self.baseuri})
        self.contentparams['base64'] = self._isBase64(attrsD, self.contentparams)
        self.push(tag, expectingText)

    def popContent(self, tag):
        value = self.pop(tag)
        self.incontent -= 1
        self.contentparams.clear()
        return value

    # a number of elements in a number of RSS variants are nominally plain
    # text, but this is routinely ignored.  This is an attempt to detect
    # the most common cases.  As false positives often result in silent
    # data loss, this function errs on the conservative side.
    @staticmethod
    def lookslikehtml(s):
        # must have a close tag or an entity reference to qualify
        if not (re.search(r'</(\w+)>',s) or re.search("&#?\w+;",s)):
            return

        # all tags must be in a restricted subset of valid HTML tags
        if filter(lambda t: t.lower() not in _HTMLSanitizer.acceptable_elements,
            re.findall(r'</?(\w+)',s)):
            return

        # all entities must have been defined as valid HTML entities
        if filter(lambda e: e not in entitydefs.keys(), re.findall(r'&(\w+);', s)):
            return

        return 1

    def _mapToStandardPrefix(self, name):
        colonpos = name.find(':')
        if colonpos <> -1:
            prefix = name[:colonpos]
            suffix = name[colonpos+1:]
            prefix = self.namespacemap.get(prefix, prefix)
            name = prefix + ':' + suffix
        return name

    def _getAttribute(self, attrsD, name):
        return attrsD.get(self._mapToStandardPrefix(name))

    def _isBase64(self, attrsD, contentparams):
        if attrsD.get('mode', '') == 'base64':
            return 1
        if self.contentparams['type'].startswith(u'text/'):
            return 0
        if self.contentparams['type'].endswith(u'+xml'):
            return 0
        if self.contentparams['type'].endswith(u'/xml'):
            return 0
        return 1

    def _itsAnHrefDamnIt(self, attrsD):
        href = attrsD.get('url', attrsD.get('uri', attrsD.get('href', None)))
        if href:
            try:
                del attrsD['url']
            except KeyError:
                pass
            try:
                del attrsD['uri']
            except KeyError:
                pass
            attrsD['href'] = href
        return attrsD

    def _save(self, key, value, overwrite=False):
        context = self._getContext()
        if overwrite:
            context[key] = value
        else:
            context.setdefault(key, value)

    def _start_rss(self, attrsD):
        versionmap = {'0.91': u'rss091u',
                      '0.92': u'rss092',
                      '0.93': u'rss093',
                      '0.94': u'rss094'}
        #If we're here then this is an RSS feed.
        #If we don't have a version or have a version that starts with something
        #other than RSS then there's been a mistake. Correct it.
        if not self.version or not self.version.startswith(u'rss'):
            attr_version = attrsD.get('version', '')
            version = versionmap.get(attr_version)
            if version:
                self.version = version
            elif attr_version.startswith('2.'):
                self.version = u'rss20'
            else:
                self.version = u'rss'

    def _start_channel(self, attrsD):
        self.infeed = 1
        self._cdf_common(attrsD)

    def _cdf_common(self, attrsD):
        if 'lastmod' in attrsD:
            self._start_modified({})
            self.elementstack[-1][-1] = attrsD['lastmod']
            self._end_modified()
        if 'href' in attrsD:
            self._start_link({})
            self.elementstack[-1][-1] = attrsD['href']
            self._end_link()

    def _start_feed(self, attrsD):
        self.infeed = 1
        versionmap = {'0.1': u'atom01',
                      '0.2': u'atom02',
                      '0.3': u'atom03'}
        if not self.version:
            attr_version = attrsD.get('version')
            version = versionmap.get(attr_version)
            if version:
                self.version = version
            else:
                self.version = u'atom'

    def _end_channel(self):
        self.infeed = 0
    _end_feed = _end_channel

    def _start_image(self, attrsD):
        context = self._getContext()
        if not self.inentry:
            context.setdefault('image', FeedParserDict())
        self.inimage = 1
        self.title_depth = -1
        self.push('image', 0)

    def _end_image(self):
        self.pop('image')
        self.inimage = 0

    def _start_textinput(self, attrsD):
        context = self._getContext()
        context.setdefault('textinput', FeedParserDict())
        self.intextinput = 1
        self.title_depth = -1
        self.push('textinput', 0)
    _start_textInput = _start_textinput

    def _end_textinput(self):
        self.pop('textinput')
        self.intextinput = 0
    _end_textInput = _end_textinput

    def _start_author(self, attrsD):
        self.inauthor = 1
        self.push('author', 1)
        # Append a new FeedParserDict when expecting an author
        context = self._getContext()
        context.setdefault('authors', [])
        context['authors'].append(FeedParserDict())
    _start_managingeditor = _start_author
    _start_dc_author = _start_author
    _start_dc_creator = _start_author
    _start_itunes_author = _start_author

    def _end_author(self):
        self.pop('author')
        self.inauthor = 0
        self._sync_author_detail()
    _end_managingeditor = _end_author
    _end_dc_author = _end_author
    _end_dc_creator = _end_author
    _end_itunes_author = _end_author

    def _start_itunes_owner(self, attrsD):
        self.inpublisher = 1
        self.push('publisher', 0)

    def _end_itunes_owner(self):
        self.pop('publisher')
        self.inpublisher = 0
        self._sync_author_detail('publisher')

    def _start_contributor(self, attrsD):
        self.incontributor = 1
        context = self._getContext()
        context.setdefault('contributors', [])
        context['contributors'].append(FeedParserDict())
        self.push('contributor', 0)

    def _end_contributor(self):
        self.pop('contributor')
        self.incontributor = 0

    def _start_dc_contributor(self, attrsD):
        self.incontributor = 1
        context = self._getContext()
        context.setdefault('contributors', [])
        context['contributors'].append(FeedParserDict())
        self.push('name', 0)

    def _end_dc_contributor(self):
        self._end_name()
        self.incontributor = 0

    def _start_name(self, attrsD):
        self.push('name', 0)
    _start_itunes_name = _start_name

    def _end_name(self):
        value = self.pop('name')
        if self.inpublisher:
            self._save_author('name', value, 'publisher')
        elif self.inauthor:
            self._save_author('name', value)
        elif self.incontributor:
            self._save_contributor('name', value)
        elif self.intextinput:
            context = self._getContext()
            context['name'] = value
    _end_itunes_name = _end_name

    def _start_width(self, attrsD):
        self.push('width', 0)

    def _end_width(self):
        value = self.pop('width')
        try:
            value = int(value)
        except ValueError:
            value = 0
        if self.inimage:
            context = self._getContext()
            context['width'] = value

    def _start_height(self, attrsD):
        self.push('height', 0)

    def _end_height(self):
        value = self.pop('height')
        try:
            value = int(value)
        except ValueError:
            value = 0
        if self.inimage:
            context = self._getContext()
            context['height'] = value

    def _start_url(self, attrsD):
        self.push('href', 1)
    _start_homepage = _start_url
    _start_uri = _start_url

    def _end_url(self):
        value = self.pop('href')
        if self.inauthor:
            self._save_author('href', value)
        elif self.incontributor:
            self._save_contributor('href', value)
    _end_homepage = _end_url
    _end_uri = _end_url

    def _start_email(self, attrsD):
        self.push('email', 0)
    _start_itunes_email = _start_email

    def _end_email(self):
        value = self.pop('email')
        if self.inpublisher:
            self._save_author('email', value, 'publisher')
        elif self.inauthor:
            self._save_author('email', value)
        elif self.incontributor:
            self._save_contributor('email', value)
    _end_itunes_email = _end_email

    def _getContext(self):
        if self.insource:
            context = self.sourcedata
        elif self.inimage and 'image' in self.feeddata:
            context = self.feeddata['image']
        elif self.intextinput:
            context = self.feeddata['textinput']
        elif self.inentry:
            context = self.entries[-1]
        else:
            context = self.feeddata
        return context

    def _save_author(self, key, value, prefix='author'):
        context = self._getContext()
        context.setdefault(prefix + '_detail', FeedParserDict())
        context[prefix + '_detail'][key] = value
        self._sync_author_detail()
        context.setdefault('authors', [FeedParserDict()])
        context['authors'][-1][key] = value

    def _save_contributor(self, key, value):
        context = self._getContext()
        context.setdefault('contributors', [FeedParserDict()])
        context['contributors'][-1][key] = value

    def _sync_author_detail(self, key='author'):
        context = self._getContext()
        detail = context.get('%ss' % key, [FeedParserDict()])[-1]
        if detail:
            name = detail.get('name')
            email = detail.get('email')
            if name and email:
                context[key] = u'%s (%s)' % (name, email)
            elif name:
                context[key] = name
            elif email:
                context[key] = email
        else:
            author, email = context.get(key), None
            if not author:
                return
            emailmatch = re.search(ur'''(([a-zA-Z0-9\_\-\.\+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?))(\?subject=\S+)?''', author)
            if emailmatch:
                email = emailmatch.group(0)
                # probably a better way to do the following, but it passes all the tests
                author = author.replace(email, u'')
                author = author.replace(u'()', u'')
                author = author.replace(u'<>', u'')
                author = author.replace(u'&lt;&gt;', u'')
                author = author.strip()
                if author and (author[0] == u'('):
                    author = author[1:]
                if author and (author[-1] == u')'):
                    author = author[:-1]
                author = author.strip()
            if author or email:
                context.setdefault('%s_detail' % key, detail)
            if author:
                detail['name'] = author
            if email:
                detail['email'] = email

    def _start_subtitle(self, attrsD):
        self.pushContent('subtitle', attrsD, u'text/plain', 1)
    _start_tagline = _start_subtitle
    _start_itunes_subtitle = _start_subtitle

    def _end_subtitle(self):
        self.popContent('subtitle')
    _end_tagline = _end_subtitle
    _end_itunes_subtitle = _end_subtitle

    def _start_rights(self, attrsD):
        self.pushContent('rights', attrsD, u'text/plain', 1)
    _start_dc_rights = _start_rights
    _start_copyright = _start_rights

    def _end_rights(self):
        self.popContent('rights')
    _end_dc_rights = _end_rights
    _end_copyright = _end_rights

    def _start_item(self, attrsD):
        self.entries.append(FeedParserDict())
        self.push('item', 0)
        self.inentry = 1
        self.guidislink = 0
        self.title_depth = -1
        self.psc_chapters_flag = None
        id = self._getAttribute(attrsD, 'rdf:about')
        if id:
            context = self._getContext()
            context['id'] = id
        self._cdf_common(attrsD)
    _start_entry = _start_item

    def _end_item(self):
        self.pop('item')
        self.inentry = 0
    _end_entry = _end_item

    def _start_dc_language(self, attrsD):
        self.push('language', 1)
    _start_language = _start_dc_language

    def _end_dc_language(self):
        self.lang = self.pop('language')
    _end_language = _end_dc_language

    def _start_dc_publisher(self, attrsD):
        self.push('publisher', 1)
    _start_webmaster = _start_dc_publisher

    def _end_dc_publisher(self):
        self.pop('publisher')
        self._sync_author_detail('publisher')
    _end_webmaster = _end_dc_publisher

    def _start_dcterms_valid(self, attrsD):
        self.push('validity', 1)

    def _end_dcterms_valid(self):
        for validity_detail in self.pop('validity').split(';'):
            if '=' in validity_detail:
                key, value = validity_detail.split('=', 1)
                if key == 'start':
                    self._save('validity_start', value, overwrite=True)
                    self._save('validity_start_parsed', _parse_date(value), overwrite=True)
                elif key == 'end':
                    self._save('validity_end', value, overwrite=True)
                    self._save('validity_end_parsed', _parse_date(value), overwrite=True)

    def _start_published(self, attrsD):
        self.push('published', 1)
    _start_dcterms_issued = _start_published
    _start_issued = _start_published
    _start_pubdate = _start_published

    def _end_published(self):
        value = self.pop('published')
        self._save('published_parsed', _parse_date(value), overwrite=True)
    _end_dcterms_issued = _end_published
    _end_issued = _end_published
    _end_pubdate = _end_published

    def _start_updated(self, attrsD):
        self.push('updated', 1)
    _start_modified = _start_updated
    _start_dcterms_modified = _start_updated
    _start_dc_date = _start_updated
    _start_lastbuilddate = _start_updated

    def _end_updated(self):
        value = self.pop('updated')
        parsed_value = _parse_date(value)
        self._save('updated_parsed', parsed_value, overwrite=True)
    _end_modified = _end_updated
    _end_dcterms_modified = _end_updated
    _end_dc_date = _end_updated
    _end_lastbuilddate = _end_updated

    def _start_created(self, attrsD):
        self.push('created', 1)
    _start_dcterms_created = _start_created

    def _end_created(self):
        value = self.pop('created')
        self._save('created_parsed', _parse_date(value), overwrite=True)
    _end_dcterms_created = _end_created

    def _start_expirationdate(self, attrsD):
        self.push('expired', 1)

    def _end_expirationdate(self):
        self._save('expired_parsed', _parse_date(self.pop('expired')), overwrite=True)

    # geospatial location, or "where", from georss.org

    def _start_georssgeom(self, attrsD):
        self.push('geometry', 0)
        context = self._getContext()
        context['where'] = FeedParserDict()

    _start_georss_point = _start_georssgeom
    _start_georss_line = _start_georssgeom
    _start_georss_polygon = _start_georssgeom
    _start_georss_box = _start_georssgeom

    def _save_where(self, geometry):
        context = self._getContext()
        context['where'].update(geometry)

    def _end_georss_point(self):
        geometry = _parse_georss_point(self.pop('geometry'))
        if geometry:
            self._save_where(geometry)

    def _end_georss_line(self):
        geometry = _parse_georss_line(self.pop('geometry'))
        if geometry:
            self._save_where(geometry)

    def _end_georss_polygon(self):
        this = self.pop('geometry')
        geometry = _parse_georss_polygon(this)
        if geometry:
            self._save_where(geometry)

    def _end_georss_box(self):
        geometry = _parse_georss_box(self.pop('geometry'))
        if geometry:
            self._save_where(geometry)

    def _start_where(self, attrsD):
        self.push('where', 0)
        context = self._getContext()
        context['where'] = FeedParserDict()
    _start_georss_where = _start_where

    def _parse_srs_attrs(self, attrsD):
        srsName = attrsD.get('srsname')
        try:
            srsDimension = int(attrsD.get('srsdimension', '2'))
        except ValueError:
            srsDimension = 2
        context = self._getContext()
        context['where']['srsName'] = srsName
        context['where']['srsDimension'] = srsDimension

    def _start_gml_point(self, attrsD):
        self._parse_srs_attrs(attrsD)
        self.ingeometry = 1
        self.push('geometry', 0)

    def _start_gml_linestring(self, attrsD):
        self._parse_srs_attrs(attrsD)
        self.ingeometry = 'linestring'
        self.push('geometry', 0)

    def _start_gml_polygon(self, attrsD):
        self._parse_srs_attrs(attrsD)
        self.push('geometry', 0)

    def _start_gml_exterior(self, attrsD):
        self.push('geometry', 0)

    def _start_gml_linearring(self, attrsD):
        self.ingeometry = 'polygon'
        self.push('geometry', 0)

    def _start_gml_pos(self, attrsD):
        self.push('pos', 0)

    def _end_gml_pos(self):
        this = self.pop('pos')
        context = self._getContext()
        srsName = context['where'].get('srsName')
        srsDimension = context['where'].get('srsDimension', 2)
        swap = True
        if srsName and "EPSG" in srsName:
            epsg = int(srsName.split(":")[-1])
            swap = bool(epsg in _geogCS)
        geometry = _parse_georss_point(this, swap=swap, dims=srsDimension)
        if geometry:
            self._save_where(geometry)

    def _start_gml_poslist(self, attrsD):
        self.push('pos', 0)

    def _end_gml_poslist(self):
        this = self.pop('pos')
        context = self._getContext()
        srsName = context['where'].get('srsName')
        srsDimension = context['where'].get('srsDimension', 2)
        swap = True
        if srsName and "EPSG" in srsName:
            epsg = int(srsName.split(":")[-1])
            swap = bool(epsg in _geogCS)
        geometry = _parse_poslist(
            this, self.ingeometry, swap=swap, dims=srsDimension)
        if geometry:
            self._save_where(geometry)

    def _end_geom(self):
        self.ingeometry = 0
        self.pop('geometry')
    _end_gml_point = _end_geom
    _end_gml_linestring = _end_geom
    _end_gml_linearring = _end_geom
    _end_gml_exterior = _end_geom
    _end_gml_polygon = _end_geom

    def _end_where(self):
        self.pop('where')
    _end_georss_where = _end_where

    # end geospatial

    def _start_cc_license(self, attrsD):
        context = self._getContext()
        value = self._getAttribute(attrsD, 'rdf:resource')
        attrsD = FeedParserDict()
        attrsD['rel'] = u'license'
        if value:
            attrsD['href']=value
        context.setdefault('links', []).append(attrsD)

    def _start_creativecommons_license(self, attrsD):
        self.push('license', 1)
    _start_creativeCommons_license = _start_creativecommons_license

    def _end_creativecommons_license(self):
        value = self.pop('license')
        context = self._getContext()
        attrsD = FeedParserDict()
        attrsD['rel'] = u'license'
        if value:
            attrsD['href'] = value
        context.setdefault('links', []).append(attrsD)
        del context['license']
    _end_creativeCommons_license = _end_creativecommons_license

    def _addTag(self, term, scheme, label):
        context = self._getContext()
        tags = context.setdefault('tags', [])
        if (not term) and (not scheme) and (not label):
            return
        value = FeedParserDict(term=term, scheme=scheme, label=label)
        if value not in tags:
            tags.append(value)

    def _start_tags(self, attrsD):
        # This is a completely-made up element. Its semantics are determined
        # only by a single feed that precipitated bug report 392 on Google Code.
        # In short, this is junk code.
        self.push('tags', 1)

    def _end_tags(self):
        for term in self.pop('tags').split(','):
            self._addTag(term.strip(), None, None)

    def _start_category(self, attrsD):
        term = attrsD.get('term')
        scheme = attrsD.get('scheme', attrsD.get('domain'))
        label = attrsD.get('label')
        self._addTag(term, scheme, label)
        self.push('category', 1)
    _start_dc_subject = _start_category
    _start_keywords = _start_category

    def _start_media_category(self, attrsD):
        attrsD.setdefault('scheme', u'http://search.yahoo.com/mrss/category_schema')
        self._start_category(attrsD)

    def _end_itunes_keywords(self):
        for term in self.pop('itunes_keywords').split(','):
            if term.strip():
                self._addTag(term.strip(), u'http://www.itunes.com/', None)

    def _end_media_keywords(self):
        for term in self.pop('media_keywords').split(','):
            if term.strip():
                self._addTag(term.strip(), None, None)

    def _start_itunes_category(self, attrsD):
        self._addTag(attrsD.get('text'), u'http://www.itunes.com/', None)
        self.push('category', 1)

    def _end_category(self):
        value = self.pop('category')
        if not value:
            return
        context = self._getContext()
        tags = context['tags']
        if value and len(tags) and not tags[-1]['term']:
            tags[-1]['term'] = value
        else:
            self._addTag(value, None, None)
    _end_dc_subject = _end_category
    _end_keywords = _end_category
    _end_itunes_category = _end_category
    _end_media_category = _end_category

    def _start_cloud(self, attrsD):
        self._getContext()['cloud'] = FeedParserDict(attrsD)

    def _start_link(self, attrsD):
        attrsD.setdefault('rel', u'alternate')
        if attrsD['rel'] == u'self':
            attrsD.setdefault('type', u'application/atom+xml')
        else:
            attrsD.setdefault('type', u'text/html')
        context = self._getContext()
        attrsD = self._itsAnHrefDamnIt(attrsD)
        if 'href' in attrsD:
            attrsD['href'] = self.resolveURI(attrsD['href'])
        expectingText = self.infeed or self.inentry or self.insource
        context.setdefault('links', [])
        if not (self.inentry and self.inimage):
            context['links'].append(FeedParserDict(attrsD))
        if 'href' in attrsD:
            expectingText = 0
            if (attrsD.get('rel') == u'alternate') and (self.mapContentType(attrsD.get('type')) in self.html_types):
                context['link'] = attrsD['href']
        else:
            self.push('link', expectingText)

    def _end_link(self):
        value = self.pop('link')

    def _start_guid(self, attrsD):
        self.guidislink = (attrsD.get('ispermalink', 'true') == 'true')
        self.push('id', 1)
    _start_id = _start_guid

    def _end_guid(self):
        value = self.pop('id')
        self._save('guidislink', self.guidislink and 'link' not in self._getContext())
        if self.guidislink:
            # guid acts as link, but only if 'ispermalink' is not present or is 'true',
            # and only if the item doesn't already have a link element
            self._save('link', value)
    _end_id = _end_guid

    def _start_title(self, attrsD):
        if self.svgOK:
            return self.unknown_starttag('title', attrsD.items())
        self.pushContent('title', attrsD, u'text/plain', self.infeed or self.inentry or self.insource)
    _start_dc_title = _start_title
    _start_media_title = _start_title

    def _end_title(self):
        if self.svgOK:
            return
        value = self.popContent('title')
        if not value:
            return
        self.title_depth = self.depth
    _end_dc_title = _end_title

    def _end_media_title(self):
        title_depth = self.title_depth
        self._end_title()
        self.title_depth = title_depth

    def _start_description(self, attrsD):
        context = self._getContext()
        if 'summary' in context:
            self._summaryKey = 'content'
            self._start_content(attrsD)
        else:
            self.pushContent('description', attrsD, u'text/html', self.infeed or self.inentry or self.insource)
    _start_dc_description = _start_description
    _start_media_description = _start_description

    def _start_abstract(self, attrsD):
        self.pushContent('description', attrsD, u'text/plain', self.infeed or self.inentry or self.insource)

    def _end_description(self):
        if self._summaryKey == 'content':
            self._end_content()
        else:
            value = self.popContent('description')
        self._summaryKey = None
    _end_abstract = _end_description
    _end_dc_description = _end_description
    _end_media_description = _end_description

    def _start_info(self, attrsD):
        self.pushContent('info', attrsD, u'text/plain', 1)
    _start_feedburner_browserfriendly = _start_info

    def _end_info(self):
        self.popContent('info')
    _end_feedburner_browserfriendly = _end_info

    def _start_generator(self, attrsD):
        if attrsD:
            attrsD = self._itsAnHrefDamnIt(attrsD)
            if 'href' in attrsD:
                attrsD['href'] = self.resolveURI(attrsD['href'])
        self._getContext()['generator_detail'] = FeedParserDict(attrsD)
        self.push('generator', 1)

    def _end_generator(self):
        value = self.pop('generator')
        context = self._getContext()
        if 'generator_detail' in context:
            context['generator_detail']['name'] = value

    def _start_admin_generatoragent(self, attrsD):
        self.push('generator', 1)
        value = self._getAttribute(attrsD, 'rdf:resource')
        if value:
            self.elementstack[-1][2].append(value)
        self.pop('generator')
        self._getContext()['generator_detail'] = FeedParserDict({'href': value})

    def _start_admin_errorreportsto(self, attrsD):
        self.push('errorreportsto', 1)
        value = self._getAttribute(attrsD, 'rdf:resource')
        if value:
            self.elementstack[-1][2].append(value)
        self.pop('errorreportsto')

    def _start_summary(self, attrsD):
        context = self._getContext()
        if 'summary' in context:
            self._summaryKey = 'content'
            self._start_content(attrsD)
        else:
            self._summaryKey = 'summary'
            self.pushContent(self._summaryKey, attrsD, u'text/plain', 1)
    _start_itunes_summary = _start_summary

    def _end_summary(self):
        if self._summaryKey == 'content':
            self._end_content()
        else:
            self.popContent(self._summaryKey or 'summary')
        self._summaryKey = None
    _end_itunes_summary = _end_summary

    def _start_enclosure(self, attrsD):
        attrsD = self._itsAnHrefDamnIt(attrsD)
        context = self._getContext()
        attrsD['rel'] = u'enclosure'
        context.setdefault('links', []).append(FeedParserDict(attrsD))

    def _start_source(self, attrsD):
        if 'url' in attrsD:
            # This means that we're processing a source element from an RSS 2.0 feed
            self.sourcedata['href'] = attrsD[u'url']
        self.push('source', 1)
        self.insource = 1
        self.title_depth = -1

    def _end_source(self):
        self.insource = 0
        value = self.pop('source')
        if value:
            self.sourcedata['title'] = value
        self._getContext()['source'] = copy.deepcopy(self.sourcedata)
        self.sourcedata.clear()

    def _start_content(self, attrsD):
        self.pushContent('content', attrsD, u'text/plain', 1)
        src = attrsD.get('src')
        if src:
            self.contentparams['src'] = src
        self.push('content', 1)

    def _start_body(self, attrsD):
        self.pushContent('content', attrsD, u'application/xhtml+xml', 1)
    _start_xhtml_body = _start_body

    def _start_content_encoded(self, attrsD):
        self.pushContent('content', attrsD, u'text/html', 1)
    _start_fullitem = _start_content_encoded

    def _end_content(self):
        copyToSummary = self.mapContentType(self.contentparams.get('type')) in ([u'text/plain'] + self.html_types)
        value = self.popContent('content')
        if copyToSummary:
            self._save('summary', value)

    _end_body = _end_content
    _end_xhtml_body = _end_content
    _end_content_encoded = _end_content
    _end_fullitem = _end_content

    def _start_itunes_image(self, attrsD):
        self.push('itunes_image', 0)
        if attrsD.get('href'):
            self._getContext()['image'] = FeedParserDict({'href': attrsD.get('href')})
        elif attrsD.get('url'):
            self._getContext()['image'] = FeedParserDict({'href': attrsD.get('url')})
    _start_itunes_link = _start_itunes_image

    def _end_itunes_block(self):
        value = self.pop('itunes_block', 0)
        self._getContext()['itunes_block'] = (value == 'yes') and 1 or 0

    def _end_itunes_explicit(self):
        value = self.pop('itunes_explicit', 0)
        # Convert 'yes' -> True, 'clean' to False, and any other value to None
        # False and None both evaluate as False, so the difference can be ignored
        # by applications that only need to know if the content is explicit.
        self._getContext()['itunes_explicit'] = (None, False, True)[(value == 'yes' and 2) or value == 'clean' or 0]

    def _start_media_group(self, attrsD):
        # don't do anything, but don't break the enclosed tags either
        pass

    def _start_media_rating(self, attrsD):
        context = self._getContext()
        context.setdefault('media_rating', attrsD)
        self.push('rating', 1)

    def _end_media_rating(self):
        rating = self.pop('rating')
        if rating is not None and rating.strip():
            context = self._getContext()
            context['media_rating']['content'] = rating

    def _start_media_credit(self, attrsD):
        context = self._getContext()
        context.setdefault('media_credit', [])
        context['media_credit'].append(attrsD)
        self.push('credit', 1)

    def _end_media_credit(self):
        credit = self.pop('credit')
        if credit != None and len(credit.strip()) != 0:
            context = self._getContext()
            context['media_credit'][-1]['content'] = credit

    def _start_media_restriction(self, attrsD):
        context = self._getContext()
        context.setdefault('media_restriction', attrsD)
        self.push('restriction', 1)

    def _end_media_restriction(self):
        restriction = self.pop('restriction')
        if restriction != None and len(restriction.strip()) != 0:
            context = self._getContext()
            context['media_restriction']['content'] = [cc.strip().lower() for cc in restriction.split(' ')]

    def _start_media_license(self, attrsD):
        context = self._getContext()
        context.setdefault('media_license', attrsD)
        self.push('license', 1)

    def _end_media_license(self):
        license = self.pop('license')
        if license != None and len(license.strip()) != 0:
            context = self._getContext()
            context['media_license']['content'] = license

    def _start_media_content(self, attrsD):
        context = self._getContext()
        context.setdefault('media_content', [])
        context['media_content'].append(attrsD)

    def _start_media_thumbnail(self, attrsD):
        context = self._getContext()
        context.setdefault('media_thumbnail', [])
        self.push('url', 1) # new
        context['media_thumbnail'].append(attrsD)

    def _end_media_thumbnail(self):
        url = self.pop('url')
        context = self._getContext()
        if url != None and len(url.strip()) != 0:
            if 'url' not in context['media_thumbnail'][-1]:
                context['media_thumbnail'][-1]['url'] = url

    def _start_media_player(self, attrsD):
        self.push('media_player', 0)
        self._getContext()['media_player'] = FeedParserDict(attrsD)

    def _end_media_player(self):
        value = self.pop('media_player')
        context = self._getContext()
        context['media_player']['content'] = value

    def _start_newlocation(self, attrsD):
        self.push('newlocation', 1)

    def _end_newlocation(self):
        url = self.pop('newlocation')
        context = self._getContext()
        # don't set newlocation if the context isn't right
        if context is not self.feeddata:
            return
        context['newlocation'] = _makeSafeAbsoluteURI(self.baseuri, url.strip())

    def _start_psc_chapters(self, attrsD):
        if self.psc_chapters_flag is None:
	    # Transition from None -> True
            self.psc_chapters_flag = True
            attrsD['chapters'] = []
            self._getContext()['psc_chapters'] = FeedParserDict(attrsD)

    def _end_psc_chapters(self):
        # Transition from True -> False
        self.psc_chapters_flag = False

    def _start_psc_chapter(self, attrsD):
        if self.psc_chapters_flag:
            start = self._getAttribute(attrsD, 'start')
            attrsD['start_parsed'] = _parse_psc_chapter_start(start)

            context = self._getContext()['psc_chapters']
            context['chapters'].append(FeedParserDict(attrsD))


if _XML_AVAILABLE:
    class _StrictFeedParser(_FeedParserMixin, xml.sax.handler.ContentHandler):
        def __init__(self, baseuri, baselang, encoding):
            xml.sax.handler.ContentHandler.__init__(self)
            _FeedParserMixin.__init__(self, baseuri, baselang, encoding)
            self.bozo = 0
            self.exc = None
            self.decls = {}

        def startPrefixMapping(self, prefix, uri):
            if not uri:
                return
            # Jython uses '' instead of None; standardize on None
            prefix = prefix or None
            self.trackNamespace(prefix, uri)
            if prefix and uri == 'http://www.w3.org/1999/xlink':
                self.decls['xmlns:' + prefix] = uri

        def startElementNS(self, name, qname, attrs):
            namespace, localname = name
            lowernamespace = str(namespace or '').lower()
            if lowernamespace.find(u'backend.userland.com/rss') <> -1:
                # match any backend.userland.com namespace
                namespace = u'http://backend.userland.com/rss'
                lowernamespace = namespace
            if qname and qname.find(':') > 0:
                givenprefix = qname.split(':')[0]
            else:
                givenprefix = None
            prefix = self._matchnamespaces.get(lowernamespace, givenprefix)
            if givenprefix and (prefix == None or (prefix == '' and lowernamespace == '')) and givenprefix not in self.namespacesInUse:
                raise UndeclaredNamespace, "'%s' is not associated with a namespace" % givenprefix
            localname = str(localname).lower()

            # qname implementation is horribly broken in Python 2.1 (it
            # doesn't report any), and slightly broken in Python 2.2 (it
            # doesn't report the xml: namespace). So we match up namespaces
            # with a known list first, and then possibly override them with
            # the qnames the SAX parser gives us (if indeed it gives us any
            # at all).  Thanks to MatejC for helping me test this and
            # tirelessly telling me that it didn't work yet.
            attrsD, self.decls = self.decls, {}
            if localname=='math' and namespace=='http://www.w3.org/1998/Math/MathML':
                attrsD['xmlns']=namespace
            if localname=='svg' and namespace=='http://www.w3.org/2000/svg':
                attrsD['xmlns']=namespace

            if prefix:
                localname = prefix.lower() + ':' + localname
            elif namespace and not qname: #Expat
                for name,value in self.namespacesInUse.items():
                    if name and value == namespace:
                        localname = name + ':' + localname
                        break

            for (namespace, attrlocalname), attrvalue in attrs.items():
                lowernamespace = (namespace or '').lower()
                prefix = self._matchnamespaces.get(lowernamespace, '')
                if prefix:
                    attrlocalname = prefix + ':' + attrlocalname
                attrsD[str(attrlocalname).lower()] = attrvalue
            for qname in attrs.getQNames():
                attrsD[str(qname).lower()] = attrs.getValueByQName(qname)
            localname = str(localname).lower()
            self.unknown_starttag(localname, attrsD.items())

        def characters(self, text):
            self.handle_data(text)

        def endElementNS(self, name, qname):
            namespace, localname = name
            lowernamespace = str(namespace or '').lower()
            if qname and qname.find(':') > 0:
                givenprefix = qname.split(':')[0]
            else:
                givenprefix = ''
            prefix = self._matchnamespaces.get(lowernamespace, givenprefix)
            if prefix:
                localname = prefix + ':' + localname
            elif namespace and not qname: #Expat
                for name,value in self.namespacesInUse.items():
                    if name and value == namespace:
                        localname = name + ':' + localname
                        break
            localname = str(localname).lower()
            self.unknown_endtag(localname)

        def error(self, exc):
            self.bozo = 1
            self.exc = exc

        # drv_libxml2 calls warning() in some cases
        warning = error

        def fatalError(self, exc):
            self.error(exc)
            raise exc

class _LooseFeedParser(_FeedParserMixin, _BaseHTMLProcessor):
    def __init__(self, baseuri, baselang, encoding, entities):
        sgmllib.SGMLParser.__init__(self)
        _FeedParserMixin.__init__(self, baseuri, baselang, encoding)
        _BaseHTMLProcessor.__init__(self, encoding, 'application/xhtml+xml')
        self.entities=entities

    def decodeEntities(self, element, data):
        data = data.replace('&#60;', '&lt;')
        data = data.replace('&#x3c;', '&lt;')
        data = data.replace('&#x3C;', '&lt;')
        data = data.replace('&#62;', '&gt;')
        data = data.replace('&#x3e;', '&gt;')
        data = data.replace('&#x3E;', '&gt;')
        data = data.replace('&#38;', '&amp;')
        data = data.replace('&#x26;', '&amp;')
        data = data.replace('&#34;', '&quot;')
        data = data.replace('&#x22;', '&quot;')
        data = data.replace('&#39;', '&apos;')
        data = data.replace('&#x27;', '&apos;')
        if not self.contentparams.get('type', u'xml').endswith(u'xml'):
            data = data.replace('&lt;', '<')
            data = data.replace('&gt;', '>')
            data = data.replace('&amp;', '&')
            data = data.replace('&quot;', '"')
            data = data.replace('&apos;', "'")
            data = data.replace('&#x2f;', '/')
            data = data.replace('&#x2F;', '/')
        return data

    def strattrs(self, attrs):
        return ''.join([' %s="%s"' % (n,v.replace('"','&quot;')) for n,v in attrs])

def _open_resource(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers):
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
        return url_file_stream_or_string

    if isinstance(url_file_stream_or_string, basestring) \
       and urlparse.urlparse(url_file_stream_or_string)[0] in ('http', 'https', 'ftp', 'file', 'feed'):
        # Deal with the feed URI scheme
        if url_file_stream_or_string.startswith('feed:http'):
            url_file_stream_or_string = url_file_stream_or_string[5:]
        elif url_file_stream_or_string.startswith('feed:'):
            url_file_stream_or_string = 'http:' + url_file_stream_or_string[5:]
        if not agent:
            agent = USER_AGENT
        # Test for inline user:password credentials for HTTP basic auth
        auth = None
        if base64 and not url_file_stream_or_string.startswith('ftp:'):
            urltype, rest = urllib.splittype(url_file_stream_or_string)
            realhost, rest = urllib.splithost(rest)
            if realhost:
                user_passwd, realhost = urllib.splituser(realhost)
                if user_passwd:
                    url_file_stream_or_string = '%s://%s%s' % (urltype, realhost, rest)
                    auth = base64.standard_b64encode(user_passwd).strip()

        # iri support
        if isinstance(url_file_stream_or_string, unicode):
            url_file_stream_or_string = _convert_to_idn(url_file_stream_or_string)

        # try to open with urllib2 (to use optional headers)
        request = _build_urllib2_request(url_file_stream_or_string, agent, ACCEPT_HEADER, etag, modified, referrer, auth, request_headers)
        opener = urllib2.build_opener(*tuple(handlers + [_FeedURLHandler()]))
        opener.addheaders = [] # RMK - must clear so we only send our custom User-Agent
        try:
            return opener.open(request)
        finally:
            opener.close() # JohnD

    # try to open with native open function (if url_file_stream_or_string is a filename)
    try:
        return open(url_file_stream_or_string, 'rb')
    except (IOError, UnicodeEncodeError, TypeError):
        # if url_file_stream_or_string is a unicode object that
        # cannot be converted to the encoding returned by
        # sys.getfilesystemencoding(), a UnicodeEncodeError
        # will be thrown
        # If url_file_stream_or_string is a string that contains NULL
        # (such as an XML document encoded in UTF-32), TypeError will
        # be thrown.
        pass

    # treat url_file_stream_or_string as string
    if isinstance(url_file_stream_or_string, unicode):
        return _StringIO(url_file_stream_or_string.encode('utf-8'))
    return _StringIO(url_file_stream_or_string)

def _parse_psc_chapter_start(start):
    FORMAT = r'^((\d{2}):)?(\d{2}):(\d{2})(\.(\d{3}))?$'

    m = re.compile(FORMAT).match(start)
    if m is None:
        return None

    _, h, m, s, _, ms = m.groups()
    h, m, s, ms = (int(h or 0), int(m), int(s), int(ms or 0))
    return datetime.timedelta(0, h*60*60 + m*60 + s, ms*1000)

# Each marker represents some of the characters of the opening XML
# processing instruction ('<?xm') in the specified encoding.
EBCDIC_MARKER = _l2bytes([0x4C, 0x6F, 0xA7, 0x94])
UTF16BE_MARKER = _l2bytes([0x00, 0x3C, 0x00, 0x3F])
UTF16LE_MARKER = _l2bytes([0x3C, 0x00, 0x3F, 0x00])
UTF32BE_MARKER = _l2bytes([0x00, 0x00, 0x00, 0x3C])
UTF32LE_MARKER = _l2bytes([0x3C, 0x00, 0x00, 0x00])

ZERO_BYTES = _l2bytes([0x00, 0x00])

# Match the opening XML declaration.
# Example: <?xml version="1.0" encoding="utf-8"?>
RE_XML_DECLARATION = re.compile('^<\?xml[^>]*?>')

# Capture the value of the XML processing instruction's encoding attribute.
# Example: <?xml version="1.0" encoding="utf-8"?>
RE_XML_PI_ENCODING = re.compile(_s2bytes('^<\?.*encoding=[\'"](.*?)[\'"].*\?>'))

def convert_to_utf8(http_headers, data):
    '''Detect and convert the character encoding to UTF-8.

    http_headers is a dictionary
    data is a raw string (not Unicode)'''

    # This is so much trickier than it sounds, it's not even funny.
    # According to RFC 3023 ('XML Media Types'), if the HTTP Content-Type
    # is application/xml, application/*+xml,
    # application/xml-external-parsed-entity, or application/xml-dtd,
    # the encoding given in the charset parameter of the HTTP Content-Type
    # takes precedence over the encoding given in the XML prefix within the
    # document, and defaults to 'utf-8' if neither are specified.  But, if
    # the HTTP Content-Type is text/xml, text/*+xml, or
    # text/xml-external-parsed-entity, the encoding given in the XML prefix
    # within the document is ALWAYS IGNORED and only the encoding given in
    # the charset parameter of the HTTP Content-Type header should be
    # respected, and it defaults to 'us-ascii' if not specified.

    # Furthermore, discussion on the atom-syntax mailing list with the
    # author of RFC 3023 leads me to the conclusion that any document
    # served with a Content-Type of text/* and no charset parameter
    # must be treated as us-ascii.  (We now do this.)  And also that it
    # must always be flagged as non-well-formed.  (We now do this too.)

    # If Content-Type is unspecified (input was local file or non-HTTP source)
    # or unrecognized (server just got it totally wrong), then go by the
    # encoding given in the XML prefix of the document and default to
    # 'iso-8859-1' as per the HTTP specification (RFC 2616).

    # Then, assuming we didn't find a character encoding in the HTTP headers
    # (and the HTTP Content-type allowed us to look in the body), we need
    # to sniff the first few bytes of the XML data and try to determine
    # whether the encoding is ASCII-compatible.  Section F of the XML
    # specification shows the way here:
    # http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info

    # If the sniffed encoding is not ASCII-compatible, we need to make it
    # ASCII compatible so that we can sniff further into the XML declaration
    # to find the encoding attribute, which will tell us the true encoding.

    # Of course, none of this guarantees that we will be able to parse the
    # feed in the declared character encoding (assuming it was declared
    # correctly, which many are not).  iconv_codec can help a lot;
    # you should definitely install it if you can.
    # http://cjkpython.i18n.org/

    bom_encoding = u''
    xml_encoding = u''
    rfc3023_encoding = u''

    # Look at the first few bytes of the document to guess what
    # its encoding may be. We only need to decode enough of the
    # document that we can use an ASCII-compatible regular
    # expression to search for an XML encoding declaration.
    # The heuristic follows the XML specification, section F:
    # http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info
    # Check for BOMs first.
    if data[:4] == codecs.BOM_UTF32_BE:
        bom_encoding = u'utf-32be'
        data = data[4:]
    elif data[:4] == codecs.BOM_UTF32_LE:
        bom_encoding = u'utf-32le'
        data = data[4:]
    elif data[:2] == codecs.BOM_UTF16_BE and data[2:4] != ZERO_BYTES:
        bom_encoding = u'utf-16be'
        data = data[2:]
    elif data[:2] == codecs.BOM_UTF16_LE and data[2:4] != ZERO_BYTES:
        bom_encoding = u'utf-16le'
        data = data[2:]
    elif data[:3] == codecs.BOM_UTF8:
        bom_encoding = u'utf-8'
        data = data[3:]
    # Check for the characters '<?xm' in several encodings.
    elif data[:4] == EBCDIC_MARKER:
        bom_encoding = u'cp037'
    elif data[:4] == UTF16BE_MARKER:
        bom_encoding = u'utf-16be'
    elif data[:4] == UTF16LE_MARKER:
        bom_encoding = u'utf-16le'
    elif data[:4] == UTF32BE_MARKER:
        bom_encoding = u'utf-32be'
    elif data[:4] == UTF32LE_MARKER:
        bom_encoding = u'utf-32le'

    tempdata = data
    try:
        if bom_encoding:
            tempdata = data.decode(bom_encoding).encode('utf-8')
    except (UnicodeDecodeError, LookupError):
        # feedparser recognizes UTF-32 encodings that aren't
        # available in Python 2.4 and 2.5, so it's possible to
        # encounter a LookupError during decoding.
        xml_encoding_match = None
    else:
        xml_encoding_match = RE_XML_PI_ENCODING.match(tempdata)

    if xml_encoding_match:
        xml_encoding = xml_encoding_match.groups()[0].decode('utf-8').lower()
        # Normalize the xml_encoding if necessary.
        if bom_encoding and (xml_encoding in (
            u'u16', u'utf-16', u'utf16', u'utf_16',
            u'u32', u'utf-32', u'utf32', u'utf_32',
            u'iso-10646-ucs-2', u'iso-10646-ucs-4',
            u'csucs4', u'csunicode', u'ucs-2', u'ucs-4'
        )):
            xml_encoding = bom_encoding

    # Find the HTTP Content-Type and, hopefully, a character
    # encoding provided by the server. The Content-Type is used
    # to choose the "correct" encoding among the BOM encoding,
    # XML declaration encoding, and HTTP encoding, following the
    # heuristic defined in RFC 3023.
    http_content_type = http_headers.get('content-type') or ''
    http_content_type, params = cgi.parse_header(http_content_type)
    http_encoding = params.get('charset', '').replace("'", "")
    if not isinstance(http_encoding, unicode):
        http_encoding = http_encoding.decode('utf-8', 'ignore')

    acceptable_content_type = 0
    application_content_types = (u'application/xml', u'application/xml-dtd',
                                 u'application/xml-external-parsed-entity')
    text_content_types = (u'text/xml', u'text/xml-external-parsed-entity')
    if (http_content_type in application_content_types) or \
       (http_content_type.startswith(u'application/') and
        http_content_type.endswith(u'+xml')):
        acceptable_content_type = 1
        rfc3023_encoding = http_encoding or xml_encoding or u'utf-8'
    elif (http_content_type in text_content_types) or \
         (http_content_type.startswith(u'text/') and
          http_content_type.endswith(u'+xml')):
        acceptable_content_type = 1
        rfc3023_encoding = http_encoding or u'us-ascii'
    elif http_content_type.startswith(u'text/'):
        rfc3023_encoding = http_encoding or u'us-ascii'
    elif http_headers and 'content-type' not in http_headers:
        rfc3023_encoding = xml_encoding or u'iso-8859-1'
    else:
        rfc3023_encoding = xml_encoding or u'utf-8'
    # gb18030 is a superset of gb2312, so always replace gb2312
    # with gb18030 for greater compatibility.
    if rfc3023_encoding.lower() == u'gb2312':
        rfc3023_encoding = u'gb18030'
    if xml_encoding.lower() == u'gb2312':
        xml_encoding = u'gb18030'

    # there are four encodings to keep track of:
    # - http_encoding is the encoding declared in the Content-Type HTTP header
    # - xml_encoding is the encoding declared in the <?xml declaration
    # - bom_encoding is the encoding sniffed from the first 4 bytes of the XML data
    # - rfc3023_encoding is the actual encoding, as per RFC 3023 and a variety of other conflicting specifications
    error = None

    if http_headers and (not acceptable_content_type):
        if 'content-type' in http_headers:
            msg = '%s is not an XML media type' % http_headers['content-type']
        else:
            msg = 'no Content-type specified'
        error = NonXMLContentType(msg)

    # determine character encoding
    known_encoding = 0
    lazy_chardet_encoding = None
    tried_encodings = []
    if chardet:
        def lazy_chardet_encoding():
            chardet_encoding = chardet.detect(data)['encoding']
            if not chardet_encoding:
                chardet_encoding = ''
            if not isinstance(chardet_encoding, unicode):
                chardet_encoding = unicode(chardet_encoding, 'ascii', 'ignore')
            return chardet_encoding
    # try: HTTP encoding, declared XML encoding, encoding sniffed from BOM
    for proposed_encoding in (rfc3023_encoding, xml_encoding, bom_encoding,
                              lazy_chardet_encoding, u'utf-8', u'windows-1252', u'iso-8859-2'):
        if callable(proposed_encoding):
            proposed_encoding = proposed_encoding()
        if not proposed_encoding:
            continue
        if proposed_encoding in tried_encodings:
            continue
        tried_encodings.append(proposed_encoding)
        try:
            data = data.decode(proposed_encoding)
        except (UnicodeDecodeError, LookupError):
            pass
        else:
            known_encoding = 1
            # Update the encoding in the opening XML processing instruction.
            new_declaration = '''<?xml version='1.0' encoding='utf-8'?>'''
            if RE_XML_DECLARATION.search(data):
                data = RE_XML_DECLARATION.sub(new_declaration, data)
            else:
                data = new_declaration + u'\n' + data
            data = data.encode('utf-8')
            break
    # if still no luck, give up
    if not known_encoding:
        error = CharacterEncodingUnknown(
            'document encoding unknown, I tried ' +
            '%s, %s, utf-8, windows-1252, and iso-8859-2 but nothing worked' %
            (rfc3023_encoding, xml_encoding))
        rfc3023_encoding = u''
    elif proposed_encoding != rfc3023_encoding:
        error = CharacterEncodingOverride(
            'document declared as %s, but parsed as %s' %
            (rfc3023_encoding, proposed_encoding))
        rfc3023_encoding = proposed_encoding

    return data, rfc3023_encoding, error

# Match XML entity declarations.
# Example: <!ENTITY copyright "(C)">
RE_ENTITY_PATTERN = re.compile(_s2bytes(r'^\s*<!ENTITY([^>]*?)>'), re.MULTILINE)

# Match XML DOCTYPE declarations.
# Example: <!DOCTYPE feed [ ]>
RE_DOCTYPE_PATTERN = re.compile(_s2bytes(r'^\s*<!DOCTYPE([^>]*?)>'), re.MULTILINE)

# Match safe entity declarations.
# This will allow hexadecimal character references through,
# as well as text, but not arbitrary nested entities.
# Example: cubed "&#179;"
# Example: copyright "(C)"
# Forbidden: explode1 "&explode2;&explode2;"
RE_SAFE_ENTITY_PATTERN = re.compile(_s2bytes('\s+(\w+)\s+"(&#\w+;|[^&"]*)"'))

def replace_doctype(data):
    '''Strips and replaces the DOCTYPE, returns (rss_version, stripped_data)

    rss_version may be 'rss091n' or None
    stripped_data is the same XML document with a replaced DOCTYPE
    '''

    # Divide the document into two groups by finding the location
    # of the first element that doesn't begin with '<?' or '<!'.
    start = re.search(_s2bytes('<\w'), data)
    start = start and start.start() or -1
    head, data = data[:start+1], data[start+1:]

    # Save and then remove all of the ENTITY declarations.
    entity_results = RE_ENTITY_PATTERN.findall(head)
    head = RE_ENTITY_PATTERN.sub(_s2bytes(''), head)

    # Find the DOCTYPE declaration and check the feed type.
    doctype_results = RE_DOCTYPE_PATTERN.findall(head)
    doctype = doctype_results and doctype_results[0] or _s2bytes('')
    if _s2bytes('netscape') in doctype.lower():
        version = u'rss091n'
    else:
        version = None

    # Re-insert the safe ENTITY declarations if a DOCTYPE was found.
    replacement = _s2bytes('')
    if len(doctype_results) == 1 and entity_results:
        match_safe_entities = lambda e: RE_SAFE_ENTITY_PATTERN.match(e)
        safe_entities = filter(match_safe_entities, entity_results)
        if safe_entities:
            replacement = _s2bytes('<!DOCTYPE feed [\n<!ENTITY') \
                        + _s2bytes('>\n<!ENTITY ').join(safe_entities) \
                        + _s2bytes('>\n]>')
    data = RE_DOCTYPE_PATTERN.sub(replacement, head) + data

    # Precompute the safe entities for the loose parser.
    safe_entities = dict((k.decode('utf-8'), v.decode('utf-8'))
                      for k, v in RE_SAFE_ENTITY_PATTERN.findall(replacement))
    return version, data, safe_entities


# GeoRSS geometry parsers. Each return a dict with 'type' and 'coordinates'
# items, or None in the case of a parsing error.

def _parse_poslist(value, geom_type, swap=True, dims=2):
    if geom_type == 'linestring':
        return _parse_georss_line(value, swap, dims)
    elif geom_type == 'polygon':
        ring = _parse_georss_line(value, swap, dims)
        return {'type': u'Polygon', 'coordinates': (ring['coordinates'],)}
    else:
        return None

def _gen_georss_coords(value, swap=True, dims=2):
    # A generator of (lon, lat) pairs from a string of encoded GeoRSS
    # coordinates. Converts to floats and swaps order.
    latlons = itertools.imap(float, value.strip().replace(',', ' ').split())
    nxt = latlons.next
    while True:
        t = [nxt(), nxt()][::swap and -1 or 1]
        if dims == 3:
            t.append(nxt())
        yield tuple(t)

def _parse_georss_point(value, swap=True, dims=2):
    # A point contains a single latitude-longitude pair, separated by
    # whitespace. We'll also handle comma separators.
    try:
        coords = list(_gen_georss_coords(value, swap, dims))
        return {u'type': u'Point', u'coordinates': coords[0]}
    except (IndexError, ValueError):
        return None

def _parse_georss_line(value, swap=True, dims=2):
    # A line contains a space separated list of latitude-longitude pairs in
    # WGS84 coordinate reference system, with each pair separated by
    # whitespace. There must be at least two pairs.
    try:
        coords = list(_gen_georss_coords(value, swap, dims))
        return {u'type': u'LineString', u'coordinates': coords}
    except (IndexError, ValueError):
        return None

def _parse_georss_polygon(value, swap=True, dims=2):
    # A polygon contains a space separated list of latitude-longitude pairs,
    # with each pair separated by whitespace. There must be at least four
    # pairs, with the last being identical to the first (so a polygon has a
    # minimum of three actual points).
    try:
        ring = list(_gen_georss_coords(value, swap, dims))
    except (IndexError, ValueError):
        return None
    if len(ring) < 4:
        return None
    return {u'type': u'Polygon', u'coordinates': (ring,)}

def _parse_georss_box(value, swap=True, dims=2):
    # A bounding box is a rectangular region, often used to define the extents
    # of a map or a rough area of interest. A box contains two space seperate
    # latitude-longitude pairs, with each pair separated by whitespace. The
    # first pair is the lower corner, the second is the upper corner.
    try:
        coords = list(_gen_georss_coords(value, swap, dims))
        return {u'type': u'Box', u'coordinates': tuple(coords)}
    except (IndexError, ValueError):
        return None

# end geospatial parsers


def parse(url_file_stream_or_string, etag=None, modified=None, agent=None, referrer=None, handlers=None, request_headers=None, response_headers=None):
    '''Parse a feed from a URL, file, stream, or string.

    request_headers, if given, is a dict from http header name to value to add
    to the request; this overrides internally generated values.

    :return: A :class:`FeedParserDict`.
    '''

    if handlers is None:
        handlers = []
    if request_headers is None:
        request_headers = {}
    if response_headers is None:
        response_headers = {}

    result = FeedParserDict()
    result['feed'] = FeedParserDict()
    result['entries'] = []
    result['bozo'] = 0
    if not isinstance(handlers, list):
        handlers = [handlers]
    try:
        f = _open_resource(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers)
        data = f.read()
    except Exception, e:
        result['bozo'] = 1
        result['bozo_exception'] = e
        data = None
        f = None

    if hasattr(f, 'headers'):
        result['headers'] = dict(f.headers)
    # overwrite existing headers using response_headers
    if 'headers' in result:
        result['headers'].update(response_headers)
    elif response_headers:
        result['headers'] = copy.deepcopy(response_headers)

    # lowercase all of the HTTP headers for comparisons per RFC 2616
    if 'headers' in result:
        http_headers = dict((k.lower(), v) for k, v in result['headers'].items())
    else:
        http_headers = {}

    # if feed is gzip-compressed, decompress it
    if f and data and http_headers:
        if gzip and 'gzip' in http_headers.get('content-encoding', ''):
            try:
                data = gzip.GzipFile(fileobj=_StringIO(data)).read()
            except (IOError, struct.error), e:
                # IOError can occur if the gzip header is bad.
                # struct.error can occur if the data is damaged.
                result['bozo'] = 1
                result['bozo_exception'] = e
                if isinstance(e, struct.error):
                    # A gzip header was found but the data is corrupt.
                    # Ideally, we should re-request the feed without the
                    # 'Accept-encoding: gzip' header, but we don't.
                    data = None
        elif zlib and 'deflate' in http_headers.get('content-encoding', ''):
            try:
                data = zlib.decompress(data)
            except zlib.error, e:
                try:
                    # The data may have no headers and no checksum.
                    data = zlib.decompress(data, -15)
                except zlib.error, e:
                    result['bozo'] = 1
                    result['bozo_exception'] = e

    # save HTTP headers
    if http_headers:
        if 'etag' in http_headers:
            etag = http_headers.get('etag', u'')
            if not isinstance(etag, unicode):
                etag = etag.decode('utf-8', 'ignore')
            if etag:
                result['etag'] = etag
        if 'last-modified' in http_headers:
            modified = http_headers.get('last-modified', u'')
            if modified:
                result['modified'] = modified
                result['modified_parsed'] = _parse_date(modified)
    if hasattr(f, 'url'):
        if not isinstance(f.url, unicode):
            result['href'] = f.url.decode('utf-8', 'ignore')
        else:
            result['href'] = f.url
        result['status'] = 200
    if hasattr(f, 'status'):
        result['status'] = f.status
    if hasattr(f, 'close'):
        f.close()

    if data is None:
        return result

    # Stop processing if the server sent HTTP 304 Not Modified.
    if getattr(f, 'code', 0) == 304:
        result['version'] = u''
        result['debug_message'] = 'The feed has not changed since you last checked, ' + \
            'so the server sent no data.  This is a feature, not a bug!'
        return result

    data, result['encoding'], error = convert_to_utf8(http_headers, data)
    use_strict_parser = result['encoding'] and True or False
    if error is not None:
        result['bozo'] = 1
        result['bozo_exception'] = error

    result['version'], data, entities = replace_doctype(data)

    # Ensure that baseuri is an absolute URI using an acceptable URI scheme.
    contentloc = http_headers.get('content-location', u'')
    href = result.get('href', u'')
    baseuri = _makeSafeAbsoluteURI(href, contentloc) or _makeSafeAbsoluteURI(contentloc) or href

    baselang = http_headers.get('content-language', None)
    if not isinstance(baselang, unicode) and baselang is not None:
        baselang = baselang.decode('utf-8', 'ignore')

    if not _XML_AVAILABLE:
        use_strict_parser = 0
    if use_strict_parser:
        # initialize the SAX parser
        feedparser = _StrictFeedParser(baseuri, baselang, 'utf-8')
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
        except xml.sax.SAXException, e:
            result['bozo'] = 1
            result['bozo_exception'] = feedparser.exc or e
            use_strict_parser = 0
    if not use_strict_parser and _SGML_AVAILABLE:
        feedparser = _LooseFeedParser(baseuri, baselang, 'utf-8', entities)
        feedparser.feed(data.decode('utf-8', 'replace'))
    result['feed'] = feedparser.feeddata
    result['entries'] = feedparser.entries
    result['version'] = result['version'] or feedparser.version
    result['namespaces'] = feedparser.namespacesInUse
    return result

# The list of EPSG codes for geographic (latitude/longitude) coordinate
# systems to support decoding of GeoRSS GML profiles.
_geogCS = [
3819, 3821, 3824, 3889, 3906, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008,
4009, 4010, 4011, 4012, 4013, 4014, 4015, 4016, 4018, 4019, 4020, 4021, 4022,
4023, 4024, 4025, 4027, 4028, 4029, 4030, 4031, 4032, 4033, 4034, 4035, 4036,
4041, 4042, 4043, 4044, 4045, 4046, 4047, 4052, 4053, 4054, 4055, 4075, 4081,
4120, 4121, 4122, 4123, 4124, 4125, 4126, 4127, 4128, 4129, 4130, 4131, 4132,
4133, 4134, 4135, 4136, 4137, 4138, 4139, 4140, 4141, 4142, 4143, 4144, 4145,
4146, 4147, 4148, 4149, 4150, 4151, 4152, 4153, 4154, 4155, 4156, 4157, 4158,
4159, 4160, 4161, 4162, 4163, 4164, 4165, 4166, 4167, 4168, 4169, 4170, 4171,
4172, 4173, 4174, 4175, 4176, 4178, 4179, 4180, 4181, 4182, 4183, 4184, 4185,
4188, 4189, 4190, 4191, 4192, 4193, 4194, 4195, 4196, 4197, 4198, 4199, 4200,
4201, 4202, 4203, 4204, 4205, 4206, 4207, 4208, 4209, 4210, 4211, 4212, 4213,
4214, 4215, 4216, 4218, 4219, 4220, 4221, 4222, 4223, 4224, 4225, 4226, 4227,
4228, 4229, 4230, 4231, 4232, 4233, 4234, 4235, 4236, 4237, 4238, 4239, 4240,
4241, 4242, 4243, 4244, 4245, 4246, 4247, 4248, 4249, 4250, 4251, 4252, 4253,
4254, 4255, 4256, 4257, 4258, 4259, 4260, 4261, 4262, 4263, 4264, 4265, 4266,
4267, 4268, 4269, 4270, 4271, 4272, 4273, 4274, 4275, 4276, 4277, 4278, 4279,
4280, 4281, 4282, 4283, 4284, 4285, 4286, 4287, 4288, 4289, 4291, 4292, 4293,
4294, 4295, 4296, 4297, 4298, 4299, 4300, 4301, 4302, 4303, 4304, 4306, 4307,
4308, 4309, 4310, 4311, 4312, 4313, 4314, 4315, 4316, 4317, 4318, 4319, 4322,
4324, 4326, 4463, 4470, 4475, 4483, 4490, 4555, 4558, 4600, 4601, 4602, 4603,
4604, 4605, 4606, 4607, 4608, 4609, 4610, 4611, 4612, 4613, 4614, 4615, 4616,
4617, 4618, 4619, 4620, 4621, 4622, 4623, 4624, 4625, 4626, 4627, 4628, 4629,
4630, 4631, 4632, 4633, 4634, 4635, 4636, 4637, 4638, 4639, 4640, 4641, 4642,
4643, 4644, 4645, 4646, 4657, 4658, 4659, 4660, 4661, 4662, 4663, 4664, 4665,
4666, 4667, 4668, 4669, 4670, 4671, 4672, 4673, 4674, 4675, 4676, 4677, 4678,
4679, 4680, 4681, 4682, 4683, 4684, 4685, 4686, 4687, 4688, 4689, 4690, 4691,
4692, 4693, 4694, 4695, 4696, 4697, 4698, 4699, 4700, 4701, 4702, 4703, 4704,
4705, 4706, 4707, 4708, 4709, 4710, 4711, 4712, 4713, 4714, 4715, 4716, 4717,
4718, 4719, 4720, 4721, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730,
4731, 4732, 4733, 4734, 4735, 4736, 4737, 4738, 4739, 4740, 4741, 4742, 4743,
4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752, 4753, 4754, 4755, 4756,
4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4801, 4802, 4803, 4804,
4805, 4806, 4807, 4808, 4809, 4810, 4811, 4813, 4814, 4815, 4816, 4817, 4818,
4819, 4820, 4821, 4823, 4824, 4901, 4902, 4903, 4904, 4979 ]
