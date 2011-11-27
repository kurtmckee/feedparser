Changes in version 3.0
======================


:program:`Universal Feed Parser` 3.0 was released on June 21, 2004.

- don't try ``iso-8859-1`` (can't distinguish between ``iso-8859-1`` and ``windows-1252`` anyway, and most incorrectly marked feeds are ``windows-1252``)

- fixed regression that could cause the same encoding to be tried twice (even if it failed the first time)


:program:`Universal Feed Parser` 3.0fc3 was released on June 18, 2004.

- fixed bug in ``_changeEncodingDeclaration`` that failed to parse UTF-16 encoded feeds

- made ``source`` into a FeedParserDict

- duplicate admin:generatorAgent/@rdf:resource in ``generator_detail.url``

- added support for image

- refactored ``parse()`` fallback logic to try other encodings if SAX parsing fails (previously it would only try other encodings if re-encoding failed)

- remove ``unichr`` madness in normalize_attrs now that we're properly tracking encoding in and out of BaseHTMLProcessor

- set ``feed.language`` from root-level xml:lang

- set ``entry.id`` from rdf:about

- send ``Accept`` header


:program:`Universal Feed Parser` 3.0fc2 was released on May 10, 2004.

- added and passed Sam's amp tests

- added and passed my blink tag tests


:program:`Universal Feed Parser` 3.0fc1 was released on April 23, 2004.

- made ``results.entries[0].links[0]`` and ``results.entries[0].enclosures[0]`` into FeedParserDict

- fixed typo that could cause the same encoding to be tried twice (even if it failed the first time)

- fixed DOCTYPE stripping when DOCTYPE contained entity declarations

- better textinput and image tracking in illformed :abbr:`RSS (Rich Site Summary)` 1.0 feeds


:program:`Universal Feed Parser` 3.0b23 was released on April 21, 2004.

- fixed ``UnicodeDecodeError`` for feeds that contain high-bit characters in attributes in embedded :abbr:`HTML (HyperText Markup Language)` in description (thanks Thijs van de Vossen)

- moved ``guid``, ``date``, and ``date_parsed`` to mapped keys in FeedParserDict

- tweaked FeedParserDict.has_key to return ``True`` if asking about a mapped key


:program:`Universal Feed Parser` 3.0b22 was released on April 19, 2004.

- changed ``channel`` to ``feed``, ``item`` to ``entries`` in ``results`` dict

- changed ``results`` dict to allow getting values with ``results.key`` as well as ``results[key]``

- work around embedded illformed :abbr:`HTML (HyperText Markup Language)` with half a DOCTYPE

- work around malformed ``Content-Type`` header

