.. _reference.entry.updated:

:py:attr:`entries[i].updated`
=============================

The date this entry was last updated, as a string in the same format as it was
published in the original feed).

This element is :ref:`parsed as a date <advanced.date>` and stored in
:ref:`reference.entry.updated_parsed`.


.. rubric:: Comes from

* /atom03:feed/atom03:entry/atom03:modified
* /atom10:feed/atom10:entry/atom10:updated
* /rdf:RDF/rdf:item/dc:date
* /rdf:RDF/rdf:item/dcterms:modified
* /rss/channel/item/dc:date
* /rss/channel/item/dcterms:modified
* /rss/channel/item/pubDate


.. seealso::

    * :ref:`reference.entry.updated_parsed`
