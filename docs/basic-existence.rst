Testing for Existence
=====================

Feeds in the real world may be missing elements, even elements that are
required by the specification.  You should always test for the existence of an
element before getting its value.  Never assume an element is present.

To test whether elements exist, you can use standard :program:`Python`
dictionary idioms.

Testing if elements are present
-------------------------------

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom10.xml')
    >>> 'title' in d.feed
    True
    >>> 'ttl' in d.feed
    False
    >>> d.feed.get('title', 'No title')
    'Sample feed'
    >>> d.feed.get('ttl', 60)
    60
