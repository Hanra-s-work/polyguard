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
# LAST Modified: 19:51:7 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: SQLite handler for PolyGuard word-lists.
# This module provides a small, explicit handler to manage a read-only or read-write SQLite database containing (lang, word) rows. It keeps a connection open, exposes simple helpers for lookups and bulk inserts, and avoids inline comprehensions to favour legibility.
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
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path: str, readonly: bool = True, *, log: bool = True, debug: bool = False) -> None:
        """Initialize SQLite connection handler.

        Sets up connection parameters but does not open the connection until
        connect() is called. Supports both read-only and read-write modes.

        Args:
            db_path: Path to SQLite database file.
            readonly: If True, opens database in read-only mode. Defaults to True.
            log: If True, enables logging of database operations. Defaults to True.
            debug: If True, enables debug-level logging. Defaults to False.
        """
        self.db_path = db_path
        self.readonly = readonly
        # Caller controllable logging flag
        self.log = bool(log)
        self._conn: Optional[sqlite3.Connection] = None
        # Per-instance lock to guard connection and operations.
        self._lock: Lock = Lock()
        self.disp.update_disp_debug(debug)

    def connect(self) -> None:
        """Open SQLite database connection.

        If readonly mode is enabled, uses SQLite URI syntax to open in read-only
        mode. Enables check_same_thread=False to allow multithreaded access
        (concurrency is controlled by instance lock). If already connected,
        this method is a no-op.

        Raises:
            sqlite3.DatabaseError: When connection fails (e.g., file not found in readonly mode).
        """
        with self._lock:
            if self._conn is not None:
                return

            if self.log:
                self.disp.log_debug(
                    f"Opening SQLite connection (readonly={self.readonly}) to {self.db_path}"
                )

            if self.readonly:
                uri = f"file:{os.path.abspath(self.db_path)}?mode=ro"
                # Allow connections to be used from different threads; guard
                # concurrency with the instance lock instead of SQLite's
                # thread-checking to support multithreaded callers.
                self._conn = sqlite3.connect(
                    uri,
                    uri=True,
                    check_same_thread=False
                )
            else:
                self._conn = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False
                )

            # Use default row factory (tuples) to keep behaviour explicit
            self._conn.row_factory = None
            if self.log:
                self.disp.log_info("SQLite connection opened")

    def close(self) -> None:
        """Close SQLite database connection.

        If not connected, this method is a no-op. Safe to call multiple times.
        """
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
        """Context manager entry: open database connection.

        Returns:
            SQLiteHandler: This instance with connection open.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Context manager exit: close database connection.

        Closes connection regardless of whether an exception occurred.
        """
        self.close()

    def create_schema(self) -> None:
        """Create words table if not already present.

        Creates a table with columns (lang TEXT, word TEXT) and a composite
        primary key on (lang, word). Idempotent — safe to call on existing tables.
        Requires a writable database connection.

        Raises:
            RuntimeError: When connection is not open.
            sqlite3.Error: When table creation fails.
        """
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
        """Bulk insert words from language to words mapping.

        Normalizes and inserts words from each language. Uses INSERT OR IGNORE
        to skip duplicate (lang, word) pairs. Returns cumulative row count
        across all languages provided (sum of per-language totals, not insert count).

        Args:
            mapping: Dictionary mapping Langs enums to iterables of words.

        Returns:
            int: Sum of word counts across all languages in mapping after insert.

        Raises:
            RuntimeError: When connection is not open.
            sqlite3.Error: When database operation fails (transaction is rolled back).
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
                        "SELECT COUNT(1) FROM words WHERE lang = ?",
                        (lang_key.value,)
                    )
                    row = cur.fetchone()

                    if row is None:
                        continue

                    count = int(row[0])
                    inserted += count

                if self.log:
                    self.disp.log_info(
                        f"Bulk insert complete; total rows (per-lang sum)={inserted}"
                    )

            except sqlite3.Error as exc:
                if self.log:
                    self.disp.log_error(f"Bulk insert failed: {exc}")
                self._conn.rollback()
                raise

            return inserted

    def get_words(self, lang: POLY_CONST.Langs) -> Set[str]:
        """Retrieve all words for a specific language from database.

        Returns an empty set if the database is empty or the language has no entries.

        Args:
            lang: Langs enum member specifying which language to retrieve.

        Returns:
            Set[str]: Set of all words for the language.

        Raises:
            RuntimeError: When connection is not open.
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
                    f"Found {len(result)} words for lang={lang.value}"
                )
            return result

    def list_languages(self) -> Dict[str, int]:
        """List all languages and their word counts in database.

        Queries all distinct language codes and returns a mapping of code to word count.
        Returns an empty dict if the database is empty or the words table is missing.

        Returns:
            Dict[str, int]: Mapping of language code strings to word counts.

        Raises:
            RuntimeError: When connection is not open.
        """
        with self._lock:
            if self._conn is None:
                raise RuntimeError("Connection is not open")

            cur = self._conn.cursor()
            cur.execute("SELECT lang, COUNT(1) FROM words GROUP BY lang")
            rows = cur.fetchall()

            result: Dict[str, int] = {}

            for row in rows:
                if not row:
                    continue

                lang = row[0]
                count = 0
                try:
                    count = 0
                    if row[1] is not None:
                        count = int(row[1])
                except (ValueError, TypeError):
                    count = 0

                result[lang] = count

            if self.log:
                self.disp.log_info(f"Languages in DB: {len(result)} found")

            return result

    def has_word(self, lang: POLY_CONST.Langs, word: str) -> bool:
        """Check if a word exists in a specific language.

        Normalizes the input word (lowercase, strip whitespace) before checking.
        Returns False for empty or whitespace-only inputs.

        Args:
            lang: Langs enum member specifying which language to search.
            word: Word string to check.

        Returns:
            bool: True if word is present for the language, False otherwise.

        Raises:
            RuntimeError: When connection is not open.
        """
        with self._lock:
            if self._conn is None:
                raise RuntimeError("Connection is not open")

            cur = self._conn.cursor()

            text = word.strip().lower()

            if not text:
                return False

            if self.log:
                self.disp.log_debug(
                    f"Checking existence for word={text!r} in lang={lang.value}"
                )
            cur.execute(
                "SELECT 1 FROM words WHERE lang = ? AND word = ? LIMIT 1",
                (lang.value, text)
            )

            row = cur.fetchone()

            found = row is not None
            if found and self.log:
                self.disp.log_info(
                    f"Word matched: {text!r} (lang={lang.value})"
                )

            return found
