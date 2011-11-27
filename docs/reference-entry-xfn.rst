.. _reference.entry.xfn:

:py:attr:`entries[i].xfn`
=========================

A list of :ref:`XFN relationships <advanced.microformats.xfn>` found in this
entry's :abbr:`HTML (HyperText Markup Language)` content.


.. rubric:: Comes from

* /atom03:feed/atom03:entry/atom03:content
* /atom03:feed/atom03:entry/atom03:summary
* /atom10:feed/atom10:entry/atom10:content
* /atom10:feed/atom10:entry/atom10:summary
* /rdf:RDF/rdf:item/content:encoded
* /rdf:RDF/rdf:item/dc:description
* /rdf:RDF/rdf:item/rdf:description
* /rss/channel/item/body
* /rss/channel/item/content:encoded
* /rss/channel/item/dc:description
* /rss/channel/item/description
* /rss/channel/item/fullitem
* /rss/channel/item/xhtml:body

entries[i].xfn is a list.  Each list item represents a single person and may
contain the following values:


:py:attr:`entries[i].xfn[j].relationships`
------------------------------------------

A list of relationships for this person.  Each list item is a string, either
one of the constants defined in the `XFN 1.1 profile`_ or :ref:`one of these
variations <advanced.microformats.xfn>`.

.. _XFN 1.1 profile: http://gmpg.org/xfn/11


:py:attr:`entries[i].xfn[j].href`
---------------------------------

The :abbr:`URI (Uniform Resource Identifier)` for this person.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].xfn[j].name`
---------------------------------

The name of this person, a string.
