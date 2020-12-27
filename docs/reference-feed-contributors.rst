``feed.contributors``
============================

A list of contributors (secondary authors) to this feed.


``feed.contributors[i].name``
------------------------------------

The name of this contributor.


.. _reference.feed.contributors.href:

``feed.contributors[i].href``
------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of this contributor.  This can be
the contributor's home page, or a contact page with a webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


``feed.contributors[i].email``
-------------------------------------

The email address of this contributor.


.. rubric:: Comes from

* /atom03:feed/atom03:contributor
* /atom10:feed/atom10:contributor
* /rss/channel/dc:contributor
