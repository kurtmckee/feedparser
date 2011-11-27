.. _advanced.sanitization:

Sanitization
============

Most feeds embed :abbr:`HTML (HyperText Markup Language)` markup within feed
elements.  Some feeds even embed other types of markup, such as :abbr:`SVG
(Scalable Vector Graphics)` or :abbr:`MathML (Mathematical Markup Language)`.
Since many feed aggregators use a web browser (or browser component) to display
content, :program:`Universal Feed Parser` sanitizes embedded markup to remove
things that could pose security risks.

These elements are sanitized by default:

* :ref:`reference.entry.content`
* :ref:`reference.entry.summary`
* :ref:`reference.entry.title`
* :ref:`reference.feed.info`
* :ref:`reference.feed.rights`
* :ref:`reference.feed.subtitle`
* :ref:`reference.feed.title`


.. note::

    If the content is declared to be (or is determined to be)
    :mimetype:`text/plain`, it will not be sanitized. This is to avoid data loss.
    It is recommended that you check the content type in e.g.
    :py:attr:`entries[i].summary_detail.type`. If it is :mimetype:`text/plain` then
    it has not been sanitized (and you should perform HTML escaping before
    rendering the content).


.. _advanced.sanitization.html:

:abbr:`HTML (HyperText Markup Language)` Sanitization
-----------------------------------------------------

The following :abbr:`HTML (HyperText Markup Language)` elements are allowed by
default (all others are stripped):

.. hlist::
   :columns: 3

   * a
   * abbr
   * acronym
   * address
   * area
   * article
   * aside
   * audio
   * b
   * big
   * blockquote
   * br
   * button
   * canvas
   * caption
   * center
   * cite
   * code
   * col
   * colgroup
   * command
   * datagrid
   * datalist
   * dd
   * del
   * details
   * dfn
   * dialog
   * dir
   * div
   * dl
   * dt
   * em
   * event-source
   * fieldset
   * figure
   * font
   * footer
   * form
   * h1
   * h2
   * h3
   * h4
   * h5
   * h6
   * header
   * hr
   * i
   * img
   * input
   * ins
   * kbd
   * keygen
   * label
   * legend
   * li
   * m
   * map
   * menu
   * meter
   * multicol
   * nav
   * nextid
   * noscript
   * ol
   * optgroup
   * option
   * output
   * p
   * pre
   * progress
   * q
   * s
   * samp
   * section
   * select
   * small
   * sound
   * source
   * spacer
   * span
   * strike
   * strong
   * sub
   * sup
   * table
   * tbody
   * td
   * textarea
   * tfoot
   * th
   * thead
   * time
   * tr
   * tt
   * u
   * ul
   * var
   * video


The following :abbr:`HTML (HyperText Markup Language)` attributes are allowed
by default (all others are stripped):

.. hlist::
   :columns: 3

   * abbr
   * accept
   * accept-charset
   * accesskey
   * action
   * align
   * alt
   * autocomplete
   * autofocus
   * autoplay
   * axis
   * background
   * balance
   * bgcolor
   * bgproperties
   * border
   * bordercolor
   * bordercolordark
   * bordercolorlight
   * bottompadding
   * cellpadding
   * cellspacing
   * ch
   * challenge
   * char
   * charoff
   * charset
   * checked
   * choff
   * cite
   * class
   * clear
   * color
   * cols
   * colspan
   * compact
   * contenteditable
   * coords
   * data
   * datafld
   * datapagesize
   * datasrc
   * datetime
   * default
   * delay
   * dir
   * disabled
   * draggable
   * dynsrc
   * enctype
   * end
   * face
   * for
   * form
   * frame
   * galleryimg
   * gutter
   * headers
   * height
   * hidden
   * hidefocus
   * high
   * href
   * hreflang
   * hspace
   * icon
   * id
   * inputmode
   * ismap
   * keytype
   * label
   * lang
   * leftspacing
   * list
   * longdesc
   * loop
   * loopcount
   * loopend
   * loopstart
   * low
   * lowsrc
   * max
   * maxlength
   * media
   * method
   * min
   * multiple
   * name
   * nohref
   * noshade
   * nowrap
   * open
   * optimum
   * pattern
   * ping
   * point-size
   * pqg
   * prompt
   * radiogroup
   * readonly
   * rel
   * repeat-max
   * repeat-min
   * replace
   * required
   * rev
   * rightspacing
   * rows
   * rowspan
   * rules
   * scope
   * selected
   * shape
   * size
   * span
   * src
   * start
   * step
   * summary
   * suppress
   * tabindex
   * target
   * template
   * title
   * toppadding
   * type
   * unselectable
   * urn
   * usemap
   * valign
   * value
   * variable
   * volume
   * vrml
   * vspace
   * width
   * wrap
   * xml:lang


.. _advanced.sanitization.svg:

:abbr:`SVG (Scalable Vector Graphics)` Sanitization
---------------------------------------------------

The following SVG elements are allowed by default (all others are stripped):

