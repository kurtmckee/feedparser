import json
import subprocess
import sys

import pytest

FEED = """\
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
    <channel>
        <title>Test feed</title>
        <link>https://example.com/</link>
        <description>Test feed</description>
        <item>
            <title>Café</title>
            <link>https://example.com/cafe</link>
        </item>
    </channel>
</rss>
"""


@pytest.mark.parametrize("from_stdin", [False, True])
def test_cli_outputs_entries(tmp_path, from_stdin):
    path = tmp_path / "feed.xml"
    path.write_text(FEED)
    source = "-" if from_stdin else str(path)

    result = subprocess.run(
        [sys.executable, "-m", "feedparser.cli", source],
        input=FEED if from_stdin else None,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["feed"]["title"] == "Test feed"
    assert output["entries"][0]["title"] == "Café"
    assert "Café" in result.stdout
    assert '\n  "feed": {' in result.stdout
    assert result.stderr == ""


def test_cli_fails_on_malformed_feed():
    result = subprocess.run(
        [sys.executable, "-m", "feedparser.cli", "-"],
        input="<rss>",
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert result.stdout == ""
    assert result.stderr
