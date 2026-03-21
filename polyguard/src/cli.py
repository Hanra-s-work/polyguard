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
# LAST Modified: 19:42:29 21-03-2026
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


def _resolve_lang(token: str):
    """Resolve a user-provided token to a `POLY_CONST.Langs` member.

    Accepts either the enum value ('en_uk') or the enum name ('EN_UK').
    Returns None if no match is found.
    """
    if not token:
        return None

    norm = token.lower().replace("-", "_")
    try:
        return POLY_CONST.Langs(norm)
    except ValueError:
        # Try matching by enum name
        name = token.upper().replace("-", "_")
        if hasattr(POLY_CONST.Langs, name):
            return getattr(POLY_CONST.Langs, name)
        return None


class CLI:
    """Simple CLI class for PolyGuard interactive and batch usage.

    Kept at module level to allow import and unit testing.
    """

    def __init__(self, guard: PolyGuard):
        self.guard = guard

    def run_single(self, word: str) -> int:
        is_swear = self.guard.is_a_swearword(word)
        status = POLY_CONST.STATUS_OK
        if is_swear:
            status = POLY_CONST.STATUS_BLOCKED
        print(f"{word}: {status}")
        return 0

    def run_stdin(self) -> int:
        for line in _iter_input_lines(sys.stdin):
            result = self.guard.is_a_swearword(line)
            if result:
                print(POLY_CONST.STATUS_BLOCKED)
            else:
                print(POLY_CONST.STATUS_OK)
        return 0

    def cmd_log(self, tokens: list[str]) -> bool:
        if len(tokens) != 2:
            print(f"Usage: {POLY_CONST.COMMAND_TOKEN}log <on|off>")
            return True
        val = tokens[1].lower() in ("on", "1", "true", "yes")
        self.guard.log = val
        if self.guard.sqlite is not None:
            self.guard.sqlite.log = val
        if val:
            print("Logging enabled")
        else:
            print("Logging disabled")
        return True

    def cmd_langopt(self, tokens: list[str]) -> bool:
        if len(tokens) != 3:
            print(f"Usage: {POLY_CONST.COMMAND_TOKEN}langopt <lang> <on|off>")
            return True
        lang_token = tokens[1]
        lang_enum = _resolve_lang(lang_token)

        if lang_enum is None:
            print(f"Unknown language: {lang_token}")
            return True

        val = tokens[2].lower() in ("on", "1", "true", "yes")
        try:
            setattr(self.guard.default_choice, lang_enum.value, val)
            status = "disabled"
            if val:
                status = "enabled"
            print(f"Set {lang_enum.value} {status}")
        except Exception as exc:
            print(f"Failed to set language option: {exc}")
        return True

    def cmd_langs(self, tokens: list[str]) -> bool:
        if not self.guard.ensure_connection():
            print("No DB connection available")
            return True

        try:
            mapping = self.guard.sqlite.list_languages()
        except Exception as exc:
            print(f"Failed to query DB: {exc}")
            return True

        if not mapping:
            print("No languages found in DB")
            return True

        # Fold entries to lines of ~80 chars for compact display
        entries = []
        for lang_code, count in sorted(mapping.items()):
            enabled = False
            try:
                enabled = bool(getattr(self.guard.default_choice, lang_code))
            except Exception:
                enabled = False
            mark = ""
            if enabled:
                mark = "[enabled]"
            entries.append(f"{lang_code}({count}){mark}")

        max_width = 80
        line = []
        cur_len = 0
        for e in entries:
            add_len = len(e)
            if line:
                add_len += 2
            if cur_len + add_len > max_width and line:
                print(", ".join(line))
                line = [e]
                cur_len = len(e)
            else:
                if line:
                    line.append(e)
                    cur_len += add_len
                else:
                    line = [e]
                    cur_len = len(e)

        if line:
            print(", ".join(line))

        return True

    def cmd_langstatus(self, tokens: list[str]) -> bool:
        for lang in POLY_CONST.Langs:
            try:
                enabled = bool(getattr(self.guard.default_choice, lang.value))
            except Exception:
                enabled = False
            status = "off"
            if enabled:
                status = "on"
            print(f"{lang.value}: {status}")
        return True

    def cmd_word(self, tokens: list[str]) -> bool:
        if len(tokens) < 2:
            print(f"Usage: {POLY_CONST.COMMAND_TOKEN}word <word> [<lang>]")
            return True

        # Support multi-word phrases. If the final token resolves to a language,
        # treat it as the optional language param, otherwise the whole remainder
        # is the phrase to check.
        if len(tokens) >= 3:
            possible_lang = tokens[-1]
            lang_enum = _resolve_lang(possible_lang)
            if lang_enum is not None:
                word = " ".join(tokens[1:-1])
            else:
                word = " ".join(tokens[1:])
                lang_enum = None
        else:
            word = tokens[1]
            lang_enum = None

        if lang_enum is not None:
            if not self.guard.ensure_connection():
                print("No DB connection available")
                return True
            try:
                found = self.guard.sqlite.has_word(lang_enum, word)
                if found:
                    print(POLY_CONST.STATUS_BLOCKED)
                else:
                    print(POLY_CONST.STATUS_OK)
            except Exception as exc:
                print(f"DB query failed: {exc}")
            return True

        # No explicit language requested; use current config (supports phrases)
        result = self.guard.is_a_swearword(word)
        if result:
            print(POLY_CONST.STATUS_BLOCKED)
        else:
            print(POLY_CONST.STATUS_OK)
        return True

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

                text = text.strip()

                # Commands are prefixed with ':' to avoid clashing with words to check
                if not text.startswith(POLY_CONST.COMMAND_TOKEN):
                    # Treat entire input as a word to check
                    result = self.guard.is_a_swearword(text)
                    if result:
                        print(POLY_CONST.STATUS_BLOCKED)
                    else:
                        print(POLY_CONST.STATUS_OK)
                    continue

                # Remove prefix and split into tokens for command dispatch
                cmd_body = text[POLY_CONST.COMMAND_TOKEN_LENGTH:]
                tokens = cmd_body.split()
                if not tokens:
                    continue
                base = tokens[0].lower()

                if base in ("quit", "exit"):
                    break

                if base == "help":
                    print(POLY_CONST.POLY_HELP_TEXT)
                    continue

                if base == "man":
                    print(POLY_CONST.POLY_MAN_TEXT)
                    continue

                if base == "db":
                    print(
                        POLY_CONST.DB_PATH_FMT.format(
                            path=self.guard.db_path
                        )
                    )
                    continue

                # Dispatch other commands to dedicated handlers
                if base == "log":
                    self.cmd_log(tokens)
                    continue

                if base == "langopt":
                    self.cmd_langopt(tokens)
                    continue

                if base == "langs":
                    self.cmd_langs(tokens)
                    continue

                if base in ("langstatus", "langsstatus"):
                    self.cmd_langstatus(tokens)
                    continue

                if base == "word":
                    self.cmd_word(tokens)
                    continue

                print(f"Unknown command: {base}")

        except KeyboardInterrupt:
            print()

        return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="polyguard", description="Run PolyGuard checks from the TTY or stdin")

    parser.add_argument(
        "--db-path",
        default=None,
        help="Path to SQLite DB (overrides package default)"
    )
    parser.add_argument(
        "--word",
        default=None,
        help="A single word to test for being a swearword"
    )

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
