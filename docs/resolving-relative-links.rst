.. _advanced.base:

Relative Link Resolution
========================

Many feed elements and attributes are :abbr:`URI (Uniform Resource Identifier)`\s.
:program:`Universal Feed Parser` resolves relative :abbr:`URI (Uniform Resource Identifier)`\s
according to the `XML:Base <http://www.w3.org/TR/xmlbase/>`_ specification.  We'll see how
that works in a minute, but first let's talk about which values are treated as
:abbr:`URI (Uniform Resource Identifier)`\s.


Which Values Are :abbr:`URI (Uniform Resource Identifier)`\s
------------------------------------------------------------

These feed elements are treated as :abbr:`URI (Uniform Resource Identifier)`\s,
and resolved if they are relative:

* :ref:`reference.entry.author_detail.href`
* :ref:`reference.entry.comments`
* :ref:`reference.entry.contributors.href`
* :ref:`reference.entry.enclosures.href`
* :ref:`reference.entry.id`
* :ref:`reference.entry.license`
* :ref:`reference.entry.link`
* :ref:`reference.entry.links.href`
* :ref:`reference.entry.publisher_detail.href`
* :ref:`reference.entry.source.author_detail.href`
* :ref:`reference.entry.source.contributors.href`
* :ref:`reference.entry.source.links.href`
* :ref:`reference.feed.author_detail.href`
* :ref:`reference.feed.contributors.href`
* :ref:`reference.feed.docs`
* :ref:`reference.feed.generator_detail.href`
* :ref:`reference.feed.id`
* :ref:`reference.feed.image.href`
* :ref:`reference.feed.image.link`
* :ref:`reference.feed.license`
* :ref:`reference.feed.link`
* :ref:`reference.feed.links.href`
* :ref:`reference.feed.publisher_detail.href`
* :ref:`reference.feed.textinput.link`

In addition, several feed elements may contain :abbr:`HTML (HyperText Markup Language)`
or :abbr:`XHTML (Extensible HyperText Markup Language)` markup. Certain elements and
attributes in :abbr:`HTML (HyperText Markup Language)` can be relative
:abbr:`URI (Uniform Resource Identifier)`\s, and :program:`Universal Feed Parser` will
resolve these :abbr:`URI (Uniform Resource Identifier)`\s according to the same rules
as the feed elements listed above.


These feed elements may contain :abbr:`HTML (HyperText Markup Language)` or
:abbr:`XHTML (Extensible HyperText Markup Language)` markup.  In Atom feeds,
whether these elements are treated as :abbr:`HTML (HyperText Markup Language)`
depends on the value of the type attribute.  In :abbr:`RSS (Rich Site Summary)`
feeds, these values are always treated as :abbr:`HTML (HyperText Markup Language)`.


* :ref:`reference.entry.content.value`
* :ref:`reference.entry.summary` (:ref:`reference.entry.summary_detail.value`)
* :ref:`reference.entry.title` (:ref:`reference.entry.title_detail.value`)
* :ref:`reference.feed.info` (:ref:`reference.feed.info_detail.value`)
* :ref:`reference.feed.rights` (:ref:`reference.feed.rights_detail.value`)
* :ref:`reference.feed.subtitle` (:ref:`reference.feed.subtitle_detail.value`)
* :ref:`reference.feed.title` (:ref:`reference.feed.title_detail.value`)


When any of these feed elements contains :abbr:`HTML (HyperText Markup Language)`
or :abbr:`XHTML (Extensible HyperText Markup Language)` markup, the
following :abbr:`HTML (HyperText Markup Language)` elements are treated as
:abbr:`URI (Uniform Resource Identifier)`\s and are resolved if they are
relative:


* <a href="...">
* <applet codebase="...">
* <area href="...">
* <blockquote cite="...">
* <body background="...">
* <del cite="...">
* <form action="...">
* <frame longdesc="...">
* <frame src="...">
* <head profile="...">
* <iframe longdesc="...">
* <iframe src="...">
* <img longdesc="...">
* <img src="...">
* <img usemap="...">
* <input src="...">
* <input usemap="...">
* <ins cite="...">
* <link href="...">
* <object classid="...">
* <object codebase="...">
* <object data="...">
* <object usemap="...">
* <q cite="...">
* <script src="...">


How Relative :abbr:`URI (Uniform Resource Identifier)`\s Are Resolved
---------------------------------------------------------------------

:program:`Universal Feed Parser` resolves relative :abbr:`URI (Uniform Resource Identifier)`\s
according to the `XML:Base <http://www.w3.org/TR/xmlbase/>`_ specification.
This defines a hierarchical inheritance system, where one element can define
the base :abbr:`URI (Uniform Resource Identifier)` for itself and all of its
child elements, using an xml:base attribute.  A child element can then override
its parent's base :abbr:`URI (Uniform Resource Identifier)` by redeclaring
xml:base to a different value.


If no xml:base is specified, the feed has a default base :abbr:`URI (Uniform Resource Identifier)`
defined in the Content-Location :abbr:`HTTP (Hypertext Transfer Protocol)` header.


