Password-Protected Feeds
========================

:program:`Universal Feed Parser` by default has no timeout on the http requests it makes.
A timeout argument can be added to the parse function to return from the request after the specified amount on time, in seconds, has passed.

::

    >>> import feedparser
    >>> timeout = 30
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml', timeout=timeout)
    >>> d.feed.title
    u'Sample Feed'


.. note::

    By default there is no timeout. This is to preserve the original behaviour and backward compatibility with code developed on older versions of the library.
