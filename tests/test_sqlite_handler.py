"""Unit tests for the SQLiteHandler module."""

import pytest
import tempfile
import os
import sqlite3

from polyguard.src import constants as POLY_CONST
from polyguard.src.sqlite_handler import SQLiteHandler


class TestSQLiteHandler:
    """Test suite for SQLiteHandler class."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file path."""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    def test_connection_open_and_close(self, temp_db_path):
        """Test opening and closing a database connection."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        assert handler._conn is None

        handler.connect()
        assert handler._conn is not None
        assert isinstance(handler._conn, sqlite3.Connection)

        handler.close()
        assert handler._conn is None

    def test_context_manager(self, temp_db_path):
        """Test SQLiteHandler as context manager."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)

        with handler as h:
            assert h._conn is not None

        assert handler._conn is None

    def test_readonly_connection_nonexistent_file(self, temp_db_path):
        """Test that readonly connection fails for nonexistent file."""
        os.unlink(temp_db_path)  # Ensure file doesn't exist
        handler = SQLiteHandler(temp_db_path, readonly=True, log=False)

        with pytest.raises(sqlite3.OperationalError):
            handler.connect()

    def test_create_schema(self, temp_db_path):
        """Test schema creation."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()

        try:
            handler.create_schema()

            # Verify table exists
            cursor = handler._conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='words'"
            )
            assert cursor.fetchone() is not None
        finally:
            handler.close()

    def test_create_schema_idempotent(self, temp_db_path):
        """Test that schema creation is idempotent."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()

        try:
            handler.create_schema()
            handler.create_schema()  # Should not raise

            cursor = handler._conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='words'")
            assert cursor.fetchone()[0] == 1
        finally:
            handler.close()

    def test_bulk_insert_basic(self, temp_db_path):
        """Test basic bulk insert."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["hello", "world"],
                POLY_CONST.Langs.FR: ["bonjour", "monde"],
            }

            inserted = handler.bulk_insert(mapping)
            assert inserted >= 4  # At least 4 rows

            # Verify insertion
            cursor = handler._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM words")
            assert cursor.fetchone()[0] >= 4
        finally:
            handler.close()

    def test_bulk_insert_normalizes_words(self, temp_db_path):
        """Test that bulk_insert normalizes words (lowercase, strip)."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["  HELLO  ", "World", "  TEST  "],
            }

            handler.bulk_insert(mapping)

            # Verify words are normalized
            cursor = handler._conn.cursor()
            cursor.execute(
                "SELECT word FROM words WHERE lang='en' ORDER BY word")
            words = [row[0] for row in cursor.fetchall()]
            assert "hello" in words
            assert "world" in words
            assert "test" in words
            # Upper case versions should not be there
            assert "HELLO" not in words
            assert "World" not in words
        finally:
            handler.close()

    def test_bulk_insert_handles_duplicates(self, temp_db_path):
        """Test that bulk_insert handles duplicates gracefully."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["hello", "hello", "world"],
            }

            inserted = handler.bulk_insert(mapping)

            # Should have 2 unique words despite duplicate input
            cursor = handler._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM words WHERE lang='en'")
            count = cursor.fetchone()[0]
            assert count == 2
        finally:
            handler.close()

    def test_bulk_insert_idempotent(self, temp_db_path):
        """Test that bulk_insert is idempotent."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["hello", "world"],
            }

            handler.bulk_insert(mapping)

            # Count after first insert
            cursor = handler._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM words")
            count_first = cursor.fetchone()[0]

            # Insert again
            handler.bulk_insert(mapping)

            # Count should be the same
            cursor.execute("SELECT COUNT(*) FROM words")
            count_second = cursor.fetchone()[0]

            assert count_first == count_second
        finally:
            handler.close()

    def test_bulk_insert_skips_none_and_empty(self, temp_db_path):
        """Test that bulk_insert skips None and empty words."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: [None, "", "  ", "hello", None, "world"],
            }

            handler.bulk_insert(mapping)

            cursor = handler._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM words")
            count = cursor.fetchone()[0]
            assert count == 2
        finally:
            handler.close()

    def test_get_words(self, temp_db_path):
        """Test getting words by language."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["hello", "world"],
                POLY_CONST.Langs.FR: ["bonjour", "monde"],
            }
            handler.bulk_insert(mapping)

            # Switch to readonly for testing get_words
            en_words = handler.get_words(POLY_CONST.Langs.EN)
            fr_words = handler.get_words(POLY_CONST.Langs.FR)

            assert "hello" in en_words
            assert "world" in en_words
            assert "bonjour" in fr_words
            assert "monde" in fr_words
        finally:
            handler.close()

    def test_get_words_empty_language(self, temp_db_path):
        """Test getting words for language with no entries."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["hello", "world"],
            }
            handler.bulk_insert(mapping)

            # Try to get words for non-existent language
            de_words = handler.get_words(POLY_CONST.Langs.DE)
            assert de_words == set()
        finally:
            handler.close()

    def test_connection_not_open_raises(self, temp_db_path):
        """Test that operations on closed connection raise."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)

        with pytest.raises(RuntimeError, match="Connection is not open"):
            handler.create_schema()

        with pytest.raises(RuntimeError, match="Connection is not open"):
            handler.bulk_insert({POLY_CONST.Langs.EN: ["test"]})

    def test_multiple_languages(self, temp_db_path):
        """Test handling multiple languages."""
        handler = SQLiteHandler(temp_db_path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        try:
            mapping = {
                POLY_CONST.Langs.EN: ["hello"],
                POLY_CONST.Langs.FR: ["bonjour"],
                POLY_CONST.Langs.DE: ["hallo"],
                POLY_CONST.Langs.IT: ["ciao"],
            }

            handler.bulk_insert(mapping)

            cursor = handler._conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT lang) FROM words")
            lang_count = cursor.fetchone()[0]
            assert lang_count == 4
        finally:
            handler.close()
