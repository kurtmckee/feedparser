:py:attr:`bozo`
===============

An integer, either ``1`` or ``0``.  Set to ``1`` if the feed is not well-formed
:abbr:`XML (Extensible Markup Language)`, and ``0`` otherwise.

See :ref:`advanced.bozo` for more details on the :py:attr:`bozo` bit.

.. tip::

    :py:attr:`bozo` may not be present.  Some platforms, such as Mac OS X 10.2 and some
    versions of FreeBSD, do not include an :abbr:`XML (Extensible Markup Language)`
    parser in their :program:`Python` distributions.  :program:`Universal Feed Parser`
    will still work on these platforms, but it will not be able to detect whether a
    feed is well-formed.  However, it *can* detect whether a feed's character
    encoding is incorrectly declared.  (This is done in :program:`Python`, not by
    the :abbr:`XML (Extensible Markup Language)` parser.) See
    :ref:`advanced.encoding` for details.
