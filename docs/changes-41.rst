Changes in version 4.1
======================

:program:`Universal Feed Parser` 4.1 was released on January 11, 2006.

- Support for the `Universal Encoding Detector <http://chardet.feedparser.org/>`_ to autodetect character encoding of feeds that declare their encoding incorrectly or don't declare it at all.  See :ref:`advanced.encoding` for details of when this gets called.

- :program:`Universal Feed Parser` no longer sets a default socket timeout (SourceForge bug `1392140 <http://sourceforge.net/tracker/index.php?func=detail&aid=1392140&group_id=112328&atid=661937>`_).  If you were relying on this feature, you will need to call socket.setdefaulttimeout(TIMEOUT_IN_SECONDS) yourself.
