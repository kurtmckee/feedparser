.. _reference.entry.publisher_detail:

:py:attr:`entries[i].publisher_detail`
======================================

A dictionary with details about the entry publisher.


:py:attr:`entries[i].publisher_detail.name`
-------------------------------------------

The name of this entry's publisher.


.. _reference.entry.publisher_detail.href:

:py:attr:`entries[i].publisher_detail.href`
-------------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of this entry's publisher.  This can
be the publisher's home page, or a contact page with a webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].publisher_detail.email`
--------------------------------------------

The email address of this entry's publisher.


.. rubric:: Comes from

* /rss/item/dc:publisher
* /rss/item/itunes:owner
* /rdf:RDF/rdf:item/dc:publisher


.. seealso::

    * :ref:`reference.entry.publisher`
