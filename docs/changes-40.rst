Changes in version 4.0
======================




:program:`Universal Feed Parser` 4.0 was released on December 23, 2005.

- Support for :ref:`annotated.atom10`.

- Support for :program:`iTunes` extensions.

- Support for dc:contributor.

- :program:`Universal Feed Parser` now captures the feed's :ref:`reference.namespaces`.  See :ref:`advanced.namespaces` for details.

- Lots of things have been renamed to match Atom 1.0 terminology.  issued is now :ref:`reference.entry.published`, modified is now :ref:`reference.entry.updated`, and url is now href everywhere.  You can still access these elements with the old names, so you shouldn't need to change any existing code, but don't be surprised if you can't find them during debugging.

- category and categories have been replaced by tags, see :ref:`reference.feed.tags` and :ref:`reference.entry.tags`.  The old names still work.

- mode is gone from all detail and content dictionaries.  It was never terribly useful, since :program:`Universal Feed Parser` unescapes content automatically.

- :ref:`reference.entry.source` is now a dictionary of feed metadata as per section 4.2.11 of RFC 4287.  :program:`Universal Feed Parser` no longer supports the :abbr:`RSS (Rich Site Summary)` 2.0's source element.

- Content in unknown namespaces is no longer discarded (`bug 993305 <http://sourceforge.net/tracker/index.php?func=detail&aid=993305&group_id=112328&atid=661937>`_)

- Lots of other bug fixes.