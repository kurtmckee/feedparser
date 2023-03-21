import codecs
import glob
import os

import pytest

import feedparser

from .helpers import fail_unless_eval, get_file_contents, get_test_data

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
    try:
        eval(skip_unless)
    except LookupError as error:
        pytest.skip(error.args[0])
    fail_unless_eval(file, eval_string)


@pytest.mark.parametrize("file", http_files)
def test_http_encoding_file(file, http_server, get_url):
    data, text = get_file_contents(file)
    description, eval_string, skip_unless = get_test_data(file, text)
    url = get_url(file)
    fail_unless_eval(url, eval_string)
