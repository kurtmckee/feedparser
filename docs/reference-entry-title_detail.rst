.. _reference.entry.title_detail:

:py:attr:`entries[i].title_detail`
==================================

A dictionary with details about the entry title.


.. _reference.entry.title_detail.value:

:py:attr:`entries[i].title_detail.value`
----------------------------------------

Same as :ref:`reference.entry.title`.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`\s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].title_detail.type`
---------------------------------------

The content type of the entry title.

Most likely values for :py:attr:`~entries[i].title_detail.type`:

* :mimetype:`text/plain`
* :mimetype:`text/html`
* :mimetype:`application/xhtml+xml`

For Atom feeds, the content type is taken from the type attribute, which
defaults to :mimetype:`text/plain` if not specified.  For :abbr:`RSS (Rich Site
Summary)` feeds, the content type is auto-determined by inspecting the content,
and defaults to :mimetype:`text/html`.  Note that this may cause silent data
loss if the value contains plain text with angle brackets.  There is nothing I
can do about this problem; it is a limitation of :abbr:`RSS (Rich Site
Summary)`.

Future enhancement: some versions of :abbr:`RSS (Rich Site Summary)` clearly
specify that certain values default to :mimetype:`text/plain`, and
:program:`Universal Feed Parser` should respect this, but it doesn't yet.


:py:attr:`entries[i].title_detail.language`
-------------------------------------------

The language of the entry title.

:py:attr:`~entries[i].title_detail.language` is supposed to be a language code,
as specified by `RFC 3066`_, but publishers have been known to
publish random values like "English" or "German".  :program:`Universal Feed
Parser` does not do any parsing or normalization of language codes.

.. _RFC 3066: http://www.ietf.org/rfc/rfc3066.txt

:py:attr:`~entries[i].title_detail.language` may come from the element's
xml:lang attribute, or it may inherit from a parent element's xml:lang, or the
Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)` header.  If the
feed does not specify a language, :py:attr:`~entries[i].title_detail.language`
will be ``None``, the :program:`Python` null value.


:py:attr:`entries[i].title_detail.base`
---------------------------------------

The original base :abbr:`URI (Uniform Resource Identifier)` for links within
the entry title.

:py:attr:`~entries[i].title_detail.base` is only useful in rare situations and
can usually be ignored.  It is the original base :abbr:`URI (Uniform Resource
Identifier)` for this value, as specified by the element's xml:base attribute,
or a parent element's xml:base, or the appropriate :abbr:`HTTP (Hypertext
Transfer Protocol)` header, or the :abbr:`URI (Uniform Resource Identifier)` of
the feed.  (See :ref:`advanced.base` for more details.)  By the time you see
it, :program:`Universal Feed Parser` has already resolved relative links in all
values where it makes sense to do so.  *Clients should never need to manually
resolve relative links.*


.. rubric:: Comes from

* /atom10:feed/atom10:entry/atom10:title
* /atom03:feed/atom03:entry/atom03:title
* /rss/channel/item/title
* /rss/channel/item/dc:title
* /rdf:RDF/rdf:item/rdf:title
* /rdf:RDF/rdf:item/dc:title


.. seealso::

    * :ref:`reference.entry.title`
