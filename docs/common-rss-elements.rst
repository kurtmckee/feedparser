Common :abbr:`RSS (Rich Site Summary)` Elements
===============================================

The most commonly used elements in :abbr:`RSS (Rich Site Summary)` feeds
(regardless of version) are title, link, description, publication date, and entry
ID.  The publication date comes from the pubDate element, and the entry ID comes
from the guid element.

This sample :abbr:`RSS (Rich Site Summary)` feed is at
`http://feedparser.org/docs/examples/rss20.xml
<http://feedparser.org/docs/examples/rss20.xml>`_.

.. sourcecode:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0">
    <channel>
    <title>Sample Feed</title>
    <description>For documentation &lt;em&gt;only&lt;/em&gt;</description>
    <link>http://example.org/</link>
    <pubDate>Sat, 07 Sep 2002 00:00:01 GMT</pubDate>
    <!-- other elements omitted from this example -->
    <item>
    <title>First entry title</title>
    <link>http://example.org/entry/3</link>
    <description>Watch out for &lt;span style="background-image:
    url(javascript:window.location='http://example.org/')"&gt;nasty
    tricks&lt;/span&gt;</description>
    <pubDate>Thu, 05 Sep 2002 00:00:01 GMT</pubDate>
    <guid>http://example.org/entry/3</guid>
    <!-- other elements omitted from this example -->
    </item>
    </channel>
    </rss>


The channel elements are available in ``d.feed``.

Accessing Common Channel Elements
---------------------------------
::


    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rss20.xml')
    >>> d.feed.title
    u'Sample Feed'
    >>> d.feed.link
    u'http://example.org/'
    >>> d.feed.description
    u'For documentation <em>only</em>'
    >>> d.feed.published
    u'Sat, 07 Sep 2002 00:00:01 GMT'
    >>> d.feed.published_parsed
    (2002, 9, 7, 0, 0, 1, 5, 250, 0)


The items are available in ``d.entries``, which is a list.  You access items in the list in the same order in which they appear in the original feed, so the first item is available in ``d.entries[0]``.

Accessing Common Item Elements
------------------------------
::


    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rss20.xml')
    >>> d.entries[0].title
    u'First item title'
    >>> d.entries[0].link
    u'http://example.org/item/1'
    >>> d.entries[0].description
    u'Watch out for <span>nasty tricks</span>'
    >>> d.entries[0].published
    u'Thu, 05 Sep 2002 00:00:01 GMT'
    >>> d.entries[0].published_parsed
    (2002, 9, 5, 0, 0, 1, 3, 248, 0)
    >>> d.entries[0].id
    u'http://example.org/guid/1'


.. tip:: You can also access data from :abbr:`RSS (Rich Site Summary)` feeds using Atom terminology.  See :ref:`advanced.normalization` for details.
