``headers``
==================

A dictionary of all the :abbr:`HTTP (Hypertext Transfer Protocol)` headers
received from the web server when retrieving the feed.

.. tip::

    ``headers`` will only be present if the feed was retrieved from a web
    server.  If the feed was parsed from a local file or from a string in memory,
    ``headers`` will not be present.
