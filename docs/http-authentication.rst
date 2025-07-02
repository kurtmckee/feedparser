Password-Protected Feeds
========================

:program:`Universal Feed Parser` supports downloading and parsing
password-protected feeds that are protected by :abbr:`HTTP (Hypertext Transfer Protocol)`
basic authentication. For any other types of authentication, you can handle the
authentication yourself and then parse the retrieved feed.


Downloading a feed protected by basic authentication (the easy way)
-------------------------------------------------------------------

The easiest way is to embed the username and password in the feed
:abbr:`URL (Uniform Resource Locator)` itself.

In this example, the username is test and the password is basic.

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('http://test:basic@$READTHEDOCS_CANONICAL_URL/examples/basic_auth.xml')
    >>> d.feed.title
    'Sample Feed'


Downloading a feed with other types of authentication
-----------------------------------------------------

For any other type of authentication, you should retrieve the feed yourself and
handle authentication as needed (e.g. via `requests
<https://requests.readthedocs.io>` - this is what :program:`Universal Feed Parser`
uses internally), and then you can just call ``feedparser.parse`` on the
retrieved feed content.


Determining that a feed is password-protected
---------------------------------------------

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
information in the www-authenticate header is probably safe to ignore.

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/basic_auth.xml')
    >>> d.status
    401
    >>> d.headers['www-authenticate']
    'Basic realm="Use test/basic"'
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/digest_auth.xml')
    >>> d.status
    401
    >>> d.headers['www-authenticate']
    'Digest realm="DigestTest",
    nonce="+LV/uLLdAwA=5d77397291261b9ef256b034e19bcb94f5b7992a",
    algorithm=MD5,
    qop="auth"'
