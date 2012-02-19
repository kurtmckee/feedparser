.. _reference.feed.updated_parsed:

:py:attr:`feed.updated_parsed`
==============================

The date the feed was last updated, as a standard :program:`Python` 9-tuple.


.. note::

    As of version 5.1.1, if this key doesn't exist but
    :py:attr:`feed.published_parsed` does, the value of
    :py:attr:`feed.published_parsed` will be returned.

    In the past the RSS pubDate element was stored in `updated`, but this incorrect
    behavior was reported in issue 310. However, developers may have come to rely
    on this incorrect behavior -- as was reported in issue 328 -- so to help avoid
    hurting their users' experience, this mapping from `updated_parsed` to
    `published_parsed` was temporarily introduced to give developers time to update
    their software, and to give users time to upgrade.

    This mapping is temporary and will be removed in a future version of
    feedparser.


.. rubric:: Comes from

* /atom03:feed/atom03:modified
* /atom10:feed/atom10:updated
* /rdf:RDF/rdf:channel/dc:date
* /rdf:RDF/rdf:channel/dcterms:modified
* /rss/channel/dc:date


.. seealso::

    * :ref:`reference.feed.updated`
