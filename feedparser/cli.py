import argparse
import json
import sys

from .api import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="feed URL, filename, or - for stdin")
    args = parser.parse_args()

    source = sys.stdin.buffer if args.source == "-" else args.source
    feed = parse(source)
    if feed.bozo:
        raise feed.bozo_exception

    json.dump(
        {"feed": feed.feed, "entries": feed.entries},
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )


if __name__ == "__main__":
    main()
