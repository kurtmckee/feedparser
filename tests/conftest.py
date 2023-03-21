from __future__ import annotations

import http.server
import io
import os
import posixpath
import re
import threading

import pytest

PORT = 8097  # not really configurable, must match hardcoded port in tests
HOST = "127.0.0.1"  # also not really configurable


class FeedParserTestRequestHandler(http.server.SimpleHTTPRequestHandler):
    headers_re = re.compile(rb"^Header:\s+([^:]+):(.+)$", re.MULTILINE)

    def send_head(self):
        """Send custom headers defined in test case

        Example:
        <!--
        Header:   Content-type: application/atom+xml
        Header:   X-Foo: bar
        -->
        """
        # Short-circuit the HTTP status test `test_redirect_to_304()`
        if self.path == "/-/return-304.xml":
            self.send_response(304)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            return io.BytesIO(b"")
        path = self.translate_path(self.path)
        # the compression tests' filenames determine the header sent
        if self.path.startswith("/tests/compression"):
            if self.path.endswith("gz"):
                headers = {"Content-Encoding": "gzip"}
            else:
                headers = {"Content-Encoding": "deflate"}
            headers["Content-type"] = "application/xml"
        else:
            with open(path, "rb") as f:
                blob = f.read()
            headers = {
                k.decode("utf-8"): v.decode("utf-8").strip()
                for k, v in self.headers_re.findall(blob)
            }
        f = open(path, "rb")
        if self.headers.get("if-modified-since") == headers.get(
            "Last-Modified", "nom"
        ) or self.headers.get("if-none-match") == headers.get("ETag", "nomatch"):
            status = "304"
        else:
            status = "200"
        headers.setdefault("Status", status)
        self.send_response(int(headers["Status"]))
        headers.setdefault("Content-type", self.guess_type(path))
        self.send_header("Content-type", headers["Content-type"])
        self.send_header("Content-Length", str(os.stat(f.name)[6]))
        for k, v in headers.items():
            if k not in ("Status", "Content-type"):
                self.send_header(k, v)
        self.end_headers()
        return f

    def log_request(self, *args):
        pass


class FeedParserTestServer(threading.Thread):
    """HTTP Server that runs in a thread and handles unlimitied requests."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.ready = threading.Event()
        self.httpd = None

    def run(self):
        self.httpd = http.server.HTTPServer((HOST, PORT), FeedParserTestRequestHandler)
        self.ready.set()
        self.httpd.serve_forever()


@pytest.fixture(scope="session")
def http_server():
    httpd = FeedParserTestServer()
    httpd.start()
    httpd.ready.wait()
    yield


@pytest.fixture(scope="session")
def get_url():
    def function(file: str) -> str:
        path = posixpath.normpath(file.replace("\\", "/"))
        return f"http://{HOST}:{PORT}/{path}"

    yield function


@pytest.fixture
def use_loose_parser(monkeypatch):
    import feedparser.api

    monkeypatch.setattr(feedparser.api, "_XML_AVAILABLE", False)
    yield
