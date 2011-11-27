Uncommon Atom Elements
======================

These elements are less common, but are useful for niche applications and may
be present in any Atom feed.

Besides an author, each Atom feed or entry can have an arbitrary number of
contributors. :program:`Universal Feed Parser` makes these available as a
list.

Accessing contributors
----------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> e = d.entries[0]
    >>> len(e.contributors)
    2
    >>> e.contributors[0]
    {'name': u'Joe',
    'href': u'http://example.org/joe/',
    'email': u'joe@example.org'}
    >>> e.contributors[1]
    {'name': u'Sam',
    'href': u'http://example.org/sam/',
    'email': u'sam@example.org'}

Besides an alternate link, each Atom feed or entry can have an arbitrary number
of other links.  Each link is distinguished by its type attribute, which is a
MIME-style content type, and its rel attribute.


Accessing multiple links
------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> e = d.entries[0]
    >>> len(e.links)
    4
    >>> e.links[0]
    {'rel': u'alternate',
    'type': u'text/html',
    'href': u'http://example.org/entry/3'}
    >>> e.links[1]
    {'rel': u'related',
    'type': u'text/html',
    'href': u'http://search.example.com/'}
    >>> e.links[2]
    {'rel': u'via',
    'type': u'text/html',
    'href': u'http://toby.example.com/examples/atom10'}
    >>> e.links[3]
    {'rel': u'enclosure',
    'type': u'video/mpeg4',
    'href': u'http://www.example.com/movie.mp4',
    'length': u'42301'}


.. note::

    For more examples of accessing Atom elements, see the annotated examples
    :ref:`annotated.atom10` and :ref:`annotated.atom03`.
