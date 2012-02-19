.. _reference.feed.updated:

:py:attr:`feed.updated`
=======================

The date the feed was last updated, as a string in the same format as it was
published in the original feed.

This element is :ref:`parsed as a date <advanced.date>` and stored in
:ref:`reference.feed.updated_parsed`.


.. note::

    As of version 5.1.1, if this key doesn't exist but
    :py:attr:`feed.published` does, the value of
    :py:attr:`feed.published` will be returned.

    In the past the RSS pubDate element was stored in `updated`, but this incorrect
    behavior was reported in issue 310. However, developers may have come to rely
    on this incorrect behavior -- as was reported in issue 328 -- so to help avoid
    hurting their users' experience, this mapping from `updated` to `published` was
    temporarily introduced to give developers time to update their software, and to
    give users time to upgrade.

    This mapping is temporary and will be removed in a future version of
    feedparser.


.. rubric:: Comes from

* /atom03:feed/atom03:modified
* /atom10:feed/atom10:updated
* /rdf:RDF/rdf:channel/dc:date
* /rdf:RDF/rdf:channel/dcterms:modified
* /rss/channel/dc:date


.. seealso::

    * :ref:`reference.feed.updated_parsed`
