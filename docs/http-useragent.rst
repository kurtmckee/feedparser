User-Agent and Referer Headers
==============================

Customizing the User-Agent
--------------------------

feedparser does not send a User-Agent header
when it requests a feed from a web server.

If you are using feedparser in an application,
you should set the User-Agent to your application name and
:abbr:`URL (Uniform Resource Locator)`.

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse(
    ...     "$READTHEDOCS_CANONICAL_URL/examples/atom10.xml",
    ...     agent="MyApp/1.0 +http://domain.example/",
    ... )


Customizing the referrer
------------------------

feedparser lets you set the Referer header
when it requests a feed from a web server.

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse(
    ...     "$READTHEDOCS_CANONICAL_URL/examples/atom10.xml",
    ...     referrer="https://domain.example/",
    ... )
