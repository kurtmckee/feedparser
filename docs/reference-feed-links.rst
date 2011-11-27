.. _reference.feed.links:



feed.links
==========




A list of dictionaries with details on the links associated with the feed.  Each link has a rel (relationship), type (content type), and href (the :abbr:`URL (Uniform Resource Locator)` that the link points to).  Some links may also have a title.

- Comes from

- /atom10:feed/atom10:link

- /atom03:feed/atom03:link

- /rss/channel/link

- /rdf:RDF/rdf:channel/rdf:link



- See also

- :ref:`reference.feed.link`





.. _reference.feed.links.rel:



feed.links[i].rel
-----------------

The relationship of this feed link.

Atom 1.0 defines five standard link relationships and describes the process for registering others.  Here are the five standard rel values:

- ``alternate``

- ``self``

- ``related``

- ``via``

- ``enclosure``





.. _reference.feed.links.type:



feed.links[i].type
------------------

The content type of the page that this feed link points to.



.. _reference.feed.links.href:



feed.links[i].href
------------------

The :abbr:`URL (Uniform Resource Locator)` of the page that this feed link points to.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is :ref:`resolved according to a set of rules <advanced.base>`.



feed.links[i].title
-------------------

The title of this feed link.