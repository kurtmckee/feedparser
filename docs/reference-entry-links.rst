.. _reference.entry.links:

:py:attr:`entries[i].links`
===========================

A list of dictionaries with details on the links associated with the feed.
Each link has a rel (relationship), type (content type), and href (the
:abbr:`URL (Uniform Resource Locator)` that the link points to).  Some links
may also have a title.


.. _reference.entry.links.rel:

:py:attr:`entries[i].links[j].rel`
----------------------------------

The relationship of this entry link.

Atom 1.0 defines five standard link relationships and describes the process for
registering others.  Here are the five standard rel values:

* `alternate`
* `enclosure`
* `related`
* `self`
* `via`


.. _reference.entry.links.type:

:py:attr:`entries[i].links[j].type`
-----------------------------------

The content type of the page that this entry link points to.


.. _reference.entry.links.href:

:py:attr:`entries[i].links[j].href`
-----------------------------------

The :abbr:`URL (Uniform Resource Locator)` of the page that this entry link
points to.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.entry.links.title:

:py:attr:`entries[i].links[j].title`
------------------------------------

The title of this entry link.


.. rubric:: Comes from

- /atom03:feed/atom03:entry/atom03:link
- /atom10:feed/atom10:entry/atom10:link
- /rdf:RDF/rdf:item/rdf:link
- /rss/channel/item/link


.. seealso::

    * :ref:`reference.entry.link`
