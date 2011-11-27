.. _reference.feed.tags:



feed.tags
=========




A list of dictionaries that contain details of the categories for the feed.

- Comes from

- /atom10:feed/category

- /atom03:feed/dc:subject

- /rss/channel/category

- /rss/channel/dc:subject

- /rss/channel/itunes:category

- /rss/channel/itunes:keywords

- /rdf:RDF/rdf:channel/dc:subject



.. note:: Prior to version 4.0, :program:`Universal Feed Parser` exposed categories in ``feed.category`` (the primary category) and ``feed.categories`` (a list of tuples containing the domain and term of each category).  These uses are still supported for backward compatibility, but you will not see them in the parsed results unless you explicitly ask for them.



.. _reference.feed.tags.term:



feed.tags[i].term
-----------------

The category term (keyword).



feed.tags[i].scheme
-------------------

The category scheme (domain).



feed.tags[i].label
------------------

A human-readable label for the category.