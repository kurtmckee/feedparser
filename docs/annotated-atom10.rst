.. _annotated.atom10:

Atom 1.0
========

This is a sample Atom 1.0 feed, annotated with links that show how each value
can be accessed once the feed is parsed.

.. caution::

    Even though many of these elements are required according to the specification,
    real-world feeds may be missing any element. If an element is not present in
    the feed, it will not be present in the parsed results. You should not rely on
    any particular element being present.

.. rubric:: Annotated Atom 1.0 feed

.. container:: pre

    <?xml version="1.0" encoding=":ref:`utf-8 <reference.encoding>`"?>
    <feed xmlns=":ref:`http://www.w3.org/2005/Atom <reference.version>`"
    xml:base=":ref:`http://example.org/ <advanced.base>`"
    xml:lang=":ref:`en <reference.feed.title_detail.language>`">
    <title type=":ref:`text <reference.feed.title_detail.type>`">
    :ref:`Sample Feed <reference.feed.title>`
    </title>
    <subtitle type=":ref:`html <reference.feed.subtitle_detail.type>`">
    :ref:`For documentation &lt;em&gt;only&lt;/em&gt; <reference.feed.subtitle>`
    </subtitle>
    <link rel=":ref:`alternate <reference.feed.links.rel>`"
    type=":ref:`html <reference.feed.links.type>`"
    href=":ref:`/ <reference.feed.links.href>`"/>
    <link rel=":ref:`self <reference.feed.links.rel>`"
    type=":ref:`application/atom+xml <reference.feed.links.type>`"
    href=":ref:`http://www.example.org/atom10.xml <reference.feed.links.href>`"/>
    <rights type=":ref:`html <reference.feed.rights_detail.type>`">
    :ref:`&lt;p>Copyright 2005, Mark Pilgrim&lt;/p> <reference.feed.rights>`
    </rights>
    <generator uri=":ref:`http://example.org/generator/ <reference.feed.generator_detail.href>`"
    version=":ref:`4.0 <reference.feed.generator_detail.version>`">
    :ref:`Sample Toolkit <reference.feed.generator>`
    </generator>
    <id>\ :ref:`tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml <reference.feed.id>`\</id>
    <updated>\ :ref:`2005-11-09T11:56:34Z <reference.feed.updated>`\</updated>
    <entry>
    <title>\ :ref:`First entry title <reference.entry.title>`\</title>
    <link rel=":ref:`alternate <reference.entry.links.type>`"
    href=":ref:`/entry/3 <reference.entry.links.href>`"/>
    <link rel=":ref:`related <reference.entry.links.type>`"
    type=":ref:`text/html <reference.entry.links.type>`"
    href=":ref:`http://search.example.com/ <reference.entry.links.href>`"/>
    <link rel=":ref:`via <reference.entry.links.type>`"
    type=":ref:`text/html <reference.entry.links.type>`"
    href=":ref:`http://toby.example.com/examples/atom10 <reference.entry.links.href>`"/>
    <link rel=":ref:`enclosure <reference.entry.enclosures>`"
    type=":ref:`video/mpeg4 <reference.entry.enclosures.type>`"
    href=":ref:`http://www.example.com/movie.mp4 <reference.entry.enclosures.href>`"
    length=":ref:`42301 <reference.entry.enclosures.length>`"/>
    <id>\ :ref:`tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3 <reference.entry.id>`\</id>
    <published>\ :ref:`2005-11-09T00:23:47Z <reference.entry.published>`\</published>
    <updated>\ :ref:`2005-11-09T11:56:34Z <reference.entry.updated>`\</updated>
    <author>
    <name>\ :ref:`Mark Pilgrim <reference.entry.author_detail.name>`\</name>
    <uri>\ :ref:`http://diveintomark.org/ <reference.entry.author_detail.href>`\</uri>
    <email>\ :ref:`mark@example.org <reference.entry.author_detail.email>`\</email>
    </author>
    <contributor>
    <name>\ :ref:`Joe <reference.entry.contributors.name>`\</name>
    <url>\ :ref:`http://example.org/joe/ <reference.entry.contributors.href>`\</url>
    <email>\ :ref:`joe@example.org <reference.entry.contributors.email>`\</email>
    </contributor>
    <contributor>
    <name>\ :ref:`Sam <reference.entry.contributors.name>`\</name>
    <url>\ :ref:`http://example.org/sam/ <reference.entry.contributors.href>`\</url>
    <email>\ :ref:`sam@example.org <reference.entry.contributors.email>`\</email>
    </contributor>
    <summary type=":ref:`text <reference.entry.summary_detail.type>`">
    :ref:`Watch out for nasty tricks <reference.entry.summary>`
    </summary>
    <content type=":ref:`xhtml <reference.entry.content.type>`"
    xml:base=":ref:`http://example.org/entry/3 <reference.entry.content.base>`"
    xml:lang=":ref:`en-US <reference.entry.content.language>`">\ :ref:`\<div xmlns="http://www.w3.org/1999/xhtml">Watch out for
    \<span style="background-image: url(javascript:window.location='http://example.org/')">
    nasty tricks\</span>\</div> <reference.entry.content.value>`
    </content>
    </entry>
    </feed>
