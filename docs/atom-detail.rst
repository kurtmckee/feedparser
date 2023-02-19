Getting Detailed Information on Atom Elements
=============================================

Several Atom elements share the Atom content model: title, subtitle, rights,
summary, and of course content. (Atom 0.3 also had an info element which
shared this content model.) :program:`Universal Feed Parser` captures all
relevant metadata about these elements, most importantly the content type and
the value itself.

Detailed Information on Feed Elements
-------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
    >>> d.feed.title_detail
    {'type': 'text/plain',
    'base': 'http://example.org/',
    'language': 'en',
    'value': 'Sample Feed'}
    >>> d.feed.subtitle_detail
    {'type': 'text/html',
    'base': 'http://example.org/',
    'language': 'en',
    'value': 'For documentation <em>only</em>'}
    >>> d.feed.rights_detail
    {'type': 'text/html',
    'base': 'http://example.org/',
    'language': 'en',
    'value': '<p>Copyright 2004, Mark Pilgrim</p>'}
    >>> d.entries[0].title_detail
    {'type': 'text/plain',
    'base': 'http://example.org/',
    'language': 'en',
    'value': 'First entry title'}
    >>> d.entries[0].summary_detail
    {'type': 'text/plain',
    'base': 'http://example.org/',
    'language': 'en',
    'value': 'Watch out for nasty tricks'}
    >>> len(d.entries[0].content)
    1
    >>> d.entries[0].content[0]
    {'type': 'application/xhtml+xml',
    'base': 'http://example.org/entry/3',
    'language': 'en-US'
    'value': '<div>Watch out for <span> nasty tricks</span></div>'}
