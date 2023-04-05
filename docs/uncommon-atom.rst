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
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom10.xml')
    >>> e = d.entries[0]
    >>> len(e.contributors)
    2
    >>> e.contributors[0]
    {'name': 'Joe',
    'href': 'http://example.org/joe/',
    'email': 'joe@example.org'}
    >>> e.contributors[1]
    {'name': 'Sam',
    'href': 'http://example.org/sam/',
    'email': 'sam@example.org'}

Besides an alternate link, each Atom feed or entry can have an arbitrary number
of other links.  Each link is distinguished by its type attribute, which is a
MIME-style content type, and its rel attribute.


Accessing multiple links
------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom10.xml')
    >>> e = d.entries[0]
    >>> len(e.links)
    4
    >>> e.links[0]
    {'rel': 'alternate',
    'type': 'text/html',
    'href': 'http://example.org/entry/3'}
    >>> e.links[1]
    {'rel': 'related',
    'type': 'text/html',
    'href': 'http://search.example.com/'}
    >>> e.links[2]
    {'rel': 'via',
    'type': 'text/html',
    'href': 'http://toby.example.com/examples/atom10'}
    >>> e.links[3]
    {'rel': 'enclosure',
    'type': 'video/mpeg4',
    'href': 'http://www.example.com/movie.mp4',
    'length': '42301'}


.. note::

    For more examples of accessing Atom elements, see the annotated examples
    :ref:`annotated.atom10` and :ref:`annotated.atom03`.
