.. _reference.feed.generator_detail:

:py:attr:`feed.generator_detail`
================================

A dictionary with details about the feed generator.



:py:attr:`feed.generator_detail.name`
-------------------------------------

Same as :ref:`reference.feed.generator`.


.. _reference.feed.generator_detail.href:

:py:attr:`feed.generator_detail.href`
-------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of the application used to generate
the feed.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.feed.generator_detail.version:

:py:attr:`feed.generator_detail.version`
----------------------------------------

The version number of the application used to generate the feed.  There is no
required format for this, but most applications use a MAJOR.MINOR version
number.


.. rubric:: Comes from

* /atom03:feed/atom03:generator
* /atom10:feed/atom10:generator
* /rdf:RDF/rdf:channel/admin:generatorAgent/@rdf:resource
* /rss/channel/generator


.. seealso::

    * :ref:`reference.feed.generator`
