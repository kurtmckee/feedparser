# The strict feed parser that interfaces with an XML parsing library
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

from xml.sax.saxutils import escape as _xmlescape

from ..urls import _urljoin, _makeSafeAbsoluteURI

bytes_ = type(b'')

class _StrictFeedParser(object):
    def __init__(self, baseuri, baselang, encoding):
        self.bozo = 0
        self.exc = None
        self.decls = {}
        self.baseuri = baseuri or ''
        self.lang = baselang
        self.encoding = encoding
        super(_StrictFeedParser, self).__init__()

    def _normalize_attributes(self, kv):
        k = kv[0]
        v = k in ('rel', 'type') and kv[1].lower() or kv[1]
        return (k, v)

    def startPrefixMapping(self, prefix, uri):
        if not uri:
            return
        self.trackNamespace(prefix, uri)
        if prefix and uri == 'http://www.w3.org/1999/xlink':
            self.decls['xmlns:' + prefix] = uri

    def startElementNS(self, name, qname, attrs):
        uri, localname = name
        localname = localname.lower()
        loweruri = (uri or '').lower()
        prefix = self._matchnamespaces.get(loweruri)

        attrsD, self.decls = self.decls, {}
        if localname == 'math' and uri == 'http://www.w3.org/1998/Math/MathML':
            attrsD['xmlns'] = uri
        if localname == 'svg' and uri == 'http://www.w3.org/2000/svg':
            attrsD['xmlns'] = uri

        for key, value in self.namespacesInUse.items():
            if key and value == uri:
                localname = '{prefix}:{localname}'.format(
                    prefix=key.lower(), localname=localname
                )
                break

        for (uri, attrlocalname), attrvalue in attrs.items():
            loweruri = (uri or '').lower()
            prefix = self._matchnamespaces.get(loweruri)
            if prefix:
                attrlocalname = '{prefix}:{localname}'.format(
                    prefix=prefix, localname=attrlocalname
                )
            attrsD[attrlocalname.lower()] = attrvalue

        tag = localname
        attrs = list(attrsD.items())

        # Increment the element hierarchy depth counter.
        self.depth += 1

        # Normalize the attributes.
        attrs = [self._normalize_attributes(attr) for attr in attrs]
        attrsD = dict(attrs)

        # Track xml:base
        baseuri = attrsD.get('xml:base', attrsD.get('base')) or self.baseuri
        if isinstance(baseuri, bytes_):
            baseuri = baseuri.decode(self.encoding, 'ignore')
        # Ensure that self.baseuri is always an absolute URI that
        # uses a whitelisted URI scheme (e.g. not `javscript:`)
        if self.baseuri:
            self.baseuri = _makeSafeAbsoluteURI(self.baseuri, baseuri) or self.baseuri
        else:
            self.baseuri = _urljoin(self.baseuri, baseuri)
        self.basestack.append(self.baseuri)

        # Track xml:lang
        lang = attrsD.get('xml:lang', attrsD.get('lang'))
        if lang == '':
            # xml:lang could be explicitly set to '', we need to capture that
            lang = None
        elif lang is None:
            # if no xml:lang is specified, use parent lang
            lang = self.lang
        if lang:
            if tag in ('feed', 'rss', 'rdf:RDF'):
                self.feeddata['language'] = lang.replace('_', '-')
        self.lang = lang
        self.langstack.append(lang)

        # If unknown_starttag is called while in content, reinterpret the tag
        # and its attributes as inline content.
        if self.incontent:
            if not self.contentparams.get('type', 'xml').endswith('xml'):
                # If the content is enclosed in a div tag, skip it.
                if tag in ('xhtml:div', 'div'):
                    return
                # This was supposed to be escaped markup, but it isn't.
                # Update the true content type.
                self.contentparams['type'] = 'application/xhtml+xml'
            # Reinterpret this tag and its attributes as XML-escaped content.
            prefix, _, name = tag.rpartition(':')
            if prefix:
                uri = self.namespacesInUse.get(prefix, '')
            if name == 'svg':
                self.svgOK += 1
            return self.handle_data('<{tag}{attrs}>'.format(tag=name, attrs=self.strattrs(attrs)), escape=0)

        # Normalize the given prefix to an expected prefix.
        prefix, _, name = tag.rpartition(':')
        prefix = self.namespacemap.get(prefix, prefix)
        if prefix:
            prefix = prefix + '_'

        # Call a handler method (if defined).
        methodname = '_start_' + prefix + name
        try:
            method = getattr(self, methodname)
            return method(attrsD)
        except AttributeError:
            # Since there's no handler or something has gone wrong we explicitly add the element and its attributes
            unknown_tag = prefix + name
            if attrsD:
                # Has attributes so create it in its own dictionary
                context = self._getContext()
                context[unknown_tag] = attrsD
            else:
                # No attributes so merge it into the encosing dictionary
                return self.push(unknown_tag, 1)

    def endElementNS(self, name, qname):
        uri, localname = name
        localname = localname.lower()
        loweruri = str(uri or '').lower()
        prefix = self._matchnamespaces.get(loweruri)

        for key, value in self.namespacesInUse.items():
            if key and value == uri:
                localname = '{prefix}:{localname}'.format(
                    prefix=key.lower(), localname=localname
                )
                break

        tag = localname

        # Normalize the given prefix to an expected prefix.
        prefix, _, name = tag.rpartition(':')
        prefix = self.namespacemap.get(prefix, prefix)
        if prefix:
            prefix = prefix + '_'
        if name == 'svg' and self.svgOK:
            self.svgOK -= 1

        # Call a handler method (if defined).
        methodname = '_end_' + prefix + name
        try:
            if self.svgOK:
                raise AttributeError()
            method = getattr(self, methodname)
            method()
        except AttributeError:
            self.pop(prefix + name)

        # If unknown_endtag is called while in content, reinterpret the tag as
        # inline content.
        if self.incontent:
            if not self.contentparams.get('type', 'xml').endswith('xml'):
                # If the content is enclosed in a div tag, skip it.
                if tag in ('xhtml:div', 'div'):
                    return
                # This was supposed to be escaped markup, but it isn't.
                # Update the true content type.
                self.contentparams['type'] = 'application/xhtml+xml'
            self.handle_data('</{tag}>'.format(tag=name), escape=0)

        # Track xml:base going out of scope
        if self.basestack:
            self.basestack.pop()
            if self.basestack: # and self.basestack[-1]:
                self.baseuri = self.basestack[-1]

        # Track xml:lang going out of scope
        if self.langstack:
            self.langstack.pop()
            if self.langstack: # and (self.langstack[-1] is not None):
                self.lang = self.langstack[-1]

        self.depth -= 1

    def handle_data(self, text, escape=1):
        # called for each block of plain text, i.e. outside of any tag and
        # not containing any character or entity references
        if not self.elementstack:
            return
        if escape and self.contentparams.get('type') == 'application/xhtml+xml':
            text = _xmlescape(text)
        self.elementstack[-1][2].append(text)

    def characters(self, text):
        self.handle_data(text)

    def error(self, exc):
        self.bozo = 1
        self.exc = exc

    def fatalError(self, exc):
        self.error(exc)
        raise exc
