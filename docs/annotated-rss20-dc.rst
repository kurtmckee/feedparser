.. _annotated.rss20dc:

RSS 2.0 with Namespaces
=======================

This is a sample :abbr:`RSS (Rich Site Summary)` 2.0 feed that uses several
allowable extension modules in namespaces. The feed is annotated with links
that show how each value can be accessed once the feed is parsed.

.. caution::

    Even though many of these elements are required according to the specification,
    real-world feeds may be missing any element.  If an element is not present in
    the feed, it will not be present in the parsed results.  You should not rely on
    any particular element being present.

.. rubric:: Annotated :abbr:`RSS (Rich Site Summary)` 2.0 feed with namespaces

.. container:: pre


    <?xml version="1.0" encoding=":ref:`utf-8 <reference.encoding>`"?>
    <rss version=":ref:`2.0 <reference.version>`"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:admin="http://webns.net/mvcb/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <channel>
    <title>\ :ref:`Sample Feed <reference.feed.title>`\</title>
    <link>\ :ref:`http://example.org/ <reference.feed.link>`\</link>
    <description>\ :ref:`For documentation only <reference.feed.subtitle>`\</description>
    <dc:language>\ :ref:`en-us <reference.feed.language>`\</dc:language>
    <dc:creator>\ :ref:`Mark Pilgrim <reference.feed.author_detail.name>` (:ref:`mark@example.org <reference.feed.author_detail.email>`)</dc:creator>
    <dc:rights>\ :ref:`Copyright 2004 Mark Pilgrim <reference.feed.rights>`\</dc:rights>
    <dc:date>\ :ref:`2004-06-04T17:40:33-05:00 <reference.feed.updated>`\</dc:date>
    <admin:generatorAgent rdf:resource=":ref:`http://www.exampletoolkit.org/ <reference.feed.generator_detail.href>`"/>
    <admin:errorReportsTo rdf:resource=":ref:`mailto:mark@example.org <reference.feed.errorreportsto>`"/>
    <item>
    <title>\ :ref:`First of all <reference.entry.title>`\</title>
    <link>\ :ref:`http://example.org/archives/2002/09/04.html#first_of_all <reference.entry.link>`\</link>
    <guid isPermaLink="false">\ :ref:`1983@example.org <reference.entry.id>`\</guid>
    <description>
    :ref:`Americans are fat. Smokers are stupid. People who don't speak Perl are irrelevant. <reference.entry.summary>`
    </description>
    <dc:subject>\ :ref:`Quotes <reference.entry.tags.term>`\</dc:subject>
    <dc:date>\ :ref:`2002-09-04T13:54:20-05:00 <reference.entry.updated>`\</dc:date>
    <content:encoded><![CDATA[:ref:`\<cite>Ian Hickson\</cite>: \<q>\<a href="http://ln.hixie.ch/?start=1030823786&amp;count=1?>
    Americans are fat. Smokers are stupid. People who don't speak Perl are irrelevant.
    \</a>\</q> <reference.entry.content.value>`
    ]]>
    </content:encoded>
    </item>
    </channel>
    </rss>
