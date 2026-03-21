""" 
# +==== BEGIN polyguard =================+
# LOGO:
#       input
# 
#    @#$%!  hello
#      |     |
#      +--+--+
#         |
#         v
#   +------------+
#   | POLY GUARD |
#   +------------+
#     |        |
#     v        v
#  BLOCKED  PASSED
#    KO       OK
# /STOP
# PROJECT: polyguard
# FILE: cli.py
# CREATION DATE: 21-03-2026
# LAST Modified: 15:19:27 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the code in charge of simulating a pseudo tty for the ones that start the module without piping content into it.
# TTY-friendly CLI wrapper for PolyGuard.
#
# Provides a simple entrypoint that accepts a path to the DB and a test
# word to check. The CLI is intentionally minimal to be easy to extend.
# // AR
# +==== END polyguard =================+
"""

from typing import Iterable, Optional, List
import argparse
import sys

from . import constants as POLY_CONST
from .polyguard import PolyGuard


def _iter_input_lines(stream: Iterable[str]):
    for line in stream:
        text = line.rstrip("\n")
        if text:
            yield text


class CLI:
    """Simple CLI class for PolyGuard interactive and batch usage.

    Kept at module level to allow import and unit testing.
    """

    def __init__(self, guard: PolyGuard):
        self.guard = guard

    def run_single(self, word: str) -> int:
        is_swear = self.guard.is_a_swearword(word)
        status = POLY_CONST.STATUS_BLOCKED if is_swear else POLY_CONST.STATUS_OK
        print(f"{word}: {status}")
        return 0

    def run_stdin(self) -> int:
        for line in _iter_input_lines(sys.stdin):
            result = self.guard.is_a_swearword(line)
            print(POLY_CONST.STATUS_BLOCKED if result else POLY_CONST.STATUS_OK)
        return 0

    def repl(self) -> int:
        print(POLY_CONST.POLY_BOOT_MSG)

        try:
            while True:
                try:
                    text = input(POLY_CONST.POLY_PROMPT)
                except EOFError:
                    break

                if not text:
                    continue

                cmd = text.strip()
                cmd_low = cmd.lower()

                if cmd_low in ("quit", "exit"):
                    break

                if cmd_low == "help":
                    print(POLY_CONST.POLY_HELP_TEXT)
                    continue

                if cmd_low == "man":
                    print(POLY_CONST.POLY_MAN_TEXT)
                    continue

                if cmd_low == "db":
                    print(POLY_CONST.DB_PATH_FMT.format(
                        path=self.guard.db_path))
                    continue

                result = self.guard.is_a_swearword(cmd)
                print(POLY_CONST.STATUS_BLOCKED if result else POLY_CONST.STATUS_OK)

        except KeyboardInterrupt:
            print()

        return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="polyguard", description="Run PolyGuard checks from the TTY or stdin")

    parser.add_argument("--db-path", default=None,
                        help="Path to SQLite DB (overrides package default)")
    parser.add_argument("--word", default=None,
                        help="A single word to test for being a swearword")

    args = parser.parse_args(argv)

    conf = POLY_CONST.LangConfig()

    guard = PolyGuard(conf, db_path=args.db_path)
    cli = CLI(guard)

    # If a single word was passed as an argument, check and print result
    if args.word:
        return cli.run_single(args.word)

    # If stdin is not a TTY, read lines from stdin and process them
    if not sys.stdin.isatty():
        return cli.run_stdin()

    # Otherwise open a simple REPL
    return cli.repl()


if __name__ == "__main__":
    raise SystemExit(main())
