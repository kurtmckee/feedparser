.. _annotated.atom03:

Atom 0.3
========

This is a sample Atom 0.3 feed, annotated with links that show how each value
can be accessed once the feed is parsed.

.. caution::

    Even though many of these elements are required according to the specification,
    real-world feeds may be missing any element.  If an element is not present in
    the feed, it will not be present in the parsed results.  You should not rely on
    any particular element being present.


.. rubric:: Annotated Atom 0.3 feed

.. container:: pre

    <?xml version="1.0" encoding=":ref:`utf-8 <reference.encoding>`"?>
    <feed version=":ref:`0.3 <reference.version>`"
    xmlns="http\://purl.org/atom/ns#"
    xml:base="http://example.org/"
    xml:lang="en">
    <title type=":ref:`text/plain <reference.feed.title_detail.type>`" mode="escaped">
    :ref:`Sample Feed <reference.feed.title>`
    </title>
    <tagline type=":ref:`text/html <reference.feed.subtitle_detail.type>`" mode="escaped">
    :ref:`For documentation &lt;em&gt;only&lt;/em&gt; <reference.feed.subtitle>`
    </tagline>
    <link rel=":ref:`alternate <reference.feed.links.rel>`"
    type=":ref:`text/html <reference.feed.links.type>`"
    href=":ref:`/ <reference.feed.links.href>`"/>
    <copyright type=":ref:`text/html <reference.feed.rights_detail.type>`" mode="escaped">
    :ref:`&lt;p>Copyright 2004, Mark Pilgrim&lt;/p>&lt; <reference.feed.rights>`
    </copyright>
    <generator url=":ref:`http://example.org/generator/ <reference.feed.generator_detail.href>`" version=":ref:`3.0 <reference.feed.generator_detail.version>`">
    :ref:`Sample Toolkit <reference.feed.generator>`
    </generator>
    <id>\ :ref:`tag:feedparser.org,2004-04-20:/docs/examples/atom03.xml <reference.feed.id>`\</id>
    <modified>\ :ref:`2004-04-20T11:56:34Z <reference.feed.updated>`\</modified>
    <info type=":ref:`application/xhtml+xml <reference.feed.info_detail.type>`" mode="xml">
    :ref:`\<div xmlns="http://www.w3.org/1999/xhtml">\<p>This is an Atom syndication feed.\</p>\</div> <reference.feed.info>`
    </info>
    <entry>
    <title>\ :ref:`First entry title <reference.entry.title>`\</title>
    <link rel=":ref:`alternate <reference.entry.links.rel>`"
    type=":ref:`text/html <reference.entry.links.type>`"
    href=":ref:`/entry/3 <reference.entry.links.href>`"/>
    <link rel=":ref:`service.edit <reference.entry.links.rel>`"
    type=":ref:`application/atom+xml <reference.entry.links.type>`"
    title=":ref:`Atom API entrypoint to edit this entry <reference.entry.links.title>`"
    href=":ref:`/api/edit/3 <reference.entry.links.href>`"/>
    <link rel=":ref:`service.post <reference.entry.links.rel>`"
    type=":ref:`application/atom+xml <reference.entry.links.type>`"
    title=":ref:`Atom API entrypoint to add comments to this entry <reference.entry.links.title>`"
    href=":ref:`/api/comment/3 <reference.entry.links.href>`"/>
    <id>\ :ref:`tag:feedparser.org,2004-04-20:/docs/examples/atom03.xml:3 <reference.entry.id>`\</id>
    <created>\ :ref:`2004-04-19T07:45:00Z <reference.entry.created>`\</created>
    <issued>\ :ref:`2004-04-20T00:23:47Z <reference.entry.published>`\</issued>
    <modified>\ :ref:`2004-04-20T11:56:34Z <reference.entry.updated>`\</modified>
    <author>
    <name>\ :ref:`Mark Pilgrim <reference.entry.author_detail.name>`\</name>
    <url>\ :ref:`http://diveintomark.org/ <reference.entry.author_detail.href>`\</url>
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
    <summary type=":ref:`text/plain <reference.entry.summary_detail.type>`" mode="escaped">
    :ref:`Watch out for nasty tricks <reference.entry.summary>`
    </summary>
    <content type=":ref:`application/xhtml+xml <reference.entry.content.type>`" mode="xml"
    xml:base=":ref:`http://example.org/entry/3 <reference.entry.content.base>`"
    xml:lang=":ref:`en-US <reference.entry.content.language>`">
    :ref:`\<div xmlns="http://www.w3.org/1999/xhtml">Watch out for \<span style="background-image: url(javascript:window.location='http://example.org/')"> nasty tricks\</span>\</div> <reference.entry.content.value>`
    </content>
    </entry>
    </feed>
