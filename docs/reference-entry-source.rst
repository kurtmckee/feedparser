.. _reference.entry.source:

:py:attr:`entries[i].source`
============================

A dictionary with details about the source of the entry.


.. rubric:: Comes from

* /atom10:feed/atom10:entry/atom10:source


:py:attr:`entries[i].source.author`
-----------------------------------

The author of the source of this entry.


:py:attr:`entries[i].source.author_detail`
------------------------------------------

A dictionary containing details about the author of the source of this entry.


:py:attr:`entries[i].source.author_detail.name`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The name of the author of the source of this entry.


.. _reference.entry.source.author_detail.href:

:py:attr:`entries[i].source.author_detail.href`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :abbr:`URL (Uniform Resource Locator)` of the author of the source of this
entry.  This can be the author's home page, or a contact page with a webmail
form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].source.author_detail.email`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The email address of the author of the source of this entry.



:py:attr:`entries[i].source.contributors`
-----------------------------------------

A list of contributors to the source of this entry.


:py:attr:`entries[i].source.contributors[j].name`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The name of a contributor to the source of this entry.


.. _reference.entry.source.contributors.href:

:py:attr:`entries[i].source.contributors[j].href`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :abbr:`URL (Uniform Resource Locator)` of a contributor to the source of
this entry.  This can be the contributor's home page, or a contact page with a
webmail form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].source.contributors[j].email`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The email address of a contributor to the source of this entry.



:py:attr:`entries[i].source.icon`
---------------------------------

The :abbr:`URL (Uniform Resource Locator)` of an icon representing the source
of this entry.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.



:py:attr:`entries[i].source.id`
-------------------------------

A globally unique identifier for the source of this entry.



:py:attr:`entries[i].source.link`
---------------------------------

The primary permanent link of the source of this entry



:py:attr:`entries[i].source.links`
----------------------------------

A list of all links defined by the source of this entry.


:py:attr:`entries[i].source.links[j].rel`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The relationship of a link defined by the source of this entry.

Atom 1.0 defines five standard link relationships and describes the process for
registering others.  Here are the five standard rel values:

* ``alternate``
* ``self``
* ``related``
* ``via``
* ``enclosure``


:py:attr:`entries[i].source.links[j].type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The content type of the page pointed to by a link defined by the source of this
entry.


.. _reference.entry.source.links.href:

:py:attr:`entries[i].source.links[j].href`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :abbr:`URL (Uniform Resource Locator)` of the page pointed to by a link
defined by the source of this entry.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].source.links[j].title`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The title of a link defined by the source of this entry.



:py:attr:`entries[i].source.logo`
---------------------------------

The :abbr:`URL (Uniform Resource Locator)` of a logo representing the source of
this entry.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.



.. _reference.entry.source.rights:

:py:attr:`entries[i].source.rights`
-----------------------------------

A human-readable copyright statement for the source of this entry.



:py:attr:`entries[i].source.rights_detail`
------------------------------------------

A dictionary containing details about the copyright statement for the source of
this entry.


:py:attr:`entries[i].source.rights_detail.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same as :ref:`reference.entry.source.rights`.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, it is
:ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements
within this value may contain relative
:abbr:`URI (Uniform Resource Identifier)`\s.  If so, they are
:ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].source.rights_detail.type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The content type of the copyright statement for the source of this entry.

Most likely values for :py:attr:`~entries[i].source.rights_detail.type`:

* :mimetype:`text/plain`
* :mimetype:`text/html`
* :mimetype:`application/xhtml+xml`

For Atom feeds, the content type is taken from the type attribute, which
defaults to :mimetype:`text/plain` if not specified.  For
:abbr:`RSS (Rich Site Summary)` feeds, the content type is auto-determined by
inspecting the content, and defaults to :mimetype:`text/html`.  Note that this
may cause silent data loss if the value contains plain text with angle
brackets.  There is nothing I can do about this problem; it is a limitation of
:abbr:`RSS (Rich Site Summary)`.

Future enhancement: some versions of :abbr:`RSS (Rich Site Summary)` clearly
specify that certain values default to :mimetype:`text/plain`, and
:program:`Universal Feed Parser` should respect this, but it doesn't yet.


:py:attr:`entries[i].source.rights_detail.language`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The language of the copyright statement for the source of this entry.

:py:attr:`~entries[i].source.rights_detail.language` is supposed to be a
language code, as specified by `RFC 3066`_, but publishers have been known to
publish random values like "English" or "German".
:program:`Universal Feed Parser` does not do any parsing or normalization of
language codes.

.. _RFC 3066: http://www.ietf.org/rfc/rfc3066.txt

:py:attr:`~entries[i].source.rights_detail.language` may come from the
element's xml:lang attribute, or it may inherit from a parent element's
xml:lang, or the Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)`
header.  If the feed does not specify a language,
:py:attr:`~entries[i].source.rights_detail.language` will be ``None``, the
:program:`Python` null value.


