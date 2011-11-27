Changes in version 3.2
======================




:program:`Universal Feed Parser` 3.2 was released on July 3, 2004.

- use :file:`cjkcodecs` and :file:`iconv_codec` if available

- always convert feed to UTF-8 before passing to :abbr:`XML (Extensible Markup Language)` parser

- completely revamped logic for determining character encoding and attempting :abbr:`XML (Extensible Markup Language)` parsing (much faster)

- increased default timeout to 20 seconds

- test for presence of ``Location`` header on redirects

- added tests for many alternate character encodings

- support various :abbr:`EBCDIC` encodings

- support UTF-16BE and UTF16-LE with or without a :abbr:`BOM (Byte Order Mark)`

- support UTF-8 with a :abbr:`BOM (Byte Order Mark)`

- support UTF-32BE and UTF-32LE with or without a :abbr:`BOM (Byte Order Mark)`

- fixed crashing bug if no :abbr:`XML (Extensible Markup Language)` parsers are available

- added support for ``Content-encoding: deflate``

- send blank ``Accept-encoding`` header if neither :file:`gzip` nor :file:`zlib` modules are available
