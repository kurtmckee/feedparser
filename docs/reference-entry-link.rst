.. _reference.entry.link:

:py:attr:`entries[i].link`
==========================

The primary link of this entry.  Most feeds use this as the permanent link to
the entry in the site's archives.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.

Some :abbr:`RSS (Rich Site Summary)` feeds use guid when they mean link.  guid
can also be used as an opaque identifier that has nothing to do with links.  If
an :abbr:`RSS (Rich Site Summary)` feed uses guid as the entry link and no link
is present, :program:`Universal Feed Parser` detects this and makes the guid
available in :py:attr:`entries[i].link`.

In other words, you can always use :py:attr:`entries[i].link` to get the entry
link, regardless of how the feed is actually structured.


.. rubric:: Comes from

- /atom03:feed/atom03:entry/atom03:link[@rel="alternate"]/@href
- /atom10:feed/atom10:entry/atom10:link[@rel="alternate"]/@href
- /atom10:feed/atom10:entry/atom10:link[not(@rel)]/@href
- /rdf:RDF/rdf:item/rdf:link
- /rss/channel/item/link


.. seealso::

    * :ref:`reference.entry.links`
