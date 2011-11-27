.. _reference.feed.title:

:py:attr:`feed.title`
=====================

The title of the feed.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /atom03:feed/atom03:title
* /atom10:feed/atom10:title
* /rdf:RDF/rdf:channel/dc:title
* /rdf:RDF/rdf:channel/rdf:title
* /rss/channel/dc:title
* /rss/channel/title


.. seealso::

    * :ref:`reference.feed.title_detail`
