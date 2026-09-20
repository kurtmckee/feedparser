Fixed
-----

*   Leave out-of-range and surrogate numeric character references unresolved
    instead of raising from the loose parser (``OverflowError``, ``ValueError``,
    or ``UnicodeEncodeError``). (#591)
