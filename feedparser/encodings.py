# Character encoding routines
# Copyright 2010-2023 Kurt McKee <contactme@kurtmckee.org>
# Copyright 2002-2008 Mark Pilgrim
# All rights reserved.
#
# This file is a part of feedparser.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import codecs
import io
import re
import typing

try:
    try:
        import cchardet as chardet  # type: ignore[import]
    except ImportError:
        import chardet  # type: ignore[no-redef]
except ImportError:
    lazy_chardet_encoding = None
else:

    def lazy_chardet_encoding(data):
        return chardet.detect(data)["encoding"] or ""


from .exceptions import (
    CharacterEncodingOverride,
    CharacterEncodingUnknown,
    FeedparserError,
    NonXMLContentType,
)

# Each marker represents some of the characters of the opening XML
# processing instruction ('<?xm') in the specified encoding.
EBCDIC_MARKER = b"\x4C\x6F\xA7\x94"
UTF16BE_MARKER = b"\x00\x3C\x00\x3F"
UTF16LE_MARKER = b"\x3C\x00\x3F\x00"
UTF32BE_MARKER = b"\x00\x00\x00\x3C"
UTF32LE_MARKER = b"\x3C\x00\x00\x00"

ZERO_BYTES = b"\x00\x00"

# Match the opening XML declaration.
# Example: <?xml version="1.0" encoding="utf-8"?>
RE_XML_DECLARATION = re.compile(r"^<\?xml[^>]*?>")

# Capture the value of the XML processing instruction's encoding attribute.
# Example: <?xml version="1.0" encoding="utf-8"?>
RE_XML_PI_ENCODING = re.compile(rb'^<\?.*encoding=[\'"](.*?)[\'"].*\?>')


def parse_content_type(line: str) -> tuple[str, str]:
    """Parse an HTTP Content-Type header.

    The return value will be a tuple of strings:
    the MIME type, and the value of the "charset" (if any).

    This is a custom replacement for Python's cgi.parse_header().
    The cgi module will be removed in Python 3.13.
    """

    chunks = line.split(";")
    if not chunks:
        return "", ""

    mime_type = chunks[0].strip()
    charset_value = ""
    for chunk in chunks[1:]:
        key, _, value = chunk.partition("=")
        if key.strip().lower() == "charset":
            charset_value = value.strip().strip("\"'")

    return mime_type, charset_value


