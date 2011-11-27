Password-Protected Feeds
========================

:program:`Universal Feed Parser` supports downloading and parsing
password-protected feeds that are protected by :abbr:`HTTP (Hypertext Transfer Protocol)`
authentication.  Both basic and digest authentication are supported.


Downloading a feed protected by basic authentication (the easy way)
-------------------------------------------------------------------

The easiest way is to embed the username and password in the feed
:abbr:`URL (Uniform Resource Locator)` itself.

In this example, the username is test and the password is basic.

::

    >>> import feedparser
    >>> d = feedparser.parse('http://test:basic@feedparser.org/docs/examples/basic_auth.xml')
    >>> d.feed.title
    u'Sample Feed'

The same technique works for digest authentication.  (Technically,
:program:`Universal Feed Parser` will attempt basic authentication first, but
if that fails and the server indicates that it requires digest authentication,
:program:`Universal Feed Parser` will automatically re-request the feed with
the appropriate digest authentication headers.  *This means that this technique
will send your password to the server in an easily decryptable form.*)


.. _example.auth.inline.digest:

Downloading a feed protected by digest authentication (the easy but horribly insecure way)
------------------------------------------------------------------------------------------

In this example, the username is test and the password is digest.

::

    >>> import feedparser
    >>> d = feedparser.parse('http://test:digest@feedparser.org/docs/examples/digest_auth.xml')
    >>> d.feed.title
    u'Sample Feed'



You can also construct a HTTPBasicAuthHandler that contains the password
information, then pass that as a handler to the ``parse`` function.
HTTPBasicAuthHandler is part of the standard `urllib2 <http://docs.python.org/lib/module-urllib2.html>`_ module.

Downloading a feed protected by :abbr:`HTTP (Hypertext Transfer Protocol)` basic authentication (the hard way)
--------------------------------------------------------------------------------------------------------------

::

    import urllib2, feedparser

    # Construct the authentication handler
    auth = urllib2.HTTPBasicAuthHandler()

    # Add password information: realm, host, user, password.
    # A single handler can contain passwords for multiple sites;
    # urllib2 will sort out which passwords get sent to which sites
    # based on the realm and host of the URL you're retrieving
    auth.add_password('BasicTest', 'feedparser.org', 'test', 'basic')

    # Pass the authentication handler to the feed parser.
    # handlers is a list because there might be more than one
    # type of handler (urllib2 defines lots of different ones,
    # and you can build your own)
    d = feedparser.parse('http://feedparser.org/docs/examples/basic_auth.xml',
                         handlers=[auth])



Digest authentication is handled in much the same way, by constructing an
HTTPDigestAuthHandler and populating it with the necessary realm, host, user,
and password information.  This is more secure than 
:ref:`stuffing the username and password in the URL <example.auth.inline.digest>`,
since the password will be encrypted before being sent to the server.


Downloading a feed protected by :abbr:`HTTP (Hypertext Transfer Protocol)` digest authentication (the secure way)
-----------------------------------------------------------------------------------------------------------------

::

    import urllib2, feedparser

    auth = urllib2.HTTPDigestAuthHandler()
    auth.add_password('DigestTest', 'feedparser.org', 'test', 'digest')
    d = feedparser.parse('http://feedparser.org/docs/examples/digest_auth.xml',
                          handlers=[auth])


The examples so far have assumed that you know in advance that the feed is
password-protected.  But what if you don't know?

If you try to download a password-protected feed without sending all the proper
password information, the server will return an 
:abbr:`HTTP (Hypertext Transfer Protocol)` status code ``401``.
:program:`Universal Feed Parser` makes this status code available in
``d.status``.

Details on the authentication scheme are in ``d.headers['www-authenticate']``.
:program:`Universal Feed Parser` does not do any further parsing on this field;
you will need to parse it yourself.  Everything before the first space is the
type of authentication (probably ``Basic`` or ``Digest``), which controls which
type of handler you'll need to construct.  The realm name is given as
realm="foo" -- so foo would be your first argument to auth.add_password.  Other
information in the www-authenticate header is probably safe to ignore; the
:file:`urllib2` module will handle it for you.


Determining that a feed is password-protected
---------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/basic_auth.xml')
    >>> d.status
    401
    >>> d.headers['www-authenticate']
    'Basic realm="Use test/basic"'
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/digest_auth.xml')
    >>> d.status
    401
    >>> d.headers['www-authenticate']
    'Digest realm="DigestTest",
    nonce="+LV/uLLdAwA=5d77397291261b9ef256b034e19bcb94f5b7992a",
    algorithm=MD5,
    qop="auth"'

