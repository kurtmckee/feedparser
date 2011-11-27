Changes in version 3.1
======================




:program:`Universal Feed Parser` 3.1 was released on June 28, 2004.

- added and passed tests for converting :abbr:`HTML (HyperText Markup Language)` entities to Unicode equivalents in illformed feeds (aaronsw)

- added and passed tests for converting character entities to Unicode equivalents in illformed feeds (aaronsw)

- test for valid parsers when setting ``XML_AVAILABLE``

- make version and encoding available when server returns a ``304``

- add ``handlers`` parameter to pass arbitrary :file:`urllib2` handlers (like digest auth or proxy support)

- add code to parse username/password out of url and send as basic authentication

- expose downloading-related exceptions in ``bozo_exception`` (aaronsw)

- added __contains__ method to FeedParserDict (aaronsw)

- added ``publisher_detail`` (aaronsw)