def convert_to_utf8(
    http_headers: dict[str, str], data: bytes, result: dict[str, typing.Any]
) -> bytes:
    """Detect and convert the character encoding to UTF-8."""

    # This is so much trickier than it sounds, it's not even funny.
    # According to RFC 3023 ('XML Media Types'), if the HTTP Content-Type
    # is application/xml, application/*+xml,
    # application/xml-external-parsed-entity, or application/xml-dtd,
    # the encoding given in the charset parameter of the HTTP Content-Type
    # takes precedence over the encoding given in the XML prefix within the
    # document, and defaults to 'utf-8' if neither are specified.  But, if
    # the HTTP Content-Type is text/xml, text/*+xml, or
    # text/xml-external-parsed-entity, the encoding given in the XML prefix
    # within the document is ALWAYS IGNORED and only the encoding given in
    # the charset parameter of the HTTP Content-Type header should be
    # respected, and it defaults to 'us-ascii' if not specified.

    # Furthermore, discussion on the atom-syntax mailing list with the
    # author of RFC 3023 leads me to the conclusion that any document
    # served with a Content-Type of text/* and no charset parameter
    # must be treated as us-ascii.  (We now do this.)  And also that it
    # must always be flagged as non-well-formed.  (We now do this too.)

    # If Content-Type is unspecified (input was local file or non-HTTP source)
    # or unrecognized (server just got it totally wrong), then go by the
    # encoding given in the XML prefix of the document and default to
    # 'iso-8859-1' as per the HTTP specification (RFC 2616).

    # Then, assuming we didn't find a character encoding in the HTTP headers
    # (and the HTTP Content-type allowed us to look in the body), we need
    # to sniff the first few bytes of the XML data and try to determine
    # whether the encoding is ASCII-compatible.  Section F of the XML
    # specification shows the way here:
    # http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info

    # If the sniffed encoding is not ASCII-compatible, we need to make it
    # ASCII compatible so that we can sniff further into the XML declaration
    # to find the encoding attribute, which will tell us the true encoding.

    # Of course, none of this guarantees that we will be able to parse the
    # feed in the declared character encoding (assuming it was declared
    # correctly, which many are not).

    bom_encoding = ""
    xml_encoding = ""

    # Look at the first few bytes of the document to guess what
    # its encoding may be. We only need to decode enough of the
    # document that we can use an ASCII-compatible regular
    # expression to search for an XML encoding declaration.
    # The heuristic follows the XML specification, section F:
    # http://www.w3.org/TR/REC-xml/#sec-guessing-no-ext-info
    # Check for BOMs first.
    if data[:4] == codecs.BOM_UTF32_BE:
        bom_encoding = "utf-32be"
        data = data[4:]
    elif data[:4] == codecs.BOM_UTF32_LE:
        bom_encoding = "utf-32le"
        data = data[4:]
    elif data[:2] == codecs.BOM_UTF16_BE and data[2:4] != ZERO_BYTES:
        bom_encoding = "utf-16be"
        data = data[2:]
    elif data[:2] == codecs.BOM_UTF16_LE and data[2:4] != ZERO_BYTES:
        bom_encoding = "utf-16le"
        data = data[2:]
    elif data[:3] == codecs.BOM_UTF8:
        bom_encoding = "utf-8"
        data = data[3:]
    # Check for the characters '<?xm' in several encodings.
    elif data[:4] == EBCDIC_MARKER:
        bom_encoding = "cp037"
    elif data[:4] == UTF16BE_MARKER:
        bom_encoding = "utf-16be"
    elif data[:4] == UTF16LE_MARKER:
        bom_encoding = "utf-16le"
    elif data[:4] == UTF32BE_MARKER:
        bom_encoding = "utf-32be"
    elif data[:4] == UTF32LE_MARKER:
        bom_encoding = "utf-32le"

    tempdata = data
    try:
        if bom_encoding:
            tempdata = data.decode(bom_encoding).encode("utf-8")
    except UnicodeDecodeError:
        xml_encoding_match = None
    else:
        xml_encoding_match = RE_XML_PI_ENCODING.match(tempdata)

    if xml_encoding_match:
        xml_encoding = xml_encoding_match.groups()[0].decode("utf-8").lower()
        # Normalize the xml_encoding if necessary.
        if bom_encoding and (
            xml_encoding
            in (
                "u16",
                "utf-16",
                "utf16",
                "utf_16",
                "u32",
                "utf-32",
                "utf32",
                "utf_32",
                "iso-10646-ucs-2",
                "iso-10646-ucs-4",
                "csucs4",
                "csunicode",
                "ucs-2",
                "ucs-4",
            )
        ):
            xml_encoding = bom_encoding

    # Find the HTTP Content-Type and, hopefully, a character
    # encoding provided by the server. The Content-Type is used
    # to choose the "correct" encoding among the BOM encoding,
    # XML declaration encoding, and HTTP encoding, following the
    # heuristic defined in RFC 3023.
    http_content_type = http_headers.get("content-type") or ""
    http_content_type, http_encoding = parse_content_type(http_content_type)

    acceptable_content_type = 0
    application_content_types = (
        "application/xml",
        "application/xml-dtd",
        "application/xml-external-parsed-entity",
    )
    text_content_types = ("text/xml", "text/xml-external-parsed-entity")
    json_content_types = ("application/feed+json", "application/json")
    json = False
    if http_content_type in application_content_types or (
        http_content_type.startswith("application/")
        and http_content_type.endswith("+xml")
    ):
        acceptable_content_type = 1
        rfc3023_encoding = http_encoding or xml_encoding or "utf-8"
    elif http_content_type in text_content_types or (
        http_content_type.startswith("text/") and http_content_type.endswith("+xml")
    ):
        acceptable_content_type = 1
        rfc3023_encoding = http_encoding or "us-ascii"
    elif http_content_type in json_content_types or (
        not http_content_type and data and data.lstrip().startswith(b"{")
    ):
        http_content_type = json_content_types[0]
        acceptable_content_type = 1
        json = True
        rfc3023_encoding = http_encoding or "utf-8"  # RFC 7159, 8.1.
    elif http_content_type.startswith("text/"):
        rfc3023_encoding = http_encoding or "us-ascii"
    elif http_headers and "content-type" not in http_headers:
        rfc3023_encoding = xml_encoding or "iso-8859-1"
    else:
        rfc3023_encoding = xml_encoding or "utf-8"
    # gb18030 is a superset of gb2312, so always replace gb2312
    # with gb18030 for greater compatibility.
    if rfc3023_encoding.lower() == "gb2312":
        rfc3023_encoding = "gb18030"
    if xml_encoding.lower() == "gb2312":
        xml_encoding = "gb18030"

    # there are four encodings to keep track of:
    # - http_encoding is the encoding declared in the Content-Type HTTP header
    # - xml_encoding is the encoding declared in the <?xml declaration
    # - bom_encoding is the encoding sniffed from the first 4 bytes of the XML data
    # - rfc3023_encoding is the actual encoding, as per RFC 3023
    #   and a variety of other conflicting specifications
    error: FeedparserError | None = None

    if http_headers and (not acceptable_content_type):
        if "content-type" in http_headers:
            msg = "%s is not an accepted media type" % http_headers["content-type"]
        else:
            msg = "no Content-type specified"
        error = NonXMLContentType(msg)

    # determine character encoding
    known_encoding = False
    tried_encodings = []
    # try: HTTP encoding, declared XML encoding, encoding sniffed from BOM
    for encoding_to_try in (
        rfc3023_encoding,
        xml_encoding,
        bom_encoding,
        lazy_chardet_encoding,
        "utf-8",
        "windows-1252",
        "iso-8859-2",
    ):
        if callable(encoding_to_try):
            proposed_encoding = encoding_to_try(data)
        else:
            proposed_encoding = encoding_to_try
        if not proposed_encoding:
            continue
        if proposed_encoding in tried_encodings:
            continue
        tried_encodings.append(proposed_encoding)
        try:
            text = data.decode(proposed_encoding)
        except (UnicodeDecodeError, LookupError):
            continue

        known_encoding = True
        if not json:
            # Update the encoding in the opening XML processing instruction.
            new_declaration = """<?xml version='1.0' encoding='utf-8'?>"""
            if RE_XML_DECLARATION.search(text):
                text = RE_XML_DECLARATION.sub(new_declaration, text)
            else:
                text = new_declaration + "\n" + text
        data = text.encode("utf-8")
        break

    # if still no luck, give up
    if not known_encoding:
        error = CharacterEncodingUnknown(
            "document encoding unknown, I tried "
            + "%s, %s, utf-8, windows-1252, and iso-8859-2 but nothing worked"
            % (rfc3023_encoding, xml_encoding)
        )
        rfc3023_encoding = ""
    elif proposed_encoding != rfc3023_encoding:
        error = CharacterEncodingOverride(
            "document declared as %s, but parsed as %s"
            % (rfc3023_encoding, proposed_encoding)
        )
        rfc3023_encoding = proposed_encoding

    result["content-type"] = http_content_type  # for selecting the parser
    result["encoding"] = rfc3023_encoding
    if error:
        result["bozo"] = True
        result["bozo_exception"] = error
    return data


