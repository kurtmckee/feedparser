.. _reference.feed.publisher_detail:

``feed.publisher_detail``
================================

A dictionary with details about the feed publisher.


``feed.publisher_detail.name``
-------------------------------------

The name of this feed's publisher.


.. _reference.feed.publisher_detail.href:

``feed.publisher_detail.href``
-------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of this feed's publisher.  This can
be the publisher's home page, or a contact page with a webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


``feed.publisher_detail.email``
--------------------------------------

The email address of this feed's publisher.


.. rubric:: Comes from

* /rdf:RDF/rdf:channel/dc:publisher
* /rss/channel/dc:publisher
* /rss/channel/itunes:owner
* /rss/channel/webMaster


.. seealso::

    * :ref:`reference.feed.publisher`
