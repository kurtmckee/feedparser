``href``
===============

The final :abbr:`URL (Uniform Resource Locator)` of the feed that was parsed.

If the feed was redirected from the original requested address, ``href``
will contain the final (redirected) address.

..  tip::

    ``href`` will only be present if the feed was retrieved from a web
    server.  If the feed was parsed from a local file or from a string in memory,
    ``href`` will not be present.
