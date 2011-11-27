Changes in version 2.6
======================

:program:`Ultra-liberal Feed Parser` 2.6 was released on January 1, 2004.

- dc:author support (MarekK)

- fixed bug tracking nested divs within content (JohnD)

- fixed missing :file:`sys` import (JohanS)

- fixed regular expression to capture :abbr:`XML (Extensible Markup Language)` character encoding (Andrei)

- added support for Atom 0.3-style links

- fixed bug with textInput tracking

- added support for cloud (MartijnP)

- added support for multiple category/dc:subject (MartijnP)

- normalize content model: ``description`` gets description (which can come from ``<description>``, ``<summary>``, or full content if no ``<description>``), ``content`` gets dict of ``base``/``language``/``type``/``value`` (which can come from ``<content:encoded>``, ``<xhtml:body>``, ``<content>``, or ``<fullitem>``)

- fixed bug matching arbitrary Userland namespaces

- added xml:base and xml:lang tracking

- fixed bug tracking unknown tags

- fixed bug tracking content when ``<content>`` element is not in default namespace (like Pocketsoap feed)

- resolve relative URLs in ``<link>``, ``<guid>``, ``<docs>``, ``<url>``, ``<comments>``, ``<wfw:comment>``, ``<wfw:commentRSS>``

- resolve relative :abbr:`URI (Uniform Resource Identifier)`s within embedded :abbr:`HTML (HyperText Markup Language)` markup in ``<description>``, ``<xhtml:body>``, ``<content>``, ``<content:encoded>``, ``<title>``, ``<subtitle>``, ``<summary>``, ``<info>``, ``<tagline>``, and ``<copyright>``

- added support for pingback and trackback namespaces
