:abbr:`HTTP (Hypertext Transfer Protocol)` Redirects
====================================================

When you download a feed from a remote web server, :program:`Universal Feed Parser`
exposes the :abbr:`HTTP (Hypertext Transfer Protocol)` status code.  You need
to understand the different codes, including permanent and temporary redirects,
and feeds that have been marked "gone".

When a feed has temporarily moved to a new location, the web server will return
a ``302`` status code.  :program:`Universal Feed Parser` makes this available
in ``d.status``.

There is nothing special you need to do with temporary redirects; by the time
you learn about it, :program:`Universal Feed Parser` has already followed the
redirect to the new location (available in ``d.href``), downloaded the feed,
and parsed it.  Since the redirect is temporary, you should continue requesting
the original :abbr:`URL (Uniform Resource Locator)` the next time you want to
parse the feed.


Noticing temporary redirects
----------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/temporary.xml')
    >>> d.status
    302
    >>> d.href
    'http://feedparser.org/docs/examples/atom10.xml'
    >>> d.feed.title
    u'Sample Feed'

When a feed has permanently moved to a new location, the web server will return
a ``301`` status code.  Again, :program:`Universal Feed Parser` makes this
available in ``d.status``.


If you are polling a feed on a regular basis, it is very important to check the
status code (``d.status``) every time you download.  If the feed has been
permanently redirected, you should update your database or configuration file
with the new address (``d.href``).  Repeatedly requesting the original address
of a feed that has been permanently redirected is very rude, and may get you
banned from the server.


Noticing permanent redirects
----------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/permanent.xml')
    >>> d.status
    301
    >>> d.href
    'http://feedparser.org/docs/examples/atom10.xml'
    >>> d.feed.title
    u'Sample Feed'


When a feed has been permanently deleted, the web server will return a ``410``
status code.  If you ever receive a ``410``, you should stop polling the feed
and inform the end user that the feed is gone for good.


Repeatedly requesting a feed that has been marked as "gone" is very rude, and
may get you banned from the server.


Noticing feeds marked "gone"
----------------------------

::

    
    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/gone.xml')
    >>> d.status
    410

