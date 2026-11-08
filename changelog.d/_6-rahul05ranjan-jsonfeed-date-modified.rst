Fixed
-----

*   Populate ``updated`` from a JSON Feed item's ``date_modified``, as
    the spec defines it. The parser only looked for a nonstandard
    ``date_updated`` key (while reading ``date_modified`` from the item),
    so a spec-compliant feed's modification date was silently dropped
    and ``updated`` fell back to the ``published`` date.
