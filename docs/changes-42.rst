Changes in version 4.2
======================

:program:`Universal Feed Parser` 4.2 was released on 2008-03-12.

- Support for :ref:`parsing microformats <advanced.microformats>`, including :ref:`rel=enclosure <advanced.microformats.relenclosure>`, :ref:`rel=tag <advanced.microformats.reltag>`, :ref:`XFN <advanced.microformats.xfn>`, and :ref:`hCard <advanced.microformats.hcard>`.

- Updated the whitelist of :ref:`acceptable HTML elements and attributes <advanced.sanitization.html>` based on the latest draft of the :abbr:`HTML (HyperText Markup Language)` 5 specification.

- Support for :ref:`advanced.sanitization.css`.  (Previous versions of :program:`Universal Feed Parser` simply stripped all inline styles.)  Many thanks to Sam Ruby for implementing this, despite my insistence that it was impossible.

- Support for :ref:`advanced.sanitization.svg`.

- Support for :ref:`advanced.sanitization.mathml`.  Many thanks to Jacques Distler for patiently debugging this feature.

- :abbr:`IRI (International Resource Identifier)` support for every element that can contain a :abbr:`URI (Uniform Resource Identifier)`.

- Ability to :ref:`disable relative URI resolution <advanced.base.disable>`.

- Command-line arguments and alternate serializers, for manipulating :program:`Universal Feed Parser` from shell scripts or other non-Python sources.

- More robust parsing of author email addresses, misencoded win-1252 content, rel=self links, and better detection of HTML content in elements with ambiguous content types.
