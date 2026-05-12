Fixed
-----

*   Map ``<itunes:explicit>`` values ``true`` and ``yes`` to ``True``
    and ``false``, ``no``, and ``clean`` to ``False``. Previously only
    ``yes`` and ``clean`` were recognized, so the boolean values defined
    by the current Apple Podcasts spec were parsed as ``None``. (#524)
