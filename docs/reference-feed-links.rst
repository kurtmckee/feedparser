.. _reference.feed.links:

:py:attr:`feed.links`
=====================

A list of dictionaries with details on the links associated with the feed.
Each link has a rel (relationship), type (content type), and href (the
:abbr:`URL (Uniform Resource Locator)` that the link points to).  Some links
may also have a title.


.. _reference.feed.links.rel:

:py:attr:`feed.links[i].rel`
----------------------------

The relationship of this feed link.

Atom 1.0 defines five standard link relationships and describes the process for
registering others.  Here are the five standard rel values:

- `alternate`
- `enclosure`
- `related`
- `self`
- `via`


.. _reference.feed.links.type:

:py:attr:`feed.links[i].type`
-----------------------------

The content type of the page that this feed link points to.


.. _reference.feed.links.href:

:py:attr:`feed.links[i].href`
-----------------------------

The :abbr:`URL (Uniform Resource Locator)` of the page that this feed link
points to.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`feed.links[i].title`
------------------------------

The title of this feed link.


.. rubric:: Comes from

* /atom03:feed/atom03:link
* /atom10:feed/atom10:link
* /rdf:RDF/rdf:channel/rdf:link
* /rss/channel/link


.. seealso::

    * :ref:`reference.feed.link`
