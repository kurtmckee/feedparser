import io

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


@pytest.mark.parametrize(
    "factory",
    [
        _make_file,
        _make_file_in_the_middle,
        _make_file_one_by_one,
    ],
)
def test_prefix_file_wrapper(factory):
    f = feedparser.encodings.PrefixFileWrapper(b"abc", factory(b"def"))
    assert f.read() == b"abcdef"
    assert f.read() == b""

    f = feedparser.encodings.PrefixFileWrapper(b"abc", factory(b"def"))
    assert f.read(2) == b"ab"
    assert f.read(2) == b"cd"
    assert f.read(2) == b"ef"
    assert f.read(2) == b""
    assert f.read() == b""

    f = feedparser.encodings.PrefixFileWrapper(b"abc", factory(b"def"))
    assert f.read(3) == b"abc"
    assert f.read(3) == b"def"
    assert f.read(3) == b""
    assert f.read() == b""

    f = feedparser.encodings.PrefixFileWrapper(b"abc", factory(b"def"))
    assert f.read(0) == b""
    assert f.read() == b"abcdef"

    f = feedparser.encodings.PrefixFileWrapper(b"abc", factory(b"def"))
    assert f.read(2) == b"ab"
    assert f.read() == b"cdef"


# Each emoji is 4 bytes long when encoded in UTF-8.
@pytest.mark.parametrize("data", ("😀😛🤯😱", "😀a😛b🤯c😱"))
@pytest.mark.parametrize(
    "data_multiplier, kwargs",
    (
        (1, {"prefix_len": 3}),
        (1, {"prefix_len": 4}),
        (1, {"prefix_len": 5}),
        (1, {"prefix_len": 8}),
        (1, {"prefix_len": 40}),
        (8, {"prefix_len": 2, "read_to_ascii_len": 4}),
        (8, {"prefix_len": 4, "read_to_ascii_len": 4}),
    ),
)
@pytest.mark.parametrize("headers", ({}, {"content-type": "not-a-valid-content-type"}))
def test_convert_file_prefix_to_utf8(data, data_multiplier, kwargs, headers):
    data = data * data_multiplier

    expected_result = {}
    expected_output = feedparser.encodings.convert_to_utf8(
        headers, data.encode("utf-8"), expected_result
    )
    file = io.BytesIO(data.encode("utf-8"))

    actual_result = {}
    prefix = feedparser.encodings.convert_file_prefix_to_utf8(
        headers, file, actual_result, **kwargs
    )
    rest = file.read()

    assert prefix + rest == expected_output
    assert prefix.decode("utf-8") + rest.decode("utf-8") == expected_output.decode(
        "utf-8"
    )

    expected_result.pop("bozo_exception", None)
    actual_result.pop("bozo_exception", None)
    assert actual_result == expected_result


@pytest.mark.parametrize("headers", ({}, {"content-type": "not-a-valid-content-type"}))
@pytest.mark.parametrize(
    "length",
    (
        feedparser.encodings.CONVERT_FILE_PREFIX_LEN,
        feedparser.encodings.CONVERT_FILE_STR_PREFIX_LEN,
    ),
)
def test_convert_file_to_utf8(headers, length):
    digits = b"0123456789abcdef"
    data = feedparser.encodings.convert_to_utf8({}, b"", {}) + digits * int(
        length / len(digits) + 2
    )

    expected_result = {}
    expected_output = feedparser.encodings.convert_to_utf8(
        headers, data, expected_result
    )
    expected_result.pop("bozo_exception", None)

    actual_result = {}
    factory = feedparser.encodings.convert_file_to_utf8(
        headers, io.BytesIO(data), actual_result
    )

    assert factory.get_text_file().read() == expected_output.decode("utf-8")
    assert factory.get_binary_file().read() == expected_output

    actual_result.pop("bozo_exception", None)
    assert actual_result == expected_result

    actual_result = {}
    factory = feedparser.encodings.convert_file_to_utf8(
        headers, io.StringIO(data.decode("utf-8")), actual_result
    )

    assert factory.get_text_file().read() == expected_output.decode("utf-8")

    actual_result.pop("bozo_exception", None)
    assert actual_result == expected_result
