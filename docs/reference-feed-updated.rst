.. _reference.feed.updated:

:py:attr:`feed.updated`
=======================

The date the feed was last updated, as a string in the same format as it was
published in the original feed.

This element is :ref:`parsed as a date <advanced.date>` and stored in
:ref:`reference.feed.updated_parsed`.


.. rubric:: Comes from

* /atom03:feed/atom03:modified
* /atom10:feed/atom10:updated
* /rdf:RDF/rdf:channel/dc:date
* /rdf:RDF/rdf:channel/dcterms:modified
* /rss/channel/dc:date
* /rss/channel/pubDate


.. seealso::

    * :ref:`reference.feed.updated_parsed`
