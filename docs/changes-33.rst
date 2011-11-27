Changes in version 3.3
======================




:program:`Universal Feed Parser` 3.3 was released on July 15, 2004.

- optimized :abbr:`EBCDIC` to :abbr:`ASCII` conversion

- fixed obscure problem tracking xml:base and xml:lang if element declares it, child doesn't, first grandchild redeclares it, and second grandchild doesn't

- refactored date parsing

- defined public ``registerDateHandler`` so callers can add support for additional date formats at runtime

- added support for OnBlog, Nate, MSSQL, Greek, and Hungarian dates (ytrewq1)

- added ``zopeCompatibilityHack()`` which turns FeedParserDict into a regular dictionary, required for :program:`Zope` compatibility, and also makes command-line debugging easier because pprint module formats real dictionaries better than dictionary-like objects

- added NonXMLContentType exception, which is stored in ``bozo_exception`` when a feed is served with a non-:abbr:`XML (Extensible Markup Language)` media type such as ``'text/plain'``

- respect ``Content-Language`` as default language if no xml:lang is present

- ``cloud`` dict is now FeedParserDict

- generator dict is now FeedParserDict

- better tracking of xml:lang, including support for xml:lang='' to unset the current language

- recognize :abbr:`RSS (Rich Site Summary)` 1.0 feeds even when :abbr:`RSS (Rich Site Summary)` 1.0 namespace is not the default namespace

- don't overwrite final status on redirects (scenarios: redirecting to a :abbr:`URI (Uniform Resource Identifier)` that returns ``304``, redirecting to a :abbr:`URI (Uniform Resource Identifier)` that redirects to another :abbr:`URI (Uniform Resource Identifier)` with a different type of redirect)

- add support for ``HTTP 303`` redirects