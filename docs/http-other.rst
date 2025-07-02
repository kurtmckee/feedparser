Other :abbr:`HTTP (Hypertext Transfer Protocol)` Headers
========================================================

When you download a feed from a remote web server,
:program:`Universal Feed Parser` exposes the complete set of
:abbr:`HTTP (Hypertext Transfer Protocol)` response headers as a dictionary.


Accessing :abbr:`HTTP (Hypertext Transfer Protocol)` response headers
---------------------------------------------------------------------

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom03.xml')
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


Customizing :abbr:`HTTP (Hypertext Transfer Protocol)` request headers
----------------------------------------------------------------------

If you need to customize aspects of requests for a feed, such as the request
headers used, you should retrieve the feed yourself with any settings you need
(e.g. via `requests <https://requests.readthedocs.io>` - this is what
:program:`Universal Feed Parser` uses internally), and then you can just call
``feedparser.parse`` on the retrieved feed content.
