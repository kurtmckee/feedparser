.. _reference.feed.rights:

:py:attr:`feed.rights`
======================

A human-readable copyright statement for the feed.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


.. note::

    For machine-readable copyright information, see :ref:`reference.feed.license`.


.. rubric:: Comes from

* /atom03:feed/atom03:copyright
* /atom10:feed/atom10:rights
* /rdf:RDF/rdf:channel/dc:rights
* /rss/channel/copyright
* /rss/channel/dc:rights


.. seealso::

    * :ref:`reference.feed.rights_detail`
