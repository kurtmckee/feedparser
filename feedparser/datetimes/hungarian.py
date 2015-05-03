from __future__ import absolute_import, unicode_literals

import re

from .w3dtf import _parse_date_w3dtf

# Unicode strings for Hungarian date strings
_hungarian_months = \
  { \
    'janu\u00e1r':   '01',  # e1 in iso-8859-2
    'febru\u00e1ri': '02',  # e1 in iso-8859-2
    'm\u00e1rcius':  '03',  # e1 in iso-8859-2
    '\u00e1prilis':  '04',  # e1 in iso-8859-2
    'm\u00e1ujus':   '05',  # e1 in iso-8859-2
    'j\u00fanius':   '06',  # fa in iso-8859-2
    'j\u00falius':   '07',  # fa in iso-8859-2
    'augusztus':     '08',
    'szeptember':    '09',
    'okt\u00f3ber':  '10',  # f3 in iso-8859-2
    'november':      '11',
    'december':      '12',
  }

_hungarian_date_format_re = \
  re.compile('(\d{4})-([^-]+)-(\d{,2})T(\d{,2}):(\d{2})((\+|-)(\d{,2}:\d{2}))')

def _parse_date_hungarian(dateString):
    '''Parse a string according to a Hungarian 8-bit date format.'''
    m = _hungarian_date_format_re.match(dateString)
    if not m or m.group(2) not in _hungarian_months:
        return None
    month = _hungarian_months[m.group(2)]
    day = m.group(3)
    if len(day) == 1:
        day = '0' + day
    hour = m.group(4)
    if len(hour) == 1:
        hour = '0' + hour
    w3dtfdate = '%(year)s-%(month)s-%(day)sT%(hour)s:%(minute)s%(zonediff)s' % \
                {'year': m.group(1), 'month': month, 'day': day,\
                 'hour': hour, 'minute': m.group(5),\
                 'zonediff': m.group(6)}
    return _parse_date_w3dtf(w3dtfdate)
