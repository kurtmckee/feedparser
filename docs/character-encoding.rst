.. _advanced.encoding:

Character Encoding Detection
============================

.. tip::

    Feeds may be published in any character encoding.  :program:`Python`
    supports only a few character encodings by default.  To support the maximum
    number of character encodings (and be able to parse the maximum number of
    feeds), you should install :file:`cjkcodecs` and :file:`iconv_codec`.  Both are
    available at `http://cjkpython.i18n.org/ <http://cjkpython.i18n.org/>`_.

`RFC 3023 <http://www.ietf.org/rfc/rfc3023.txt>`_ defines the interaction
between :abbr:`XML (Extensible Markup Language)` and :abbr:`HTTP (Hypertext Transfer Protocol)`
as it relates to character encoding.  :abbr:`XML (Extensible Markup Language)`
and :abbr:`HTTP (Hypertext Transfer Protocol)` have different ways of
specifying character encoding and different defaults in case no encoding is
specified, and determining which value takes precedence depends on a variety of
factors.


Introduction to Character Encoding
----------------------------------

In :abbr:`XML (Extensible Markup Language)`, the character encoding is optional
and may be given in the :abbr:`XML (Extensible Markup Language)` declaration in
the first line of the document, like this:

.. sourcecode:: xml

    <?xml version="1.0" encoding="utf-8"?>

If no encoding is given, :abbr:`XML (Extensible Markup Language)` supports the
use of a Byte Order Mark to identify the document as some flavor of UTF-32,
UTF-16, or UTF-8.  `Section F of the XML specification <http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info>`_
outlines the process for determining the character encoding based on unique
properties of the Byte Order Mark in the first two to four bytes of the
document.

If no encoding is specified and no Byte Order Mark is present, :abbr:`XML (Extensible Markup Language)`
defaults to UTF-8.

:abbr:`HTTP (Hypertext Transfer Protocol)` uses :abbr:`MIME` to define a method
of specifying the character encoding, as part of the Content-Type :abbr:`HTTP (Hypertext Transfer Protocol)`
header, which looks like this:

::

    Content-Type: text/html; charset="utf-8"


If no charset is specified, :abbr:`HTTP (Hypertext Transfer Protocol)` defaults
to iso-8859-1, but only for text/* media types. For other media types, the
default encoding is undefined, which is where :abbr:`RFC (Request For Comments)` 3023 comes in.

According to :abbr:`RFC (Request For Comments)` 3023, if the media type given
in the Content-Type :abbr:`HTTP (Hypertext Transfer Protocol)` header is
application/xml, application/xml-dtd, application/xml-external-parsed-entity,
or any one of the subtypes of application/xml such as application/atom+xml or
application/rss+xml or even application/rdf+xml, then the encoding is


#. the encoding given in the ``charset`` parameter of the Content-Type :abbr:`HTTP (Hypertext Transfer Protocol)` header, or

#. the encoding given in the encoding attribute of the :abbr:`XML (Extensible Markup Language)` declaration within the document, or

#. utf-8.


On the other hand, if the media type given in the Content-Type
:abbr:`HTTP (Hypertext Transfer Protocol)` header is text/xml,
text/xml-external-parsed-entity, or a subtype like text/AnythingAtAll+xml, then
the encoding attribute of the :abbr:`XML (Extensible Markup Language)`
declaration within the document is ignored completely, and the encoding is


#. the encoding given in the charset parameter of the Content-Type :abbr:`HTTP (Hypertext Transfer Protocol)` header, or

#. us-ascii.


Handling Incorrectly-Declared Encodings
---------------------------------------

:program:`Universal Feed Parser` initially uses the rules specified in
:abbr:`RFC (Request For Comments)` 3023 to determine the character encoding of
the feed.  If parsing succeeds, then that's that.  If parsing fails,
:program:`Universal Feed Parser` sets the ``bozo`` bit to ``1`` and sets
``bozo_exception`` to ``feedparser.CharacterEncodingOverride``.  Then it tries
to reparse the feed with the following character encodings:


#. the encoding specified in the :abbr:`XML (Extensible Markup Language)` declaration

#. the encoding sniffed from the first four bytes of the document (as per `Section F <http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info>`_)

#. the encoding auto-detected by the `Universal Encoding Detector <http://chardet.feedparser.org/>`_, if installed

#. utf-8

#. windows-1252


If the character encoding can not be determined, :program:`Universal Feed Parser`
sets the ``bozo`` bit to ``1`` and sets ``bozo_exception`` to
``feedparser.CharacterEncodingUnknown``.  In this case, parsed values will be
strings, not Unicode strings.


Handling Incorrectly-Declared Media Types
-----------------------------------------

:abbr:`RFC (Request For Comments)` 3023 only applies when the feed is served
over :abbr:`HTTP (Hypertext Transfer Protocol)` with a Content-Type that
declares the feed to be some kind of :abbr:`XML (Extensible Markup Language)`.
However, some web servers are severely misconfigured and serve feeds with a
Content-Type of text/plain, application/octet-stream, or some completely bogus
media type.

:program:`Universal Feed Parser` will attempt to parse such feeds, but it will
set the ``bozo`` bit to ``1`` and set ``bozo_exception`` to
``feedparser.NonXMLContentType``.


.. seealso::

    * `RFC 3023 <http://www.ietf.org/rfc/rfc3023.txt>`_

    * `Section F of the XML specification <http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info>`_

    * `On the well-formedness of XML documents served as text/plain <http://www.imc.org/atom-syntax/mail-archive/msg05575.html>`_

    * `CJKCodecs and iconv_codec <http://cjkpython.i18n.org/>`_
