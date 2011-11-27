Changes in earlier versions
===========================




:program:`Universal Feed Parser` began as an "ultra-liberal RSS parser" named :file:`rssparser.py`.  It was written as a weapon for battles that no one remembers, to work around problems that no longer exist.

:program:`Ultra-liberal Feed Parser` 2.5.3 was released on August 3, 2003.

- track whether we're inside an image or textInput (TvdV)

- return the character encoding, if specified


:program:`Ultra-liberal Feed Parser` 2.5.2 was released on July 28, 2003.

- entity-decode inline :abbr:`XML (Extensible Markup Language)` properly

- added support for inline <xhtml:body> and <xhtml:div> as used in some :abbr:`RSS (Rich Site Summary)` 2.0 feeds


:program:`Ultra-liberal Feed Parser` 2.5.1 was released on July 26, 2003.

- clear ``opener.addheaders`` so we only send our custom ``User-Agent`` (otherwise :file:`urllib2` sends two, which confuses some servers) (RMK)


:program:`Ultra-liberal Feed Parser` 2.5 was released on July 25, 2003.

- changed to :program:`Python` license (all contributors agree)

- removed unnecessary :file:`>urllib` code -- :file:`urllib2` should always be available anyway

- return actual ``url``, ``status``, and full :abbr:`HTTP (Hypertext Transfer Protocol)` headers (as ``result['url']``, ``result['status']``, and ``result['headers']``) if parsing a remote feed over :abbr:`HTTP (Hypertext Transfer Protocol)`.  This should pass all the `Aggregator client :abbr:`HTTP (Hypertext Transfer Protocol)` tests <http://diveintomark.org/tests/client/http/>`_.

- added the latest namespace-of-the-week for :abbr:`RSS (Rich Site Summary)` 2.0


:program:`Ultra-liberal Feed Parser` 2.4 was released on July 9, 2003.

- added preliminary Pie/Atom/Echo support based on `Sam Ruby's snapshot of July 1 <http://www.intertwingly.net/blog/1506.html>`_

- changed project name


:program:`Ultra-liberal RSS Parser` 2.3.1 was released on June 12, 2003.

- if item has both link and guid, return both as-is


:program:`Ultra-liberal RSS Parser` 2.3 was released on June 11, 2003.

- added ``USER_AGENT`` for default (if caller doesn't specify)

- make sure we send the ``User-Agent`` even if :file:`urllib2` isn't available

- Match any variation of ``backend.userland.com/rss`` namespace


:program:`Ultra-liberal RSS Parser` 2.2 was released on January 27, 2003.

- added attribute support and admin:generatorAgent.  start_admingeneratoragent is an example of how to handle elements with only attributes, no content.


:program:`Ultra-liberal RSS Parser` 2.1 was released on November 14, 2002.

- added gzip support


:program:`Ultra-liberal RSS Parser` 2.0.2 was released on October 21, 2002.

- added the ``inchannel`` to the ``if`` statement, otherwise it's useless.  Fixes the problem JD was addressing by adding it. (JB)


:program:`Ultra-liberal RSS Parser` 2.0.1 was released on October 21, 2002.

- changed ``parse()`` so that if we don't get anything because of ``etag``/``modified``, return the old ``etag``/``modified`` to the caller to indicate why nothing is being returned


:program:`Ultra-liberal RSS Parser` 2.0 was released on October 19, 2002.

- use ``inchannel`` to watch out for image and textinput elements which can also contain title, link, and description elements (JD)

- check for isPermaLink='false' attribute on guid elements (JD)

- replaced ``openAnything`` with ``open_resource`` supporting ``ETag`` and ``If-Modified-Since`` request headers (JD)

- ``parse`` now accepts ``etag``, ``modified``, ``agent``, and ``referrer`` optional arguments (JD)

- modified ``parse`` to return a dictionary instead of a tuple so that any ``etag`` or ``modified`` information can be returned and cached by the caller


:program:`Ultra-liberal RSS Parser` 1.1 was released on September 27, 2002.

- fixed infinite loop on incomplete CDATA sections


:program:`Ultra-liberal RSS Parser` 1.0 was released on September 27, 2002.

- fixed namespace processing on prefixed :abbr:`RSS (Rich Site Summary)` 2.0 elements

- added Simon Fell's namespace test suite


:program:`Ultra-liberal RSS Parser` was first released on August 13, 2002.

`Announcement <http://diveintomark.org/archives/2002/08/13/ultraliberal_rss_parser>`_:

    Aaron Swartz has been looking for an ultra-liberal :abbr:`RSS (Rich Site Summary)` parser. Now that I'm experimenting with a homegrown :abbr:`RSS (Rich Site Summary)`-to-email news aggregator, so am I. You see, most :abbr:`RSS (Rich Site Summary)` feeds suck. Invalid characters, unescaped ampersands (Blogger feeds), invalid entities (Radio feeds), unescaped and invalid HTML (The Register's feed most days). Or just a bastardized mix of :abbr:`RSS (Rich Site Summary)` 0.9x elements with :abbr:`RSS (Rich Site Summary)` 1.0 elements (Movable Type feeds).

    Then there are feeds, like Aaron's feed, which are too bleeding edge. He puts an excerpt in the description element but puts the full text in the content:encoded element (as CDATA). This is valid :abbr:`RSS (Rich Site Summary)` 1.0, but nobody actually uses it (except Aaron), few news aggregators support it, and many parsers choke on it. Other parsers are confused by the new elements (guid) in :abbr:`RSS (Rich Site Summary)` 0.94 (see Dave Winer's feed for an example). And then there's Jon Udell's feed, with the fullitem element that he just sort of made up.

    :file:`rssparser.py`. GPL-licensed. Tested on 5000 active feeds.
