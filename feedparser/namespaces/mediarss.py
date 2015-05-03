# Support for the Media RSS format
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

from ..util import FeedParserDict

class Namespace(object):
    supported_namespaces = {
        # Canonical namespace
        'http://search.yahoo.com/mrss/': 'media',

        # Old namespace (no trailing slash)
        'http://search.yahoo.com/mrss': 'media',
    }

    def _start_media_category(self, attrsD):
        attrsD.setdefault('scheme', 'http://search.yahoo.com/mrss/category_schema')
        self._start_category(attrsD)

    def _end_media_category(self):
        self._end_category()

    def _end_media_keywords(self):
        for term in self.pop('media_keywords').split(','):
            if term.strip():
                self._addTag(term.strip(), None, None)

    def _start_media_title(self, attrsD):
        self._start_title(attrsD)

    def _end_media_title(self):
        title_depth = self.title_depth
        self._end_title()
        self.title_depth = title_depth

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

    def _start_media_description(self, attrsD):
        self._start_description(attrsD)

    def _end_media_description(self):
        self._end_description()

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
