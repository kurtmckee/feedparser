# Shared code that is common to the strict and loose feed parsers
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

import copy
import re

from xml.sax.saxutils import escape as _xmlescape

# base64 support for Atom feeds that contain embedded binary data
try:
    import base64, binascii
except ImportError:
    base64 = binascii = None
else:
    # Python 3.1 deprecates decodestring in favor of decodebytes
    _base64decode = getattr(base64, 'decodebytes', base64.decodestring)

try:
    from html.entities import entitydefs
except ImportError:
    from htmlentitydefs import entitydefs

from .html import _cp1252
from .namespaces import _base, cc, dc, georss, itunes, mediarss, psc
from .sanitizer import _sanitizeHTML, _HTMLSanitizer
from .util import FeedParserDict
from .urls import _urljoin, _resolveRelativeURIs

bytes_ = type(b'')

class _FeedParserMixin(
        _base.Namespace,
        cc.Namespace,
        dc.Namespace,
        georss.Namespace,
        itunes.Namespace,
        mediarss.Namespace,
        psc.Namespace,
):
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
        'http://creativecommons.org/ns#license':                 'cc',
        'http://web.resource.org/cc/':                           'cc',
        'http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html': 'creativeCommons',
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
    html_types = ['text/html', 'application/xhtml+xml']

    def __init__(self):
        if not self._matchnamespaces:
            for k, v in self.namespaces.items():
                self._matchnamespaces[k.lower()] = v
        self.feeddata = FeedParserDict() # feed-level data
        self.entries = [] # list of entry-level data
        self.version = '' # feed type/version, see SUPPORTED_VERSIONS
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

        self.sourcedata = FeedParserDict()
        self.contentparams = FeedParserDict()
        self._summaryKey = None
        self.namespacemap = {}
        self.elementstack = []
        self.basestack = []
        self.langstack = []
        self.svgOK = 0
        self.title_depth = -1
        self.depth = 0
        if self.lang:
            self.feeddata['language'] = self.lang.replace('_','-')

        # A map of the following form:
        #     {
        #         object_that_value_is_set_on: {
        #             property_name: depth_of_node_property_was_extracted_from,
        #             other_property: depth_of_node_property_was_extracted_from,
        #         },
        #     }
        self.property_depth_map = {}
        super(_FeedParserMixin, self).__init__()

    def mapContentType(self, contentType):
        contentType = contentType.lower()
        if contentType == 'text' or contentType == 'plain':
            contentType = 'text/plain'
        elif contentType == 'html':
            contentType = 'text/html'
        elif contentType == 'xhtml':
            contentType = 'application/xhtml+xml'
        return contentType

    def trackNamespace(self, prefix, uri):
        loweruri = uri.lower()
        if not self.version:
            if (prefix, loweruri) == (None, 'http://my.netscape.com/rdf/simple/0.9/'):
                self.version = 'rss090'
            elif loweruri == 'http://purl.org/rss/1.0/':
                self.version = 'rss10'
            elif loweruri == 'http://www.w3.org/2005/atom':
                self.version = 'atom10'
        if loweruri.find('backend.userland.com/rss') != -1:
            # match any backend.userland.com namespace
            uri = 'http://backend.userland.com/rss'
            loweruri = uri
        if loweruri in self._matchnamespaces:
            self.namespacemap[prefix] = self._matchnamespaces[loweruri]
            self.namespacesInUse[self._matchnamespaces[loweruri]] = uri
        else:
            self.namespacesInUse[prefix or ''] = uri

    def resolveURI(self, uri):
        return _urljoin(self.baseuri or '', uri)

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

        if self.version == 'atom10' and self.contentparams.get('type', 'text') == 'application/xhtml+xml':
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
            if isinstance(v, bytes_):
                pieces[i] = v.decode('utf-8')

        output = ''.join(pieces)
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
        if not self.version.startswith('atom') and self.contentparams.get('type') == 'text/plain':
            if self.lookslikehtml(output):
                self.contentparams['type'] = 'text/html'

        # remove temporary cruft from contentparams
        try:
            del self.contentparams['mode']
        except KeyError:
            pass
        try:
            del self.contentparams['base64']
        except KeyError:
            pass

        is_htmlish = self.mapContentType(self.contentparams.get('type', 'text/html')) in self.html_types
        # resolve relative URIs within embedded markup
        if is_htmlish and RESOLVE_RELATIVE_URIS:
            if element in self.can_contain_relative_uris:
                output = _resolveRelativeURIs(output, self.baseuri, self.encoding, self.contentparams.get('type', 'text/html'))

        # sanitize embedded markup
        if is_htmlish and SANITIZE_HTML:
            if element in self.can_contain_dangerous_markup:
                output = _sanitizeHTML(output, self.encoding, self.contentparams.get('type', 'text/html'))

        if self.encoding and isinstance(output, bytes_):
            output = output.decode(self.encoding, 'ignore')

        # address common error where people take data that is already
        # utf-8, presume that it is iso-8859-1, and re-encode it.
        if self.encoding in ('utf-8', 'utf-8_INVALID_PYTHON_3') and not isinstance(output, bytes_):
            try:
                output = output.encode('iso-8859-1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

        # map win-1252 extensions to the proper code points
        if not isinstance(output, bytes_):
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
        if not (re.search(r'</(\w+)>', s) or re.search(r'&#?\w+;', s)):
            return

        # all tags must be in a restricted subset of valid HTML tags
        if any((t for t in re.findall(r'</?(\w+)', s) if t.lower() not in _HTMLSanitizer.acceptable_elements)):
            return

        # all entities must have been defined as valid HTML entities
        if any((e for e in re.findall(r'&(\w+);', s) if e not in entitydefs)):
            return

        return 1

    def _mapToStandardPrefix(self, name):
        colonpos = name.find(':')
        if colonpos != -1:
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
        if self.contentparams['type'].startswith('text/'):
            return 0
        if self.contentparams['type'].endswith('+xml'):
            return 0
        if self.contentparams['type'].endswith('/xml'):
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
                context[key] = '%s (%s)' % (name, email)
            elif name:
                context[key] = name
            elif email:
                context[key] = email
        else:
            author, email = context.get(key), None
            if not author:
                return
            emailmatch = re.search(r'''(([a-zA-Z0-9\_\-\.\+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?))(\?subject=\S+)?''', author)
            if emailmatch:
                email = emailmatch.group(0)
                # probably a better way to do the following, but it passes all the tests
                author = author.replace(email, '')
                author = author.replace('()', '')
                author = author.replace('<>', '')
                author = author.replace('&lt;&gt;', '')
                author = author.strip()
                if author and (author[0] == '('):
                    author = author[1:]
                if author and (author[-1] == ')'):
                    author = author[:-1]
                author = author.strip()
            if author or email:
                context.setdefault('%s_detail' % key, detail)
            if author:
                detail['name'] = author
            if email:
                detail['email'] = email

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
