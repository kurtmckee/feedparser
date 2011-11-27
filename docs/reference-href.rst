:py:attr:`href`
===============

The final :abbr:`URL (Uniform Resource Locator)` of the feed that was parsed.

If the feed was redirected from the original requested address, :py:attr:`href`
will contain the final (redirected) address.

.. tip::

   :py:attr:`href` will only be present if the feed was retrieved from a web
   server.  If the feed was parsed from a local file or from a string in memory,
   :py:attr:`href` will not be present.
