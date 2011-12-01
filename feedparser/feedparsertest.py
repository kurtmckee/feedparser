#!/usr/bin/env python
"""$Id$"""

__author__ = "Mark Pilgrim <http://diveintomark.org/>"
__license__ = """
Copyright (c) 2010-2011 Kurt McKee <contactme@kurtmckee.org>
Copyright (c) 2004-2008 Mark Pilgrim
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

import codecs
import datetime
import glob
import operator
import os
import posixpath
import pprint
import re
import struct
import sys
import threading
import time
import unittest
import urllib
import zlib
import BaseHTTPServer
import SimpleHTTPServer

import feedparser

if not feedparser._XML_AVAILABLE:
    sys.stderr.write('No XML parsers available, unit testing can not proceed\n')
    sys.exit(1)

try:
    codecs.lookup('utf-32be')
except LookupError:
    _utf32_available = 0
else:
    _utf32_available = 1
  
_s2bytes = feedparser._s2bytes
_l2bytes = feedparser._l2bytes

#---------- custom HTTP server (used to serve test feeds) ----------

_PORT = 8097 # not really configurable, must match hardcoded port in tests

class FeedParserTestRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  headers_re = re.compile(_s2bytes(r"^Header:\s+([^:]+):(.+)$"), re.MULTILINE)
  
  def send_head(self):
    """Send custom headers defined in test case

    Example:
    <!--
    Header:   Content-type: application/atom+xml
    Header:   X-Foo: bar
    -->
    """
    path = self.translate_path(self.path)
    # the compression tests' filenames determine the header sent
    if self.path.startswith('/tests/compression'):
      if self.path.endswith('gz'):
        headers = {'Content-Encoding': 'gzip'}
      else:
        headers = {'Content-Encoding': 'deflate'}
    else:
      headers = dict([(k.decode('utf-8'), v.decode('utf-8').strip()) for k, v in self.headers_re.findall(open(path, 'rb').read())])
    f = open(path, 'rb')
    if (self.headers.get('if-modified-since') == headers.get('Last-Modified', 'nom')) \
        or (self.headers.get('if-none-match') == headers.get('ETag', 'nomatch')):
        status = 304
    else:
        status = 200
    headers.setdefault('Status', status)
    self.send_response(int(headers['Status']))
    headers.setdefault('Content-type', self.guess_type(path))
    self.send_header("Content-type", headers['Content-type'])
    self.send_header("Content-Length", str(os.stat(f.name)[6]))
    for k, v in headers.items():
      if k not in ('Status', 'Content-type'):
        self.send_header(k, v)
    self.end_headers()
    return f

  def log_request(self, *args):
    pass

class FeedParserTestServer(threading.Thread):
  """HTTP Server that runs in a thread and handles a predetermined number of requests"""
  
  def __init__(self, requests):
    threading.Thread.__init__(self)
    self.requests = requests
    self.ready = threading.Event()
    
  def run(self):
    self.httpd = BaseHTTPServer.HTTPServer(('', _PORT), FeedParserTestRequestHandler)
    self.ready.set()
    while self.requests:
      self.httpd.handle_request()
      self.requests -= 1
    self.ready.clear()

#---------- dummy test case class (test methods are added dynamically) ----------
unicode1_re = re.compile(_s2bytes(" u'"))
unicode2_re = re.compile(_s2bytes(' u"'))

def everythingIsUnicode(d):
    """Takes a dictionary, recursively verifies that every value is unicode"""
    for k, v in d.iteritems():
        if isinstance(v, dict) and k != 'headers':
            if not everythingIsUnicode(v):
                return False
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict) and not everythingIsUnicode(i):
                    return False
                elif isinstance(v, basestring) and not isinstance(i, unicode):
                    return False
        elif isinstance(v, basestring) and not isinstance(v, unicode):
            return False
    return True

def failUnlessEval(self, xmlfile, evalString, msg=None):
    """Fail unless eval(evalString, env)"""
    env = feedparser.parse(xmlfile)
    try:
        if not eval(evalString, globals(), env):
            failure=(msg or 'not eval(%s) \nWITH env(%s)' % (evalString, pprint.pformat(env)))
            raise self.failureException, failure
        if not everythingIsUnicode(env):
            raise self.failureException, "not everything is unicode \nWITH env(%s)" % (pprint.pformat(env), )
    except SyntaxError:
        # Python 3 doesn't have the `u""` syntax, so evalString needs to be modified,
        # which will require the failure message to be updated
        evalString = re.sub(unicode1_re, _s2bytes(" '"), evalString)
        evalString = re.sub(unicode2_re, _s2bytes(' "'), evalString)
        if not eval(evalString, globals(), env):
            failure=(msg or 'not eval(%s) \nWITH env(%s)' % (evalString, pprint.pformat(env)))
            raise self.failureException, failure

class BaseTestCase(unittest.TestCase):
    failUnlessEval = failUnlessEval

class TestCase(BaseTestCase):
    pass

class TestLooseParser(BaseTestCase):
    def __init__(self, arg):
        unittest.TestCase.__init__(self, arg)
        self._xml_available = feedparser._XML_AVAILABLE
    def setUp(self):
        feedparser._XML_AVAILABLE = 0
    def tearDown(self):
        feedparser._XML_AVAILABLE = self._xml_available

class TestStrictParser(BaseTestCase):
    pass

class TestMicroformats(BaseTestCase):
    pass

class TestEncodings(BaseTestCase):
    pass

class TestFeedParserDict(unittest.TestCase):
    def setUp(self):
        self.d = feedparser.FeedParserDict()
    def _check_key(self, k):
        self.assertTrue(k in self.d)
        self.assertTrue(hasattr(self.d, k))
        self.assertEqual(self.d[k], 1)
        self.assertEqual(getattr(self.d, k), 1)
    def _check_no_key(self, k):
        self.assertTrue(k not in self.d)
        self.assertTrue(not hasattr(self.d, k))
    def test_empty(self):
        keys = (
            'a','entries', 'id', 'guid', 'summary', 'subtitle', 'description',
            'category', 'enclosures', 'license', 'categories',
        )
        for k in keys:
            self._check_no_key('a')
        self.assertTrue('items' not in self.d)
        self.assertTrue(hasattr(self.d, 'items')) # dict.items() exists
    def test_neutral(self):
        self.d['a'] = 1
        self._check_key('a')
    def test_single_mapping_target(self):
        self.d['id'] = 1
        self._check_key('id')
        self._check_key('guid')
    def test_single_mapping_target(self):
        self.d['guid'] = 1
        self._check_key('id')
        self._check_key('guid')
    def test_multiple_mapping_target_1(self):
        self.d['summary'] = 1
        self._check_key('summary')
        self._check_key('description')
    def test_multiple_mapping_target_2(self):
        self.d['subtitle'] = 1
        self._check_key('subtitle')
        self._check_key('description')
    def test_multiple_mapping_mapped_key(self):
        self.d['description'] = 1
        self._check_key('summary')
        self._check_key('description')
    def test_license(self):
        self.d['links'] = []
        try:
            self.d['license']
            self.assertTrue(False)
        except KeyError:
            pass
        self.d['links'].append({'rel': 'license'})
        try:
            self.d['license']
            self.assertTrue(False)
        except KeyError:
            pass
        self.d['links'].append({'rel': 'license', 'href': 'http://dom.test/'})
        self.assertEqual(self.d['license'], 'http://dom.test/')
    def test_category(self):
        self.d['tags'] = []
        try:
            self.d['category']
            self.assertTrue(False)
        except KeyError:
            pass
        self.d['tags'] = [{}]
        try:
            self.d['category']
            self.assertTrue(False)
        except KeyError:
            pass
        self.d['tags'] = [{'term': 'cat'}]
        self.assertEqual(self.d['category'], 'cat')
        self.d['tags'].append({'term': 'dog'})
        self.assertEqual(self.d['category'], 'cat')

class TestOpenResource(unittest.TestCase):
    def test_fileobj(self):
        r = feedparser._open_resource(sys.stdin, '', '', '', '', [], {})
        self.assertTrue(r is sys.stdin)
    def test_feed(self):
        f = feedparser.parse(u'feed://localhost:8097/tests/http/target.xml')
        self.assertEqual(f.href, u'http://localhost:8097/tests/http/target.xml')
    def test_feed_http(self):
        f = feedparser.parse(u'feed:http://localhost:8097/tests/http/target.xml')
        self.assertEqual(f.href, u'http://localhost:8097/tests/http/target.xml')
    def test_bytes(self):
        s = '<feed><item><title>text</title></item></feed>'.encode('utf-8')
        r = feedparser._open_resource(s, '', '', '', '', [], {})
        self.assertEqual(s, r.read())
    def test_string(self):
        s = '<feed><item><title>text</title></item></feed>'
        r = feedparser._open_resource(s, '', '', '', '', [], {})
        self.assertEqual(s.encode('utf-8'), r.read())
    def test_unicode_1(self):
        s = u'<feed><item><title>text</title></item></feed>'
        r = feedparser._open_resource(s, '', '', '', '', [], {})
        self.assertEqual(s.encode('utf-8'), r.read())
    def test_unicode_2(self):
        s = u'<feed><item><title>t\u00e9xt</title></item></feed>'
        r = feedparser._open_resource(s, '', '', '', '', [], {})
        self.assertEqual(s.encode('utf-8'), r.read())

class TestMakeSafeAbsoluteURI(unittest.TestCase):
    base = u'http://d.test/d/f.ext'
    def _mktest(rel, expect, doc):
        def fn(self):
            value = feedparser._makeSafeAbsoluteURI(self.base, rel)
            self.assertEqual(value, expect)
        fn.__doc__ = doc
        return fn

    # make the test cases; the call signature is:
    # (relative_url, expected_return_value, test_doc_string)
    test_abs = _mktest(u'https://s.test/', u'https://s.test/', 'absolute uri')
    test_rel = _mktest(u'/new', u'http://d.test/new', 'relative uri')
    test_bad = _mktest(u'x://bad.test/', u'', 'unacceptable uri protocol')

class TestConvertToIdn(unittest.TestCase):
    # this is the greek test domain
    hostname = u'\u03c0\u03b1\u03c1\u03ac\u03b4\u03b5\u03b9\u03b3\u03bc\u03b1'
    hostname += u'.\u03b4\u03bf\u03ba\u03b9\u03bc\u03ae'
    def test_control(self):
        r = feedparser._convert_to_idn(u'http://example.test/')
        self.assertEqual(r, u'http://example.test/')
    def test_idn(self):
        r = feedparser._convert_to_idn(u'http://%s/' % (self.hostname,))
        self.assertEqual(r, u'http://xn--hxajbheg2az3al.xn--jxalpdlp/')
    def test_port(self):
        r = feedparser._convert_to_idn(u'http://%s:8080/' % (self.hostname,))
        self.assertEqual(r, u'http://xn--hxajbheg2az3al.xn--jxalpdlp:8080/')

class TestCompression(unittest.TestCase):
    def test_gzip_good(self):
        f = feedparser.parse('http://localhost:8097/tests/compression/gzip.gz')
        self.assertEqual(f.version, 'atom10')
    def test_gzip_not_gzipped(self):
        f = feedparser.parse('http://localhost:8097/tests/compression/gzip-not-gzipped.gz')
        self.assertEqual(f.bozo, 1)
        self.assertTrue(isinstance(f.bozo_exception, IOError))
    def test_gzip_struct_error(self):
        f = feedparser.parse('http://localhost:8097/tests/compression/gzip-struct-error.gz')
        self.assertEqual(f.bozo, 1)
        self.assertTrue(isinstance(f.bozo_exception, struct.error))
    def test_zlib_good(self):
        f = feedparser.parse('http://localhost:8097/tests/compression/deflate.z')
        self.assertEqual(f.version, 'atom10')
    def test_zlib_bad(self):
        f = feedparser.parse('http://localhost:8097/tests/compression/deflate-error.z')
        self.assertEqual(f.bozo, 1)
        self.assertTrue(isinstance(f.bozo_exception, zlib.error))

class TestHTTPStatus(unittest.TestCase):
    def test_301(self):
        f = feedparser.parse('http://localhost:8097/tests/http/http_status_301.xml')
        self.assertEqual(f.status, 301)
        self.assertEqual(f.href, 'http://localhost:8097/tests/http/target.xml')
        self.assertEqual(f.entries[0].title, 'target')
    def test_302(self):
        f = feedparser.parse('http://localhost:8097/tests/http/http_status_302.xml')
        self.assertEqual(f.status, 302)
        self.assertEqual(f.href, 'http://localhost:8097/tests/http/target.xml')
        self.assertEqual(f.entries[0].title, 'target')
    def test_303(self):
        f = feedparser.parse('http://localhost:8097/tests/http/http_status_303.xml')
        self.assertEqual(f.status, 303)
        self.assertEqual(f.href, 'http://localhost:8097/tests/http/target.xml')
        self.assertEqual(f.entries[0].title, 'target')
    def test_307(self):
        f = feedparser.parse('http://localhost:8097/tests/http/http_status_307.xml')
        self.assertEqual(f.status, 307)
        self.assertEqual(f.href, 'http://localhost:8097/tests/http/target.xml')
        self.assertEqual(f.entries[0].title, 'target')
    def test_304(self):
        # first retrieve the url
        u = 'http://localhost:8097/tests/http/http_status_304.xml'
        f = feedparser.parse(u)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.entries[0].title, 'title 304')
        # extract the etag and last-modified headers
        e = [v for k, v in f.headers.items() if k.lower() == 'etag'][0]
        mh = [v for k, v in f.headers.items() if k.lower() == 'last-modified'][0]
        ms = f.updated
        mt = f.updated_parsed
        md = datetime.datetime(*mt[0:7])
        self.assertTrue(isinstance(mh, basestring))
        self.assertTrue(isinstance(ms, basestring))
        self.assertTrue(isinstance(mt, time.struct_time))
        self.assertTrue(isinstance(md, datetime.datetime))
        # test that sending back the etag results in a 304
        f = feedparser.parse(u, etag=e)
        self.assertEqual(f.status, 304)
        # test that sending back last-modified (string) results in a 304
        f = feedparser.parse(u, modified=ms)
        self.assertEqual(f.status, 304)
        # test that sending back last-modified (9-tuple) results in a 304
        f = feedparser.parse(u, modified=mt)
        self.assertEqual(f.status, 304)
        # test that sending back last-modified (datetime) results in a 304
        f = feedparser.parse(u, modified=md)
        self.assertEqual(f.status, 304)
    def test_404(self):
        f = feedparser.parse('http://localhost:8097/tests/http/http_status_404.xml')
        self.assertEqual(f.status, 404)
    def test_9001(self):
        f = feedparser.parse('http://localhost:8097/tests/http/http_status_9001.xml')
        self.assertEqual(f.bozo, 1)

class TestDateParsers(unittest.TestCase):
    def test_None(self):
        self.assertTrue(feedparser._parse_date(None) is None)
    def _check_date(self, func, dtstring, dttuple):
        try:
            tup = func(dtstring)
        except (OverflowError, ValueError):
            tup = None
        self.assertEqual(tup, dttuple)
        self.assertEqual(tup, feedparser._parse_date(dtstring))

date_tests = {
    feedparser._parse_date_greek: (
        (u'', None), # empty string
        (u'\u039a\u03c5\u03c1, 11 \u0399\u03bf\u03cd\u03bb 2004 12:00:00 EST', (2004, 7, 11, 17, 0, 0, 6, 193, 0)),
    ),
    feedparser._parse_date_hungarian: (
        (u'', None), # empty string
        (u'2004-j\u00falius-13T9:15-05:00', (2004, 7, 13, 14, 15, 0, 1, 195, 0)), 
    ),
    feedparser._parse_date_iso8601: (
        (u'', None), # empty string
        (u'-0312', (2003, 12, 1, 0, 0, 0, 0, 335, 0)), # 2-digit year/month only variant
        (u'031231', (2003, 12, 31, 0, 0, 0, 2, 365, 0)), # 2-digit year/month/day only, no hyphens
        (u'03-12-31', (2003, 12, 31, 0, 0, 0, 2, 365, 0)), # 2-digit year/month/day only
        (u'-03-12', (2003, 12, 1, 0, 0, 0, 0, 335, 0)), # 2-digit year/month only
        (u'03335', (2003, 12, 1, 0, 0, 0, 0, 335, 0)), # 2-digit year/ordinal, no hyphens
        (u'2003-12-31T10:14:55.1234Z', (2003, 12, 31, 10, 14, 55, 2, 365, 0)), # fractional seconds
        # Special case for Google's extra zero in the month
        (u'2003-012-31T10:14:55+00:00', (2003, 12, 31, 10, 14, 55, 2, 365, 0)),
    ),
    feedparser._parse_date_nate: (
        (u'', None), # empty string
        (u'2004-05-25 \uc624\ud6c4 11:23:17', (2004, 5, 25, 14, 23, 17, 1, 146, 0)),
    ),
    feedparser._parse_date_onblog: (
        (u'', None), # empty string
        (u'2004\ub144 05\uc6d4 28\uc77c  01:31:15', (2004, 5, 27, 16, 31, 15, 3, 148, 0)),
    ),
    feedparser._parse_date_perforce: (
        (u'', None), # empty string
        (u'Fri, 2006/09/15 08:19:53 EDT', (2006, 9, 15, 12, 19, 53, 4, 258, 0)),
    ),
    feedparser._parse_date_rfc822: (
        (u'', None), # empty string
        (u'Sun, 31 Dec 9999 23:59:59 -9999', None), # wildly out-of-range, catch OverflowError
        (u'Mon, 11 Aug 0307 00:01:00 +0200', None), # wildly out-of-range, catch ValueError
        (u'Thu, 01 Jan 04 19:48:21 GMT', (2004, 1, 1, 19, 48, 21, 3, 1, 0)), # 2-digit year
        (u'Thu, 01 Jan 2004 19:48:21 GMT', (2004, 1, 1, 19, 48, 21, 3, 1, 0)), # 4-digit year
        (u'Thu, 31 Jun 2004 19:48:21 GMT', (2004, 7, 1, 19, 48, 21, 3, 183, 0)), # rollover june 31st
        (u'Wed, 19 Aug 2009 18:28:00 Etc/GMT', (2009, 8, 19, 18, 28, 0, 2, 231, 0)), # etc/gmt timezone
        (u'Thu, 01 Jan 2004 00:00 GMT', (2004, 1, 1, 0, 0, 0, 3, 1, 0)), # no seconds
        (u'Thu, 01 Jan 2004', (2004, 1, 1, 0, 0, 0, 3, 1, 0)), # no time
        # Test asctime-style dates and times
        (u'Sun Jan  4 16:29:06 PST 2004', (2004, 1, 5, 0, 29, 6, 0, 5, 0)),
        # Additional tests to handle Disney's long month names and invalid timezones
        (u'Mon, 26 January 2004 16:31:00 AT', (2004, 1, 26, 20, 31, 0, 0, 26, 0)), 
        (u'Mon, 26 January 2004 16:31:00 ET', (2004, 1, 26, 21, 31, 0, 0, 26, 0)),
        (u'Mon, 26 January 2004 16:31:00 CT', (2004, 1, 26, 22, 31, 0, 0, 26, 0)),
        (u'Mon, 26 January 2004 16:31:00 MT', (2004, 1, 26, 23, 31, 0, 0, 26, 0)),
        (u'Mon, 26 January 2004 16:31:00 PT', (2004, 1, 27, 0, 31, 0, 1, 27, 0)),
    ),
    feedparser._parse_date_w3dtf: (
        (u'', None), # empty string
        (u'2003-12-31T10:14:55Z', (2003, 12, 31, 10, 14, 55, 2, 365, 0)), # UTC
        (u'2003-12-31T10:14:55-08:00', (2003, 12, 31, 18, 14, 55, 2, 365, 0)), # San Francisco timezone
        (u'2003-12-31T18:14:55+08:00', (2003, 12, 31, 10, 14, 55, 2, 365, 0)), # Tokyo timezone
        (u'2007-04-23T23:25:47.538+10:00', (2007, 4, 23, 13, 25, 47, 0, 113, 0)), # fractional seconds
        (u'2003-12-31', (2003, 12, 31, 0, 0, 0, 2, 365, 0)), # year/month/day only
        (u'20031231', (2003, 12, 31, 0, 0, 0, 2, 365, 0)), # year/month/day only, no hyphens
        (u'2003-12', (2003, 12, 1, 0, 0, 0, 0, 335, 0)), # year/month only
        (u'2003', (2003, 1, 1, 0, 0, 0, 2, 1, 0)), # year only
        # MSSQL-style dates
        (u'2004-07-08 23:56:58 -00:20', (2004, 7, 9, 0, 16, 58, 4, 191, 0)), # with timezone
        (u'2004-07-08 23:56:58', (2004, 7, 8, 23, 56, 58, 3, 190, 0)), # without timezone
        (u'2004-07-08 23:56:58.0', (2004, 7, 8, 23, 56, 58, 3, 190, 0)), # with fractional second
        # Special cases for out-of-range times
        (u'2003-12-31T25:14:55Z', (2004, 1, 1, 1, 14, 55, 3, 1, 0)), # invalid (25 hours)
        (u'2003-12-31T10:61:55Z', (2003, 12, 31, 11, 1, 55, 2, 365, 0)), # invalid (61 minutes)
        (u'2003-12-31T10:14:61Z', (2003, 12, 31, 10, 15, 1, 2, 365, 0)), # invalid (61 seconds)
        # Special cases for rollovers in leap years
        (u'2004-02-28T18:14:55-08:00', (2004, 2, 29, 2, 14, 55, 6, 60, 0)), # feb 28 in leap year
        (u'2003-02-28T18:14:55-08:00', (2003, 3, 1, 2, 14, 55, 5, 60, 0)), # feb 28 in non-leap year
        (u'2000-02-28T18:14:55-08:00', (2000, 2, 29, 2, 14, 55, 1, 60, 0)), # feb 28 in leap year on century divisible by 400
    )
}

def make_date_test(f, s, t):
    return lambda self: self._check_date(f, s, t)

for func, items in date_tests.iteritems():
    for i, (dtstring, dttuple) in enumerate(items):
        uniqfunc = make_date_test(func, dtstring, dttuple)
        setattr(TestDateParsers, 'test_%s_%02i' % (func.__name__, i), uniqfunc)


class TestHTMLGuessing(unittest.TestCase):
    def _mktest(text, expect, doc):
        def fn(self):
            value = bool(feedparser._FeedParserMixin.lookslikehtml(text))
            self.assertEqual(value, expect)
        fn.__doc__ = doc
        return fn

    test_text_1 = _mktest(u'plain text', False, u'plain text')
    test_text_2 = _mktest(u'2 < 3', False, u'plain text with angle bracket')
    test_html_1 = _mktest(u'<a href="">a</a>', True, u'anchor tag')
    test_html_2 = _mktest(u'<i>i</i>', True, u'italics tag')
    test_html_3 = _mktest(u'<b>b</b>', True, u'bold tag')
    test_html_4 = _mktest(u'<code>', False, u'allowed tag, no end tag')
    test_html_5 = _mktest(u'<rss> .. </rss>', False, u'disallowed tag')
    test_entity_1 = _mktest(u'AT&T', False, u'corporation name')
    test_entity_2 = _mktest(u'&copy;', True, u'named entity reference')
    test_entity_3 = _mktest(u'&#169;', True, u'numeric entity reference')
    test_entity_4 = _mktest(u'&#xA9;', True, u'hex numeric entity reference')

#---------- additional api unit tests, not backed by files

class TestBuildRequest(unittest.TestCase):
  def test_extra_headers(self):
    """You can pass in extra headers and they go into the request object."""

    request = feedparser._build_urllib2_request(
      'http://example.com/feed',
      'agent-name',
      None, None, None, None,
      {'Cache-Control': 'max-age=0'})
    # nb, urllib2 folds the case of the headers
    self.assertEqual(
      request.get_header('Cache-control'), 'max-age=0')


#---------- parse test files and create test methods ----------

skip_re = re.compile(_s2bytes("SkipUnless:\s*(.*?)\n"))
desc_re = re.compile(_s2bytes("Description:\s*(.*?)\s*Expect:\s*(.*)\s*-->"))
def getDescription(xmlfile):
  """Extract test data

  Each test case is an XML file which contains not only a test feed
  but also the description of the test, i.e. the condition that we
  would expect the parser to create when it parses the feed.  Example:
  <!--
  Description: feed title
  Expect:      feed['title'] == u'Example feed'
  -->
  """

  data = open(xmlfile, 'rb').read()
  if data[:4] == _l2bytes([0x4c, 0x6f, 0xa7, 0x94]):
    data = unicode(data, 'cp037').encode('utf-8')
  elif data[:4] == _l2bytes([0x00, 0x00, 0xfe, 0xff]):
    if not _utf32_available: return None, None, '0'
    data = unicode(data, 'utf-32be').encode('utf-8')
  elif data[:4] == _l2bytes([0xff, 0xfe, 0x00, 0x00]):
    if not _utf32_available: return None, None, '0'
    data = unicode(data, 'utf-32le').encode('utf-8')
  elif data[:4] == _l2bytes([0x00, 0x00, 0x00, 0x3c]):
    if not _utf32_available: return None, None, '0'
    data = unicode(data, 'utf-32be').encode('utf-8')
  elif data[:4] == _l2bytes([0x3c, 0x00, 0x00, 0x00]):
    if not _utf32_available: return None, None, '0'
    data = unicode(data, 'utf-32le').encode('utf-8')
  elif data[:4] == _l2bytes([0x00, 0x3c, 0x00, 0x3f]):
    data = unicode(data, 'utf-16be').encode('utf-8')
  elif data[:4] == _l2bytes([0x3c, 0x00, 0x3f, 0x00]):
    data = unicode(data, 'utf-16le').encode('utf-8')
  elif (data[:2] == _l2bytes([0xfe, 0xff])) and (data[2:4] != _l2bytes([0x00, 0x00])):
    data = unicode(data[2:], 'utf-16be').encode('utf-8')
  elif (data[:2] == _l2bytes([0xff, 0xfe])) and (data[2:4] != _l2bytes([0x00, 0x00])):
    data = unicode(data[2:], 'utf-16le').encode('utf-8')
  elif data[:3] == _l2bytes([0xef, 0xbb, 0xbf]):
    data = data[3:]
  skip_results = skip_re.search(data)
  if skip_results:
    skipUnless = skip_results.group(1).strip()
  else:
    skipUnless = '1'
  search_results = desc_re.search(data)
  if not search_results:
    raise RuntimeError, "can't parse %s" % xmlfile
  description, evalString = map(lambda s: s.strip(), list(search_results.groups()))
  description = xmlfile + ": " + unicode(description, 'utf8')
  return description, evalString, skipUnless

def buildTestCase(xmlfile, description, evalString):
  func = lambda self, xmlfile=xmlfile, evalString=evalString: \
       self.failUnlessEval(xmlfile, evalString)
  func.__doc__ = description
  return func

if __name__ == "__main__":
  if sys.argv[1:]:
    allfiles = filter(lambda s: s.endswith('.xml'), reduce(operator.add, map(glob.glob, sys.argv[1:]), []))
    sys.argv = [sys.argv[0]] #+ sys.argv[2:]
  else:
    allfiles = glob.glob(os.path.join('.', 'tests', '**', '**', '*.xml'))
    wellformedfiles = glob.glob(os.path.join('.', 'tests', 'wellformed', '**', '*.xml'))
    illformedfiles = glob.glob(os.path.join('.', 'tests', 'illformed', '*.xml'))
    encodingfiles = glob.glob(os.path.join('.', 'tests', 'encoding', '*.xml'))
    microformatfiles = glob.glob(os.path.join('.', 'tests', 'microformats', '**', '*.xml'))
#  print allfiles
#  print sys.argv
  httpd = None
  # there are several compression test cases that must be accounted for
  # as well as a number of http status tests that redirect to a target
  # and a few `_open_resource`-related tests
  httpcount = 5 + 15 + 2
  httpcount += len([f for f in allfiles if 'http' in f])
  httpcount += len([f for f in wellformedfiles if 'http' in f])
  httpcount += len([f for f in illformedfiles if 'http' in f])
  httpcount += len([f for f in encodingfiles if 'http' in f])
  try:
    for c, xmlfile in enumerate(allfiles + encodingfiles + illformedfiles):
      addTo = TestCase
      if xmlfile in encodingfiles:
        addTo = TestEncodings
      elif xmlfile in microformatfiles:
        addTo = TestMicroformats
      elif xmlfile in wellformedfiles:
        addTo = (TestStrictParser, TestLooseParser)
      description, evalString, skipUnless = getDescription(xmlfile)
      testName = 'test_%06d' % c
      ishttp = 'http' in xmlfile
      try:
        if not eval(skipUnless): raise NotImplementedError
      except (ImportError, LookupError, NotImplementedError, AttributeError):
        if ishttp:
          httpcount -= 1 + (xmlfile in wellformedfiles)
        continue
      if ishttp:
        xmlfile = 'http://127.0.0.1:%s/%s' % (_PORT, posixpath.normpath(xmlfile.replace('\\', '/')))
      testFunc = buildTestCase(xmlfile, description, evalString)
      if isinstance(addTo, tuple):
        setattr(addTo[0], testName, testFunc)
        setattr(addTo[1], testName, testFunc)
      else:
        setattr(addTo, testName, testFunc)
    if feedparser.TIDY_MARKUP and feedparser._mxtidy:
      sys.stderr.write('\nWarning: feedparser.TIDY_MARKUP invalidates tests, turning it off temporarily\n\n')
      feedparser.TIDY_MARKUP = 0
    if httpcount:
      httpd = FeedParserTestServer(httpcount)
      httpd.daemon = True
      httpd.start()
      httpd.ready.wait()
    testsuite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    testsuite.addTest(testloader.loadTestsFromTestCase(TestCase))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestStrictParser))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestLooseParser))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestEncodings))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestDateParsers))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestHTMLGuessing))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestHTTPStatus))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestCompression))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestConvertToIdn))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestMicroformats))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestOpenResource))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestFeedParserDict))
    testsuite.addTest(testloader.loadTestsFromTestCase(TestMakeSafeAbsoluteURI))
    testresults = unittest.TextTestRunner(verbosity=1).run(testsuite)

    # Return 0 if successful, 1 if there was a failure
    sys.exit(not testresults.wasSuccessful())
  finally:
    if httpd:
      if httpd.requests:
        # Should never get here unless something went horribly wrong, like the
        # user hitting Ctrl-C.  Tell our HTTP server that it's done, then do
        # one more request to flush it.  This rarely works; the combination of
        # threading, self-terminating HTTP servers, and unittest is really
        # quite flaky.  Just what you want in a testing framework, no?
        httpd.requests = 0
        if httpd.ready:
          urllib.urlopen('http://127.0.0.1:8097/tests/wellformed/rss/aaa_wellformed.xml').read()
      httpd.join(0)
