.. _reference.feed.author_detail:

:py:attr:`feed.author_detail`
=============================

A dictionary with details about the feed author.


.. _reference.feed.author_detail.name:

:py:attr:`feed.author_detail.name`
----------------------------------

The name of the feed author.


.. _reference.feed.author_detail.href:

:py:attr:`feed.author_detail.href`
----------------------------------

The :abbr:`URL (Uniform Resource Locator)` of the feed author.  This can be the
author's home page, or a contact page with a webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.feed.author_detail.email:

:py:attr:`feed.author_detail.email`
-----------------------------------

The email address of the feed author.


.. rubric:: Comes from

* /atom03:feed/atom03:author
* /atom10:feed/atom10:author
* /rdf:RDF/rdf:channel/dc:author
* /rdf:RDF/rdf:channel/dc:creator
* /rss/channel/dc:author
* /rss/channel/dc:creator
* /rss/channel/itunes:author
* /rss/channel/managingEditor


.. seealso::

    * :ref:`reference.feed.author`
