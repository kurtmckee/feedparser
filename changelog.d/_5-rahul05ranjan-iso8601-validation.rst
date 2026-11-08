Fixed
-----

*   Decline structurally invalid ISO-8601 dates (like ``0000-00-00``,
    month 13, day 39, or a ``-99:99`` offset) instead of normalizing
    them into a neighboring valid date. Previously the MySQL zero date
    parsed as 1899-11-30, month 13 rolled into the following January,
    and an out-of-range offset could produce a ``struct_time`` with a
    year of 10000, which cannot be converted to a ``datetime``. (#612)
