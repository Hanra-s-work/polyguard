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
# FILE: generate_db.py
# CREATION DATE: 21-03-2026
# LAST Modified: 14:24:18 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# Build-time helper to generate the SQLite DB from plaintext word lists.
#
# Usage (console script): polyguard-generate-db --source-dir ./wordlists --db-path <path>
#
# The script expects files named using language codes (e.g. `en_uk.txt`, `fr.txt`).
# Files whose stem doesn't match a known `Langs` entry will be stored under `Langs.OTHER`.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the file in charge of generating the database file.
# // AR
# +==== END polyguard =================+
"""

import os
from typing import Dict, Iterable
import argparse

from . import constants as POLY_CONST
from .normalise import Normalise
from .sqlite_handler import SQLiteHandler


def build_db_from_dir(source_dir: str, db_path: str) -> int:
    """Scan `source_dir` for .txt files and write them into `db_path`.

    Returns the number of languages processed.
    """
    files = []

    for entry in os.listdir(source_dir):
        full = os.path.join(source_dir, entry)
        if not os.path.isfile(full):
            continue

        if not entry.lower().endswith(".txt"):
            continue

        files.append(full)

    if not files:
        return 0

    # Map language enum values to Enum members for fast lookup
    lang_map: Dict[str, POLY_CONST.Langs] = {}
    for l in POLY_CONST.Langs:
        lang_map[l.value] = l

    mapping: Dict[POLY_CONST.Langs, Iterable[str]] = {}

    for file_path in files:
        stem = os.path.splitext(os.path.basename(file_path))[0]

        lang_key = lang_map.get(stem, POLY_CONST.Langs.OTHER)

        words = Normalise.load_from_file(file_path)

        # Store as list for sqlite_handler.bulk_insert
        mapping[lang_key] = list(words)

    # Ensure data folder exists for DB path
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    handler = SQLiteHandler(db_path, readonly=False)
    handler.connect()
    handler.create_schema()

    _ = handler.bulk_insert(mapping)

    handler.close()

    return len(mapping)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate polyguard SQLite DB from text lists")

    parser.add_argument(
        "--source-dir",
        default="wordlists",
        help="Directory containing newline-delimited .txt word lists"
    )
    parser.add_argument(
        "--db-path",
        default=POLY_CONST.DEFAULT_DB_PATH,
        help="Path to the SQLite DB to create"
    )

    args = parser.parse_args(argv)

    count = build_db_from_dir(args.source_dir, args.db_path)

    print(f"Processed {count} language files into {args.db_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