# How much to read from a binary file in order to detect encoding.
# In initial tests, 4k was enough for ~160 mostly-English feeds;
# 64k seems like a safe margin.
CONVERT_FILE_PREFIX_LEN = 2**16

# How much to read from a text file, and use as an utf-8 bytes prefix.
# Note that no encoding detection is needed in this case.
CONVERT_FILE_STR_PREFIX_LEN = 2**13

CONVERT_FILE_TEST_CHUNK_LEN = 2**16


def convert_file_to_utf8(
    http_headers, file, result, optimistic_encoding_detection=True
):
    """Like convert_to_utf8(), but for a stream.

    Unlike convert_to_utf8(), do not read the entire file in memory;
    instead, return a text stream that decodes it on the fly.
    This should consume significantly less memory,
    because it avoids (repeatedly) converting the entire file contents
    from bytes to str and back.

    To detect the encoding, only a prefix of the file contents is used.
    In rare cases, the wrong encoding may be detected for this prefix;
    use optimistic_encoding_detection=False to use the entire file contents
    (equivalent to a plain convert_to_utf8() call).

    Args:
        http_headers (dict): The response headers.
        file (IO[bytes] or IO[str]): A read()-able (binary) stream.
        result (dict): The result dictionary.
        optimistic_encoding_detection (bool):
            If true, use only a prefix of the file content to detect encoding.

    Returns:
        StreamFactory: a stream factory, with the detected encoding set, if any

    """
    # Currently, this wraps convert_to_utf8(), because the logic is simply
    # too complicated to ensure it's re-implemented correctly for a stream.
    # That said, it should be possible to change the implementation
    # transparently (not sure it's worth it, though).

    # If file is a text stream, we don't need to detect encoding;
    # we still need a bytes prefix to run functions on for side effects:
    # convert_to_utf8() to sniff / set result['content-type'], and
    # replace_doctype() to extract safe_entities.

    if isinstance(file.read(0), str):
        prefix = file.read(CONVERT_FILE_STR_PREFIX_LEN).encode("utf-8")
        prefix = convert_to_utf8(http_headers, prefix, result)
        result["encoding"] = "utf-8"
        return StreamFactory(prefix, file, "utf-8")

    if optimistic_encoding_detection:
        prefix = convert_file_prefix_to_utf8(http_headers, file, result)
        factory = StreamFactory(prefix, file, result.get("encoding"))

        # Before returning factory, ensure the entire file can be decoded;
        # if it cannot, fall back to convert_to_utf8().
        #
        # Not doing this means feedparser.parse() may raise UnicodeDecodeError
        # instead of setting bozo_exception to CharacterEncodingOverride,
        # breaking the 6.x API.

        try:
            text_file = factory.get_text_file()
        except MissingEncoding:
            return factory
        try:
            # read in chunks to limit memory usage
            while text_file.read(CONVERT_FILE_TEST_CHUNK_LEN):
                pass
        except UnicodeDecodeError:
            # fall back to convert_to_utf8()
            file = factory.get_binary_file()
        else:
            return factory

    # this shouldn't increase memory usage if file is BytesIO,
    # since BytesIO does copy-on-write; https://bugs.python.org/issue22003
    data = convert_to_utf8(http_headers, file.read(), result)

    # note that data *is* the prefix
    return StreamFactory(data, io.BytesIO(b""), result.get("encoding"))


