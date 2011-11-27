The ETag of the feed, as specified in the :abbr:`HTTP (Hypertext Transfer Protocol)` headers.

etag
====

The purpose of ``etag`` is explained more fully in :ref:`http.etag`.

.. tip:: ``etag`` will only be present if the feed was retrieved from a web server, and only if the web server provided an ETag :abbr:`HTTP (Hypertext Transfer Protocol)` header for the feed.  If the feed was parsed from a local file or from a string in memory, ``etag`` will not be present.