.. _reference.entry.expired_parsed:

:py:attr:`entries[i].expired_parsed`
====================================

The date this entry is set to expire, as a standard :program:`Python` 9-tuple.

This element is rare.  It only existed in :abbr:`RSS (Rich Site Summary)` 0.93,
and it was never widely implemented by publishers.  Most clients ignore it in
favor of user-defined expiration algorithms.


.. rubric:: Comes from

* /rss/channel/item/expirationDate


.. seealso::

    * :ref:`reference.entry.expired`
