from __future__ import absolute_import, unicode_literals

try:
    import rfc822
except ImportError:
    from email import _parseaddr as rfc822

import re
import time

def _parse_date_perforce(aDateString):
    """parse a date in yyyy/mm/dd hh:mm:ss TTT format"""
    # Fri, 2006/09/15 08:19:53 EDT
    _my_date_pattern = re.compile( \
        r'(\w{,3}), (\d{,4})/(\d{,2})/(\d{2}) (\d{,2}):(\d{2}):(\d{2}) (\w{,3})')

    m = _my_date_pattern.search(aDateString)
    if m is None:
        return None
    dow, year, month, day, hour, minute, second, tz = m.groups()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    dateString = "%s, %s %s %s %s:%s:%s %s" % (dow, day, months[int(month) - 1], year, hour, minute, second, tz)
    tm = rfc822.parsedate_tz(dateString)
    if tm:
        return time.gmtime(rfc822.mktime_tz(tm))
