import codecs
import glob
import os

import pytest

import feedparser

from .helpers import (
    fail_unless_eval,
    get_file_contents,
    get_http_test_data,
    get_test_data,
)

encoding_files = glob.glob(os.path.join(".", "tests", "encoding", "*.xml"))
local_files = [file for file in encoding_files if "http" not in file]
http_files = [file for file in encoding_files if "http" in file]


def test_doctype_replacement():
    """
    Ensure that non-ASCII-compatible encodings don't hide disallowed ENTITY declarations
    """

    doc = """<?xml version="1.0" encoding="utf-16be"?>
    <!DOCTYPE feed [
        <!ENTITY exponential1 "bogus ">
        <!ENTITY exponential2 "&exponential1;&exponential1;">
        <!ENTITY exponential3 "&exponential2;&exponential2;">
    ]>
    <feed><title type="html">&exponential3;</title></feed>"""
    doc = codecs.BOM_UTF16_BE + doc.encode("utf-16be")
    result = feedparser.parse(doc)
    assert result["feed"]["title"] == "&amp;exponential3"


def test_gb2312_converted_to_gb18030_in_xml_encoding():
    # \u55de was chosen because it exists in gb18030 but not gb2312
    feed = """<?xml version="1.0" encoding="gb2312"?>
            <feed><title>\u55de</title></feed>"""
    result = feedparser.parse(
        feed.encode("gb18030"), response_headers={"Content-Type": "text/xml"}
    )
    assert result.encoding == "gb18030"


@pytest.mark.parametrize("file", local_files)
def test_local_encoding_file(file):
    data, text = get_file_contents(file)
    description, eval_string, skip_unless = get_test_data(file, text)
    assert eval(skip_unless)
    fail_unless_eval(file, eval_string)


@pytest.mark.parametrize("file", http_files)
def test_http_encoding_file(file):
    data, text = get_file_contents(file)
    url, description, eval_string, skip_unless = get_http_test_data(file, data, text)
    fail_unless_eval(url, eval_string)


@pytest.mark.parametrize(
    "encoding",
    (
        "437",
        "850",
        "852",
        "855",
        "857",
        "860",
        "861",
        "862",
        "863",
        "865",
        "866",
        "cp037",
        "cp1125",
        "cp1250",
        "cp1251",
        "cp1252",
        "cp1253",
        "cp1254",
        "cp1255",
        "cp1256",
        "cp1257",
        "cp1258",
        "cp437",
        "cp500",
        "cp737",
        "cp775",
        "cp850",
        "cp852",
        "cp855",
        "cp856",
        "cp857",
        "cp860",
        "cp861",
        "cp862",
        "cp863",
        "cp864",
        "cp865",
        "cp866",
        "cp874",
        "cp875",
        "cp_is",
        "csibm037",
        "csibm500",
        "csibm855",
        "csibm857",
        "csibm860",
        "csibm861",
        "csibm863",
        "csibm864",
        "csibm865",
        "csibm866",
        "cskoi8r",
        "cspc775baltic",
        "cspc850multilingual",
        "cspc862latinhebrew",
        "cspc8codepage437",
        "cspcp852",
        "ebcdic-cp-be",
        "ebcdic-cp-ca",
        "ebcdic-cp-ch",
        "ebcdic-cp-nl",
        "ebcdic-cp-us",
        "ebcdic-cp-wt",
        "ebcdic_cp_be",
        "ebcdic_cp_ca",
        "ebcdic_cp_ch",
        "ebcdic_cp_nl",
        "ebcdic_cp_us",
        "ebcdic_cp_wt",
        "ibm037",
        "ibm039",
        "ibm1140",
        "ibm437",
        "ibm500",
        "ibm775",
        "ibm850",
        "ibm852",
        "ibm855",
        "ibm857",
        "ibm860",
        "ibm861",
        "ibm862",
        "ibm863",
        "ibm864",
        "ibm865",
        "ibm866",
        "koi8-r",
        "koi8-t",
        "koi8-u",
        "mac-cyrillic",
        "maccentraleurope",
        "maccyrillic",
        "macgreek",
        "maciceland",
        "macintosh",
        "maclatin2",
        "macroman",
        "macturkish",
        "windows-1250",
        "windows-1251",
        "windows-1252",
        "windows-1253",
        "windows-1254",
        "windows-1255",
        "windows-1256",
        "windows-1257",
        "windows-1258",
        "windows_1250",
        "windows_1251",
        "windows_1252",
        "windows_1253",
        "windows_1254",
        "windows_1255",
        "windows_1256",
        "windows_1257",
        "windows_1258",
    ),
)
def test_encoding(encoding):
    """The XML encoding declaration must be found and honored in binary content."""
    expected = b"\x80".decode(encoding)
    data = f"""
        <?xml version="1.0" encoding="{encoding}"?>
        <feed version="0.3" xmlns="http://purl.org/atom/ns#">
        <title>{expected}</title>
        </feed>
    """

    result = feedparser.parse(data.strip().encode(encoding))
    assert result["encoding"] == encoding
    assert result["feed"]["title"] == expected
