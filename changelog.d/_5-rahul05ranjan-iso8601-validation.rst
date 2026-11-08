Fixed
-----

*   Decline structurally invalid ISO-8601 dates (like ``0000-00-00``,
    month 13, day 39, or a ``-99:99`` offset) instead of normalizing
    them into a neighboring valid date. Previously the MySQL zero date
    parsed as 1899-11-30, month 13 rolled into the following January,
    and an out-of-range offset could produce a ``struct_time`` with a
    year of 10000, which cannot be converted to a ``datetime``. (#612)
*   Decline calendar-invalid days (``2026-11-31``, ``2023-02-29``) and
    invalid times (``25:61:61``) in the ISO-8601 handler instead of
    silently turning them into the next month or the next day, matching
    what the W3DTF handler already does. ISO 8601 end-of-day timestamps
    (``24:00:00``) and leap seconds (``23:59:60``) keep their existing
    valid handling. (#612)
