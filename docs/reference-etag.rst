:py:attr:`etag`
===============

The ETag of the feed, as specified in the :abbr:`HTTP (Hypertext Transfer Protocol)` headers.

The purpose of :py:attr:`etag` is explained more fully in :ref:`http.etag`.

.. tip::

    :py:attr:`etag` will only be present if the feed was retrieved from a web server, and
    only if the web server provided an ETag :abbr:`HTTP (Hypertext Transfer Protocol)`
    header for the feed.  If the feed was parsed from a local file or from a string
    in memory, :py:attr:`etag` will not be present.
