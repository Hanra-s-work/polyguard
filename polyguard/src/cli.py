"""TTY-friendly CLI wrapper for PolyGuard.

Provides a simple entrypoint that accepts a path to the DB and a test
word to check. The CLI is intentionally minimal to be easy to extend.
"""
from __future__ import annotations

import argparse
import sys
from typing import Iterable

from .polyguard import PolyGuard
from . import constants as POLY_CONST


def _iter_input_lines(stream: Iterable[str]):
    for line in stream:
        text = line.rstrip("\n")
        if text:
            yield text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="polyguard", description="Run PolyGuard checks from the TTY or stdin")

    parser.add_argument("--db-path", default=None,
                        help="Path to SQLite DB (overrides package default)")
    parser.add_argument("--word", default=None,
                        help="A single word to test for being a swearword")

    args = parser.parse_args(argv)

    conf = POLY_CONST.LangConfig()

    guard = PolyGuard(conf, db_path=args.db_path)

    # If a single word was passed as an argument, check and print result
    if args.word:
        is_swear = guard.is_a_swearword(args.word)
        status = "BLOCKED" if is_swear else "OK"
        print(f"{args.word}: {status}")
        return 0

    # If stdin is not a TTY, read lines from stdin and process them
    if not sys.stdin.isatty():
        for line in _iter_input_lines(sys.stdin):
            result = guard.is_a_swearword(line)
            print("BLOCKED" if result else "OK")

        return 0

    # Otherwise open a simple REPL
    try:
        while True:
            try:
                text = input("polyguard> ")
            except EOFError:
                break

            if not text:
                continue

            if text.strip().lower() in ("quit", "exit"):
                break

            result = guard.is_a_swearword(text)
            print("BLOCKED" if result else "OK")

    except KeyboardInterrupt:
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
