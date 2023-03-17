import io
import unittest

import pytest

import feedparser.encodings


class Unseekable(io.BytesIO):
    def tell(self):
        raise io.UnsupportedOperation

    def seek(self, *args):
        raise io.UnsupportedOperation


def test_reset_file_wrapper():
    f = feedparser.encodings.ResetFileWrapper(io.BytesIO(b"abcdef"))
    assert f.read(2) == b"ab"
    f.reset()
    assert f.read() == b"abcdef"

    f = io.BytesIO(b"abcdef")
    f.read(2)
    f = feedparser.encodings.ResetFileWrapper(f)
    assert f.read(2) == b"cd"
    f.reset()
    assert f.read() == b"cdef"

    f = feedparser.encodings.ResetFileWrapper(Unseekable(b"abcdef"))
    assert f.read() == b"abcdef"
    assert f.read() == b""
    with pytest.raises(io.UnsupportedOperation):
        f.reset()
    assert f.read() == b""

    f = feedparser.encodings.ResetFileWrapper(Unseekable(b"abcdef"))
    assert f.read(3) == b"abc"
    with pytest.raises(io.UnsupportedOperation):
        f.reset()
    assert f.read() == b"def"


def test_prefix_file_wrapper_no_prefix():
    f = feedparser.encodings.PrefixFileWrapper(b"", io.BytesIO(b"abc"))
    assert f.read() == b"abc"

    f = feedparser.encodings.PrefixFileWrapper(b"", io.BytesIO(b"abc"))
    assert f.read(1) == b"a"


def test_convert_file_to_utf8_decode_error_fallback():
    # TODO: Confirm this test is useful. It looks like a tautology.
    data = (
        "abcd😀".encode() * feedparser.encodings.CONVERT_FILE_PREFIX_LEN
        + "abcd😀".encode("utf-32")
    )
    headers = {}

    expected_result = {}
    expected_output = feedparser.encodings.convert_to_utf8(
        headers, data, expected_result
    )
    actual_result = {}
    factory = feedparser.encodings.convert_file_to_utf8(
        headers, io.BytesIO(data), actual_result
    )

    assert factory.get_binary_file().read() == expected_output
    assert actual_result["encoding"] == expected_result["encoding"]
    assert isinstance(
        actual_result["bozo_exception"], type(expected_result["bozo_exception"])
    )


class TestEncodingsHelpers(unittest.TestCase):
    ...


def make_prefix_file_wrapper_test(make_file):
    def test(self):
        f = feedparser.encodings.PrefixFileWrapper(b"abc", make_file(b"def"))
        self.assertEqual(f.read(), b"abcdef")
        self.assertEqual(f.read(), b"")

        f = feedparser.encodings.PrefixFileWrapper(b"abc", make_file(b"def"))
        self.assertEqual(f.read(2), b"ab")
        self.assertEqual(f.read(2), b"cd")
        self.assertEqual(f.read(2), b"ef")
        self.assertEqual(f.read(2), b"")
        self.assertEqual(f.read(), b"")

        f = feedparser.encodings.PrefixFileWrapper(b"abc", make_file(b"def"))
        self.assertEqual(f.read(3), b"abc")
        self.assertEqual(f.read(3), b"def")
        self.assertEqual(f.read(3), b"")
        self.assertEqual(f.read(), b"")

        f = feedparser.encodings.PrefixFileWrapper(b"abc", make_file(b"def"))
        self.assertEqual(f.read(0), b"")
        self.assertEqual(f.read(), b"abcdef")

    return test


def _make_file(data):
    return io.BytesIO(data)


def _make_file_in_the_middle(data):
    prefix = b"zzzzz"
    rv = io.BytesIO(prefix + data)
    rv.seek(len(prefix))
    return rv


def _make_file_one_by_one(data):
    return ReadOneByOne(data)


class ReadOneByOne(io.BytesIO):
    def read(self, size=-1):
        if size <= 0:
            return super().read(size)
        return super().read(1)


