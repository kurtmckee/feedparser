Uncommon :abbr:`RSS (Rich Site Summary)` Elements
=================================================

These elements are less common, but are useful for niche applications and may
be present in any :abbr:`RSS (Rich Site Summary)` feed.

An :abbr:`RSS (Rich Site Summary)` feed can specify a small image which some
aggregators display as a logo.


Accessing feed image
--------------------

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss20.xml')
    >>> d.feed.image
    {'title': 'Example banner',
    'href': 'http://example.org/banner.png',
    'width': 80,
    'height': 15,
    'link': 'http://example.org/'}

Feeds and entries can be assigned to multiple categories, and in some versions
of :abbr:`RSS (Rich Site Summary)`, categories can be associated with a
"domain".  Both are free-form strings.  For historical reasons,
:program:`Universal Feed Parser` makes multiple categories available as a list
of tuples, rather than a list of dictionaries.


Accessing multiple categories
-----------------------------

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss20.xml')
    >>> d.feed.categories
    [('Syndic8', '1024'),
    ('dmoz', 'Top/Society/People/Personal_Homepages/P/')]

Each item in an :abbr:`RSS (Rich Site Summary)` feed can have an "enclosure", a
delightful misnomer that is simply a link to an external file (usually a music
or video file, but any type of file can be "enclosed").  Once rare, this
element has recently gained popularity due to the rise of
`podcasting <http://en.wikipedia.org/wiki/Podcasting>`_.  Some clients (such
as Apple's :program:`iTunes`) may automatically download enclosures; others
(such as the web-based Bloglines) may simply render each enclosure as a link.

The :abbr:`RSS (Rich Site Summary)` specification states that there can be at
most one enclosure per item.  However, Atom entries may contain more than one
enclosure per entry, so :program:`Universal Feed Parser` captures all of them
and makes them available as a list.


Accessing enclosures
--------------------

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss20.xml')
    >>> e = d.entries[0]
    >>> len(e.enclosures)
    1
    >>> e.enclosures[0]
    {'type': 'audio/mpeg',
    'length': '1069871',
    'href': 'http://example.org/audio/demo.mp3'}


Accessing feed cloud
--------------------

No one is quite sure what a cloud is.

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss20.xml')
    >>> d.feed.cloud
    {'domain': 'rpc.example.com',
    'port': '80',
    'path': '/RPC2',
    'registerprocedure': 'pingMe',
    'protocol': 'soap'}

.. note::

    For more examples of accessing :abbr:`RSS (Rich Site Summary)` elements,
    see the annotated examples: :ref:`annotated.rss10`, :ref:`annotated.rss20`,
    and :ref:`annotated.rss20dc`.
