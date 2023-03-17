import feedparser.util


def _check_key(k, d):
    assert k in d
    assert hasattr(d, k)
    assert d[k] == 1
    assert getattr(d, k) == 1


def _check_no_key(k, d):
    assert k not in d
    assert not hasattr(d, k)


def test_empty():
    d = feedparser.util.FeedParserDict()
    keys = (
        "a",
        "entries",
        "id",
        "guid",
        "summary",
        "subtitle",
        "description",
        "category",
        "enclosures",
        "license",
        "categories",
    )
    for k in keys:
        _check_no_key(k, d)
    assert "items" not in d
    assert hasattr(d, "items")  # dict.items() exists


def test_neutral():
    d = feedparser.util.FeedParserDict()
    d["a"] = 1
    _check_key("a", d)


def test_single_mapping_target_1():
    d = feedparser.util.FeedParserDict()
    d["id"] = 1
    _check_key("id", d)
    _check_key("guid", d)


def test_single_mapping_target_2():
    d = feedparser.util.FeedParserDict()
    d["guid"] = 1
    _check_key("id", d)
    _check_key("guid", d)


def test_multiple_mapping_target_1():
    d = feedparser.util.FeedParserDict()
    d["summary"] = 1
    _check_key("summary", d)
    _check_key("description", d)


def test_multiple_mapping_target_2():
    d = feedparser.util.FeedParserDict()
    d["subtitle"] = 1
    _check_key("subtitle", d)
    _check_key("description", d)


def test_multiple_mapping_mapped_key():
    d = feedparser.util.FeedParserDict()
    d["description"] = 1
    _check_key("summary", d)
    _check_key("description", d)


def test_license():
    d = feedparser.util.FeedParserDict()
    d["links"] = []
    assert "license" not in d

    d["links"].append({"rel": "license"})
    assert "license" not in d

    d["links"].append({"rel": "license", "href": "http://dom.test/"})
    assert "license" in d
    assert d["license"] == "http://dom.test/"


def test_category():
    d = feedparser.util.FeedParserDict()
    d["tags"] = []
    assert "category" not in d

    d["tags"] = [{}]
    assert "category" not in d

    d["tags"] = [{"term": "cat"}]
    assert "category" in d
    assert d["category"] == "cat"
    d["tags"].append({"term": "dog"})
    assert d["category"] == "cat"