PREFIX_FILE_WRAPPER_FACTORIES = [
    _make_file,
    _make_file_in_the_middle,
    _make_file_one_by_one,
]

for factory in PREFIX_FILE_WRAPPER_FACTORIES:
    func = make_prefix_file_wrapper_test(factory)
    setattr(
        TestEncodingsHelpers,
        f"test_prefix_file_wrapper_{factory.__name__.lstrip('_')}",
        func,
    )
del factory, func


def make_convert_file_prefix_to_utf8_test(headers):
    from feedparser.encodings import convert_file_prefix_to_utf8, convert_to_utf8

    def test(self):
        def call(data, **kwargs):
            expected_result = {}
            expected_output = convert_to_utf8(
                headers, data.encode("utf-8"), expected_result
            )
            file = io.BytesIO(data.encode("utf-8"))

            actual_result = {}
            prefix = convert_file_prefix_to_utf8(headers, file, actual_result, **kwargs)
            rest = file.read()

            self.assertEqual(prefix + rest, expected_output)
            self.assertEqual(
                prefix.decode("utf-8") + rest.decode("utf-8"),
                expected_output.decode("utf-8"),
            )

            expected_result.pop("bozo_exception", None)
            actual_result.pop("bozo_exception", None)
            self.assertEqual(actual_result, expected_result)

        # these should be parametrized, but it's too complicated to do

        # each of the emojis is 4 bytes long when encoded as utf-8
        data = "😀😛🤯😱"
        call(data, prefix_len=3)
        call(data, prefix_len=4)
        call(data, prefix_len=5)
        call(data, prefix_len=8)
        call(data, prefix_len=40)
        call(data * 8, prefix_len=2, read_to_ascii_len=4)
        call(data * 8, prefix_len=4, read_to_ascii_len=4)

        data = "😀a😛b🤯c😱"
        call(data, prefix_len=3)
        call(data, prefix_len=4)
        call(data, prefix_len=5)
        call(data * 8, prefix_len=2, read_to_ascii_len=4)
        call(data * 8, prefix_len=4, read_to_ascii_len=4)

    return test


def make_convert_file_to_utf8_test(headers, length):
    from feedparser.encodings import convert_file_to_utf8, convert_to_utf8

    digits = b"0123456789abcdef"
    input = convert_to_utf8({}, b"", {}) + digits * int(length / len(digits) + 2)

    def test(self):
        expected_result = {}
        expected_output = convert_to_utf8(headers, input, expected_result)
        expected_result.pop("bozo_exception", None)

        actual_result = {}
        factory = convert_file_to_utf8(headers, io.BytesIO(input), actual_result)

        self.assertEqual(
            factory.get_text_file().read(), expected_output.decode("utf-8")
        )
        self.assertEqual(factory.get_binary_file().read(), expected_output)

        actual_result.pop("bozo_exception", None)
        self.assertEqual(actual_result, expected_result)

        actual_result = {}
        factory = convert_file_to_utf8(
            headers, io.StringIO(input.decode("utf-8")), actual_result
        )

        self.assertEqual(
            factory.get_text_file().read(), expected_output.decode("utf-8")
        )

        actual_result.pop("bozo_exception", None)
        self.assertEqual(actual_result, expected_result)

    return test


CONVERT_TO_UTF8_HEADERS = {
    "simple": {},
    "bad_content_type": {"content-type": "not-a-valid-content-type"},
}
CONVERT_TO_UTF8_LENGTHS = [
    feedparser.encodings.CONVERT_FILE_PREFIX_LEN,
    feedparser.encodings.CONVERT_FILE_STR_PREFIX_LEN,
]

for name, headers in CONVERT_TO_UTF8_HEADERS.items():
    setattr(
        TestEncodingsHelpers,
        f"test_convert_file_prefix_to_utf8_{name}",
        make_convert_file_prefix_to_utf8_test(headers),
    )
    for length in CONVERT_TO_UTF8_LENGTHS:
        setattr(
            TestEncodingsHelpers,
            f"test_convert_file_to_utf8_{name}",
            make_convert_file_to_utf8_test(headers, length),
        )
