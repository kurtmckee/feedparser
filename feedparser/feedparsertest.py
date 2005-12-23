"""$Id$"""

__author__ = "Mark Pilgrim <http://diveintomark.org/>"
__license__ = """Copyright (c) 2004-2005, Mark Pilgrim, All rights reserved.

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
        urllib.urlopen('http://127.0.0.1:8097/tests/wellformed/rss/aaa_wellformed.xml').read()
      httpd.join(0)

"""
RSS 2.0
* channel
  * title
  * link
  * description
    * plain text
    * escaped markup
    * naked markup
    * always duplicated into "tagline"
  * language
  * copyright (maps to "rights")
  * managingEditor (maps to "author" and possibly "author_detail")
  * webMaster (maps to "publisher")
  * pubDate (maps to "date")
    * asctime
    * rfc822 (2 digit year)
    * rfc2822 (4 digit year)
    * w3dtf
    * iso8601
    * always duplicated into "modified"
  X lastBuildDate
  * category
    * single category
    * multiple categories maps to "categories"
    * @domain maps to "categories"
  * generator
  * docs
  * cloud
    * @domain
    * @port
    * @path
    * @registerProcedure
    * @protocol
  * ttl
  * image
    * title
    * url
    * link
    * width
    * height
    * check that title, link don't conflict with channel title, link
  X rating
  * textInput
    * title
    * description
    * name
    * link
    * check that title, link, and description don't conflict with channel stuff
  * skipHours
  * skipDays
* item
  * title
  * link
  * description
    * plain text
    * escaped markup
    * naked markup
    * always duplicated in "summary"
  * author
  * category
    * multiple categories
    * @domain
  * comments
  * enclosure
    * @url
    * @length
    * @type
    * multiple enclosures
  * guid
    * should duplicate into link if @isPermaLink="true" or missing
    * should NOT duplicate into link if link already exists
  * pubDate
    * string
    * parsed
    * always maps to date_parsed
  * source
    * @url

RSS 0.93
* item
  * expirationDate

Dublin Core
* channel
  * dc:date (maps to "date" and "date_parsed" and "modified" and "modified_parsed")
  * dc:language (maps to "language")
  * dc:creator (maps to "author" and possibly "author_detail")
  * dc:author (maps to "author" and possibly "author_detail")
  * dc:publisher (maps to "publisher")
  * dc:rights (maps to "rights")
  * dc:subject (maps to "category" and "categories")
  * dc:title (maps to "title")
  * dcterms:issued (maps to "issued" and "issued_parsed")
  * dcterms:created (maps to "created" and "created_parsed")
  * dcterms:modified (maps to "modified" and "modified_parsed" and "date" and "date_parsed")
* item
  * dc:date (maps to "date" and "date_parsed" and "modified" and "modified_parsed")
  * dc:language (maps to "language")
  * dc:creator (maps to "author" and possibly "author_detail")
  * dc:author (maps to "author" and possibly "author_detail")
  * dc:publisher (maps to "publisher")
  * dc:rights (maps to "rights")
  * dc:subject (maps to "category" and "categories")
  * dc:title (maps to "title")
  * dcterms:issued (maps to "issued" and "issued_parsed")
  * dcterms:created (maps to "created" and "created_parsed")
  * dcterms:modified (maps to "modified" and "modified_parsed" and "date" and "date_parsed")

Undocumented
* channel
  * author (treat like dc:author)
* item
  * xhtml:body (maps to "content")
    * value
    * mode
    * type
    * xml:lang
  * content:encoded (maps to "content")
    * value
    * mode
    * type
    * xml:lang
  * fullitem (maps to "content")
    * value
    * mode
    * type
    * xml:lang

RSS 1.0
* version
* channel
  * title
  * link
  * description
* item
  * title
  * link
  * description
- content module - http://purl.org/rss/1.0/modules/content/
  - TODO
- syndication module - http://purl.org/rss/1.0/modules/syndication/
  - TODO
- link module - http://www.purl.org/rss/1.0/modules/link/
  - map to "links"
  - TODO

Atom
* feed
  * namespaces
    * http://purl.org/atom/ns#
    * http://example.com/necho
    * http://purl.org/echo/
    * http://purl.org/pie/
    * http://example.com/newformat#
    * uri/of/echo/namespace# (note: invalid namespace, can never be wellformed XML)
  * title
    * plaintext
    * escaped markup
    * naked (unqualified) markup
    * base64 encoded
    * inline markup
    * inline markup with escaped markup (@mode="xml" + <div xmlns="...">History of the &lt;blink&gt; tag</div>)
    * full content model --> "title_detail"
      * value
      * @type
      * @mode
      * @xml:lang
      * @xml:lang inherited
      * @xml:base
      * @xml:base inherited
  * link
    * rel="alternate"/type in ['application/xhtml+xml','text/html'] --> channel['link']
    * all --> channel['links']
      * @rel
      * @type
      * @href
      * @title
  * modified
    * parses to "modified_parsed"
    * always duplicated to "date" and "date_parsed"
  * info
    * plaintext or html in "info"
    * full content model in "info_detail"
  * tagline
    * plaintext or html in "tagline"
    * full content model in "tagline_detail"
    * if plaintext or html, duplicated into channel/description
  * id
    * id
    * maps to guid
  * generator
    * url
    * version
    * value
  * copyright
    * plaintext or html in "rights"
    * full content model in "rights_detail"
  * author --> author_detail
    * name
    * url
    * email
    * name + (email) --> "author"
  * contributor --> contributors, list of
    * name
    * url
    * email
