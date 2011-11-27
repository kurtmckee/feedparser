.. _reference.feed.info:

:py:attr:`feed.info`
====================

Free-form human-readable description of the feed format itself.  Intended for
people who view the feed in a browser, to explain what they just clicked on.
This element is generally ignored by feed readers.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /atom03:feed/atom03:info
* /rss/channel/feedburner:browserFriendly


.. seealso::

    * :ref:`reference.feed.info_detail`
