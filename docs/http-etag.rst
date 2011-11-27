.. _http.etag:

ETag and Last-Modified Headers
==============================

ETags and Last-Modified headers are two ways that feed publishers can save
bandwidth, but they only work if clients take advantage of them.
:program:`Universal Feed Parser` gives you the ability to take advantage of
these features, but you must use them properly.

The basic concept is that a feed publisher may provide a special
:abbr:`HTTP (Hypertext Transfer Protocol)` header, called an ETag, when it
publishes a feed.  You should send this ETag back to the server on subsequent
requests.  If the feed has not changed since the last time you requested it,
the server will return a special :abbr:`HTTP (Hypertext Transfer Protocol)`
status code (``304``) and no feed data.

Using ETags to reduce bandwidth
-------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.etag
    '"6c132-941-ad7e3080"'
    >>> d2 = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml', etag=d.etag)
    >>> d2.status
    304
    >>> d2.feed
    {}
    >>> d2.entries
    []
    >>> d2.debug_message
    'The feed has not changed since you last checked, so
    the server sent no data.  This is a feature, not a bug!'

There is a related concept which accomplishes the same thing, but slightly
differently.  In this case, the server publishes the last-modified date of the
feed in the :abbr:`HTTP (Hypertext Transfer Protocol)` header.  You can send
this back to the server on subsequent requests, and if the feed has not
changed, the server will return :abbr:`HTTP (Hypertext Transfer Protocol)`
status code ``304`` and no feed data.


Using Last-Modified headers to reduce bandwidth
-----------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.modified
    (2004, 6, 11, 23, 0, 34, 4, 163, 0)
    >>> d2 = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml', modified=d.modified)
    >>> d2.status
    304
    >>> d2.feed
    {}
    >>> d2.entries
    []
    >>> d2.debug_message
    'The feed has not changed since you last checked, so
    the server sent no data.  This is a feature, not a bug!'

Clients should support both ETag and Last-Modified headers, as some servers support one but not the other.


.. important::

    If you do not support ETag and Last-Modified headers, you will repeatedly
    download feeds that have not changed.  This wastes your bandwidth and the
    publisher's bandwidth, and the publisher may ban you from accessing their
    server.


.. note::

    You can control the behaviour of :abbr:`HTTP (Hypertext Transfer Protocol)`
    caches between your application and the origin server by using the
    ``extra_headers`` parameter.  For example, you may want to send
    ``Cache-control: max-age=60`` to make the caches revalidate against the
    origin server unless their cached copy is less than a minute old.  Again,
    this should be used with consideration.


.. seealso::

    * `HTTP Conditional Get For RSS Hackers <http://fishbowl.pastiche.org/2002/10/21/http_conditional_get_for_rss_hackers>`_
    * `HTTP Web Services <http://diveintopython.org/http_web_services/>`_
