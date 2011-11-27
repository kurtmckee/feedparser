Other :abbr:`HTTP (Hypertext Transfer Protocol)` Headers
========================================================

You can specify extra :abbr:`HTTP (Hypertext Transfer Protocol)` request
headers as a dictionary.  When you download a feed from a remote web server,
:program:`Universal Feed Parser` exposes the complete set of
:abbr:`HTTP (Hypertext Transfer Protocol)` response headers as a dictionary.


.. _example.http.headers.request:

Sending custom :abbr:`HTTP (Hypertext Transfer Protocol)` request headers
-------------------------------------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom03.xml',
                              extra_headers={'Cache-control': 'max-age=0'})


Accessing other :abbr:`HTTP (Hypertext Transfer Protocol)` response headers
---------------------------------------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom03.xml')
    >>> d.headers
    {'date': 'Fri, 11 Jun 2004 23:57:50 GMT',
    'server': 'Apache/2.0.49 (Debian GNU/Linux)',
    'last-modified': 'Fri, 11 Jun 2004 23:00:34 GMT',
    'etag': '"6c132-941-ad7e3080"',
    'accept-ranges': 'bytes',
    'vary': 'Accept-Encoding,User-Agent',
    'content-encoding': 'gzip',
    'content-length': '883',
    'connection': 'close',
    'content-type': 'application/xml'}

