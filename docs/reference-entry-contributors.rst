:py:attr:`entries[i].contributors`
==================================

A list of contributors (secondary authors) to this entry.


.. _reference.entry.contributors.name:

:py:attr:`entries[i].contributors[j].name`
------------------------------------------

The name of this contributor.


.. _reference.entry.contributors.href:

:py:attr:`entries[i].contributors[j].href`
------------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of this contributor.  This can be
the contributor's home page, or a contact page with a webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.entry.contributors.email:

:py:attr:`entries[i].contributors[j].email`
-------------------------------------------

The email address of this contributor.


.. rubric:: Comes from

* /atom03:feed/atom03:entry/atom03:contributor
* /atom10:feed/atom10:entry/atom10:contributor
* /rss/channel/item/dc:contributor
