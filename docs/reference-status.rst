:py:attr:`status`
=================

The :abbr:`HTTP (Hypertext Transfer Protocol)` status code that was returned by
the web server when the feed was fetched.

If the feed was redirected from its original :abbr:`URL (Uniform Resource Locator)`,
:py:attr:`status` will contain the redirect status code, not the final status
code.

If :py:attr:`status` is ``301``, the feed was permanently redirected to a new
:abbr:`URL (Uniform Resource Locator)`.  Clients should update their address
book to request the new :abbr:`URL (Uniform Resource Locator)` from now on.

If :py:attr:`status` is ``410``, the feed is gone.  Clients should stop polling the
feed.

.. tip::

    :py:attr:`status` will only be present if the feed was retrieved from a web
    server.  If the feed was parsed from a local file or from a string in memory,
    :py:attr:`status` will not be present.
