from __future__ import absolute_import, unicode_literals

import re

from .html import _BaseHTMLProcessor
from .sgml import _SGML_AVAILABLE
from .urls import _makeSafeAbsoluteURI

class _HTMLSanitizer(_BaseHTMLProcessor):
    acceptable_elements = set(['a', 'abbr', 'acronym', 'address', 'area',
        'article', 'aside', 'audio', 'b', 'big', 'blockquote', 'br', 'button',
        'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup',
        'command', 'datagrid', 'datalist', 'dd', 'del', 'details', 'dfn',
        'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'event-source', 'fieldset',
        'figcaption', 'figure', 'footer', 'font', 'form', 'header', 'h1',
        'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'input', 'ins',
        'keygen', 'kbd', 'label', 'legend', 'li', 'm', 'map', 'menu', 'meter',
        'multicol', 'nav', 'nextid', 'ol', 'output', 'optgroup', 'option',
        'p', 'pre', 'progress', 'q', 's', 'samp', 'section', 'select',
        'small', 'sound', 'source', 'spacer', 'span', 'strike', 'strong',
        'sub', 'sup', 'table', 'tbody', 'td', 'textarea', 'time', 'tfoot',
        'th', 'thead', 'tr', 'tt', 'u', 'ul', 'var', 'video', 'noscript'])

    acceptable_attributes = set(['abbr', 'accept', 'accept-charset', 'accesskey',
      'action', 'align', 'alt', 'autocomplete', 'autofocus', 'axis',
      'background', 'balance', 'bgcolor', 'bgproperties', 'border',
      'bordercolor', 'bordercolordark', 'bordercolorlight', 'bottompadding',
      'cellpadding', 'cellspacing', 'ch', 'challenge', 'char', 'charoff',
      'choff', 'charset', 'checked', 'cite', 'class', 'clear', 'color', 'cols',
      'colspan', 'compact', 'contenteditable', 'controls', 'coords', 'data',
      'datafld', 'datapagesize', 'datasrc', 'datetime', 'default', 'delay',
      'dir', 'disabled', 'draggable', 'dynsrc', 'enctype', 'end', 'face', 'for',
      'form', 'frame', 'galleryimg', 'gutter', 'headers', 'height', 'hidefocus',
      'hidden', 'high', 'href', 'hreflang', 'hspace', 'icon', 'id', 'inputmode',
      'ismap', 'keytype', 'label', 'leftspacing', 'lang', 'list', 'longdesc',
      'loop', 'loopcount', 'loopend', 'loopstart', 'low', 'lowsrc', 'max',
      'maxlength', 'media', 'method', 'min', 'multiple', 'name', 'nohref',
      'noshade', 'nowrap', 'open', 'optimum', 'pattern', 'ping', 'point-size',
      'poster', 'pqg', 'preload', 'prompt', 'radiogroup', 'readonly', 'rel',
      'repeat-max', 'repeat-min', 'replace', 'required', 'rev', 'rightspacing',
      'rows', 'rowspan', 'rules', 'scope', 'selected', 'shape', 'size', 'span',
      'src', 'start', 'step', 'summary', 'suppress', 'tabindex', 'target',
      'template', 'title', 'toppadding', 'type', 'unselectable', 'usemap',
      'urn', 'valign', 'value', 'variable', 'volume', 'vspace', 'vrml',
      'width', 'wrap', 'xml:lang'])

    unacceptable_elements_with_end_tag = set(['script', 'applet', 'style'])

    acceptable_css_properties = set(['azimuth', 'background-color',
      'border-bottom-color', 'border-collapse', 'border-color',
      'border-left-color', 'border-right-color', 'border-top-color', 'clear',
      'color', 'cursor', 'direction', 'display', 'elevation', 'float', 'font',
      'font-family', 'font-size', 'font-style', 'font-variant', 'font-weight',
      'height', 'letter-spacing', 'line-height', 'overflow', 'pause',
      'pause-after', 'pause-before', 'pitch', 'pitch-range', 'richness',
      'speak', 'speak-header', 'speak-numeral', 'speak-punctuation',
      'speech-rate', 'stress', 'text-align', 'text-decoration', 'text-indent',
      'unicode-bidi', 'vertical-align', 'voice-family', 'volume',
      'white-space', 'width'])

    # survey of common keywords found in feeds
    acceptable_css_keywords = set(['auto', 'aqua', 'black', 'block', 'blue',
      'bold', 'both', 'bottom', 'brown', 'center', 'collapse', 'dashed',
      'dotted', 'fuchsia', 'gray', 'green', '!important', 'italic', 'left',
      'lime', 'maroon', 'medium', 'none', 'navy', 'normal', 'nowrap', 'olive',
      'pointer', 'purple', 'red', 'right', 'solid', 'silver', 'teal', 'top',
      'transparent', 'underline', 'white', 'yellow'])

    valid_css_values = re.compile('^(#[0-9a-f]+|rgb\(\d+%?,\d*%?,?\d*%?\)?|' +
      '\d{0,2}\.?\d{0,2}(cm|em|ex|in|mm|pc|pt|px|%|,|\))?)$')

    mathml_elements = set([
        'annotation',
        'annotation-xml',
        'maction',
        'maligngroup',
        'malignmark',
        'math',
        'menclose',
        'merror',
        'mfenced',
        'mfrac',
        'mglyph',
        'mi',
        'mlabeledtr',
        'mlongdiv',
        'mmultiscripts',
        'mn',
        'mo',
        'mover',
        'mpadded',
        'mphantom',
        'mprescripts',
        'mroot',
        'mrow',
        'ms',
        'mscarries',
        'mscarry',
        'msgroup',
        'msline',
        'mspace',
        'msqrt',
        'msrow',
        'mstack',
        'mstyle',
        'msub',
        'msubsup',
        'msup',
        'mtable',
        'mtd',
        'mtext',
        'mtr',
        'munder',
        'munderover',
        'none',
        'semantics',
    ])

    mathml_attributes = set([
        'accent',
        'accentunder',
        'actiontype',
        'align',
        'alignmentscope',
        'altimg',
        'altimg-height',
        'altimg-valign',
        'altimg-width',
        'alttext',
        'bevelled',
        'charalign',
        'close',
        'columnalign',
        'columnlines',
        'columnspacing',
        'columnspan',
        'columnwidth',
        'crossout',
        'decimalpoint',
        'denomalign',
        'depth',
        'dir',
        'display',
        'displaystyle',
        'edge',
        'encoding',
        'equalcolumns',
        'equalrows',
        'fence',
        'fontstyle',
        'fontweight',
        'form',
        'frame',
        'framespacing',
        'groupalign',
        'height',
        'href',
        'id',
        'indentalign',
        'indentalignfirst',
        'indentalignlast',
        'indentshift',
        'indentshiftfirst',
        'indentshiftlast',
        'indenttarget',
        'infixlinebreakstyle',
        'largeop',
        'length',
        'linebreak',
        'linebreakmultchar',
        'linebreakstyle',
        'lineleading',
        'linethickness',
        'location',
        'longdivstyle',
        'lquote',
        'lspace',
        'mathbackground',
        'mathcolor',
        'mathsize',
        'mathvariant',
        'maxsize',
        'minlabelspacing',
        'minsize',
        'movablelimits',
        'notation',
        'numalign',
        'open',
        'other',
        'overflow',
        'position',
        'rowalign',
        'rowlines',
        'rowspacing',
        'rowspan',
        'rquote',
        'rspace',
        'scriptlevel',
        'scriptminsize',
        'scriptsizemultiplier',
        'selection',
        'separator',
        'separators',
        'shift',
        'side',
        'src',
        'stackalign',
        'stretchy',
        'subscriptshift',
        'superscriptshift',
        'symmetric',
        'voffset',
        'width',
        'xlink:href',
        'xlink:show',
        'xlink:type',
        'xmlns',
        'xmlns:xlink',
    ])

    # svgtiny - foreignObject + linearGradient + radialGradient + stop
    svg_elements = set(['a', 'animate', 'animateColor', 'animateMotion',
      'animateTransform', 'circle', 'defs', 'desc', 'ellipse', 'foreignObject',
      'font-face', 'font-face-name', 'font-face-src', 'g', 'glyph', 'hkern',
      'linearGradient', 'line', 'marker', 'metadata', 'missing-glyph', 'mpath',
      'path', 'polygon', 'polyline', 'radialGradient', 'rect', 'set', 'stop',
      'svg', 'switch', 'text', 'title', 'tspan', 'use'])

    # svgtiny + class + opacity + offset + xmlns + xmlns:xlink
    svg_attributes = set(['accent-height', 'accumulate', 'additive', 'alphabetic',
       'arabic-form', 'ascent', 'attributeName', 'attributeType',
       'baseProfile', 'bbox', 'begin', 'by', 'calcMode', 'cap-height',
       'class', 'color', 'color-rendering', 'content', 'cx', 'cy', 'd', 'dx',
       'dy', 'descent', 'display', 'dur', 'end', 'fill', 'fill-opacity',
       'fill-rule', 'font-family', 'font-size', 'font-stretch', 'font-style',
       'font-variant', 'font-weight', 'from', 'fx', 'fy', 'g1', 'g2',
       'glyph-name', 'gradientUnits', 'hanging', 'height', 'horiz-adv-x',
       'horiz-origin-x', 'id', 'ideographic', 'k', 'keyPoints', 'keySplines',
       'keyTimes', 'lang', 'mathematical', 'marker-end', 'marker-mid',
       'marker-start', 'markerHeight', 'markerUnits', 'markerWidth', 'max',
       'min', 'name', 'offset', 'opacity', 'orient', 'origin',
       'overline-position', 'overline-thickness', 'panose-1', 'path',
       'pathLength', 'points', 'preserveAspectRatio', 'r', 'refX', 'refY',
       'repeatCount', 'repeatDur', 'requiredExtensions', 'requiredFeatures',
       'restart', 'rotate', 'rx', 'ry', 'slope', 'stemh', 'stemv',
       'stop-color', 'stop-opacity', 'strikethrough-position',
       'strikethrough-thickness', 'stroke', 'stroke-dasharray',
       'stroke-dashoffset', 'stroke-linecap', 'stroke-linejoin',
       'stroke-miterlimit', 'stroke-opacity', 'stroke-width', 'systemLanguage',
       'target', 'text-anchor', 'to', 'transform', 'type', 'u1', 'u2',
       'underline-position', 'underline-thickness', 'unicode', 'unicode-range',
       'units-per-em', 'values', 'version', 'viewBox', 'visibility', 'width',
       'widths', 'x', 'x-height', 'x1', 'x2', 'xlink:actuate', 'xlink:arcrole',
       'xlink:href', 'xlink:role', 'xlink:show', 'xlink:title', 'xlink:type',
       'xml:base', 'xml:lang', 'xml:space', 'xmlns', 'xmlns:xlink', 'y', 'y1',
       'y2', 'zoomAndPan'])

    svg_attr_map = None
    svg_elem_map = None

    acceptable_svg_properties = set([ 'fill', 'fill-opacity', 'fill-rule',
      'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin',
      'stroke-opacity'])

    def reset(self):
        _BaseHTMLProcessor.reset(self)
        self.unacceptablestack = 0
        self.mathmlOK = 0
        self.svgOK = 0

    def unknown_starttag(self, tag, attrs):
        acceptable_attributes = self.acceptable_attributes
        keymap = {}
        if not tag in self.acceptable_elements or self.svgOK:
            if tag in self.unacceptable_elements_with_end_tag:
                self.unacceptablestack += 1

            # add implicit namespaces to html5 inline svg/mathml
            if self._type.endswith('html'):
                if not dict(attrs).get('xmlns'):
                    if tag=='svg':
                        attrs.append( ('xmlns','http://www.w3.org/2000/svg') )
                    if tag=='math':
                        attrs.append( ('xmlns','http://www.w3.org/1998/Math/MathML') )

            # not otherwise acceptable, perhaps it is MathML or SVG?
            if tag=='math' and ('xmlns','http://www.w3.org/1998/Math/MathML') in attrs:
                self.mathmlOK += 1
            if tag=='svg' and ('xmlns','http://www.w3.org/2000/svg') in attrs:
                self.svgOK += 1

            # chose acceptable attributes based on tag class, else bail
            if  self.mathmlOK and tag in self.mathml_elements:
                acceptable_attributes = self.mathml_attributes
            elif self.svgOK and tag in self.svg_elements:
                # for most vocabularies, lowercasing is a good idea.  Many
                # svg elements, however, are camel case
                if not self.svg_attr_map:
                    lower=[attr.lower() for attr in self.svg_attributes]
                    mix=[a for a in self.svg_attributes if a not in lower]
                    self.svg_attributes = lower
                    self.svg_attr_map = dict([(a.lower(),a) for a in mix])

                    lower=[attr.lower() for attr in self.svg_elements]
                    mix=[a for a in self.svg_elements if a not in lower]
                    self.svg_elements = lower
                    self.svg_elem_map = dict([(a.lower(),a) for a in mix])
                acceptable_attributes = self.svg_attributes
                tag = self.svg_elem_map.get(tag,tag)
                keymap = self.svg_attr_map
            elif not tag in self.acceptable_elements:
                return

        # declare xlink namespace, if needed
        if self.mathmlOK or self.svgOK:
            if any((a for a in attrs if a[0].startswith('xlink:'))):
                if not ('xmlns:xlink','http://www.w3.org/1999/xlink') in attrs:
                    attrs.append(('xmlns:xlink','http://www.w3.org/1999/xlink'))

        clean_attrs = []
        for key, value in self.normalize_attrs(attrs):
            if key in acceptable_attributes:
                key=keymap.get(key,key)
                # make sure the uri uses an acceptable uri scheme
                if key == 'href':
                    value = _makeSafeAbsoluteURI(value)
                clean_attrs.append((key,value))
            elif key=='style':
                clean_value = self.sanitize_style(value)
                if clean_value:
                    clean_attrs.append((key,clean_value))
        _BaseHTMLProcessor.unknown_starttag(self, tag, clean_attrs)

    def unknown_endtag(self, tag):
        if not tag in self.acceptable_elements:
            if tag in self.unacceptable_elements_with_end_tag:
                self.unacceptablestack -= 1
            if self.mathmlOK and tag in self.mathml_elements:
                if tag == 'math' and self.mathmlOK:
                    self.mathmlOK -= 1
            elif self.svgOK and tag in self.svg_elements:
                tag = self.svg_elem_map.get(tag,tag)
                if tag == 'svg' and self.svgOK:
                    self.svgOK -= 1
            else:
                return
        _BaseHTMLProcessor.unknown_endtag(self, tag)

    def handle_pi(self, text):
        pass

    def handle_decl(self, text):
        pass

    def handle_data(self, text):
        if not self.unacceptablestack:
            _BaseHTMLProcessor.handle_data(self, text)

    def sanitize_style(self, style):
        # disallow urls
        style=re.compile('url\s*\(\s*[^\s)]+?\s*\)\s*').sub(' ',style)

        # gauntlet
        if not re.match("""^([:,;#%.\sa-zA-Z0-9!]|\w-\w|'[\s\w]+'|"[\s\w]+"|\([\d,\s]+\))*$""", style):
            return ''
        # This replaced a regexp that used re.match and was prone to pathological back-tracking.
        if re.sub("\s*[-\w]+\s*:\s*[^:;]*;?", '', style).strip():
            return ''

        clean = []
        for prop,value in re.findall("([-\w]+)\s*:\s*([^:;]*)",style):
            if not value:
                continue
            if prop.lower() in self.acceptable_css_properties:
                clean.append(prop + ': ' + value + ';')
            elif prop.split('-')[0].lower() in ['background','border','margin','padding']:
                for keyword in value.split():
                    if not keyword in self.acceptable_css_keywords and \
                        not self.valid_css_values.match(keyword):
                        break
                else:
                    clean.append(prop + ': ' + value + ';')
            elif self.svgOK and prop.lower() in self.acceptable_svg_properties:
                clean.append(prop + ': ' + value + ';')

        return ' '.join(clean)

    def parse_comment(self, i, report=1):
        ret = _BaseHTMLProcessor.parse_comment(self, i, report)
        if ret >= 0:
            return ret
        # if ret == -1, this may be a malicious attempt to circumvent
        # sanitization, or a page-destroying unclosed comment
        match = re.compile(r'--[^>]*>').search(self.rawdata, i+4)
        if match:
            return match.end()
        # unclosed comment; deliberately fail to handle_data()
        return len(self.rawdata)