:py:attr:`entries[i].source.rights_detail.base`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original base :abbr:`URI (Uniform Resource Identifier)` for links within
the copyright statement for the source of this entry.

:py:attr:`entries[i].source.rights_detail.base` is only useful in rare
situations and can usually be ignored.  It is the original base
:abbr:`URI (Uniform Resource Identifier)` for this value, as specified by the
element's xml:base attribute, or a parent element's xml:base, or the
appropriate :abbr:`HTTP (Hypertext Transfer Protocol)` header, or the
:abbr:`URI (Uniform Resource Identifier)` of the feed.  (See
:ref:`advanced.base` for more details.)  By the time you see it,
:program:`Universal Feed Parser` has already resolved relative links in all
values where it makes sense to do so.  *Clients should never need to manually
resolve relative links.*



.. _reference.entry.source.subtitle:

:py:attr:`entries[i].source.subtitle`
-------------------------------------

A subtitle, tagline, slogan, or other short description of the source of this
entry.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, it is
:ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements
within this value may contain relative
:abbr:`URI (Uniform Resource Identifier)`\s.  If so, they are
:ref:`resolved according to a set of rules <advanced.base>`.



:py:attr:`entries[i].source.subtitle_detail`
--------------------------------------------

A dictionary containing details about the subtitle for the source of this
entry.


:py:attr:`entries[i].source.subtitle_detail.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same as :ref:`reference.entry.source.subtitle`.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, it is
:ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements
within this value may contain relative
:abbr:`URI (Uniform Resource Identifier)`\s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].source.subtitle_detail.type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The content type of the subtitle of the source of this entry.

Most likely values for :py:attr:`~entries[i].source.subtitle_detail.type`:

* :mimetype:`text/plain``
* :mimetype:`text/html``
* :mimetype:`application/xhtml+xml``

For Atom feeds, the content type is taken from the type attribute, which
defaults to :mimetype:`text/plain`` if not specified.  For
:abbr:`RSS (Rich Site Summary)` feeds, the content type is auto-determined by
inspecting the content, and defaults to :mimetype:`text/html``.  Note that this
may cause silent data loss if the value contains plain text with angle
brackets.  There is nothing I can do about this problem; it is a limitation of
:abbr:`RSS (Rich Site Summary)`.

Future enhancement: some versions of :abbr:`RSS (Rich Site Summary)` clearly
specify that certain values default to :mimetype:`text/plain``, and
:program:`Universal Feed Parser` should respect this, but it doesn't yet.


:py:attr:`entries[i].source.subtitle_detail.language`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The language of the subtitle of the source of this entry.

:py:attr:`~entries[i].source.subtitle_detail.language` is supposed to be a
language code, as specified by `RFC 3066`_, but publishers have been known to
publish random values like "English" or "German".
:program:`Universal Feed Parser` does not do any parsing or normalization of
language codes.

:py:attr:`~entries[i].source.subtitle_detail.language` may come from the
element's xml:lang attribute, or it may inherit from a parent element's
xml:lang, or the Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)`
header.  If the feed does not specify a language,
:py:attr:`~entries[i].source.subtitle_detail.language` will be ``None``, the
:program:`Python` null value.


:py:attr:`entries[i].source.subtitle_detail.base`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original base :abbr:`URI (Uniform Resource Identifier)` for links within
the subtitle of the source of this entry.