If no Content-Location :abbr:`HTTP (Hypertext Transfer Protocol)` header is
present, the :abbr:`URL (Uniform Resource Locator)` used to retrieve the feed
itself is the default base :abbr:`URI (Uniform Resource Identifier)` for all
relative links within the feed.  If the feed was retrieved via an
:abbr:`HTTP (Hypertext Transfer Protocol)` redirect (any :abbr:`HTTP (Hypertext Transfer Protocol)`
3xx status code), then the final :abbr:`URL (Uniform Resource Locator)` of the
feed is the default base :abbr:`URI (Uniform Resource Identifier)`.


For example, an xml:base on the root-level element sets the base
:abbr:`URI (Uniform Resource Identifier)` for all :abbr:`URI (Uniform Resource Identifier)`\s in the feed.


xml:base on the root-level element
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse("http://feedparser.org/docs/examples/base.xml")
    >>> d.feed.link
    u'http://example.org/index.html'
    >>> d.feed.generator_detail.href
    u'http://example.org/generator/'


An xml:base attribute on an <entry> overrides the xml:base on the parent <feed>.


Overriding xml:base on an <entry>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse("http://feedparser.org/docs/examples/base.xml")
    >>> d.entries[0].link
    u'http://example.org/archives/000001.html'
    >>> d.entries[0].author_detail.href
    u'http://example.org/about/'


An xml:base on <content> overrides the xml:base on the parent <entry>.  In
addition, whatever the base :abbr:`URI (Uniform Resource Identifier)` is for
the <content> element (whether defined directly on the <content> element, or
inherited from the parent element) is used as the base :abbr:`URI (Uniform Resource Identifier)`
for the embedded :abbr:`HTML (HyperText Markup Language)`
or :abbr:`XHTML (Extensible HyperText Markup Language)` markup within the
content.


Relative links within embedded :abbr:`HTML (HyperText Markup Language)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse("http://feedparser.org/docs/examples/base.xml")
    >>> d.entries[0].content[0].value
    u'<p id="anchor1"><a href="http://example.org/archives/000001.html#anchor2">skip to anchor 2</a></p>
    <p>Some content</p>
    <p id="anchor2">This is anchor 2</p>'



The xml:base affects other attributes in the element in which it is declared.


xml:base and sibling attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse("http://feedparser.org/docs/examples/base.xml")
    >>> d.entries[0].links[1].rel
    u'service.edit'
    >>> d.entries[0].links[1].href
    u'http://example.com/api/client/37'


If no xml:base is specified on the root-level element, the default base
:abbr:`URI (Uniform Resource Identifier)` is given in the Content-Location
:abbr:`HTTP (Hypertext Transfer Protocol)` header.  This can still be
overridden by any child element that declares an xml:base attribute.


Content-Location :abbr:`HTTP (Hypertext Transfer Protocol)` header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse("http://feedparser.org/docs/examples/http_base.xml")
    >>> d.feed.link
    u'http://example.org/index.html'
    >>> d.entries[0].link
    u'http://example.org/archives/000001.html'


Finally, if no root-level xml:base is declared, and no Content-Location
:abbr:`HTTP (Hypertext Transfer Protocol)` header is present, the
:abbr:`URL (Uniform Resource Locator)` of the feed itself is the default base
:abbr:`URI (Uniform Resource Identifier)`.  Again, this can still be overridden
by any element that declares an xml:base attribute.


Feed :abbr:`URL (Uniform Resource Locator)` as default base :abbr:`URI (Uniform Resource Identifier)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse("http://feedparser.org/docs/examples/no_base.xml")
    >>> d.feed.link
    u'http://feedparser.org/docs/examples/index.html
    >>> d.entries[0].link
    u'http://example.org/archives/000001.html'


.. _advanced.base.disable:

Disabling Relative :abbr:`URI (Uniform Resource Identifier)`\s Resolution
-------------------------------------------------------------------------

Though not recommended, it is possible to disable :program:`Universal Feed Parser`\'s relative
:abbr:`URI (Uniform Resource Identifier)` resolution by setting feedparser.RESOLVE_RELATIVE_URIS to ``0``.


How to disable relative :abbr:`URI (Uniform Resource Identifier)` resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/base.xml')
    >>> d.entries[0].content[0].base
    u'http://example.org/archives/000001.html'
    >>> print d.entries[0].content[0].value
    <p id="anchor1"><a href="http://example.org/archives/000001.html#anchor2">skip to anchor 2</a></p>
    <p>Some content</p>
    <p id="anchor2">This is anchor 2</p>
    >>> feedparser.RESOLVE_RELATIVE_URIS = 0
    >>> d2 = feedparser.parse('http://feedparser.org/docs/examples/base.xml')
    >>> d2.entries[0].content[0].base
    u'http://example.org/archives/000001.html'
    >>> print d2.entries[0].content[0].value
    <p id="anchor1"><a href="#anchor2">skip to anchor 2</a></p>
    <p>Some content</p>
    <p id="anchor2">This is anchor 2</p>