* entry
  * title
    * same as channel
  * link
    * same as channel
  * id
    * same as channel
  * issued
    * stored in "issued"
    * parsed to "issued_parsed"
  * modified
    * stored in "modified", "date"
    * parsed to "modified_parsed", "date_parsed"
  * created
    * stored in "created"
    * parsed to "created_parsed"
  * summary
    * full content model
    * duplicated in "description"
  * author
    * same as channel
  * contributor
    * same as channel
  * content
    * full content model

* CDATA sections
  * in various elements
  * with embedded markup

* HTML sanitizing
  * parent elements:
    * RSS
      * description
      * content:encoded
      * xhtml:body
      * body
      * fullitem
    * Atom
      * feed/title
      * feed/tagline
      * feed/subtitle
      * feed/info
      * feed/copyright
      * entry/title
      * entry/summary
      * entry/content
    * Atom styles
      * @type=text/html, @mode=escaped
      * @type=text/html, @mode=escaped, CDATA
      * @type=application/xhtml, @mode=xml
      * @type=text/html, @mode=base64
  * elements to strip:
    * script
    * embed
    * meta
    * link
    * object
    * frameset/frame
    * iframe
    * applet
    * blink
    * @style
    * @onabort
    * @onblur
    * @onchange
    * @onclick
    * @ondblclick
    * @onerror
    * @onfocus
    * @onkeydown
    * @onkeypress
    * @onkeyup
    * @onload
    * @onmousedown
    * @onmouseout
    * @onmouseover
    * @onmouseup
    * @onreset
    * @onresize
    * @onsubmit
    * @onunload
    * crazy RSS

* relative links
  * elements that can be relative links:
    * rss/channel/link
    * rss/channel/docs
    * rss/item/link
    * rss/item/comments
    * rss/item/wfw:comment
    * rss/item/wfw:commentRSS
    * atom/feed/link/@href
    * atom/feed/id
    * atom/feed/author/url
    * atom/feed/contributor/url
    * atom/feed/generator/@url
    * atom/entry/link/@href
    * atom/entry/id
    * atom/entry/author/url
    * atom/entry/contributor/url
  * elements that can contain embedded markup with relative links:
    * rss/item/description
    * rss/item/fullitem
    * rss/item/content:encoded
    * rss/item/xhtml:body
    * rss/item/body
    * atom/feed/title
    * atom/feed/tagline
    * atom/feed/subtitle
    * atom/feed/info
    * atom/feed/copyright
    * atom/entry/title
    * atom/entry/summary
    * atom/entry/content
  * ways to get base URI:
    * document uri
    * content-location http header
    * xml:base
    * overridden xml:base

Atom 1.0:
* feed/atom:generator (doublecheck syntax against atom03:generator)
  * @uri (was @url)
  * @version (unchanged)
  * content (unchanged)
* feed/atom:icon
  * content is URI
* feed/atom:logo
  * content is URI
* feed/atom:subtitle (was atom03:tagline)
* feed/atom:updated (was atom03:modified, sort of)
  * no more feed/modified, feed/created, or feed/created
* feed/atom:rights (was atom03:copyright)
* feed/atom:link new rels
  * see entry/atom:link new rels
* feed/atom:link new attributes
  * see entry/atom:link new attributes

* entry/id no normalization (section 4.2.6.1)
* entry/atom:category (section 4.2.2)
  * @term
  * @scheme
  * @label
* entry/atom:link rels
  * rel="alternate"
  * rel="related"
  * rel="self"
  * rel="enclosure"
    * map to enclosures array
  * rel="via"
  * rel="<absoluteURI>"
* entry/atom:link new attributes
  * @hreflang
  * @length
* entry/atom:content new standard types
  * text (was text/plain)
  * html (was text/html)
  * xhtml (was application/xhtml+xml)
  * !!!see section 4.1.3.3 Processing Model
    * startswith('text/') --> text
    * endswith('+xml') --> xml
    * endswith('/xml') --> xml
    * all others base64 (but no mode attr)
* entry/atom:content/@src
  * new src property in content dict
* entry/atom:updated (was atom03:modified, sort of)
* entry/atom:published (was atom03:issued)
  * no more modified or created
* entry/atom:rights (was atom03:copyright)
* entry/atom:source a.k.a. "Smells Like Wyman Spirit"
  * atom:author
  * atom:category
  * atom:contributor
  * atom:generator
  * atom:icon
  * atom:id
  * atom:link
  * atom:logo
  * atom:rights
  * atom:subtitle
  * atom:title
  * atom:updated

iTunes support:
* namespace variations
  * namespace are case-insensitive
* elements outside the iTunes namespace are case-insensitive
* channel/itunes:block
  * content="yes" --> true, otherwise false, see http://lists.apple.com/faq/pub/syndication-dev/index.php?sid=359&aktion=artikel&rubrik=001&id=3&lang=en
* channel/itunes:category --> category
  * @text --> term
  * @scheme is always "itms://itunes.com/browse?bp=/"
  * @label is always blank
  * subcategories are nested itunes:category elements
  * don't worry about establishing hierarchy, just treat each itunes:category as a category
* channel/itunes:explicit
* channel/itunes:image
  * itunes:link rel="image" @href
* channel/itunes:keywords
* channel/itunes:owner
* channel/itunes:subtitle
* channel/itunes:summary
* item/itunes:author
* item/itunes:block
  * see channel/itunes:block
* item/itunes:category
  * see channel/itunes:category
- item/itunes:duration
* item/itunes:explicit
* item/itunes:image
* item/itunes:keywords
* item/itunes:subtitle
* item/itunes:summary

"""