- if character encoding is wrong, try several common ones before falling back to regexes (if this works, ``bozo_exception`` is set to ``CharacterEncodingOverride``

- fixed character encoding issues in BaseHTMLProcessor by tracking encoding and converting from Unicode to raw strings before feeding data to sgmllib.SGMLParser

- convert each value in results to Unicode (if possible), even if using regex-based parsing


:program:`Universal Feed Parser` 3.0b21 was released on April 14, 2004.

- added Hot RSS support


:program:`Universal Feed Parser` 3.0b20 was released on April 7, 2004.

- added :abbr:`CDF (Channel Definition Format)` support


:program:`Universal Feed Parser` 3.0b19 was released on March 15, 2004.

- fixed bug exploding author information when author name was in parentheses

- removed ultra-problematic :file:`mxTidy` support

- patch to workaround crash in PyXML/expat when encountering invalid entities (MarkMoraes)

- support for textinput/textInput


:program:`Universal Feed Parser` 3.0b18 was released on February 17, 2004.

- always map description to ``summary_detail`` (Andrei)

- use :file:`libxml2` (if available)


:program:`Universal Feed Parser` 3.0b17 was released on February 13, 2004.

- determine character encoding as per `RFC 3023 <http://www.ietf.org/rfc/rfc3023.txt>`_


:program:`Universal Feed Parser` 3.0b16 was released on February 12, 2004.

- fixed support for :abbr:`RSS (Rich Site Summary)` 0.90 (broken in b15)


:program:`Universal Feed Parser` 3.0b15 was released on February 11, 2004.

- fixed bug resolving relative links in wfw:commentRSS

- fixed bug capturing author and contributor :abbr:`URI (Uniform Resource Identifier)`

- fixed bug resolving relative links in author and contributor :abbr:`URI (Uniform Resource Identifier)`

- fixed bug resolving relative links in generator :abbr:`URI (Uniform Resource Identifier)`

- added support for recognizing :abbr:`RSS (Rich Site Summary)` 1.0

- passed Simon Fell's namespace tests, and included them permanently in the test suite with his permission

- fixed namespace handling under :program:`Python` 2.1


:program:`Universal Feed Parser` 3.0b14 was released on February 8, 2004.

- fixed CDATA handling in non-wellformed feeds under :program:`Python` 2.1


:program:`Universal Feed Parser` 3.0b13 was released on February 8, 2004.

- better handling of empty :abbr:`HTML (HyperText Markup Language)` tags (br, hr, img, etc.) in embedded markup, in either :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML (Extensible HyperText Markup Language)` form (<br>, <br/>, <br />)


:program:`Universal Feed Parser` 3.0b12 was released on February 6, 2004.

- fiddled with ``decodeEntities`` (still not right)

- added support to Atom 0.2 subtitle

- added support for Atom content model in copyright

- better sanitizing of dangerous :abbr:`HTML (HyperText Markup Language)` elements with end tags (script, frameset)


:program:`Universal Feed Parser` 3.0b11 was released on February 2, 2004.

- added rights to list of elements that can contain dangerous markup

- fiddled with ``decodeEntities`` (not right)

- liberalized date parsing even further


:program:`Universal Feed Parser` 3.0b10 was released on January 31, 2004.

- incorporated ISO-8601 date parsing routines from :file:`xml.util.iso8601`


:program:`Universal Feed Parser` 3.0b9 was released on January 29, 2004.

- fixed check for presence of ``dict`` function

- added support for summary


:program:`Universal Feed Parser` 3.0b8 was released on January 28, 2004.

- added support for contributor


:program:`Universal Feed Parser` 3.0b7 was released on January 28, 2004.

- support Atom-style author element in ``author_detail`` (dictionary of ``name``, ``url``, ``email``)

- map ``author`` to ``author_detail`` if ``author`` contains name + email address


:program:`Universal Feed Parser` 3.0b6 was released on January 27, 2004.

- added feed type and version detection, ``result['version']`` will be one of ``SUPPORTED_VERSIONS.keys()`` or empty string if unrecognized

- added support for creativeCommons:license and cc:license

- added support for full Atom content model in title, tagline, info, copyright, summary

- fixed bug with gzip encoding (not always telling server we support it when we do)


:program:`Universal Feed Parser` 3.0b5 was released on January 26, 2004.

- fixed bug parsing multiple links at feed level


:program:`Universal Feed Parser` 3.0b4 was released on January 26, 2004.

- fixed xml:lang inheritance

- fixed multiple bugs tracking xml:base :abbr:`URI (Uniform Resource Identifier)`, one for documents that don't define one explicitly and one for documents that define an outer and an inner xml:base that goes out of scope before the end of the document


:program:`Universal Feed Parser` 3.0b3 was released on January 23, 2004.

- parse entire feed with real :abbr:`XML (Extensible Markup Language)` parser (if available)

- added several new supported namespaces

- fixed bug tracking naked markup in description

- added support for enclosure

- added support for source

- re-added support for cloud which got dropped somehow

- added support for expirationDate


:program:`Universal Feed Parser` 3.0b2 and 3.0b1 have been lost in the mists of time.
