Fixed
-----

*   Substitute the XML declaration in documents that begin with whitespace,
    instead of prepending a second declaration.

    A duplicate declaration caused the strict XML parser to fail with
    "XML or text declaration not at start of entity",
    which flagged the document as ``bozo`` and fell back to the loose parser.

    Reported in `#508 <https://github.com/kurtmckee/feedparser/issues/508>`_
    and `#511 <https://github.com/kurtmckee/feedparser/issues/511>`_.
