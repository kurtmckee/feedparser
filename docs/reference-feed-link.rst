.. _reference.feed.link:

:py:attr:`feed.link`
====================

The :abbr:`URL (Uniform Resource Locator)` of the :abbr:`HTML (HyperText Markup
Language)` page associated with this feed.

For site feeds, this is probably the home page of the site.  For category
feeds, this is probably the category's archive page.  For search feeds, this is
probably the web page that displays the search results for the given search
parameters.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. rubric:: Comes from

* /atom03:feed/atom03:link[@rel="alternate"]/@href
* /atom10:feed/atom10:link[@rel="alternate"]/@href
* /atom10:feed/atom10:link[not(@rel)]/@href
* /rdf:RDF/rdf:channel/rdf:link
* /rss/channel/link


.. seealso::

    * :ref:`reference.feed.links`
