.. _advanced.bozo:

Bozo Detection
==============

:program:`Universal Feed Parser` can parse feeds whether they are well-formed
:abbr:`XML (Extensible Markup Language)` or not.  However, since some
applications may wish to reject or warn users about non-well-formed feeds,
:program:`Universal Feed Parser` sets the ``bozo`` bit when it detects that a
feed is not well-formed.  Thanks to `Tim Bray
<http://www.tbray.org/ongoing/When/200x/2004/01/11/PostelPilgrim>`_ for
suggesting this terminology.

Detecting a non-well-formed feed
--------------------------------

::

    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.bozo
    0
    >>> d = feedparser.parse('http://feedparser.org/tests/illformed/rss/aaa_illformed.xml')
    >>> d.bozo
    1
    >>> d.bozo_exception
    <xml.sax._exceptions.SAXParseException instance at 0x00BAAA08>
    >>> exc = d.bozo_exception
    >>> exc.getMessage()
    "expected '>'\\n"
    >>> exc.getLineNumber()
    6


There are many reasons an :abbr:`XML (Extensible Markup Language)` document
could be non-well-formed besides this example (incomplete end tags)  See
:ref:`advanced.encoding` for some other ways to trip the bozo bit.
