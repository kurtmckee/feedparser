.. _reference.version:






The format and version of the feed.

version
=======

Here is the complete list of known feed types and versions that may be returned in ``version``:

``rss090``
    `:abbr:`RSS (Rich Site Summary)` 0.90 <http://www.purplepages.ie/RSS/netscape/rss0.90.html>`_

``rss091n``
    `Netscape :abbr:`RSS (Rich Site Summary)` 0.91 <http://my.netscape.com/publish/formats/rss-spec-0.91.html>`_

``rss091u``
    `Userland :abbr:`RSS (Rich Site Summary)` 0.91 <http://backend.userland.com/rss091>`_ (`differences from Netscape :abbr:`RSS (Rich Site Summary)` 0.91 <http://diveintomark.org/archives/2004/02/04/incompatible-rss#example3>`_)

``rss10``
    `:abbr:`RSS (Rich Site Summary)` 1.0 <http://purl.org/rss/1.0/>`_

``rss092``
    `:abbr:`RSS (Rich Site Summary)` 0.92 <http://backend.userland.com/rss092>`_

``rss093``
    `:abbr:`RSS (Rich Site Summary)` 0.93 <http://backend.userland.com/rss093>`_

``rss094``
    :abbr:`RSS (Rich Site Summary)` 0.94 (no accurate specification is known to exist)

``rss20``
    `:abbr:`RSS (Rich Site Summary)` 2.0 <http://blogs.law.harvard.edu/tech/rss>`_

``rss``
    :abbr:`RSS (Rich Site Summary)` (unknown or unrecognized version)

``atom01``
    `Atom 0.1 <http://www.intertwingly.net/blog/1506.html>`_

``atom02``
    `Atom 0.2 <http://diveintomark.org/public/2003/08/atom02spec.txt>`_

``atom03``
    `Atom 0.3 <http://www.mnot.net/drafts/draft-nottingham-atom-format-02.html>`_

``atom10``
    `Atom 1.0 <http://www.ietf.org/rfc/rfc4287>`_

``atom``
    Atom (unknown or unrecognized version)

``cdf``
    `:abbr:`CDF (Channel Definition Format)` <http://www.w3.org/TR/NOTE-CDFsubmit.html>`_

``hotrss``
    `Hot :abbr:`RSS (Rich Site Summary)` <http://diveintomark.org/archives/2004/04/14/hot-rss>`_

If the feed type is completely unknown, ``version`` will be an empty string.

.. tip:: This element always exists, although it may be an empty string if the version can not be determined.