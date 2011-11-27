.. _reference.entry.license:

:py:attr:`entries[i].license`
=============================

A :abbr:`URL (Uniform Resource Locator)` of the license under which this entry
is distributed.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.

.. rubric:: Comes from

* /atom10:feed/atom10:entry/atom10:link[@rel="license"]/@href
* /rdf:RDF/rdf:item/cc:license/@rdf:resource
* /rss/channel/item/creativeCommons:license
