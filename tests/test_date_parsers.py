import pytest

from feedparser.datetimes import (
    _parse_date,
    _parse_date_asctime,
    _parse_date_greek,
    _parse_date_hungarian,
    _parse_date_iso8601,
    _parse_date_nate,
    _parse_date_onblog,
    _parse_date_perforce,
    _parse_date_rfc822,
    _parse_date_w3dtf,
)


def test_none():
    assert _parse_date(None) is None


def _check_date(fn, dt, expected_value):
    try:
        parsed_value = fn(dt)
    except (OverflowError, ValueError):
        parsed_value = None
    assert parsed_value == expected_value


def test_year_10000_date():
    # On some systems this date string will trigger an OverflowError.
    # On Jython and x64 systems, however, it's interpreted just fine.
    try:
        date = _parse_date_rfc822("Sun, 31 Dec 9999 23:59:59 -9999")
    except OverflowError:
        date = None
    assert date in (None, (10000, 1, 5, 4, 38, 59, 2, 5, 0))


@pytest.mark.parametrize(
    "parse_date, input_value, expected_value",
    (
        # _parse_date_greek
        (_parse_date_greek, "", None),  # empty string
        (
            _parse_date_greek,
            "\u039a\u03c5\u03c1, 11 \u0399\u03bf\u03cd\u03bb 2004 12:00:00 EST",
            (2004, 7, 11, 17, 0, 0, 6, 193, 0),
        ),
        #
        # _parse_date_hungarian
        (_parse_date_hungarian, "", None),  # empty string
        (
            _parse_date_hungarian,
            "2004-j\u00falius-13T9:15-05:00",
            (2004, 7, 13, 14, 15, 0, 1, 195, 0),
        ),
        #
        # _parse_date_iso8601
        (_parse_date_iso8601, "", None),  # empty string
        (
            _parse_date_iso8601,
            "-0312",
            (2003, 12, 1, 0, 0, 0, 0, 335, 0),
        ),  # 2-digit year/month only variant
        (
            _parse_date_iso8601,
            "031231",
            (2003, 12, 31, 0, 0, 0, 2, 365, 0),
        ),  # 2-digit year/month/day only, no hyphens
        (
            _parse_date_iso8601,
            "03-12-31",
            (2003, 12, 31, 0, 0, 0, 2, 365, 0),
        ),  # 2-digit year/month/day only
        (
            _parse_date_iso8601,
            "-03-12",
            (2003, 12, 1, 0, 0, 0, 0, 335, 0),
        ),  # 2-digit year/month only
        (
            _parse_date_iso8601,
            "03335",
            (2003, 12, 1, 0, 0, 0, 0, 335, 0),
        ),  # 2-digit year/ordinal, no hyphens
        (
            _parse_date_iso8601,
            "2003-12-31T10:14:55.1234Z",
            (2003, 12, 31, 10, 14, 55, 2, 365, 0),
        ),  # fractional seconds
        # Special case for Google's extra zero in the month
        (
            _parse_date_iso8601,
            "2003-012-31T10:14:55+00:00",
            (2003, 12, 31, 10, 14, 55, 2, 365, 0),
        ),
        #
        # _parse_date_nate
        (_parse_date_nate, "", None),  # empty string
        (
            _parse_date_nate,
            "2004-05-25 \uc624\ud6c4 11:23:17",
            (2004, 5, 25, 14, 23, 17, 1, 146, 0),
        ),
        #
        # _parse_date_onblog
        (_parse_date_onblog, "", None),  # empty string
        (
            _parse_date_onblog,
            "2004\ub144 05\uc6d4 28\uc77c  01:31:15",
            (2004, 5, 27, 16, 31, 15, 3, 148, 0),
        ),
        #
        # _parse_date_perforce
        (_parse_date_perforce, "", None),  # empty string
        (
            _parse_date_perforce,
            "Fri, 2006/09/15 08:19:53 EDT",
            (2006, 9, 15, 12, 19, 53, 4, 258, 0),
        ),
        #
        # _parse_date_rfc822
        (_parse_date_rfc822, "", None),  # empty string
        (
            _parse_date_rfc822,
            "Thu, 30 Apr 2015 08:57:00 MET",
            (2015, 4, 30, 7, 57, 0, 3, 120, 0),
        ),
        (
            _parse_date_rfc822,
            "Thu, 30 Apr 2015 08:57:00 MEST",
            (2015, 4, 30, 6, 57, 0, 3, 120, 0),
        ),
        (
            _parse_date_rfc822,
            "Thu, 01 Jan 0100 00:00:01 +0100",
            (99, 12, 31, 23, 0, 1, 3, 365, 0),
        ),  # ancient date
        (
            _parse_date_rfc822,
            "Thu, 01 Jan 04 19:48:21 GMT",
            (2004, 1, 1, 19, 48, 21, 3, 1, 0),
        ),  # 2-digit year
        (
            _parse_date_rfc822,
            "Thu, 01 Jan 2004 19:48:21 GMT",
            (2004, 1, 1, 19, 48, 21, 3, 1, 0),
        ),  # 4-digit year
        (
            _parse_date_rfc822,
            "Thu,  5 Apr 2012 10:00:00 GMT",
            (2012, 4, 5, 10, 0, 0, 3, 96, 0),
        ),  # 1-digit day
        (
            _parse_date_rfc822,
            "Wed, 19 Aug 2009 18:28:00 Etc/GMT",
            (2009, 8, 19, 18, 28, 0, 2, 231, 0),
        ),  # etc/gmt timezone
        (
            _parse_date_rfc822,
            "Wed, 19 Feb 2012 22:40:00 GMT-01:01",
            (2012, 2, 19, 23, 41, 0, 6, 50, 0),
        ),  # gmt+hh:mm timezone
        (
            _parse_date_rfc822,
            "Wed, 19 Feb 2012 22:40:00 -01:01",
            (2012, 2, 19, 23, 41, 0, 6, 50, 0),
        ),  # +hh:mm timezone
        (
            _parse_date_rfc822,
            "Mon, 13 Feb, 2012 06:28:00 UTC",
            (2012, 2, 13, 6, 28, 0, 0, 44, 0),
        ),  # extraneous comma
        (
            _parse_date_rfc822,
            "Thu, 01 Jan 2004 00:00 GMT",
            (2004, 1, 1, 0, 0, 0, 3, 1, 0),
        ),  # no seconds
        (
            _parse_date_rfc822,
            "Thu, 01 Jan 2004",
            (2004, 1, 1, 0, 0, 0, 3, 1, 0),
        ),  # no time
        # Additional tests to handle Disney's long month names and invalid timezones
        (
            _parse_date_rfc822,
            "Mon, 26 January 2004 16:31:00 AT",
            (2004, 1, 26, 20, 31, 0, 0, 26, 0),
        ),
        (
            _parse_date_rfc822,
            "Mon, 26 January 2004 16:31:00 ET",
            (2004, 1, 26, 21, 31, 0, 0, 26, 0),
        ),
        (
            _parse_date_rfc822,
            "Mon, 26 January 2004 16:31:00 CT",
            (2004, 1, 26, 22, 31, 0, 0, 26, 0),
        ),
        (
            _parse_date_rfc822,
            "Mon, 26 January 2004 16:31:00 MT",
            (2004, 1, 26, 23, 31, 0, 0, 26, 0),
        ),
        (
            _parse_date_rfc822,
            "Mon, 26 January 2004 16:31:00 PT",
            (2004, 1, 27, 0, 31, 0, 1, 27, 0),
        ),
        # Swapped month and day
        (
            _parse_date_rfc822,
            "Thu Aug 30 2012 17:26:16 +0200",
            (2012, 8, 30, 15, 26, 16, 3, 243, 0),
        ),
        (_parse_date_rfc822, "Sun, 16 Dec 2012 1:2:3:4 GMT", None),  # invalid time
        (_parse_date_rfc822, "Sun, 16 zzz 2012 11:47:32 GMT", None),  # invalid month
        (
            _parse_date_rfc822,
            "Sun, Dec x 2012 11:47:32 GMT",
            None,
        ),  # invalid day (swapped day/month)
        (_parse_date_rfc822, "Sun, 16 Dec zz 11:47:32 GMT", None),  # invalid year
        (
            _parse_date_rfc822,
            "Sun, 16 Dec 2012 11:47:32 +zz:00",
            None,
        ),  # invalid timezone hour
        (
            _parse_date_rfc822,
            "Sun, 16 Dec 2012 11:47:32 +00:zz",
            None,
        ),  # invalid timezone minute
        (_parse_date_rfc822, "Sun, 99 Jun 2009 12:00:00 GMT", None),  # out-of-range day
        #
        # _parse_date_asctime
        (
            _parse_date_asctime,
            "Sun Jan  4 16:29:06 2004",
            (2004, 1, 4, 16, 29, 6, 6, 4, 0),
        ),
        (
            _parse_date_asctime,
            "Sun Jul 15 01:16:00 +0000 2012",
            (2012, 7, 15, 1, 16, 0, 6, 197, 0),
        ),
        #
        # _parse_date_w3dtf
        (_parse_date_w3dtf, "", None),  # empty string
        (
            _parse_date_w3dtf,
            "2003-12-31T10:14:55Z",
            (2003, 12, 31, 10, 14, 55, 2, 365, 0),
        ),  # UTC
        (
            _parse_date_w3dtf,
            "2003-12-31T10:14:55-08:00",
            (2003, 12, 31, 18, 14, 55, 2, 365, 0),
        ),  # San Francisco timezone
        (
            _parse_date_w3dtf,
            "2003-12-31T18:14:55+08:00",
            (2003, 12, 31, 10, 14, 55, 2, 365, 0),
        ),  # Tokyo timezone
        (
            _parse_date_w3dtf,
            "2007-04-23T23:25:47.538+10:00",
            (2007, 4, 23, 13, 25, 47, 0, 113, 0),
        ),  # fractional seconds
        (
            _parse_date_w3dtf,
            "2003-12-31",
            (2003, 12, 31, 0, 0, 0, 2, 365, 0),
        ),  # year/month/day only
        (
            _parse_date_w3dtf,
            "2003-12",
            (2003, 12, 1, 0, 0, 0, 0, 335, 0),
        ),  # year/month only
        (_parse_date_w3dtf, "2003", (2003, 1, 1, 0, 0, 0, 2, 1, 0)),  # year only
        # Special cases for rollovers in leap years
        (
            _parse_date_w3dtf,
            "2004-02-28T18:14:55-08:00",
            (2004, 2, 29, 2, 14, 55, 6, 60, 0),
        ),  # feb 28 in leap year
        (
            _parse_date_w3dtf,
            "2003-02-28T18:14:55-08:00",
            (2003, 3, 1, 2, 14, 55, 5, 60, 0),
        ),  # feb 28 in non-leap year
        (
            _parse_date_w3dtf,
            "2000-02-28T18:14:55-08:00",
            (2000, 2, 29, 2, 14, 55, 1, 60, 0),
        ),  # feb 28 in leap year on century divisible by 400
        # Out-of-range times
        (_parse_date_w3dtf, "9999-12-31T23:59:59-99:99", None),  # Date is out-of-range
        (_parse_date_w3dtf, "2003-12-31T25:14:55Z", None),  # invalid (25 hours)
        (_parse_date_w3dtf, "2003-12-31T10:61:55Z", None),  # invalid (61 minutes)
        (_parse_date_w3dtf, "2003-12-31T10:14:61Z", None),  # invalid (61 seconds)
        # Invalid formats
        (_parse_date_w3dtf, "22013", None),  # Year is too long
        (_parse_date_w3dtf, "013", None),  # Year is too short
        (_parse_date_w3dtf, "2013-01-27-01", None),  # Date has to many parts
        (_parse_date_w3dtf, "2013-01-28T11:30:00-06:00Textra", None),  # Too many 't's
        # Non-integer values
        (_parse_date_w3dtf, "2013-xx-27", None),  # Date
        (_parse_date_w3dtf, "2013-01-28T09:xx:00Z", None),  # Time
        (_parse_date_w3dtf, "2013-01-28T09:00:00+00:xx", None),  # Timezone
        # MSSQL-style dates
        (
            _parse_date_w3dtf,
            "2004-07-08 23:56:58 -00:20",
            (2004, 7, 9, 0, 16, 58, 4, 191, 0),
        ),  # with timezone
        (
            _parse_date_w3dtf,
            "2004-07-08 23:56:58",
            (2004, 7, 8, 23, 56, 58, 3, 190, 0),
        ),  # without timezone
        (
            _parse_date_w3dtf,
            "2004-07-08 23:56:58.0",
            (2004, 7, 8, 23, 56, 58, 3, 190, 0),
        ),  # with fractional second
    ),
)
def test_date_parser(parse_date, input_value, expected_value):
    try:
        parsed_value = parse_date(input_value)
    except (OverflowError, ValueError):
        parsed_value = None
    assert parsed_value == expected_value
