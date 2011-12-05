.. _annotated.rss20:

:abbr:`RSS (Rich Site Summary)` 2.0
===================================

This is a sample :abbr:`RSS (Rich Site Summary)` 2.0 feed, annotated with links
that show how each value can be accessed once the feed is parsed.

.. caution::

    Even though many of these elements are required according to the specification,
    real-world feeds may be missing any element. If an element is not present in
    the feed, it will not be present in the parsed results. You should not rely on
    any particular element being present.

.. rubric:: Annotated :abbr:`RSS (Rich Site Summary)` 2.0 feed

.. container:: pre

    <?xml version="1.0" encoding=":ref:`utf-8 <reference.encoding>`"?>
    <rss version=":ref:`2.0 <reference.version>`">
    <channel>
    <title>\ :ref:`Sample Feed <reference.feed.title>`\</title>
    <description>\ :ref:`For documentation &lt;em&gt;only&lt;/em&gt; <reference.feed.subtitle>`\</description>
    <link>\ :ref:`http://example.org/ <reference.feed.link>`\</link>
    <language>\ :ref:`en <reference.feed.language>`\</language>
    <copyright>\ :ref:`Copyright 2004, Mark Pilgrim <reference.feed.rights>`\</copyright>
    <managingEditor>\ :ref:`editor@example.org <reference.feed.author>`\</managingEditor>
    <webMaster>\ :ref:`webmaster@example.org <reference.feed.publisher>`\</webMaster>
    <pubDate>\ :ref:`Sat, 07 Sep 2002 0:00:01 GMT <reference.feed.published>`\</pubDate>
    <category>\ :ref:`Examples <reference.feed.tags.term>`\</category>
    <generator>\ :ref:`Sample Toolkit <reference.feed.generator>`\</generator>
    <docs>\ :ref:`http://feedvalidator.org/docs/rss2.html <reference.feed.docs>`\</docs>
    <cloud domain=":ref:`rpc.example.com <reference.feed.cloud.domain>`"
    port=":ref:`80 <reference.feed.cloud.port>`"
    path=":ref:`/RPC2 <reference.feed.cloud.path>`"
    registerProcedure=":ref:`pingMe <reference.feed.cloud.registerProcedure>`"
    protocol=":ref:`soap <reference.feed.cloud.protocol>`"/>
    <ttl>\ :ref:`60 <reference.feed.ttl>`\</ttl>
    <image>
    <url>\ :ref:`http://example.org/banner.png <reference.feed.image.href>`\</url>
    <title>\ :ref:`Example banner <reference.feed.image.title>`\</title>
    <link>\ :ref:`http://example.org/ <reference.feed.image.link>`\</link>
    <width>\ :ref:`80 <reference.feed.image.width>`\</width>
    <height>\ :ref:`15 <reference.feed.image.height>`\</height>
    </image>
    <textInput>
    <title>\ :ref:`Search <reference.feed.textinput.title>`\</title>
    <description>\ :ref:`Search this site: <reference.feed.textinput.description>`\</description>
    <name>\ :ref:`q <reference.feed.textinput.name>`\</name>
    <link>\ :ref:`http://example.org/mt/mt-search.cgi <reference.feed.textinput.link>`\</link>
    </textInput>
    <item>
    <title>\ :ref:`First item title <reference.entry.title>`\</title>
    <link>\ :ref:`http://example.org/item/1 <reference.entry.link>`\</link>
    <description>\ :ref:`Watch out for
    &lt;span style="background: url(javascript:window.location='http://example.org/')"&gt;
    nasty tricks&lt;/span&gt; <reference.entry.summary>`
    </description>
    <author>\ :ref:`mark@example.org <reference.entry.author>`\</author>
    <category>\ :ref:`Miscellaneous <reference.entry.tags.term>`\</category>
    <comments>\ :ref:`http://example.org/comments/1 <reference.entry.comments>`\</comments>
    <enclosure url=":ref:`http://example.org/audio/demo.mp3 <reference.entry.enclosures.href>`" length=":ref:`1069871 <reference.entry.enclosures.length>`" type=":ref:`audio/mpeg <reference.entry.enclosures.type>`"/>
    <guid>\ :ref:`http://example.org/guid/1 <reference.entry.id>`\</guid>
    <pubDate>\ :ref:`Thu, 05 Sep 2002 0:00:01 GMT <reference.entry.published>`\</pubDate>
    </item>
    </channel>
    </rss>
