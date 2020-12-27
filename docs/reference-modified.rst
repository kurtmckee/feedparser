``modified``
===================

The last-modified date of the feed, as specified in the
:abbr:`HTTP (Hypertext Transfer Protocol)` headers.

The purpose of ``modified`` is explained more fully in :ref:`http.etag`.

.. tip::

    ``modified`` will only be present if the feed was retrieved from a web
    server, and only if the web server provided a Last-Modified
    :abbr:`HTTP (Hypertext Transfer Protocol)` header for the feed.  If the feed
    was parsed from a local file or from a string in memory, ``modified``
    will not be present.
