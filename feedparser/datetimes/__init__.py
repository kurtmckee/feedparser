from __future__ import absolute_import

from .asctime import _parse_date_asctime
from .greek import _parse_date_greek
from .hungarian import _parse_date_hungarian
from .iso8601 import _parse_date_iso8601
from .korean import _parse_date_onblog, _parse_date_nate
from .perforce import _parse_date_perforce
from .rfc822 import _parse_date_rfc822
from .w3dtf import _parse_date_w3dtf

_date_handlers = []
def registerDateHandler(func):
    '''Register a date handler function (takes string, returns 9-tuple date in GMT)'''
    _date_handlers.insert(0, func)

def _parse_date(dateString):
    '''Parses a variety of date formats into a 9-tuple in GMT'''
    if not dateString:
        return None
    for handler in _date_handlers:
        try:
            date9tuple = handler(dateString)
        except (KeyError, OverflowError, ValueError):
            continue
        if not date9tuple:
            continue
        if len(date9tuple) != 9:
            continue
        return date9tuple
    return None

registerDateHandler(_parse_date_onblog)
registerDateHandler(_parse_date_nate)
registerDateHandler(_parse_date_greek)
registerDateHandler(_parse_date_hungarian)
registerDateHandler(_parse_date_perforce)
registerDateHandler(_parse_date_asctime)
registerDateHandler(_parse_date_iso8601)
registerDateHandler(_parse_date_rfc822)
registerDateHandler(_parse_date_w3dtf)
