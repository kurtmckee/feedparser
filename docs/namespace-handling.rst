.. _advanced.namespaces:

Namespace Handling
==================

:program:`Universal Feed Parser` attempts to expose all possible data in feeds,
including elements in extension namespaces.

Some common namespaced elements are mapped to core elements.  For further
information about these mappings, see :ref:`reference`.

Other namespaced elements are available as ``prefixelement``.

The namespaces defined in the feed are available in the parsed results as
``namespaces``, a dictionary of {prefix: namespaceURI}.  If the feed defines a
default namespace, it is listed as ``namespaces['']``.


Accessing namespaced elements
-----------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/prism.rdf')
    >>> d.feed.prism_issn
    u'0028-0836'
    >>> d.namespaces
    {'': u'http://purl.org/rss/1.0/',
    'prism': u'http://prismstandard.org/namespaces/1.2/basic/',
    'rdf': u'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}


The prefix used to construct the variable name is not guaranteed to be the same
as the prefix of the namespaced element in the original feed.  If
:program:`Universal Feed Parser` recognizes the namespace, it will use the
namespace's preferred prefix to construct the variable name.  It will also list
the namespace in the ``namespaces`` dictionary using the namespace's preferred
prefix.

In the previous example, the namespace
(http://prismstandard.org/namespaces/1.2/basic/) was defined with the
namespace's preferred prefix (prism), so the prism:issn element was accessible
as the variable ``d.feed.prism_issn``.  However, if the namespace is defined
with a non-standard prefix, :program:`Universal Feed Parser` will still
construct the variable name using the preferred prefix, *not* the actual prefix
that is used in the feed.

This will become clear with an example.


Accessing namespaced elements with non-standard prefixes
--------------------------------------------------------

::

    >>> import feedparser
    >>> d = feedparser.parse('http://feedparser.org/docs/examples/nonstandard_prefix.rdf')
    >>> d.feed.prism_issn
    u'0028-0836'
    >>> d.feed.foo_issn
    Traceback (most recent call last):
    File "<stdin>", line 1, in ?
    File "feedparser.py", line 158, in __getattr__
    raise AttributeError, "object has no attribute '%s'" % key
    AttributeError: object has no attribute 'foo_issn'
    >>> d.namespaces
    {'': u'http://purl.org/rss/1.0/',
    'prism': u'http://prismstandard.org/namespaces/1.2/basic/',
    'rdf': u'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}


This is the complete list of namespaces that :program:`Universal Feed Parser`
recognizes and uses to construct the variable names for data in these
namespaces:

=============== =====================================================
Prefix          Namespace                                            
=============== =====================================================
admin           http://webns.net/mvcb/                               
ag              http://purl.org/rss/1.0/modules/aggregation/         
annotate        http://purl.org/rss/1.0/modules/annotate/            
audio           http://media.tangent.org/rss/1.0/                    
blogChannel     http://backend.userland.com/blogChannelModule        
cc              http://web.resource.org/cc/                          
co              http://purl.org/rss/1.0/modules/company              
content         http://purl.org/rss/1.0/modules/content/             
cp              http://my.theinfo.org/changed/1.0/rss/               
creativeCommons http://backend.userland.com/creativeCommonsRssModule 
dc              http://purl.org/dc/elements/1.1/                     
dcterms         http://purl.org/dc/terms/                            
email           http://purl.org/rss/1.0/modules/email/               
ev              http://purl.org/rss/1.0/modules/event/               
feedburner      http://rssnamespace.org/feedburner/ext/1.0           
fm              http://freshmeat.net/rss/fm/                         
foaf            http://xmlns.com/foaf/0.1/                           
geo             http://www.w3.org/2003/01/geo/wgs84_pos#             
icbm            http://postneo.com/icbm/                             
image           http://purl.org/rss/1.0/modules/image/               
itunes          http://example.com/DTDs/PodCast-1.0.dtd              
itunes          http://www.itunes.com/DTDs/PodCast-1.0.dtd           
l               http://purl.org/rss/1.0/modules/link/                
media           http://search.yahoo.com/mrss                         
pingback        http://madskills.com/public/xml/rss/module/pingback/ 
prism           http://prismstandard.org/namespaces/1.2/basic/       
rdf             http://www.w3.org/1999/02/22-rdf-syntax-ns#          
rdfs            http://www.w3.org/2000/01/rdf-schema#                
ref             http://purl.org/rss/1.0/modules/reference/           
reqv            http://purl.org/rss/1.0/modules/richequiv/           
search          http://purl.org/rss/1.0/modules/search/              
slash           http://purl.org/rss/1.0/modules/slash/               
soap            http://schemas.xmlsoap.org/soap/envelope/            
ss              http://purl.org/rss/1.0/modules/servicestatus/       
str             http://hacks.benhammersley.com/rss/streaming/        
sub             http://purl.org/rss/1.0/modules/subscription/        
sy              http://purl.org/rss/1.0/modules/syndication/         
szf             http://schemas.pocketsoap.com/rss/myDescModule/      
taxo            http://purl.org/rss/1.0/modules/taxonomy/            
thr             http://purl.org/rss/1.0/modules/threading/           
ti              http://purl.org/rss/1.0/modules/textinput/           
trackback       http://madskills.com/public/xml/rss/module/trackback/
wfw             http://wellformedweb.org/CommentAPI/                 
wiki            http://purl.org/rss/1.0/modules/wiki/                
xhtml           http://www.w3.org/1999/xhtml                         
xlink           http://www.w3.org/1999/xlink                         
xml             http://www.w3.org/XML/1998/namespace                 
=============== =====================================================

.. note::

    :program:`Universal Feed Parser` treats namespaces as case-insensitive to
    match the behavior of certain versions of :program:`iTunes`.

.. warning::

    Data from namespaced elements is not :ref:`sanitized <advanced.sanitization>`
    (even if it contains :abbr:`HTML (HyperText Markup Language)` markup).
