User-Agent and Referer Headers
==============================

:program:`Universal Feed Parser` sends a default User-Agent string when it
requests a feed from a web server.


The default User-Agent string looks like this:

..  code-block:: text

    feedparser/6.0.11 +https://github.com/kurtmckee/feedparser/

If you are embedding :program:`Universal Feed Parser` in a larger application,
you should change the User-Agent to your application name and
:abbr:`URL (Uniform Resource Locator)`.


Customizing the User-Agent
--------------------------

..  code-block:: pycon

    >>> import feedparser
    >>> feedparser.USER_AGENT = "MyApp/1.0 +http://example.com/"
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom10.xml')


:program:`Universal Feed Parser` also lets you set the referrer when you
download a feed from a web server.  This is discouraged, because it is a
violation of `RFC 2616 <http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.36>`_.
The default behavior is to send a blank referrer, and you should never need to
override this.
