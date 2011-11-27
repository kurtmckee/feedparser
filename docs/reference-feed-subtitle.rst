.. _reference.feed.subtitle:

:py:attr:`feed.subtitle`
========================

A subtitle, tagline, slogan, or other short description of the feed.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /atom03:feed/atom03:tagline
* /atom10:feed/atom10:subtitle
* /rdf:RDF/rdf:channel/dc:description
* /rdf:RDF/rdf:channel/rdf:description
* /rss/channel/dc:description
* /rss/channel/description
* /rss/channel/itunes:subtitle


.. seealso::

    * :ref:`reference.feed.subtitle_detail`
