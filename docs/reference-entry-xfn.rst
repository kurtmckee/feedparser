.. _reference.entry.xfn:



entries[i].xfn
==============




A list of :ref:`:abbr:`XFN (XHTML Friends Network)` relationships <advanced.microformats.xfn>` found in this entry's :abbr:`HTML (HyperText Markup Language)` content.

- Comes from

- /atom10:feed/atom10:entry/atom10:summary

- /atom03:feed/atom03:entry/atom03:summary

- /rss/channel/item/description

- /rss/channel/item/dc:description

- /rdf:RDF/rdf:item/rdf:description

- /rdf:RDF/rdf:item/dc:description

- /atom10:feed/atom10:entry/atom10:content

- /atom03:feed/atom03:entry/atom03:content

- /rss/channel/item/content:encoded

- /rss/channel/item/body

- /rss/channel/item/xhtml:body

- /rss/channel/item/fullitem

- /rdf:RDF/rdf:item/content:encoded




entries[i].xfn is a list.  Each list item represents a single person and may contain the following values:




entries[i].xfn[j].relationships
-------------------------------

A list of relationships for this person.  Each list item is a string, either one of the constants defined in the `:abbr:`XFN (XHTML Friends Network)` 1.1 profile <http://gmpg.org/xfn/11>`_ or :ref:`one of these variations <advanced.microformats.xfn>`.




entries[i].xfn[j].href
----------------------

The :abbr:`URI (Uniform Resource Identifier)` for this person.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is :ref:`resolved according to a set of rules <advanced.base>`.




entries[i].xfn[j].name
----------------------

The name of this person, a string.