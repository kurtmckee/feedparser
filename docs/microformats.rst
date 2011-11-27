.. _advanced.microformats:

Microformats
============

An emerging trend in feed syndication is the inclusion of `microformats`_.
Besides the semantics defined by individual feed formats, publishers can add
additional semantics using rel and class attributes in embedded
:abbr:`HTML (HyperText Markup Language)` content.

.. _microformats: http://microformats.org/

.. note::

   To parse microformats. :program:`Universal Feed Parser` relies on a
   third-party library called `Beautiful Soup`_, which is distributed
   separately.  If Beautiful Soup is not installed,
   :program:`Universal Feed Parser` will silently skip microformats parsing.

.. _Beautiful Soup: http://www.crummy.com/software/BeautifulSoup/


The following elements are parsed for microformats:

* :ref:`reference.entry.summary_detail.value`
* :ref:`reference.entry.content.value`



.. _advanced.microformats.relenclosure:

rel=enclosure
-------------

The `rel=enclosure`_ microformat provides a way for embedded
:abbr:`HTML (HyperText Markup Language)` content to specify that a certain link
should be treated as an :ref:`enclosure <reference.entry.enclosures>`.
:program:`Universal Feed Parser` looks for links within embedded markup that
meet any of the following conditions:

.. _rel=enclosure: http://microformats.org/wiki/rel-enclosure

* rel attribute contains enclosure (note: rel attributes can contain a list of space-separated values)
* type attribute starts with audio/
* type attribute starts with video/
* type attribute starts with application/ but does not end with xml
* href attribute ends with one of the following file extensions:
  :file:`.7z`,
  :file:`.avi`,
  :file:`.bin`,
  :file:`.bz2`,
  :file:`.bz2`,
  :file:`.deb`,
  :file:`.dmg`,
  :file:`.exe`,
  :file:`.gz`,
  :file:`.hqx`,
  :file:`.img`,
  :file:`.iso`,
  :file:`.jar`,
  :file:`.m4a`,
  :file:`.m4v`,
  :file:`.mp2`,
  :file:`.mp3`,
  :file:`.mp4`,
  :file:`.msi`,
  :file:`.ogg`,
  :file:`.ogm`,
  :file:`.rar`,
  :file:`.rpm`,
  :file:`.sit`,
  :file:`.sitx`,
  :file:`.tar`,
  :file:`.tbz2`,
  :file:`.tgz`,
  :file:`.wma`,
  :file:`.wmv`,
  :file:`.z`,
  :file:`.zip`


When :program:`Universal Feed Parser` finds a link that satisfies any of these
conditions, it adds it to :ref:`reference.entry.enclosures`.


.. rubric:: Parsing embedded enclosures

.. sourcecode:: python

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rel-enclosure.xml')
    >>> d.entries[0].enclosures
    [{u'href': u'http://example.com/movie.mp4', 'title': u'awesome movie'}]



.. _advanced.microformats.reltag:

rel=tag
-------

The `rel=tag`_ microformat allows you to define
:ref:`tags <reference.entry.tags>` within embedded
:abbr:`HTML (HyperText Markup Language)` content.
:program:`Universal Feed Parser` looks for these attribute values in embedded
markup and maps them to :ref:`reference.entry.tags`.

.. _rel=tag: http://microformats.org/wiki/rel-tag


.. rubric:: Parsing embedded tags

.. sourcecode:: python

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/rel-tag.xml')
    >>> d.entries[0].tags
    [{'term': u'tech', 'scheme': u'http://del.icio.us/tag/', 'label': u'Technology'}]



.. _advanced.microformats.xfn:

:abbr:`XFN (XHTML Friends Network)`
-----------------------------------


The `XFN`_ microformat allows you to define human relationships between
:abbr:`URI (Uniform Resource Identifier)`\s.  For example, you could link from
your weblog to your spouse's weblog with the ``rel="spouse"`` relation.  It is
intended primarily for "blogrolls" or other static lists of links, but the
relations can occur anywhere in :abbr:`HTML (HyperText Markup Language)`
content.  If found, :program:`Universal Feed Parser` will return the
:abbr:`XFN (XHTML Friends Network)` information in :ref:`reference.entry.xfn`.

.. _XFN: http://microformats.org/wiki/XFN

:program:`Universal Feed Parser` supports all of the relationships listed in
the `XFN 1.1 profile`_, as well as the following variations:

.. _XFN 1.1 profile: http://gmpg.org/xfn/11

* ``coworker`` in addition to ``co-worker``
* ``coresident`` in addition to ``co-resident``
* ``relative`` in addition to ``kin``
* ``brother`` and ``sister`` in addition to ``sibling``
* ``husband`` and ``wife`` in addition to ``spouse``




.. rubric:: Parsing :abbr:`XFN (XHTML Friends Network)` relationships

.. sourcecode:: python

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/xfn.xml')
    >>> person = d.entries[0].xfn[0]
    >>> person.name
    u'John Doe'
    >>> person.href
    u'http://example.com/johndoe'
    >>> person.relationships
    [u'coworker', u'friend']



.. _advanced.microformats.hcard:

hCard
-----

The `hCard`_ microformat allows you to embed address book information within
:abbr:`HTML (HyperText Markup Language)` content.  If
:program:`Universal Feed Parser` finds an hCard within supported elements, it
converts it into an RFC 2426-compliant vCard and returns it in
:ref:`reference.entry.vcard`.

.. _hCard: http://microformats.org/wiki/hcard


.. rubric:: Converting embedded hCard markup into a vCard

.. sourcecode:: python

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/hcard.xml')
    >>> print d.entries[0].vcard
    BEGIN:vCard
    VERSION:3.0
    FN:Frank Dawson
    N:Dawson;Frank
    ADR;TYPE=work,postal,parcel:;;6544 Battleford Drive;Raleigh;NC;27613-3502;U
    .S.A.
    TEL;TYPE=WORK,VOICE,MSG:+1-919-676-9515
    TEL;TYPE=WORK,FAX:+1-919-676-9564
    EMAIL;TYPE=internet,pref:Frank_Dawson at Lotus.com
    EMAIL;TYPE=internet:fdawson at earthlink.net
    ORG:Lotus Development Corporation
    URL:http://home.earthlink.net/~fdawson
    END:vCard
    BEGIN:vCard
    VERSION:3.0
    FN:Tim Howes
    N:Howes;Tim
    ADR;TYPE=work:;;501 E. Middlefield Rd.;Mountain View;CA;94043;U.S.A.
    TEL;TYPE=WORK,VOICE,MSG:+1-415-937-3419
    TEL;TYPE=WORK,FAX:+1-415-528-4164
    EMAIL;TYPE=internet:howes at netscape.com
    ORG:Netscape Communications Corp.
    END:vCard



.. note::

    There are a growing number of microformats, and
    :program:`Universal Feed Parser` does not parse all of them.  However, both the
    rel and class attributes survive :ref:`HTML sanitizing <advanced.sanitization>`,
    so applications built on :program:`Universal Feed Parser` that wish to parse
    additional microformat content are free to do so.


.. seealso::

 * `Microformats.org <http://microformats.org/>`_
 * `rel=enclosure specification <http://microformats.org/wiki/rel-enclosure>`_
 * `rel=tag specification <http://microformats.org/wiki/rel-tag>`_
 * `XFN specification <http://microformats.org/wiki/XFN>`_
 * `hCard specification <http://microformats.org/wiki/hcard>`_