def convert_file_prefix_to_utf8(
    http_headers,
    file: typing.IO[bytes],
    result,
    *,
    prefix_len: int = CONVERT_FILE_PREFIX_LEN,
    read_to_ascii_len: int = 2**8,
) -> bytes:
    """Like convert_to_utf8(), but only use the prefix of a binary file.

    Set result like convert_to_utf8() would.

    Return the updated prefix, as bytes.

    """
    # This is complicated by convert_to_utf8() detecting the wrong encoding
    # if we have only part of the bytes that make a code-point:
    #
    # '😀'.encode('utf-8')      -> utf-8
    # '😀'.encode('utf-8')[:-1] -> windows-1252 + bozo

    prefix = file.read(prefix_len - 1)

    # reading up to after an ASCII byte increases
    # the likelihood of being on a code point boundary
    prefix += read_to_after_ascii_byte(file, read_to_ascii_len)

    # call convert_to_utf8() up to 4 times,
    # to make sure we eventually land on a code point boundary
    candidates = []
    for attempt in range(4):
        byte = file.read(1)

        # we're at the end of the file, and the loop already ran once
        if not byte and attempt != 0:
            break

        prefix += byte

        fake_result: typing.Any = {}
        converted_prefix = convert_to_utf8(http_headers, prefix, fake_result)

        # an encoding was detected successfully, keep it
        if not fake_result.get("bozo"):
            break

        candidates.append((file.tell(), converted_prefix, fake_result))

    # no encoding was detected successfully, pick the "best" one
    else:

        def key(candidate):
            *_, result = candidate

            exc = result.get("bozo_exception")
            exc_score = 0
            if isinstance(exc, NonXMLContentType):
                exc_score = 20
            elif isinstance(exc, CharacterEncodingOverride):
                exc_score = 10

            return (
                exc_score,
                # prefer utf- encodings to anything else
                result.get("encoding").startswith("utf-"),
            )

        candidates.sort(key=key)
        offset, converted_prefix, fake_result = candidates[-1]

        file.seek(offset)

    result.update(fake_result)
    return converted_prefix