.. hlist::
   :columns: 3

   * a
   * animate
   * animateColor
   * animateMotion
   * animateTransform
   * circle
   * defs
   * desc
   * ellipse
   * font-face
   * font-face-name
   * font-face-src
   * foreignObject
   * g
   * glyph
   * hkern
   * line
   * linearGradient
   * marker
   * metadata
   * missing-glyph
   * mpath
   * path
   * polygon
   * polyline
   * radialGradient
   * rect
   * set
   * stop
   * svg
   * switch
   * text
   * title
   * tspan
   * use


The following :abbr:`SVG (Scalable Vector Graphics)` attributes are allowed by
default (all others are stripped):

.. hlist::
   :columns: 3

   * accent-height
   * accumulate
   * additive
   * alphabetic
   * arabic-form
   * ascent
   * attributeName
   * attributeType
   * baseProfile
   * bbox
   * begin
   * by
   * calcMode
   * cap-height
   * class
   * color
   * color-rendering
   * content
   * cx
   * cy
   * d
   * descent
   * display
   * dur
   * dx
   * dy
   * end
   * fill
   * fill-opacity
   * fill-rule
   * font-family
   * font-size
   * font-stretch
   * font-style
   * font-variant
   * font-weight
   * from
   * fx
   * fy
   * g1
   * g2
   * glyph-name
   * gradientUnits
   * hanging
   * height
   * horiz-adv-x
   * horiz-origin-x
   * id
   * ideographic
   * k
   * keyPoints
   * keySplines
   * keyTimes
   * lang
   * marker-end
   * marker-mid
   * marker-start
   * markerHeight
   * markerUnits
   * markerWidth
   * mathematical
   * max
   * min
   * name
   * offset
   * opacity
   * orient
   * origin
   * overline-position
   * overline-thickness
   * panose-1
   * path
   * pathLength
   * points
   * preserveAspectRatio
   * r
   * refX
   * refY
   * repeatCount
   * repeatDur
   * requiredExtensions
   * requiredFeatures
   * restart
   * rotate
   * rx
   * ry
   * slope
   * stemh
   * stemv
   * stop-color
   * stop-opacity
   * strikethrough-position
   * strikethrough-thickness
   * stroke
   * stroke-dasharray
   * stroke-dashoffset
   * stroke-linecap
   * stroke-linejoin
   * stroke-miterlimit
   * stroke-opacity
   * stroke-width
   * systemLanguage
   * target
   * text-anchor
   * to
   * transform
   * type
   * u1
   * u2
   * underline-position
   * underline-thickness
   * unicode
   * unicode-range
   * units-per-em
   * values
   * version
   * viewBox
   * visibility
   * width
   * widths
   * x
   * x-height
   * x1
   * x2
   * xlink:actuate
   * xlink:arcrole
   * xlink:href
   * xlink:role
   * xlink:show
   * xlink:title
   * xlink:type
   * xml:base
   * xml:lang
   * xml:space
   * xmlns
   * xmlns:xlink
   * y
   * y1
   * y2
   * zoomAndPan


.. _advanced.sanitization.mathml:

:abbr:`MathML (Mathematical Markup Language)` Sanitization
----------------------------------------------------------

The following :abbr:`MathML (Mathematical Markup Language)` elements are
allowed by default (all others are stripped):

.. hlist::
   :columns: 3

   * annotation
   * annotation-xml
   * maction
   * math
   * merror
   * mfenced
   * mfrac
   * mi
   * mmultiscripts
   * mn
   * mo
   * mover
   * mpadded
   * mphantom
   * mprescripts
   * mroot
   * mrow
   * mspace
   * msqrt
   * mstyle
   * msub
   * msubsup
   * msup
   * mtable
   * mtd
   * mtext
   * mtr
   * munder
   * munderover
   * none
   * semantics


The following :abbr:`MathML (Mathematical Markup Language)` attributes are
allowed by default (all others are stripped):

.. hlist::
   :columns: 3

   * actiontype
   * align
   * close
   * columnalign
   * columnlines
   * columnspacing
   * columnspan
   * depth
   * display
   * displaystyle
   * encoding
   * equalcolumns
   * equalrows
   * fence
   * fontstyle
   * fontweight
   * frame
   * height
   * linethickness
   * lspace
   * mathbackground
   * mathcolor
   * mathvariant
   * maxsize
   * minsize
   * open
   * other
   * rowalign
   * rowlines
   * rowspacing
   * rowspan
   * rspace
   * scriptlevel
   * selection
   * separator
   * separators
   * stretchy
   * width
   * xlink:href
   * xlink:show
   * xlink:type
   * xmlns
   * xmlns:xlink


.. _advanced.sanitization.css:

:abbr:`CSS (Cascading Style Sheets)` Sanitization
-------------------------------------------------

The following :abbr:`CSS (Cascading Style Sheets)` properties are allowed by
default in style attributes (all others are stripped):

