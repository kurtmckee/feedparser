from htmlentitydefs import name2codepoint
import re

from .sgml import *

_cp1252 = {
    128: unichr(8364), # euro sign
    130: unichr(8218), # single low-9 quotation mark
    131: unichr( 402), # latin small letter f with hook
    132: unichr(8222), # double low-9 quotation mark
    133: unichr(8230), # horizontal ellipsis
    134: unichr(8224), # dagger
    135: unichr(8225), # double dagger
    136: unichr( 710), # modifier letter circumflex accent
    137: unichr(8240), # per mille sign
    138: unichr( 352), # latin capital letter s with caron
    139: unichr(8249), # single left-pointing angle quotation mark
    140: unichr( 338), # latin capital ligature oe
    142: unichr( 381), # latin capital letter z with caron
    145: unichr(8216), # left single quotation mark
    146: unichr(8217), # right single quotation mark
    147: unichr(8220), # left double quotation mark
    148: unichr(8221), # right double quotation mark
    149: unichr(8226), # bullet
    150: unichr(8211), # en dash
    151: unichr(8212), # em dash
    152: unichr( 732), # small tilde
    153: unichr(8482), # trade mark sign
    154: unichr( 353), # latin small letter s with caron
    155: unichr(8250), # single right-pointing angle quotation mark
    156: unichr( 339), # latin small ligature oe
    158: unichr( 382), # latin small letter z with caron
    159: unichr( 376), # latin capital letter y with diaeresis
}