:py:attr:`entries[i].source.subtitle_detail.base` is only useful in rare
situations and can usually be ignored.  It is the original base
:abbr:`URI (Uniform Resource Identifier)` for this value, as specified by the
element's xml:base attribute, or a parent element's xml:base, or the
appropriate :abbr:`HTTP (Hypertext Transfer Protocol)` header, or the
:abbr:`URI (Uniform Resource Identifier)` of the feed.  (See
:ref:`advanced.base` for more details.)  By the time you see it,
:program:`Universal Feed Parser` has already resolved relative links in all
values where it makes sense to do so.  *Clients should never need to manually
resolve relative links.*



.. _reference.entry.source.title:

:py:attr:`entries[i].source.title`
----------------------------------

The title of the source of this entry.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, it is
:ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`\s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.



:py:attr:`entries[i].source.title_detail`
-----------------------------------------

A dictionary containing details about the title for the source of this entry.


:py:attr:`entries[i].source.title_detail.value`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same as :ref:`reference.entry.source.title`.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, it is
:ref:`sanitized <advanced.sanitization>` by default.

If this contains :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)`, certain (X)HTML elements within this
value may contain relative :abbr:`URI (Uniform Resource Identifier)`\s.  If so,
they are :ref:`resolved according to a set of rules <advanced.base>`.


:py:attr:`entries[i].source.title_detail.type`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The content type of the title of the source of this entry.

Most likely values for :py:attr:`entries[i].source.title_detail.type`:

* :mimetype:`text/plain`
* :mimetype:`text/html`
* :mimetype:`application/xhtml+xml`

For Atom feeds, the content type is taken from the type attribute, which
defaults to :mimetype:`text/plain` if not specified.  For
:abbr:`RSS (Rich Site Summary)` feeds, the content type is auto-determined by
inspecting the content, and defaults to :mimetype:`text/html`.  Note that this
may cause silent data loss if the value contains plain text with angle
brackets.  There is nothing I can do about this problem; it is a limitation of
:abbr:`RSS (Rich Site Summary)`.

Future enhancement: some versions of :abbr:`RSS (Rich Site Summary)` clearly
specify that certain values default to :mimetype:`text/plain`, and
:program:`Universal Feed Parser` should respect this, but it doesn't yet.


:py:attr:`entries[i].source.title_detail.language`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The language of the title of the source of this entry.

:py:attr:`~entries[i].source.title_detail.language` is supposed to be a
language code, as specified by `RFC 3066`_, but publishers have been known to
publish random values like "English" or "German".
:program:`Universal Feed Parser` does not do any parsing or normalization of language codes.

:py:attr:`~entries[i].source.title_detail.language` may come from the element's
xml:lang attribute, or it may inherit from a parent element's xml:lang, or the
Content-Language :abbr:`HTTP (Hypertext Transfer Protocol)` header.  If the
feed does not specify a language,
:py:attr:`~entries[i].source.title_detail.language` will be ``None``, the
:program:`Python` null value.


:py:attr:`entries[i].source.title_detail.base`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original base :abbr:`URI (Uniform Resource Identifier)` for links within
the title of the source of this entry.

:py:attr:`entries[i].source.title_detail.base` is only useful in rare
situations and can usually be ignored.  It is the original base
:abbr:`URI (Uniform Resource Identifier)` for this value, as specified by the element's
xml:base attribute, or a parent element's xml:base, or the appropriate
:abbr:`HTTP (Hypertext Transfer Protocol)` header, or the
:abbr:`URI (Uniform Resource Identifier)` of the feed.  (See :ref:`advanced.base` for more
details.)  By the time you see it, :program:`Universal Feed Parser` has already
resolved relative links in all values where it makes sense to do so.  *Clients
should never need to manually resolve relative links.*


:py:attr:`entries[i].source.updated`
------------------------------------

The date the source of this entry was last updated, as a string in the same
format as it was published in the original feed.

This element is :ref:`parsed as a date <advanced.date>` and stored in
:ref:`reference.entry.source.updated_parsed`.



.. _reference.entry.source.updated_parsed:

:py:attr:`entries[i].source.updated_parsed`
-------------------------------------------

The date this entry was last updated, as a standard :program:`Python` 9-tuple.
