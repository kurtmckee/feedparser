.. _reference.entry.author_detail:

:py:attr:`entries[i].author_detail`
===================================

A dictionary with details about the author of this entry.

.. seealso::

    * :ref:`reference.entry.author`


.. _reference.entry.author_detail.name:

:py:attr:`entries[i].author_detail.name`
----------------------------------------

The name of this entry's author.


.. _reference.entry.author_detail.href:

:py:attr:`entries[i].author_detail.href`
----------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of this entry's author.  This can be
the author's home page, or a contact page with a webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.entry.author_detail.email:

:py:attr:`entries[i].author_detail.email`
-----------------------------------------

The email address of this entry's author.

.. rubric:: Comes from

* /atom10:feed/atom10:entry/atom10:author
* /atom03:feed/atom03:entry/atom03:author
* /rss/channel/item/dc:creator
* /rss/channel/item/dc:author
* /rss/channel/itunes:author
* /rdf:RDF/rdf:item/dc:creator
* /rdf:RDF/rdf:item/dc:author
