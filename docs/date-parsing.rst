.. _advanced.date:

Date Parsing
============

Different feed types and versions use wildly different date formats.
:program:`Universal Feed Parser` will attempt to auto-detect the date format
used in any date element, and parse it into a standard :program:`Python`
9-tuple, as documented in `the Python time module <http://docs.python.org/lib/module-time.html>`_.

The following elements are parsed as dates:

- :ref:`reference.feed.updated` is parsed into :ref:`reference.feed.updated_parsed`.

- :ref:`reference.entry.published` is parsed into :ref:`reference.entry.published_parsed`.

- :ref:`reference.entry.updated` is parsed into :ref:`reference.entry.updated_parsed`.

- :ref:`reference.entry.created` is parsed into :ref:`reference.entry.created_parsed`.

- :ref:`reference.entry.expired` is parsed into :ref:`reference.entry.expired_parsed`.


History of Date Formats
-----------------------


Here is a brief history of feed date formats:

- :abbr:`CDF (Channel Definition Format)` states that all date values must
  conform to ISO 8601:1988.  ISO 8601:1988 is not a freely
  available specification, but a brief (non-normative) description of the date
  formats it describes is available here: `ISO 8601:1988 Date/Time Representations <http://hydracen.com/dx/iso8601.htm>`_.

- :abbr:`RSS (Rich Site Summary)` 0.90 has no date elements.

- Netscape :abbr:`RSS (Rich Site Summary)` 0.91 does not specify a date format,
  but examples within the specification show :abbr:`RFC (Request For Comments)`
  822-style dates with 4-digit years.

- Userland :abbr:`RSS (Rich Site Summary)` 0.91 states, "All date-times in
  :abbr:`RSS (Rich Site Summary)` conform to the Date and Time Specification of
  :abbr:`RFC (Request For Comments)` 822." `RFC 822 <http://www.ietf.org/rfc/rfc822.txt>`_
  mandates 2-digit years; it does not allow 4-digit years.

- :abbr:`RSS (Rich Site Summary)` 1.0 states that all date elements must
  conform to `W3CDTF <http://www.w3.org/TR/NOTE-datetime>`_,
  which is a profile of ISO 8601:1988.

- :abbr:`RSS (Rich Site Summary)` 2.0 states, "All date-times in :abbr:`RSS (Rich Site Summary)` conform to the Date and Time Specification of RFC 822, with the exception that the year may be expressed with two characters or four characters (four preferred)."

- Atom 0.3 states that all date elements must conform to
  `W3CDTF <http://www.w3.org/TR/NOTE-datetime>`_.

- Atom 1.0 states that all date elements "MUST conform to the date-time
  production in `RFC 3339 <http://www.ietf.org/rfc/rfc3339.txt>`_.
  In addition, an uppercase T character MUST be used to separate date and time,
  and an uppercase Z character MUST be present in the absence of a numeric time
  zone offset."


Recognized Date Formats
-----------------------

Here is a representative list of the formats that :program:`Universal Feed
Parser` can recognize in any date element:


Recognized Date Formats


