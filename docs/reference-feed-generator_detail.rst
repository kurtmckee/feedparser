.. _reference.feed.generator_detail:



feed.generator_detail
=====================




A dictionary with details about the feed generator.

- Comes from

- /atom10:feed/atom10:generator

- /atom03:feed/atom03:generator

- /rss/channel/generator

- /rdf:RDF/rdf:channel/admin:generatorAgent/@rdf:resource



- See also

- :ref:`reference.feed.generator`





feed.generator_detail.name
--------------------------

Same as :ref:`reference.feed.generator`.



.. _reference.feed.generator_detail.href:



feed.generator_detail.href
--------------------------

The :abbr:`URL (Uniform Resource Locator)` of the application used to generate the feed.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is :ref:`resolved according to a set of rules <advanced.base>`.



.. _reference.feed.generator_detail.version:



feed.generator_detail.version
-----------------------------

The version number of the application used to generate the feed.  There is no required format for this, but most applications use a MAJOR.MINOR version number.