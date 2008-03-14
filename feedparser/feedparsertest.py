#!/usr/bin/env python
"""$Id$"""

__author__ = "Mark Pilgrim <http://diveintomark.org/>"
__license__ = """Copyright (c) 2004-2008, Mark Pilgrim, All rights reserved.

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

import feedparser, unittest, new, os, sys, glob, re, urllib, string, posixpath, time, codecs
if not feedparser._XML_AVAILABLE:
  sys.stderr.write('No XML parsers available, unit testing can not proceed\n')
  sys.exit(1)
from UserDict import UserDict
import SimpleHTTPServer, BaseHTTPServer
from threading import *
try:
  dict
except NameError:
  from feedparser import dict

_debug = 0
try:
  codecs.lookup('utf-32be')
  _utf32_available = 1
except:
  _utf32_available = 0
  
#---------- custom HTTP server (used to serve test feeds) ----------

_PORT = 8097 # not really configurable, must match hardcoded port in tests

class FeedParserTestRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  headers_re = re.compile(r"^Header:\s+([^:]+):(.+)$", re.MULTILINE)
  
  def send_head(self):
    """Send custom headers defined in test case

    Example:
    <!--
    Header:   Content-type: application/atom+xml
    Header:   X-Foo: bar
    -->
    """
    path = self.translate_path(self.path)
    headers = dict(self.headers_re.findall(open(path).read()))
    f = open(path, 'rb')
    headers.setdefault('Status', 200)
    self.send_response(int(headers['Status']))
    headers.setdefault('Content-type', self.guess_type(path))
    self.send_header("Content-type", headers['Content-type'])
    self.send_header("Content-Length", str(os.fstat(f.fileno())[6]))
    for k, v in headers.items():
      if k not in ('Status', 'Content-type'):
        self.send_header(k, v)
    self.end_headers()
    return f

  def log_request(self, *args):
    pass

class FeedParserTestServer(Thread):
  """HTTP Server that runs in a thread and handles a predetermined number of requests"""
  
  def __init__(self, requests):
    Thread.__init__(self)
    self.requests = requests
    self.ready = 0
    
  def run(self):
    self.httpd = BaseHTTPServer.HTTPServer(('', _PORT), FeedParserTestRequestHandler)
    self.ready = 1
    while self.requests:
      self.httpd.handle_request()
      self.requests -= 1
    self.ready = 0

#---------- dummy test case class (test methods are added dynamically) ----------

class TestCase(unittest.TestCase):
  def failUnlessEval(self, evalString, env, msg=None):
    """Fail unless eval(evalString, env)"""
    failure=(msg or 'not eval(%s)' % evalString)
    try:
      env = env.data
    except:
      pass
    if not eval(evalString, env):
      raise self.failureException, failure
  
#---------- parse test files and create test methods ----------

skip_re = re.compile("SkipUnless:\s*(.*?)\n")
desc_re = re.compile("Description:\s*(.*?)\s*Expect:\s*(.*)\s*-->")
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

  data = open(xmlfile).read()
  if data[:4] == '\x4c\x6f\xa7\x94':
    data = feedparser._ebcdic_to_ascii(data)
  elif data[:4] == '\x00\x00\xfe\xff':
    if not _utf32_available: return None, None, None, '0'
    data = unicode(data, 'utf-32be').encode('utf-8')
  elif data[:4] == '\xff\xfe\x00\x00':
    if not _utf32_available: return None, None, None, '0'
    data = unicode(data, 'utf-32le').encode('utf-8')
  elif data[:4] == '\x00\x00\x00\x3c':
    if not _utf32_available: return None, None, None, '0'
    data = unicode(data, 'utf-32be').encode('utf-8')
  elif data[:4] == '\x3c\x00\x00\x00':
    if not _utf32_available: return None, None, None, '0'
    data = unicode(data, 'utf-32le').encode('utf-8')
  elif data[:4] == '\x00\x3c\x00\x3f':
    data = unicode(data, 'utf-16be').encode('utf-8')
  elif data[:4] == '\x3c\x00\x3f\x00':
    data = unicode(data, 'utf-16le').encode('utf-8')
  elif (data[:2] == '\xfe\xff') and (data[2:4] != '\x00\x00'):
    data = unicode(data[2:], 'utf-16be').encode('utf-8')
  elif (data[:2] == '\xff\xfe') and (data[2:4] != '\x00\x00'):
    data = unicode(data[2:], 'utf-16le').encode('utf-8')
  elif data[:3] == '\xef\xbb\xbf':
    data = data[3:]
  skip_results = skip_re.search(data)
  if skip_results:
    skipUnless = skip_results.group(1).strip()
  else:
    skipUnless = '1'
  search_results = desc_re.search(data)
  if not search_results:
    raise RuntimeError, "can't parse %s" % xmlfile
  description, evalString = map(string.strip, list(search_results.groups()))
  description = xmlfile + ": " + description
  return TestCase.failUnlessEval, description, evalString, skipUnless

def buildTestCase(xmlfile, description, method, evalString):
  func = lambda self, xmlfile=xmlfile, method=method, evalString=evalString: \
       method(self, evalString, feedparser.parse(xmlfile))
  func.__doc__ = description
  return func

if __name__ == "__main__":
  if sys.argv[1:]:
    import operator
    allfiles = filter(lambda s: s.endswith('.xml'), reduce(operator.add, map(glob.glob, sys.argv[1:]), []))
    sys.argv = [sys.argv[0]] #+ sys.argv[2:]
  else:
    allfiles = glob.glob(os.path.join('.', 'tests', '**', '**', '*.xml'))
#  print allfiles
#  print sys.argv
  httpfiles = [f for f in allfiles if f.count('http')]
  files = httpfiles[:]
  for f in allfiles:
    if f not in httpfiles:
      files.append(f)
  httpd = None
  if httpfiles:
    httpd = FeedParserTestServer(len(httpfiles))
    httpd.start()
  try:
    c = 1
    for xmlfile in files:
      method, description, evalString, skipUnless = getDescription(xmlfile)
      testName = 'test_%06d' % c
      c += 1
      ishttp = xmlfile.count('http')
      try:
        if not eval(skipUnless): raise Exception
      except:
        if ishttp: httpd.requests = httpd.requests - 1
        continue
      if ishttp:
        xmlfile = 'http://127.0.0.1:%s/%s' % (_PORT, posixpath.normpath(xmlfile.replace('\\', '/')))
      testFunc = buildTestCase(xmlfile, description, method, evalString)
      instanceMethod = new.instancemethod(testFunc, None, TestCase)
      setattr(TestCase, testName, instanceMethod)
    if feedparser._debug and not _debug:
      sys.stderr.write('\nWarning: feedparser._debug is on, turning it off temporarily\n\n')
      feedparser._debug = 0
    elif _debug:
      feedparser._debug = 1
    if feedparser.TIDY_MARKUP and feedparser._mxtidy:
      sys.stderr.write('\nWarning: feedparser.TIDY_MARKUP invalidates tests, turning it off temporarily\n\n')
      feedparser.TIDY_MARKUP = 0
    if httpd:
      while not httpd.ready:
        time.sleep(0.1)
    unittest.main()
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
