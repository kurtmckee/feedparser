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
    {'type': u'text/plain',
    'base': u'http://example.org/',
    'language': u'en',
    'value': u'Sample Feed'}
    >>> d.feed.subtitle_detail
    {'type': u'text/html',
    'base': u'http://example.org/',
    'language': u'en',
    'value': u'For documentation <em>only</em>'}
    >>> d.feed.rights_detail
    {'type': u'text/html',
    'base': u'http://example.org/',
    'language': u'en',
    'value': u'<p>Copyright 2004, Mark Pilgrim</p>'}
    >>> d.entries[0].title_detail
    {'type': 'text/plain',
    'base': u'http://example.org/',
    'language': u'en',
    'value': u'First entry title'}
    >>> d.entries[0].summary_detail
    {'type': u'text/plain',
    'base': u'http://example.org/',
    'language': u'en',
    'value': u'Watch out for nasty tricks'}
    >>> len(d.entries[0].content)
    1
    >>> d.entries[0].content[0]
    {'type': u'application/xhtml+xml',
    'base': u'http://example.org/entry/3',
    'language': u'en-US'
    'value': u'<div>Watch out for <span> nasty tricks</span></div>'}

