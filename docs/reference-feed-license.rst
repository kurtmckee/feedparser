.. _reference.feed.license:

:py:attr:`feed.license`
=======================

A :abbr:`URL (Uniform Resource Locator)` of the license under which this feed
is distributed.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /atom10:feed/atom10:link[@rel="license"]/@href
* /rdf:RDF/cc:license/@rdf:resource
* /rss/channel/creativeCommons:license
