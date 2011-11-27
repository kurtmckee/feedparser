.. _advanced.normalization:

Content Normalization
=====================

:program:`Universal Feed Parser` can parse many different types of feeds: Atom,
:abbr:`CDF (Channel Definition Format)`, and nine different versions of
:abbr:`RSS (Rich Site Summary)`.  You should not be forced to learn the
differences between these formats.  :program:`Universal Feed Parser` does its
best to ensure that you can treat all feeds the same way, regardless of format
or version.

You can access the basic elements of an Atom feed using :abbr:`RSS (Rich Site Summary)` terminology.

Accessing an Atom feed as an :abbr:`RSS (Rich Site Summary)` feed
-----------------------------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d['channel']['title']
    u'Sample Feed'
    >>> d['channel']['link']
    u'http://example.org/'
    >>> d['channel']['description']
    u'For documentation <em>only</em>
    >>> len(d['items'])
    1
    >>> e = d['items'][0]
    >>> e['title']
    u'First entry title'
    >>> e['link']
    u'http://example.org/entry/3'
    >>> e['description']
    u'Watch out for nasty tricks'
    >>> e['author']
    u'Mark Pilgrim (mark@example.org)'


The same thing works in reverse: you can access :abbr:`RSS (Rich Site Summary)` feeds as if they were Atom feeds.

Accessing an :abbr:`RSS (Rich Site Summary)` feed as an Atom feed
-----------------------------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse(' http://feedparser.org/docs/examples/rss20.xml')
    >>> d.feed.subtitle_detail
    {'type': 'text/html',
    'base': 'http://feedparser.org/docs/examples/rss20.xml',
    'language': None,
    'value': u'For documentation <em>only</em>'}
    >>> len(d.entries)
    1
    >>> e = d.entries[0]
    >>> e.links
    [{'rel': 'alternate',
    'type': 'text/html',
    'href': u'http://example.org/item/1'}]
    >>> e.summary_detail
    {'type': 'text/html',
    'base': 'http://feedparser.org/docs/examples/rss20.xml',
    'language': u'en',
    'value': u'Watch out for <span>nasty tricks</span>'}
    >>> e.updated_parsed
    (2002, 9, 5, 0, 0, 1, 3, 248, 0)


.. note::

    For more examples of how :program:`Universal Feed Parser` normalizes
    content from different formats, see :ref:`annotated`.