.. hlist::
   :columns: 3

   * azimuth
   * background-color
   * border-bottom-color
   * border-collapse
   * border-color
   * border-left-color
   * border-right-color
   * border-top-color
   * clear
   * color
   * cursor
   * direction
   * display
   * elevation
   * float
   * font
   * font-family
   * font-size
   * font-style
   * font-variant
   * font-weight
   * height
   * letter-spacing
   * line-height
   * overflow
   * pause
   * pause-after
   * pause-before
   * pitch
   * pitch-range
   * richness
   * speak
   * speak-header
   * speak-numeral
   * speak-punctuation
   * speech-rate
   * stress
   * text-align
   * text-decoration
   * text-indent
   * unicode-bidi
   * vertical-align
   * voice-family
   * volume
   * white-space
   * width


.. note::

    Not all possible CSS values are allowed for these properties.  The
    allowable values are restricted by a whitelist and a regular expression that
    allows color values and lengths.  :abbr:`URI (Uniform Resource Identifier)`\s
    are not allowed, to prevent `platypus attacks <http://diveintomark.org/archives/2003/06/12/how_to_consume_rss_safely>`_.
    See the _HTMLSanitizer class for more details.


Whitelist, Don't Blacklist
--------------------------

I am often asked why :program:`Universal Feed Parser` is so hard-assed about
:abbr:`HTML (HyperText Markup Language)` and :abbr:`CSS (Cascading Style
Sheets)` sanitizing.  To illustrate the problem, here is an incomplete list of
potentially dangerous :abbr:`HTML (HyperText Markup Language)` tags and
attributes:

* script, which can contain malicious script
* applet, embed, and object, which can automatically download and execute malicious code
* meta, which can contain malicious redirects
* onload, onunload, and all other on* attributes, which can contain malicious script
* style, link, and the style attribute, which can contain malicious script

*style?* Yes, style. :abbr:`CSS (Cascading Style Sheets)` definitions can contain executable code.


Embedding Javascript in :abbr:`CSS (Cascading Style Sheets)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This sample is taken from `http://feedparser.org/docs/examples/rss20.xml <http://feedparser.org/docs/examples/rss20.xml>`_:

.. sourcecode:: html


    <description>Watch out for
    &lt;span style="background: url(javascript:window.location='http://example.org/')"&gt;
    nasty tricks&lt;/span&gt;</description>


This sample is more advanced, and does not contain the keyword javascript: that
many naive :abbr:`HTML (HyperText Markup Language)` sanitizers scan for:

.. sourcecode:: html

    <description>Watch out for
    &lt;span style="any: expression(window.location='http://example.org/')"&gt;
    nasty tricks&lt;/span&gt;</description>


Internet Explorer for Windows will execute the Javascript in both of these examples.

Now consider that in :abbr:`HTML (HyperText Markup Language)`, attribute values may be entity-encoded in several different ways.


Embedding encoded Javascript in :abbr:`CSS (Cascading Style Sheets)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To a browser, this:

.. sourcecode:: html

    <span style="any: expression(window.location='http://example.org/')">


is the same as this (without the line breaks):

.. sourcecode:: html

    <span style="&#97;&#110;&#121;&#58;&#32;&#101;&#120;&#112;&#114;&#101;
    &#115;&#115;&#105;&#111;&#110;&#40;&#119;&#105;&#110;&#100;&#111;&#119;
    &#46;&#108;&#111;&#99;&#97;&#116;&#105;&#111;&#110;&#61;&#39;&#104;
    &#116;&#116;&#112;&#58;&#47;&#47;&#101;&#120;&#97;&#109;&#112;&#108;
    &#101;&#46;&#111;&#114;&#103;&#47;&#39;&#41;">


which is the same as this (without the line breaks):

.. sourcecode:: html

    <span style="&#x61;&#x6e;&#x79;&#x3a;&#x20;&#x65;&#x78;&#x70;&#x72;
    &#x65;&#x73;&#x73;&#x69;&#x6f;&#x6e;&#x28;&#x77;&#x69;&#x6e;
    &#x64;&#x6f;&#x77;&#x2e;&#x6c;&#x6f;&#x63;&#x61;&#x74;&#x69;
    &#x6f;&#x6e;&#x3d;&#x27;&#x68;&#x74;&#x74;&#x70;&#x3a;&#x2f;
    &#x2f;&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;&#x65;&#x2e;&#x6f;
    &#x72;&#x67;&#x2f;&#x27;&#x29;">


And so on, plus several other variations, plus every combination of every
variation.

The more I investigate, the more cases I find where Internet Explorer for
Windows will treat seemingly innocuous markup as code and blithely execute it.
This is why :program:`Universal Feed Parser` uses a whitelist and not a
blacklist. I am reasonably confident that none of the elements or attributes on
the whitelist are security risks. I am not at all confident about elements or
attributes that I have not explicitly investigated. And I have no confidence at
all in my ability to detect strings within attribute values that Internet
Explorer for Windows will treat as executable code.

.. seealso::

    `How to consume RSS safely <http://diveintomark.org/archives/2003/06/12/how_to_consume_rss_safely>`_
        Explains the platypus attack.
