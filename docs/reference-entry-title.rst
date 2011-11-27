.. _reference.entry.title:

:py:attr:`entries[i].title`
===========================

The title of the entry.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /atom03:feed/atom03:entry/atom03:title
* /atom10:feed/atom10:entry/atom10:title
* /rdf:RDF/rdf:item/dc:title
* /rdf:RDF/rdf:item/rdf:title
* /rss/channel/item/dc:title
* /rss/channel/item/title


.. seealso::

    * :ref:`reference.entry.title_detail`