============================================ ================================= =====================================
Description                                  Example                           Parsed Value                         
============================================ ================================= =====================================
valid RFC 822 (2-digit year)                 Thu, 01 Jan 04 19:48:21 GMT       (2004, 1, 1, 19, 48, 21, 3, 1, 0)    
valid RFC 822 (4-digit year)                 Thu, 01 Jan 2004 19:48:21 GMT     (2004, 1, 1, 19, 48, 21, 3, 1, 0)    
invalid RFC 822 (no time)                    01 Jan 2004                       (2004, 1, 1, 0, 0, 0, 3, 1, 0)       
invalid RFC 822 (no seconds)                 01 Jan 2004 00:00 GMT             (2004, 1, 1, 0, 0, 0, 3, 1, 0)       
valid W3CDTF (numeric timezone)              2003-12-31T10:14:55-08:00         (2003, 12, 31, 18, 14, 55, 2, 365, 0)
valid W3CDTF (UTC timezone)                  2003-12-31T10:14:55Z              (2003, 12, 31, 10, 14, 55, 2, 365, 0)
valid W3CDTF (yyyy)                          2003                              (2003, 1, 1, 0, 0, 0, 2, 1, 0)       
valid W3CDTF (yyyy-mm)                       2003-12                           (2003, 12, 1, 0, 0, 0, 0, 335, 0)    
valid W3CDTF (yyyy-mm-dd)                    2003-12-31                        (2003, 12, 31, 0, 0, 0, 2, 365, 0)   
valid ISO 8601 (yyyymmdd)                    20031231                          (2003, 12, 31, 0, 0, 0, 2, 365, 0)   
valid ISO 8601 (-yy-mm)                      -03-12                            (2003, 12, 1, 0, 0, 0, 0, 335, 0)    
valid ISO 8601 (-yymm)                       -0312                             (2003, 12, 1, 0, 0, 0, 0, 335, 0)    
valid ISO 8601 (-yy-mm-dd)                   -03-12-31                         (2003, 12, 31, 0, 0, 0, 2, 365, 0)   
valid ISO 8601 (yymmdd)                      031231                            (2003, 12, 31, 0, 0, 0, 2, 365, 0)   
valid ISO 8601 (yyyy-o)                      2003-335                          (2003, 12, 1, 0, 0, 0, 0, 335, 0)    
valid ISO 8601 (yyo)                         03335                             (2003, 12, 1, 0, 0, 0, 0, 335, 0)    
valid asctime                                Sun Jan  4 16:29:06 PST 2004      (2004, 1, 5, 0, 29, 6, 0, 5, 0)      
bogus RFC 822 (invalid day/month)            Thu, 31 Jun 2004 19:48:21 GMT     (2004, 7, 1, 19, 48, 21, 3, 183, 0)  
bogus RFC 822 (invalid month)                Mon, 26 January 2004 16:31:00 EST (2004, 1, 26, 21, 31, 0, 0, 26, 0)   
bogus RFC 822 (invalid timezone)             Mon, 26 Jan 2004 16:31:00 ET      (2004, 1, 26, 21, 31, 0, 0, 26, 0)   
bogus W3CDTF (invalid hour)                  2003-12-31T25:14:55Z              (2004, 1, 1, 1, 14, 55, 3, 1, 0)     
bogus W3CDTF (invalid minute)                2003-12-31T10:61:55Z              (2003, 12, 31, 11, 1, 55, 2, 365, 0) 
bogus W3CDTF (invalid second)                2003-12-31T10:14:61Z              (2003, 12, 31, 10, 15, 1, 2, 365, 0) 
bogus (MSSQL)                                2004-07-08 23:56:58.0             (2004, 7, 8, 14, 56, 58, 3, 190, 0)  
bogus (MSSQL-ish, without fractional second) 2004-07-08 23:56:58               (2004, 7, 8, 14, 56, 58, 3, 190, 0)  
bogus (Korean)                               2004-05-25 오 11:23:17            (2004, 5, 25, 14, 23, 17, 1, 146, 0) 
bogus (Greek)                                Κυρ, 11 Ιούλ 2004 12:00:00 EST    (2004, 7, 11, 17, 0, 0, 6, 193, 0)   
bogus (Hungarian)                            július-13T9:15-05:00              (2004, 7, 13, 14, 15, 0, 1, 195, 0)  
============================================ ================================= =====================================


:program:`Universal Feed Parser` recognizes all character-based timezone
abbreviations defined in :abbr:`RFC (Request For Comments)` 822.  In addition,
:program:`Universal Feed Parser` recognizes the following invalid timezones:


- ``AT`` is treated as ``AST``

- ``ET`` is treated as ``EST``

- ``CT`` is treated as ``CST``

- ``MT`` is treated as ``MST``

- ``PT`` is treated as ``PST``



Supporting Additional Date Formats
----------------------------------

:program:`Universal Feed Parser` supports many different date formats, but
there are probably many more in the wild that are still unsupported.  If you
find other date formats, you can support them by registering them with
``registerDateHandler``.  It takes a single argument, a callback function.  The
callback function should take a single argument, a string, and return a single
value, a 9-tuple :program:`Python` date in UTC.


Registering a third-party date handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    import feedparser
    import re

    _my_date_pattern = re.compile(
        r'(\d{,2})/(\d{,2})/(\d{4}) (\d{,2}):(\d{2}):(\d{2})')

    def myDateHandler(aDateString):
        """parse a UTC date in MM/DD/YYYY HH:MM:SS format"""
        month, day, year, hour, minute, second = \
            _my_date_pattern.search(aDateString).groups()
        return (int(year), int(month), int(day), \
            int(hour), int(minute), int(second), 0, 0, 0)

    feedparser.registerDateHandler(myDateHandler)
    d = feedparser.parse(...)



Your newly-registered date handler will be tried before all the other date
handlers built into :program:`Universal Feed Parser`.  (More specifically, all
date handlers are tried in "last in, first out" order; i.e. the last handler to
be registered is the first one tried, and so on in reverse order of
registration.)


If your date handler returns ``None``, or anything other than a
:program:`Python` 9-tuple date, or raises an exception of any kind, the error
will be silently ignored and the other registered date handlers will be tried
in order.  If no date handlers succeed, then the date is not parsed, and the
\*_parsed value will not be present in the results dictionary.  The original
date string will still be available in the appropriate element in the results
dictionary.


.. tip::

   If you write a new date handler, you are encouraged (but not required) to
   `submit a patch <http://sourceforge.net/projects/feedparser/>`_ so it can be
   integrated into the next version of :program:`Universal Feed Parser`.
