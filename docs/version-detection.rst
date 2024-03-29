Feed Type and Version Detection
===============================

:program:`Universal Feed Parser` attempts to autodetect the type and version of
the feeds it parses.  There are many subtle and not-so-subtle differences
between the different versions of :abbr:`RSS (Rich Site Summary)`, and
applications may choose to handle different feed types in different ways.

Accessing feed version
----------------------

..  code-block:: pycon

    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom10.xml')
    >>> d.version
    'atom10'
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom03.xml')
    >>> d.version
    'atom03'
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss20.xml')
    >>> d.version
    'rss20'
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss20dc.xml')
    >>> d.version
    'rss20'
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/rss10.rdf')
    >>> d.version
    'rss10'


Here is the complete list of known feed types and versions that may be returned in ``version``:

``rss090``
    `RSS 0.90 <http://www.purplepages.ie/RSS/netscape/rss0.90.html>`_

``rss091n``
    `Netscape RSS 0.91 <http://my.netscape.com/publish/formats/rss-spec-0.91.html>`_

``rss091u``
    `Userland RSS 0.91 <http://backend.userland.com/rss091>`_ (`differences from Netscape RSS 0.91 <https://web.archive.org/web/20110927015220/http://diveintomark.org/archives/2004/02/04/incompatible-rss#example3>`_)

``rss10``
    `RSS 1.0 <http://purl.org/rss/1.0/>`_

``rss092``
    `RSS 0.92 <http://backend.userland.com/rss092>`_

``rss093``
    `RSS 0.93 <http://backend.userland.com/rss093>`_

``rss094``
    :abbr:`RSS (Rich Site Summary)` 0.94 (no accurate specification is known to exist)

``rss20``
    `RSS 2.0 <http://blogs.law.harvard.edu/tech/rss>`_

``rss``
    :abbr:`RSS (Rich Site Summary)` (unknown or unrecognized version)

``atom01``
    `Atom 0.1 <http://www.intertwingly.net/blog/1506.html>`_

``atom02``
    `Atom 0.2 <https://web.archive.org/web/20080612041743/http://diveintomark.org/public/2003/08/atom02spec.txt>`_

``atom03``
    `Atom 0.3 <http://www.mnot.net/drafts/draft-nottingham-atom-format-02.html>`_

``atom10``
    `Atom 1.0 <http://www.ietf.org/rfc/rfc4287>`_

``atom``
    Atom (unknown or unrecognized version)

``cdf``
    `CDF <http://www.w3.org/TR/NOTE-CDFsubmit.html>`_

``json1``
    `JSONFeed v1 <https://jsonfeed.org/version/1>`_. In cases where no MIME type is
    available, JSON is assumed if the first non-whitespace character of the
    data is an opening brace ``{``.

``json11``
    `JSONFeed v1.1 <https://jsonfeed.org/version/1.1>`_

If the feed type is completely unknown, ``version`` will be an empty string.
