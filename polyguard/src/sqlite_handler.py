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
# LAST Modified: 14:46:58 21-03-2026
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
import sqlite3
from threading import Lock
from typing import Optional, Iterable, Set, Dict

from display_tty import Disp, initialise_logger

from . import constants as POLY_CONST


class SQLiteHandler:
    """Manage a connection to an SQLite database storing language word-lists.

    The expected schema is a table `words(lang TEXT, word TEXT, PRIMARY KEY(lang, word))`.
    """
    _instance: Optional["SQLiteHandler"] = None
    _class_lock: Lock = Lock()
    disp: Disp = initialise_logger(__qualname__, False)

    def __new__(cls, *args, **kwargs) -> "SQLiteHandler":
        with cls._class_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, db_path: str, readonly: bool = True, *, log: bool = True, debug: bool = False) -> None:
        self.db_path = db_path
        self.readonly = readonly
        # Caller controllable logging flag
        self.log = bool(log)
        self._conn: Optional[sqlite3.Connection] = None
        # Per-instance lock to guard connection and operations.
        self._lock: Lock = Lock()
        self.disp.update_disp_debug(debug)

    def connect(self) -> None:
        """Open the SQLite connection.

        If `readonly` is True the connection attempts to open in read-only mode
        using SQLite URI syntax. If that fails (file missing), an exception
        will be raised.
        """
        with self._lock:
            if self._conn is not None:
                return

            if self.log:
                self.disp.log_debug(
                    f"Opening SQLite connection (readonly={self.readonly}) to {self.db_path}")

            if self.readonly:
                uri = f"file:{os.path.abspath(self.db_path)}?mode=ro"
                self._conn = sqlite3.connect(uri, uri=True)
            else:
                self._conn = sqlite3.connect(self.db_path)

            # Use default row factory (tuples) to keep behaviour explicit
            self._conn.row_factory = None
            if self.log:
                self.disp.log_info("SQLite connection opened")

    def close(self) -> None:
        with self._lock:
            if self._conn is None:
                return

            try:
                if self.log:
                    self.disp.log_debug("Closing SQLite connection")
                self._conn.close()
            finally:
                self._conn = None
                if self.log:
                    self.disp.log_info("SQLite connection closed")

    def __enter__(self) -> "SQLiteHandler":
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def create_schema(self) -> None:
        """Create the words table if it does not exist. Requires a writeable connection."""
        with self._lock:
            if self._conn is None:
                raise RuntimeError("Connection is not open")

            if self.log:
                self.disp.log_debug("Creating schema if missing")
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
            if self.log:
                self.disp.log_info("Schema ensured")

    def bulk_insert(self, mapping: Dict[POLY_CONST.Langs, Iterable[str]]) -> int:
        """Insert many words from a mapping Lang -> iterable(words).

        Returns the number of rows inserted (new unique entries).
        """
        with self._lock:
            if self._conn is None:
                raise RuntimeError("Connection is not open")

            cur = self._conn.cursor()

            inserted = 0

            try:
                if self.log:
                    self.disp.log_debug("Beginning bulk insert")
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

                if self.log:
                    self.disp.log_info(
                        f"Bulk insert complete; total rows (per-lang sum)={inserted}")

            except sqlite3.Error as exc:
                if self.log:
                    self.disp.log_error(f"Bulk insert failed: {exc}")
                self._conn.rollback()
                raise

            return inserted

    def get_words(self, lang: POLY_CONST.Langs) -> Set[str]:
        """Return a set of words for the given language.

        If the DB is empty or lang is missing, returns an empty set.
        """
        with self._lock:
            if self._conn is None:
                raise RuntimeError("Connection is not open")

            if self.log:
                self.disp.log_debug(f"Fetching words for lang={lang.value}")
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

            if self.log:
                self.disp.log_info(
                    f"Found {len(result)} words for lang={lang.value}")
            return result

    def has_word(self, lang: POLY_CONST.Langs, word: str) -> bool:
        """Return True if given word exists for language."""
        with self._lock:
            if self._conn is None:
                raise RuntimeError("Connection is not open")

            cur = self._conn.cursor()

            text = word.strip().lower()

            if not text:
                return False

            if self.log:
                self.disp.log_debug(
                    f"Checking existence for word={text!r} in lang={lang.value}")
            cur.execute(
                "SELECT 1 FROM words WHERE lang = ? AND word = ? LIMIT 1", (lang.value, text))

            row = cur.fetchone()

            found = row is not None
            if found and self.log:
                self.disp.log_info(
                    f"Word matched: {text!r} (lang={lang.value})")

            return found
