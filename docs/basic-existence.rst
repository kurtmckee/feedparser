Testing for Existence
=====================

Feeds in the real world may be missing elements, even elements that are
required by the specification.  You should always test for the existence of an
element before getting its value.  Never assume an element is present.

Use standard :program:`Python` dictionary functions such as ``has_key`` to test
whether an element exists.

Testing if elements are present
-------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.feed.has_key('title')
    True
    >>> d.feed.has_key('ttl')
    False
    >>> d.feed.get('title', 'No title')
    u'Sample feed'
    >>> d.feed.get('ttl', 60)
    60

