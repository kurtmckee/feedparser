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

        self.unknown_starttag(localname, list(attrsD.items()))

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

        self.unknown_endtag(localname)

    def characters(self, text):
        self.handle_data(text)

    def error(self, exc):
        self.bozo = 1
        self.exc = exc

    def fatalError(self, exc):
        self.error(exc)
        raise exc
