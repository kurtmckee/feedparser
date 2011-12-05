.. _reference.entry.published:

:py:attr:`entries[i].published`
===============================

The date this entry was first published, as a string in the same format as it
was published in the original feed.

This element is :ref:`parsed as a date <advanced.date>` and stored in
:ref:`reference.entry.published_parsed`.


.. rubric:: Comes from

* /atom10:feed/atom10:entry/atom10:published
* /atom03:feed/atom03:entry/atom03:issued
* /rss/channel/item/dcterms:issued
* /rss/channel/item/pubDate
* /rdf:RDF/rdf:item/dcterms:issued


.. seealso::

    * :ref:`reference.entry.published_parsed`