def read_to_after_ascii_byte(file: typing.IO[bytes], max_len: int) -> bytes:
    offset = file.tell()
    buffer = b""

    for _ in range(max_len):
        byte = file.read(1)

        # end of file, nothing to do
        if not byte:
            break

        buffer += byte

        # we stop after a ASCII character
        if byte < b"\x80":
            break

    # couldn't find an ASCII character, reset the file to the original offset
    else:
        file.seek(offset)
        return b""

    return buffer


class MissingEncoding(io.UnsupportedOperation):
    pass


class StreamFactory:
    """Decode on the fly a binary stream that *may* have a known encoding.

    If the underlying stream is seekable, it is possible to call
    the get_{text,binary}_file() methods more than once.

    """

    def __init__(self, prefix: bytes, file, encoding=None):
        self.prefix = prefix
        self.file = ResetFileWrapper(file)
        self.encoding = encoding
        self.should_reset = False

    def get_text_file(self, fallback_encoding=None, errors="strict"):
        encoding = self.encoding or fallback_encoding
        if encoding is None:
            raise MissingEncoding("cannot create text stream without encoding")

        if isinstance(self.file.read(0), str):
            file = PrefixFileWrapper(self.prefix.decode(encoding), self.file)
        else:
            file = PrefixFileWrapper(
                self.prefix.decode("utf-8", errors),
                codecs.getreader(encoding)(self.file, errors),
            )

        self.reset()
        return file

    def get_binary_file(self):
        if isinstance(self.file.read(0), str):
            raise io.UnsupportedOperation(
                "underlying stream is text, not binary"
            ) from None

        file = PrefixFileWrapper(self.prefix, self.file)

        self.reset()
        return file

    def get_file(self):
        try:
            return self.get_text_file()
        except MissingEncoding:
            return self.get_binary_file()

    def reset(self):
        if self.should_reset:
            self.file.reset()
        self.should_reset = True


class ResetFileWrapper:
    """Given a seekable file, allow reading its content again
    (from the current position) by calling reset().

    """

    def __init__(self, file):
        self.file = file
        try:
            self.file_initial_offset = file.tell()
        except OSError:
            self.file_initial_offset = None

    def read(self, size=-1):
        return self.file.read(size)

    def reset(self):
        # raises io.UnsupportedOperation if the underlying stream is not seekable
        self.file.seek(self.file_initial_offset)


class PrefixFileWrapper:
    """Stitch a (possibly modified) prefix and a file into a new file object.

    >>> file = io.StringIO('abcdef')
    >>> file.read(2)
    'ab'
    >>> wrapped = PrefixFileWrapper(file.read(2).upper(), file)
    >>> wrapped.read()
    'CDef'

    """

    def __init__(self, prefix, file):
        self.prefix = prefix
        self.file = file
        self.offset = 0

    def read(self, size=-1):
        buffer = self.file.read(0)

        if self.offset < len(self.prefix):
            if size < 0:
                chunk = self.prefix
            else:
                chunk = self.prefix[self.offset : self.offset + size]
                size -= len(chunk)
            buffer += chunk
            self.offset += len(chunk)

        while True:
            chunk = self.file.read(size)
            if not chunk:
                break
            buffer += chunk
            self.offset += len(chunk)

            if size <= 0:
                break

            size -= len(chunk)

        return buffer

    def close(self):
        # do not touch the underlying stream
        pass
