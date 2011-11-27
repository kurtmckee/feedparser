Uncommon :abbr:`RSS (Rich Site Summary)` Elements
=================================================

These elements are less common, but are useful for niche applications and may
be present in any :abbr:`RSS (Rich Site Summary)` feed.

An :abbr:`RSS (Rich Site Summary)` feed can specify a small image which some
aggregators display as a logo.


Accessing feed image
--------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rss20.xml')
    >>> d.feed.image
    {'title': u'Example banner',
    'href': u'http://example.org/banner.png',
    'width': 80,
    'height': 15,
    'link': u'http://example.org/'}

Feeds and entries can be assigned to multiple categories, and in some versions
of :abbr:`RSS (Rich Site Summary)`, categories can be associated with a
"domain".  Both are free-form strings.  For historical reasons,
:program:`Universal Feed Parser` makes multiple categories available as a list
of tuples, rather than a list of dictionaries.


Accessing multiple categories
-----------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rss20.xml')
    >>> d.feed.categories
    [(u'Syndic8', u'1024'),
    (u'dmoz', 'Top/Society/People/Personal_Homepages/P/')]

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

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rss20.xml')
    >>> e = d.entries[0]
    >>> len(e.enclosures)
    1
    >>> e.enclosures[0]
    {'type': u'audio/mpeg',
    'length': u'1069871',
    'href': u'http://example.org/audio/demo.mp3'}


Accessing feed cloud
--------------------

No one is quite sure what a cloud is.

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rss20.xml')
    >>> d.feed.cloud
    {'domain': u'rpc.example.com',
    'port': u'80',
    'path': u'/RPC2', 
    'registerprocedure': u'pingMe',
    'protocol': u'soap'}

.. note::

    For more examples of accessing :abbr:`RSS (Rich Site Summary)` elements,
    see the annotated examples: :ref:`annotated.rss10`, :ref:`annotated.rss20`,
    and :ref:`annotated.rss20dc`.
