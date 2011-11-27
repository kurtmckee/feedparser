Common Atom Elements
====================

Atom feeds generally contain more information than :abbr:`RSS (Rich Site Summary)`
feeds (because more elements are required), but the most commonly used elements
are still title, link, subtitle/description, various dates, and ID.

This sample Atom feed is at `http://feedparser.org/docs/examples/atom10.xml
<http://feedparser.org/docs/examples/atom10.xml>`_.

.. sourcecode:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
    xml:base="http://example.org/"
    xml:lang="en">
    <title type="text">Sample Feed</title>
    <subtitle type="html">
    For documentation &lt;em&gt;only&lt;/em&gt;
    </subtitle>
    <link rel="alternate" href="/"/>
    <link rel="self"
    type="application/atom+xml"
    href="http://www.example.org/atom10.xml"/>
    <rights type="html">
    &lt;p>Copyright 2005, Mark Pilgrim&lt;/p>&lt;
    </rights>
    <id>tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml</id>
    <generator
    uri="http://example.org/generator/"
    version="4.0">
    Sample Toolkit
    </generator>
    <updated>2005-11-09T11:56:34Z</updated>
    <entry>
    <title>First entry title</title>
    <link rel="alternate"
    href="/entry/3"/>
    <link rel="related"
    type="text/html"
    href="http://search.example.com/"/>
    <link rel="via"
    type="text/html"
    href="http://toby.example.com/examples/atom10"/>
    <link rel="enclosure"
    type="video/mpeg4"
    href="http://www.example.com/movie.mp4"
    length="42301"/>
    <id>tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3</id>
    <published>2005-11-09T00:23:47Z</published>
    <updated>2005-11-09T11:56:34Z</updated>
    <summary type="text/plain" mode="escaped">Watch out for nasty tricks</summary>
    <content type="application/xhtml+xml" mode="xml"
    xml:base="http://example.org/entry/3" xml:lang="en-US">
    <div xmlns="http://www.w3.org/1999/xhtml">Watch out for
    <span style="background: url(javascript:window.location='http://example.org/')">
    nasty tricks</span></div>
    </content>
    </entry>
    </feed>

The feed elements are available in ``d.feed``.

Accessing Common Feed Elements
------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.feed.title
    u'Sample feed'
    >>> d.feed.link
    u'http://example.org/'
    >>> d.feed.subtitle
    u'For documentation <em>only</em>'
    >>> d.feed.updated
    u'2005-11-09T11:56:34Z'
    >>> d.feed.updated_parsed
    (2005, 11, 9, 11, 56, 34, 2, 313, 0)
    >>> d.feed.id
    u'tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml'

Entries are available in ``d.entries``, which is a list. You access entries in
the order in which they appear in the original feed, so the first entry is
``d.entries[0]``.

Accessing Common Entry Elements
-------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.entries[0].title
    u'First entry title'
    >>> d.entries[0].link
    u'http://example.org/entry/3
    >>> d.entries[0].id
    u'tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3'
    >>> d.entries[0].published
    u'2005-11-09T00:23:47Z'
    >>> d.entries[0].published_parsed
    (2005, 11, 9, 0, 23, 47, 2, 313, 0)
    >>> d.entries[0].updated
    u'2005-11-09T11:56:34Z'
    >>> d.entries[0].updated_parsed
    (2005, 11, 9, 11, 56, 34, 2, 313, 0)
    >>> d.entries[0].summary
    u'Watch out for nasty tricks'
    >>> d.entries[0].content
    [{'type': u'application/xhtml+xml',
    'base': u'http://example.org/entry/3',
    'language': u'en-US',
    'value': u'<div>Watch out for <span>nasty tricks</span></div>'}]

.. note::

    The parsed summary and content are not the same as they appear in the
    original feed. The original elements contained dangerous :abbr:`HTML
    (HyperText Markup Language)` markup which was sanitized. See
    :ref:`advanced.sanitization` for details.

Because Atom entries can have more than one content element,
``d.entries[0].content`` is a list of dictionaries. Each dictionary contains
metadata about a single content element. The two most important values in the
dictionary are the content type, in ``d.entries[0].content[0].type``, and the
actual content value, in ``d.entries[0].content[0].value``.

You can get this level of detail on other Atom elements too.
