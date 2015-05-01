# Support for the Dublin Core metadata extensions
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
from ..datetimes import _parse_date

class Namespace(object):
    supported_namespaces = {
        'http://purl.org/dc/elements/1.1/': 'dc',
        'http://purl.org/dc/terms/': 'dcterms',
    }

    def _end_dc_author(self):
        self._end_author()

    def _end_dc_creator(self):
        self._end_author()

    def _end_dc_date(self):
        self._end_updated()

    def _end_dc_description(self):
        self._end_description()

    def _end_dc_language(self):
        self._end_language()

    def _end_dc_publisher(self):
        self._end_webmaster()

    def _end_dc_rights(self):
        self._end_rights()

    def _end_dc_subject(self):
        self._end_category()

    def _end_dc_title(self):
        self._end_title()

    def _end_dcterms_created(self):
        self._end_created()

    def _end_dcterms_issued(self):
        self._end_published()

    def _end_dcterms_modified(self):
        self._end_updated()

    def _start_dc_author(self, attrsD):
        self._start_author(attrsD)

    def _start_dc_creator(self, attrsD):
        self._start_author(attrsD)

    def _start_dc_date(self, attrsD):
        self._start_updated(attrsD)

    def _start_dc_description(self, attrsD):
        self._start_description(attrsD)

    def _start_dc_language(self, attrsD):
        self._start_language(attrsD)

    def _start_dc_publisher(self, attrsD):
        self._start_webmaster(attrsD)

    def _start_dc_rights(self, attrsD):
        self._start_rights(attrsD)

    def _start_dc_subject(self, attrsD):
        self._start_category(attrsD)

    def _start_dc_title(self, attrsD):
        self._start_title(attrsD)

    def _start_dcterms_created(self, attrsD):
        self._start_created(attrsD)

    def _start_dcterms_issued(self, attrsD):
        self._start_published(attrsD)

    def _start_dcterms_modified(self, attrsD):
        self._start_updated(attrsD)

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

    def _start_dc_contributor(self, attrsD):
        self.incontributor = 1
        context = self._getContext()
        context.setdefault('contributors', [])
        context['contributors'].append(FeedParserDict())
        self.push('name', 0)

    def _end_dc_contributor(self):
        self._end_name()
        self.incontributor = 0

