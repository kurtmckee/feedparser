:py:attr:`headers`
==================

A dictionary of all the :abbr:`HTTP (Hypertext Transfer Protocol)` headers
received from the web server when retrieving the feed.

.. tip::

    :py:attr:`headers` will only be present if the feed was retrieved from a web
    server.  If the feed was parsed from a local file or from a string in memory,
    :py:attr:`headers` will not be present.
