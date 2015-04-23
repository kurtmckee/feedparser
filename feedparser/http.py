from __future__ import absolute_import

import datetime
import re
import urllib2
import urlparse

try:
    import base64, binascii
except ImportError:
    base64 = binascii = None
else:
    # Python 3.1 deprecated decodestring in favor of decodebytes
    _base64decode = getattr(base64, 'decodebytes', base64.decodestring)

try:
    import gzip
except ImportError:
    gzip = None
try:
    import zlib
except ImportError:
    zlib = None

from .datetimes import _parse_date

class _FeedURLHandler(urllib2.HTTPDigestAuthHandler, urllib2.HTTPRedirectHandler, urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        # The default implementation just raises HTTPError.
        # Forget that.
        fp.status = code
        return fp

    def http_error_301(self, req, fp, code, msg, hdrs):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp,
                                                            code, msg, hdrs)
        result.status = code
        result.newurl = result.geturl()
        return result
    # The default implementations in urllib2.HTTPRedirectHandler
    # are identical, so hardcoding a http_error_301 call above
    # won't affect anything
    http_error_300 = http_error_301
    http_error_302 = http_error_301
    http_error_303 = http_error_301
    http_error_307 = http_error_301

    def http_error_401(self, req, fp, code, msg, headers):
        # Check if
        # - server requires digest auth, AND
        # - we tried (unsuccessfully) with basic auth, AND
        # If all conditions hold, parse authentication information
        # out of the Authorization header we sent the first time
        # (for the username and password) and the WWW-Authenticate
        # header the server sent back (for the realm) and retry
        # the request with the appropriate digest auth headers instead.
        # This evil genius hack has been brought to you by Aaron Swartz.
        host = urlparse.urlparse(req.get_full_url())[1]
        if base64 is None or 'Authorization' not in req.headers \
                          or 'WWW-Authenticate' not in headers:
            return self.http_error_default(req, fp, code, msg, headers)
        auth = _base64decode(req.headers['Authorization'].split(' ')[1])
        user, passw = auth.split(':')
        realm = re.findall('realm="([^"]*)"', headers['WWW-Authenticate'])[0]
        self.add_password(realm, host, user, passw)
        retry = self.http_error_auth_reqed('www-authenticate', host, req, headers)
        self.reset_retry_count()
        return retry

def _build_urllib2_request(url, agent, accept_header, etag, modified, referrer, auth, request_headers):
    request = urllib2.Request(url)
    request.add_header('User-Agent', agent)
    if etag:
        request.add_header('If-None-Match', etag)
    if isinstance(modified, basestring):
        modified = _parse_date(modified)
    elif isinstance(modified, datetime.datetime):
        modified = modified.utctimetuple()
    if modified:
        # format into an RFC 1123-compliant timestamp. We can't use
        # time.strftime() since the %a and %b directives can be affected
        # by the current locale, but RFC 2616 states that dates must be
        # in English.
        short_weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        request.add_header('If-Modified-Since', '%s, %02d %s %04d %02d:%02d:%02d GMT' % (short_weekdays[modified[6]], modified[2], months[modified[1] - 1], modified[0], modified[3], modified[4], modified[5]))
    if referrer:
        request.add_header('Referer', referrer)
    if gzip and zlib:
        request.add_header('Accept-encoding', 'gzip, deflate')
    elif gzip:
        request.add_header('Accept-encoding', 'gzip')
    elif zlib:
        request.add_header('Accept-encoding', 'deflate')
    else:
        request.add_header('Accept-encoding', '')
    if auth:
        request.add_header('Authorization', 'Basic %s' % auth)
    if accept_header:
        request.add_header('Accept', accept_header)
    # use this for whatever -- cookies, special headers, etc
    # [('Cookie','Something'),('x-special-header','Another Value')]
    for header_name, header_value in request_headers.items():
        request.add_header(header_name, header_value)
    request.add_header('A-IM', 'feed') # RFC 3229 support
    return request
