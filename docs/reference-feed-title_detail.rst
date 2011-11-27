.. _reference.feed.title_detail:



feed.title_detail
=================




A dictionary with details about the feed title.

- Comes from

- /atom10:feed/atom10:title

- /atom03:feed/atom03:title

- /rss/channel/title

- /rss/channel/dc:title

- /rdf:RDF/rdf:channel/rdf:title

- /rdf:RDF/rdf:channel/dc:title



- See also

- :ref:`reference.feed.title`





.. _reference.feed.title_detail.value:



feed.title_detail.value
-----------------------

Same as :ref:`reference.feed.title`.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML (Extensible HyperText Markup Language)`, it is :ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements within this value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so, they are :ref:`resolved according to a set of rules <advanced.base>`.



.. _reference.feed.title_detail.type:



feed.title_detail.type
----------------------

The content type of the feed title.

Most likely values for ``type``:

- ``text/plain``

- ``text/html``

- ``application/xhtml+xml``



For Atom feeds, the content type is taken from the type attribute, which defaults to ``text/plain`` if not specified.  For :abbr:`RSS (Rich Site Summary)` feeds, the content type is auto-determined by inspecting the content, and defaults to ``text/html``.  Note that this may cause silent data loss if the value contains plain text with angle brackets.  There is nothing I can do about this problem; it is a limitation of :abbr:`RSS (Rich Site Summary)`.

Future enhancement: some versions of :abbr:`RSS (Rich Site Summary)` clearly specify that certain values default to ``text/plain``, and :program:`Universal Feed Parser` should respect this, but it doesn't yet.



.. _reference.feed.title_detail.language:



feed.title_detail.language
--------------------------

The language of the feed title.

``language`` is supposed to be a language code, as specified by `:abbr:`RFC (Request For Comments)` 3066 <http://www.ietf.org/rfc/rfc3066.txt>`_, but publishers have been known to publish random values like "English" or "German".  :program:`Universal Feed Parser` does not do any parsing or normalization of language codes.

``language`` may come from the element's xml:lang attribute, or it may inherit from a parent element's xml:lang, or the Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)` header.  If the feed does not specify a language, ``language`` will be ``None``, the :program:`Python` null value.



feed.title_detail.base
----------------------

The original base :abbr:`URI (Uniform Resource Identifier)` for links within the feed title.

``base`` is only useful in rare situations and can usually be ignored.  It is the original base :abbr:`URI (Uniform Resource Identifier)` for this value, as specified by the element's xml:base attribute, or a parent element's xml:base, or the appropriate :abbr:`HTTP (Hypertext Transfer Protocol)` header, or the :abbr:`URI (Uniform Resource Identifier)` of the feed.  (See :ref:`advanced.base` for more details.)  By the time you see it, :program:`Universal Feed Parser` has already resolved relative links in all values where it makes sense to do so.  *Clients should never need to manually resolve relative links.*