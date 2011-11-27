.. _reference.feed.tags:

:py:attr:`feed.tags`
====================

A list of dictionaries that contain details of the categories for the feed.


.. note::

    Prior to version 4.0, :program:`Universal Feed Parser` exposed categories in
    ``feed.category`` (the primary category) and ``feed.categories`` (a list of
    tuples containing the domain and term of each category).  These uses are still
    supported for backward compatibility, but you will not see them in the parsed
    results unless you explicitly ask for them.


.. _reference.feed.tags.term:

:py:attr:`feed.tags[i].term`
----------------------------

The category term (keyword).


:py:attr:`feed.tags[i].scheme`
------------------------------

The category scheme (domain).


:py:attr:`feed.tags[i].label`
-----------------------------

A human-readable label for the category.


.. rubric:: Comes from

* /atom03:feed/dc:subject
* /atom10:feed/category
* /rdf:RDF/rdf:channel/dc:subject
* /rss/channel/category
* /rss/channel/dc:subject
* /rss/channel/itunes:category
* /rss/channel/itunes:keywords
