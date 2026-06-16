Fixed
-----

*   Accessing ``enclosures`` or ``license`` on a feed or entry that has no
    link no longer raises an error; ``enclosures`` is now an empty list, as
    documented. (#340)