def _sanitizeHTML(htmlSource, encoding, _type):
    if not _SGML_AVAILABLE:
        return htmlSource
    p = _HTMLSanitizer(encoding, _type)
    htmlSource = htmlSource.replace('<![CDATA[', '&lt;![CDATA[')
    p.feed(htmlSource)
    data = p.output()
    data = data.strip().replace('\r\n', '\n')
    return data

# Match XML entity declarations.
# Example: <!ENTITY copyright "(C)">
RE_ENTITY_PATTERN = re.compile(br'^\s*<!ENTITY([^>]*?)>', re.MULTILINE)

# Match XML DOCTYPE declarations.
# Example: <!DOCTYPE feed [ ]>
RE_DOCTYPE_PATTERN = re.compile(br'^\s*<!DOCTYPE([^>]*?)>', re.MULTILINE)

# Match safe entity declarations.
# This will allow hexadecimal character references through,
# as well as text, but not arbitrary nested entities.
# Example: cubed "&#179;"
# Example: copyright "(C)"
# Forbidden: explode1 "&explode2;&explode2;"
RE_SAFE_ENTITY_PATTERN = re.compile(b'\s+(\w+)\s+"(&#\w+;|[^&"]*)"')

def replace_doctype(data):
    '''Strips and replaces the DOCTYPE, returns (rss_version, stripped_data)

    rss_version may be 'rss091n' or None
    stripped_data is the same XML document with a replaced DOCTYPE
    '''

    # Divide the document into two groups by finding the location
    # of the first element that doesn't begin with '<?' or '<!'.
    start = re.search(b'<\w', data)
    start = start and start.start() or -1
    head, data = data[:start+1], data[start+1:]

    # Save and then remove all of the ENTITY declarations.
    entity_results = RE_ENTITY_PATTERN.findall(head)
    head = RE_ENTITY_PATTERN.sub(b'', head)

    # Find the DOCTYPE declaration and check the feed type.
    doctype_results = RE_DOCTYPE_PATTERN.findall(head)
    doctype = doctype_results and doctype_results[0] or b''
    if b'netscape' in doctype.lower():
        version = 'rss091n'
    else:
        version = None

    # Re-insert the safe ENTITY declarations if a DOCTYPE was found.
    replacement = b''
    if len(doctype_results) == 1 and entity_results:
        match_safe_entities = lambda e: RE_SAFE_ENTITY_PATTERN.match(e)
        safe_entities = [e for e in entity_results if match_safe_entities(e)]
        if safe_entities:
            replacement = b'<!DOCTYPE feed [\n<!ENTITY' \
                        + b'>\n<!ENTITY '.join(safe_entities) \
                        + b'>\n]>'
    data = RE_DOCTYPE_PATTERN.sub(replacement, head) + data

    # Precompute the safe entities for the loose parser.
    safe_entities = dict((k.decode('utf-8'), v.decode('utf-8'))
                      for k, v in RE_SAFE_ENTITY_PATTERN.findall(replacement))
    return version, data, safe_entities
