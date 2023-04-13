Fixed
-----

*   Fix a bug that prevented JSON feeds from being parsed.

    A comparison was failing due to incompatible types,
    which allowed XML declarations to be added to JSON feeds.

*   Fallback to JSON feed parsing if the XML parsers completely fail.
