Fixed
-----

*   When a feed contains both ``itunes:author`` and ``itunes:owner``,
    the owner name no longer overwrites the author. ``itunes:owner``
    is now exposed only through ``publisher_detail``, as documented.
