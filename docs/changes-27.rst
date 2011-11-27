Changes in version 2.7.x
========================

The 2.7 series was a brief but necessary transition towards some of the core ideas in version 3.0.

:program:`Ultra-liberal Feed Parser` 2.7.6 was released on January 16, 2004.

- fixed bug with :file:`StringIO` importing


:program:`Ultra-liberal Feed Parser` 2.7.5 was released on January 15, 2004.

- added workaround for malformed DOCTYPE (seen on many ``blogspot.com`` sites)

- added ``_debug`` variable


:program:`Ultra-liberal Feed Parser` 2.7.4 was released on January 14, 2004.

- added workaround for improperly formed <br/> tags in encoded :abbr:`HTML (HyperText Markup Language)` (skadz)

- fixed unicode handling in normalize_attrs (ChrisL)

- fixed relative :abbr:`URI (Uniform Resource Identifier)` processing for guid (skadz)

- added ICBM support

- added :file:`base64` support


:program:`Ultra-liberal Feed Parser` 2.7.3 was released on January 14, 2004.

- reverted all changes made in 2.7.2


:program:`Ultra-liberal Feed Parser` 2.7.2 was released on January 13, 2004.

- "Version 2.7.2 of my feed parser, released today, will by default refuse to parse `this feed <http://intertwingly.net/stories/2004/01/12/broken.rss>`_.  It does a first-pass check for wellformedness, and when that fails it sets the 'bozo' bit in the result to ``1`` and immediately terminates.  You can revert to the previous behavior by passing ``disableWellFormedCheck=1``, but it will print arrogant warning messages to stderr to the effect that anyone who can't create a well-formed :abbr:`XML (Extensible Markup Language)` feed is a bozo and an incompetent fool." `source <http://intertwingly.net/blog/2004/01/12/Scientific-Method#c1074047818>`_


:program:`Ultra-liberal Feed Parser` 2.7.1 was released on January 9, 2004.

- fixed bug handling &quot; and &apos;

- fixed memory leak not closing url opener (JohnD)

- added dc:publisher support (MarekK)

- added admin:errorReportsTo support (MarekK)

- :program:`Python` 2.1 ``dict`` support (MarekK)


:program:`Ultra-liberal Feed Parser` 2.7 was released on January 5, 2004.

- really added support for trackback and pingback namespaces, as opposed to 2.6 when I said I did but didn't really

- sanitize :abbr:`HTML (HyperText Markup Language)` markup within some elements

- added :file:`mxTidy` support (if installed) to tidy :abbr:`HTML (HyperText Markup Language)` markup within some elements

- fixed indentation bug in ``_parse_date`` (FazalM)

- use ``socket.setdefaulttimeout`` if available (FazalM)

- universal date parsing and normalization (FazalM): ``created``, ``modified``, ``issued`` are parsed into 9-tuple date format and stored in ``created_parsed``, ``modified_parsed``, and ``issued_parsed``

- ``date`` is duplicated in ``modified`` and vice-versa

- ``date_parsed`` is duplicated in ``modified_parsed`` and vice-versa
