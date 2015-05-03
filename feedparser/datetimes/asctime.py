from __future__ import absolute_import, unicode_literals

from .rfc822 import _parse_date_rfc822

_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
           'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
def _parse_date_asctime(dt):
    """Parse asctime-style dates.

    Converts asctime to RFC822-compatible dates and uses the RFC822 parser
    to do the actual parsing.

    Supported formats (format is standardized to the first one listed):

    * {weekday name} {month name} dd hh:mm:ss {+-tz} yyyy
    * {weekday name} {month name} dd hh:mm:ss yyyy
    """

    parts = dt.split()

    # Insert a GMT timezone, if needed.
    if len(parts) == 5:
        parts.insert(4, '+0000')

    # Exit if there are not six parts.
    if len(parts) != 6:
        return None

    # Reassemble the parts in an RFC822-compatible order and parse them.
    return _parse_date_rfc822(' '.join([
        parts[0], parts[2], parts[1], parts[5], parts[3], parts[4],
    ]))