class _BaseHTMLProcessor(sgmllib.SGMLParser):
    special = re.compile('''[<>'"]''')
    bare_ampersand = re.compile("&(?!#\d+;|#x[0-9a-fA-F]+;|\w+;)")
    elements_no_end_tag = set([
      'area', 'base', 'basefont', 'br', 'col', 'command', 'embed', 'frame',
      'hr', 'img', 'input', 'isindex', 'keygen', 'link', 'meta', 'param',
      'source', 'track', 'wbr'
    ])

    def __init__(self, encoding, _type):
        self.encoding = encoding
        self._type = _type
        sgmllib.SGMLParser.__init__(self)

    def reset(self):
        self.pieces = []
        sgmllib.SGMLParser.reset(self)

    def _shorttag_replace(self, match):
        tag = match.group(1)
        if tag in self.elements_no_end_tag:
            return '<' + tag + ' />'
        else:
            return '<' + tag + '></' + tag + '>'

    # By declaring these methods and overriding their compiled code
    # with the code from sgmllib, the original code will execute in
    # feedparser's scope instead of sgmllib's. This means that the
    # `tagfind` and `charref` regular expressions will be found as
    # they're declared above, not as they're declared in sgmllib.
    def goahead(self, i):
        pass
    goahead.func_code = sgmllib.SGMLParser.goahead.func_code

    def __parse_starttag(self, i):
        pass
    __parse_starttag.func_code = sgmllib.SGMLParser.parse_starttag.func_code

    def parse_starttag(self,i):
        j = self.__parse_starttag(i)
        if self._type == 'application/xhtml+xml':
            if j>2 and self.rawdata[j-2:j]=='/>':
                self.unknown_endtag(self.lasttag)
        return j

    def feed(self, data):
        data = re.compile(r'<!((?!DOCTYPE|--|\[))', re.IGNORECASE).sub(r'&lt;!\1', data)
        data = re.sub(r'<([^<>\s]+?)\s*/>', self._shorttag_replace, data)
        data = data.replace('&#39;', "'")
        data = data.replace('&#34;', '"')
        try:
            bytes
            if bytes is str:
                raise NameError
            self.encoding = self.encoding + u'_INVALID_PYTHON_3'
        except NameError:
            if self.encoding and isinstance(data, unicode):
                data = data.encode(self.encoding)
        sgmllib.SGMLParser.feed(self, data)
        sgmllib.SGMLParser.close(self)

    def normalize_attrs(self, attrs):
        if not attrs:
            return attrs
        # utility method to be called by descendants
        attrs = dict([(k.lower(), v) for k, v in attrs]).items()
        attrs = [(k, k in ('rel', 'type') and v.lower() or v) for k, v in attrs]
        attrs.sort()
        return attrs

    def unknown_starttag(self, tag, attrs):
        # called for each start tag
        # attrs is a list of (attr, value) tuples
        # e.g. for <pre class='screen'>, tag='pre', attrs=[('class', 'screen')]
        uattrs = []
        strattrs=''
        if attrs:
            for key, value in attrs:
                value=value.replace('>','&gt;').replace('<','&lt;').replace('"','&quot;')
                value = self.bare_ampersand.sub("&amp;", value)
                # thanks to Kevin Marks for this breathtaking hack to deal with (valid) high-bit attribute values in UTF-8 feeds
                if not isinstance(value, unicode):
                    value = value.decode(self.encoding, 'ignore')
                try:
                    # Currently, in Python 3 the key is already a str, and cannot be decoded again
                    uattrs.append((unicode(key, self.encoding), value))
                except TypeError:
                    uattrs.append((key, value))
            strattrs = u''.join([u' %s="%s"' % (key, value) for key, value in uattrs])
            if self.encoding:
                try:
                    strattrs = strattrs.encode(self.encoding)
                except (UnicodeEncodeError, LookupError):
                    pass
        if tag in self.elements_no_end_tag:
            self.pieces.append('<%s%s />' % (tag, strattrs))
        else:
            self.pieces.append('<%s%s>' % (tag, strattrs))

    def unknown_endtag(self, tag):
        # called for each end tag, e.g. for </pre>, tag will be 'pre'
        # Reconstruct the original end tag.
        if tag not in self.elements_no_end_tag:
            self.pieces.append("</%s>" % tag)

    def handle_charref(self, ref):
        # called for each character reference, e.g. for '&#160;', ref will be '160'
        # Reconstruct the original character reference.
        ref = ref.lower()
        if ref.startswith('x'):
            value = int(ref[1:], 16)
        else:
            value = int(ref)

        if value in _cp1252:
            self.pieces.append('&#%s;' % hex(ord(_cp1252[value]))[1:])
        else:
            self.pieces.append('&#%s;' % ref)

    def handle_entityref(self, ref):
        # called for each entity reference, e.g. for '&copy;', ref will be 'copy'
        # Reconstruct the original entity reference.
        if ref in name2codepoint or ref == 'apos':
            self.pieces.append('&%s;' % ref)
        else:
            self.pieces.append('&amp;%s' % ref)

    def handle_data(self, text):
        # called for each block of plain text, i.e. outside of any tag and
        # not containing any character or entity references
        # Store the original text verbatim.
        self.pieces.append(text)

    def handle_comment(self, text):
        # called for each HTML comment, e.g. <!-- insert Javascript code here -->
        # Reconstruct the original comment.
        self.pieces.append('<!--%s-->' % text)

    def handle_pi(self, text):
        # called for each processing instruction, e.g. <?instruction>
        # Reconstruct original processing instruction.
        self.pieces.append('<?%s>' % text)

    def handle_decl(self, text):
        # called for the DOCTYPE, if present, e.g.
        # <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        #     "http://www.w3.org/TR/html4/loose.dtd">
        # Reconstruct original DOCTYPE
        self.pieces.append('<!%s>' % text)

    _new_declname_match = re.compile(r'[a-zA-Z][-_.a-zA-Z0-9:]*\s*').match
    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return None, -1
        m = self._new_declname_match(rawdata, i)
        if m:
            s = m.group()
            name = s.strip()
            if (i + len(s)) == n:
                return None, -1  # end of buffer
            return name.lower(), m.end()
        else:
            self.handle_data(rawdata)
#            self.updatepos(declstartpos, i)
            return None, -1

    def convert_charref(self, name):
        return '&#%s;' % name

    def convert_entityref(self, name):
        return '&%s;' % name

    def output(self):
        '''Return processed HTML as a single string'''
        return ''.join([str(p) for p in self.pieces])

    def parse_declaration(self, i):
        try:
            return sgmllib.SGMLParser.parse_declaration(self, i)
        except sgmllib.SGMLParseError:
            # escape the doctype declaration and continue parsing
            self.handle_data('&lt;')
            return i+1
