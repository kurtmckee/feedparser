.. _reference.entry.tags:



entries[i].tags
===============




A list of dictionaries that contain details of the categories for the entry.

- Comes from

- /atom10:feed/atom10:entry/category

- /atom03:feed/atom03:entry/dc:subject

- /rss/channel/item/category

- /rss/channel/item/dc:subject

- /rss/channel/item/itunes:category

- /rss/channel/item/itunes:keywords

- /rdf:RDF/rdf:channel/rdf:item/dc:subject



.. note:: Prior to version 4.0, :program:`Universal Feed Parser` exposed categories in ``feed.category`` (the primary category) and ``feed.categories`` (a list of tuples containing the domain and term of each category).  These uses are still supported for backward compatibility, but you will not see them in the parsed results unless you explicitly ask for them.



.. _reference.entry.tags.term:



entries[i].tags[j].term
-----------------------

The category term (keyword).



entries[i].tags[j].scheme
-------------------------

The category scheme (domain).



entries[i].tags[j].label
------------------------

A human-readable label for the category.