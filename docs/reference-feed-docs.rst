.. _reference.feed.docs:

:py:attr:`feed.docs`
====================

A :abbr:`URL (Uniform Resource Locator)` pointing to the specification which
this feed conforms to.

This element is rare.  The reasoning was that in 25 years, someone will stumble
on an :abbr:`RSS (Rich Site Summary)` feed and not know what it is, so we
should waste everyone's bandwidth with useless links until then.  Most
publishers skip it, and all clients ignore it.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /rss/channel/docs
