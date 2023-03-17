from __future__ import annotations

import pprint
import re

import feedparser

skip_re = re.compile(r"SkipUnless:\s*(.*?)\n")
desc_re = re.compile(r"Description:\s*(.*?)\s*Expect:\s*(.*)\s*-->")


def get_file_contents(file: str) -> tuple[bytes, str]:
    """Identify data's encoding using its byte order mark and convert it to text."""

    with open(file, "rb") as fp:
        data = fp.read()

    if data[:4] == b"\x4c\x6f\xa7\x94":
        return data, data.decode("cp037")
    elif data[:4] == b"\x00\x00\xfe\xff":
        return data, data.decode("utf-32be")
    elif data[:4] == b"\xff\xfe\x00\x00":
        return data, data.decode("utf-32le")
    elif data[:4] == b"\x00\x00\x00\x3c":
        return data, data.decode("utf-32be")
    elif data[:4] == b"\x3c\x00\x00\x00":
        return data, data.decode("utf-32le")
    elif data[:4] == b"\x00\x3c\x00\x3f":
        return data, data.decode("utf-16be")
    elif data[:4] == b"\x3c\x00\x3f\x00":
        return data, data.decode("utf-16le")
    elif (data[:2] == b"\xfe\xff") and (data[2:4] != b"\x00\x00"):
        return data, data[2:].decode("utf-16be")
    elif (data[:2] == b"\xff\xfe") and (data[2:4] != b"\x00\x00"):
        return data, data[2:].decode("utf-16le")
    elif data[:3] == b"\xef\xbb\xbf":
        return data, data[3:].decode("utf-8", errors="ignore")

    # No byte order mark was found. Assume UTF-8, and ignore errors.
    return data, data.decode("utf-8", errors="ignore")


def get_test_data(path: str, text: str) -> tuple[str, list[str], str]:
    """Extract test data

    Each test case is an XML file which contains not only a test feed
    but also the description of the test and the condition that we
    would expect the parser to create when it parses the feed.  Example:
    <!--
    Description: feed title
    Expect:      feed['title'] == 'Example feed'
    -->
    """
    skip_results = skip_re.search(text)
    if skip_results:
        skip_unless = skip_results.group(1).strip()
    else:
        skip_unless = "1"
    search_results = desc_re.search(text)
    if not search_results:
        raise RuntimeError("can't parse %s" % path)
    description, eval_string = (s.strip() for s in list(search_results.groups()))
    description = path + ": " + description
    return description, eval_string, skip_unless


def everything_is_unicode(d: dict) -> bool:
    """Takes a dictionary, recursively verifies that every value is unicode"""
    for k, v in d.items():
        if isinstance(v, dict) and k != "headers":
            if not everything_is_unicode(v):
                return False
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict) and not everything_is_unicode(i):
                    return False
                elif isinstance(i, bytes):
                    return False
        elif isinstance(v, bytes):
            return False
    return True


def fail_unless_eval(xmlfile, eval_string, msg=None):
    """Fail unless eval(eval_string, env)"""
    env = feedparser.parse(xmlfile)
    if not eval(eval_string, globals(), env):
        failure = msg or f"not eval({eval_string}) \nWITH env({pprint.pformat(env)})"
        raise AssertionError(failure)
    if not everything_is_unicode(env):
        failure = f"not everything is unicode \nWITH env({pprint.pformat(env)})"
        raise AssertionError(failure)
