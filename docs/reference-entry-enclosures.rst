.. _reference.entry.enclosures:

:py:attr:`entries[i].enclosures`
================================

A list of links to external files associated with this entry.

Some aggregators automatically download enclosures (although this technique has
`known problems <http://gonze.com/weblog/story/5-17-4>`_).  Some aggregators
render each enclosure as a link.  Most aggregators ignore them.

The :abbr:`RSS (Rich Site Summary)` specification states that there can be at
most one enclosure per item.  However, because some feeds break this rule,
:program:`Universal Feed Parser` captures all of them and makes them available
as a list.

.. rubric:: Comes from

- /atom10:feed/atom10:entry/atom10:link[@rel="enclosure"]
- /rss/channel/item/enclosure
- additionally, :ref:`certain links within embedded markup <advanced.microformats.relenclosure>`


.. _reference.entry.enclosures.href:

:py:attr:`entries[i].enclosures[j].href`
----------------------------------------

The :abbr:`URL (Uniform Resource Locator)` of the linked file.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.entry.enclosures.length:

:py:attr:`entries[i].enclosures[j].length`
------------------------------------------

The length of the linked file.


.. _reference.entry.enclosures.type:

:py:attr:`entries[i].enclosures[j].type`
----------------------------------------

The content type of the linked file.
