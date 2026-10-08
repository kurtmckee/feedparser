Fixed
-----

*   Handle Podlove Simple Chapters without a ``start`` attribute without raising
    ``TypeError``, retaining chapter metadata with ``start_parsed`` set to ``None``.
    (#599)
