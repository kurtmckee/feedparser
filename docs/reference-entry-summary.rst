.. _reference.entry.summary:

:py:attr:`entries[i].summary`
=============================

A summary of the entry.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`\s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.

Some publishing systems auto-generate this value from the first few words or
first paragraph of the entry.  Other publishing systems misuse it to include
the full content.  In the latter cases, :program:`Universal Feed Parser` ought
to detect it and put the value in :ref:`reference.entry.content` instead, but
it doesn't.


.. note::

    Some feeds include both a summary and description element for each entry.  In
    this case, the first element will be available in ``entry['summary']`` and the
    second will be available in ``entry['content'][0]``.


.. rubric:: Comes from

* /atom10:feed/atom10:entry/atom10:summary
* /atom03:feed/atom03:entry/atom03:summary
* /rss/channel/item/description
* /rss/channel/item/dc:description
* /rdf:RDF/rdf:item/rdf:description
* /rdf:RDF/rdf:item/dc:description


.. seealso::

    * :ref:`reference.entry.summary_detail`
