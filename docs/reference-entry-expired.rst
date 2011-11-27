.. _reference.entry.expired:

:py:attr:`entries[i].expired`
=============================

The date this entry is set to expire, as a string in the same format as it was
published in the original feed).

This element is :ref:`parsed as a date <advanced.date>` and stored in
:ref:`reference.entry.expired_parsed`.

This element is rare.  It only existed in :abbr:`RSS (Rich Site Summary)` 0.93,
and it was never widely implemented by publishers.  Most clients ignore it in
favor of user-defined expiration algorithms.


.. rubric:: Comes from

* /rss/channel/item/expirationDate


.. seealso::

    * :ref:`reference.entry.expired_parsed`
