from __future__ import absolute_import, unicode_literals
import dateutil.parser

def _parse_date_dateutil(dateString):
    date = dateutil.parser.parse(dateString, default=None)
    if date:
        return date.timetuple()
    return None
