.. _reference.entry.content:



entries[i].content
==================




A list of dictionaries with details about the full content of the entry.

Atom feeds may contain multiple content elements.  Clients should render as many of them as possible, based on the type and the client's abilities.

- Comes from

- /atom10:feed/atom10:entry/atom10:content

- /atom03:feed/atom03:entry/atom03:content

- /rss/channel/item/content:encoded

- /rss/channel/item/body

- /rss/channel/item/xhtml:body

- /rss/channel/item/fullitem

- /rdf:RDF/rdf:item/content:encoded





.. _reference.entry.content.value:



entries[i].content[j].value
---------------------------

The value of this piece of content.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML (Extensible HyperText Markup Language)`, it is :ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements within this value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so, they are :ref:`resolved according to a set of rules <advanced.base>`.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML (Extensible HyperText Markup Language)`, it will be :ref:`parsed for microformats <advanced.microformats>`.



.. _reference.entry.content.type:



entries[i].content[j].type
--------------------------

The content type of this piece of content.

Most likely values for ``type``:

- ``text/plain``

- ``text/html``

- ``application/xhtml+xml``



For Atom feeds, the content type is taken from the type attribute, which defaults to ``text/plain`` if not specified.  For :abbr:`RSS (Rich Site Summary)` feeds, the content type is auto-determined by inspecting the content, and defaults to ``text/html``.  Note that this may cause silent data loss if the value contains plain text with angle brackets.  There is nothing I can do about this problem; it is a limitation of :abbr:`RSS (Rich Site Summary)`.

Future enhancement: some versions of :abbr:`RSS (Rich Site Summary)` clearly specify that certain values default to ``text/plain``, and :program:`Universal Feed Parser` should respect this, but it doesn't yet.



.. _reference.entry.content.language:



entries[i].content[j].language
------------------------------

The language of this piece of content.

``language`` is supposed to be a language code, as specified by `:abbr:`RFC (Request For Comments)` 3066 <http://www.ietf.org/rfc/rfc3066.txt>`_, but publishers have been known to publish random values like "English" or "German".  :program:`Universal Feed Parser` does not do any parsing or normalization of language codes.

``language`` may come from the element's xml:lang attribute, or it may inherit from a parent element's xml:lang, or the Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)` header.  If the feed does not specify a language, ``language`` will be ``None``, the :program:`Python` null value.



.. _reference.entry.content.base:



entries[i].content[j].base
--------------------------

The original base :abbr:`URI (Uniform Resource Identifier)` for links within this piece of content.

``base`` is only useful in rare situations and can usually be ignored.  It is the original base :abbr:`URI (Uniform Resource Identifier)` for this value, as specified by the element's xml:base attribute, or a parent element's xml:base, or the appropriate :abbr:`HTTP (Hypertext Transfer Protocol)` header, or the :abbr:`URI (Uniform Resource Identifier)` of the feed.  (See :ref:`advanced.base` for more details.)  By the time you see it, :program:`Universal Feed Parser` has already resolved relative links in all values where it makes sense to do so.  *Clients should never need to manually resolve relative links.*