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
# FILE: sqlite_handler.py
# CREATION DATE: 21-03-2026
# LAST Modified: 1:10:14 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: SQLite handler for PolyGuard word-lists.
This module provides a small, explicit handler to manage a read-only
or read-write SQLite database containing (lang, word) rows. It keeps a
connection open, exposes simple helpers for lookups and bulk inserts,
and avoids inline comprehensions to favour legibility.
# // AR
# +==== END polyguard =================+
"""

import os
from typing import Optional, Iterable, Set, Dict
import sqlite3

from . import constants as POLY_CONST


class SQLiteHandler:
    """Manage a connection to an SQLite database storing language word-lists.

    The expected schema is a table `words(lang TEXT, word TEXT, PRIMARY KEY(lang, word))`.
    """

    def __init__(self, db_path: str, readonly: bool = True) -> None:
        self.db_path = db_path
        self.readonly = readonly
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Open the SQLite connection.

        If `readonly` is True the connection attempts to open in read-only mode
        using SQLite URI syntax. If that fails (file missing), an exception
        will be raised.
        """
        if self._conn is not None:
            return

        if self.readonly:
            uri = f"file:{os.path.abspath(self.db_path)}?mode=ro"
            self._conn = sqlite3.connect(uri, uri=True)
        else:
            self._conn = sqlite3.connect(self.db_path)

        # Use default row factory (tuples) to keep behaviour explicit
        self._conn.row_factory = None

    def close(self) -> None:
        if self._conn is None:
            return

        try:
            self._conn.close()
        finally:
            self._conn = None

    def __enter__(self) -> "SQLiteHandler":
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def create_schema(self) -> None:
        """Create the words table if it does not exist. Requires a writeable connection."""
        if self._conn is None:
            raise RuntimeError("Connection is not open")

        cur = self._conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS words (
                lang TEXT NOT NULL,
                word TEXT NOT NULL,
                PRIMARY KEY(lang, word)
            )
            """
        )

        self._conn.commit()

    def bulk_insert(self, mapping: Dict[POLY_CONST.Langs, Iterable[str]]) -> int:
        """Insert many words from a mapping Lang -> iterable(words).

        Returns the number of rows inserted (new unique entries).
        """
        if self._conn is None:
            raise RuntimeError("Connection is not open")

        cur = self._conn.cursor()

        inserted = 0

        try:
            cur.execute("BEGIN")

            for lang_key, words in mapping.items():
                # Only accept known Langs values for clarity
                if not isinstance(lang_key, POLY_CONST.Langs):
                    continue

                lang_text = lang_key.value

                for w in words:
                    if w is None:
                        continue

                    word = w.strip().lower()

                    if not word:
                        continue

                    # Use INSERT OR IGNORE to avoid duplicate key errors
                    cur.execute(
                        "INSERT OR IGNORE INTO words (lang, word) VALUES (?, ?)",
                        (lang_text, word),
                    )

            # rowcount is not reliable for executemany with OR IGNORE; commit and
            # compute delta using a simple count query if needed.
            self._conn.commit()

            # Compute inserted by counting rows for provided langs
            for lang_key in mapping.keys():
                if not isinstance(lang_key, POLY_CONST.Langs):
                    continue

                cur.execute(
                    "SELECT COUNT(1) FROM words WHERE lang = ?", (lang_key.value,))
                row = cur.fetchone()

                if row is None:
                    continue

                count = int(row[0])
                inserted += count

        except Exception:
            self._conn.rollback()
            raise

        return inserted

    def get_words(self, lang: POLY_CONST.Langs) -> Set[str]:
        """Return a set of words for the given language.

        If the DB is empty or lang is missing, returns an empty set.
        """
        if self._conn is None:
            raise RuntimeError("Connection is not open")

        cur = self._conn.cursor()

        cur.execute("SELECT word FROM words WHERE lang = ?", (lang.value,))

        rows = cur.fetchall()

        result: Set[str] = set()

        for row in rows:
            if not row:
                continue

            word = row[0]

            if word is None:
                continue

            result.add(word)

        return result

    def has_word(self, lang: POLY_CONST.Langs, word: str) -> bool:
        """Return True if given word exists for language."""
        if self._conn is None:
            raise RuntimeError("Connection is not open")

        cur = self._conn.cursor()

        text = word.strip().lower()

        if not text:
            return False

        cur.execute(
            "SELECT 1 FROM words WHERE lang = ? AND word = ? LIMIT 1", (lang.value, text))

        row = cur.fetchone()

        return row is not None
