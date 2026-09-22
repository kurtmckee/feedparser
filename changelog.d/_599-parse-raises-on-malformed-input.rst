Fixed
-----

*   Stop ``parse()`` from raising on a backslash in a DOCTYPE entity value,
    on character references outside the Unicode range, and on a GML
    ``srsName`` with a non-numeric EPSG code. Backslashes in entity values
    are also no longer treated as escapes. (#599)
