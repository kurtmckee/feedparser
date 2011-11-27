.. _reference.feed.info_detail:

:py:attr:`feed.info_detail`
===========================

A dictionary with details about the feed info.


.. rubric:: Comes from

* /atom03:feed/atom03:info


.. seealso::

    * :ref:`reference.feed.info`


.. _reference.feed.info_detail.value:

:py:attr:`feed.info_detail.value`
---------------------------------

Same as :ref:`reference.feed.info`.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, it is :ref:`sanitized
<advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or :abbr:`XHTML
(Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.feed.info_detail.type:

:py:attr:`feed.info_detail.type`
--------------------------------

The content type of the feed info.

Most likely values for :py:attr:`~feed.info_detail.type`:

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


:py:attr:`feed.info_detail.language`
------------------------------------

The language of the feed info.

:py:attr:`~feed.info_detail.language` is supposed to be a language code, as
specified by `:abbr:`RFC (Request For Comments)` 3066
<http://www.ietf.org/rfc/rfc3066.txt>`_, but publishers have been known to
publish random values like "English" or "German".  :program:`Universal Feed
Parser` does not do any parsing or normalization of language codes.

:py:attr:`~feed.info_detail.language` may come from the element's xml:lang
attribute, or it may inherit from a parent element's xml:lang, or the
Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)` header.  If the
feed does not specify a language, :py:attr:`~feed.info_detail.language` will be
``None``, the :program:`Python` null value.


:py:attr:`feed.info_detail.base`
--------------------------------

The original base :abbr:`URI (Uniform Resource Identifier)` for links within
the feed copyright.

:py:attr:`~feed.info_detail.base` is only useful in rare situations and can
usually be ignored.  It is the original base :abbr:`URI (Uniform Resource
Identifier)` for this value, as specified by the element's xml:base attribute,
or a parent element's xml:base, or the appropriate :abbr:`HTTP (Hypertext
Transfer Protocol)` header, or the :abbr:`URI (Uniform Resource Identifier)` of
the feed.  (See :ref:`advanced.base` for more details.)  By the time you see
it, :program:`Universal Feed Parser` has already resolved relative links in all
values where it makes sense to do so.  *Clients should never need to manually
resolve relative links.*
