Fixed
-----

*   Stop raising an exception when a numeric character reference is outside the
    valid Unicode range (for example ``&#xFFFFFFFF;``, ``&#x110000;`` or a lone
    surrogate like ``&#xD800;``). Such references are now left unresolved
    instead of leaking ``OverflowError``, ``ValueError``, or
    ``UnicodeEncodeError`` out of ``feedparser.parse()``.
