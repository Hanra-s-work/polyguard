"""Unit tests for the generate_db module."""

import pytest
import tempfile
import os
import sqlite3

from polyguard.src import constants as POLY_CONST
from polyguard.src.generate_db import build_db_from_dir
from polyguard.src.sqlite_handler import SQLiteHandler


class TestGenerateDB:
    """Test suite for generate_db functionality."""

    @pytest.fixture
    def temp_wordlist_dir(self):
        """Create a temporary directory with wordlist files."""
        tmpdir = tempfile.mkdtemp()

        # Create test wordlist files
        wordlists = {
            "en.txt": "hello\nworld\nhell\n",
            "en_uk.txt": "bloke\ntosser\nknobhead\n",
            "fr.txt": "bonjour\nmonde\nmerde\n",
            "de.txt": "hallo\nwelt\nverdammt\n",
            "es.txt": "hola\nmundo\nmierda\n",
        }

        for filename, content in wordlists.items():
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        yield tmpdir

        # Cleanup
        for filename in wordlists:
            filepath = os.path.join(tmpdir, filename)
            if os.path.exists(filepath):
                os.unlink(filepath)
        os.rmdir(tmpdir)

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file path."""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    def test_build_db_from_dir_basic(self, temp_wordlist_dir, temp_db_path):
        """Test basic database building from wordlist directory."""
        count = build_db_from_dir(temp_wordlist_dir, temp_db_path)

        assert count == 5  # 5 language files
        assert os.path.exists(temp_db_path)

    def test_build_db_creates_correct_schema(self, temp_wordlist_dir, temp_db_path):
        """Test that built database has correct schema."""
        build_db_from_dir(temp_wordlist_dir, temp_db_path)

        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # Check table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='words'"
        )
        assert cursor.fetchone() is not None

        # Check columns
        cursor.execute("PRAGMA table_info(words)")
        columns = {row[1] for row in cursor.fetchall()}
        assert "lang" in columns
        assert "word" in columns

        conn.close()

    def test_build_db_imports_words_correctly(self, temp_wordlist_dir, temp_db_path):
        """Test that words are imported correctly from files."""
        build_db_from_dir(temp_wordlist_dir, temp_db_path)

        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # Check English words
        cursor.execute("SELECT word FROM words WHERE lang='en'")
        en_words = {row[0] for row in cursor.fetchall()}
        assert "hello" in en_words
        assert "world" in en_words

        # Check French words
        cursor.execute("SELECT word FROM words WHERE lang='fr'")
        fr_words = {row[0] for row in cursor.fetchall()}
        assert "bonjour" in fr_words

        conn.close()

    def test_build_db_normalizes_words(self, temp_wordlist_dir, temp_db_path):
        """Test that words are normalized (lowercase)."""
        build_db_from_dir(temp_wordlist_dir, temp_db_path)

        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # All words should be lowercase
        cursor.execute("SELECT word FROM words")
        words = [row[0] for row in cursor.fetchall()]

        for word in words:
            assert word == word.lower(), f"Word {word} is not lowercase"

        conn.close()

    def test_build_db_maps_languages_correctly(self, temp_wordlist_dir, temp_db_path):
        """Test that language codes are mapped correctly."""
        build_db_from_dir(temp_wordlist_dir, temp_db_path)

        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # Check that all language codes are recognized
        cursor.execute("SELECT DISTINCT lang FROM words ORDER BY lang")
        langs = {row[0] for row in cursor.fetchall()}

        assert "en" in langs
        assert "en_uk" in langs
        assert "fr" in langs
        assert "de" in langs
        assert "es" in langs

        conn.close()

    def test_build_db_empty_directory(self, temp_db_path):
        """Test building from empty directory."""
        empty_dir = tempfile.mkdtemp()

        try:
            count = build_db_from_dir(empty_dir, temp_db_path)
            assert count == 0
        finally:
            os.rmdir(empty_dir)

    def test_build_db_no_txt_files(self, temp_db_path):
        """Test building from directory with no .txt files."""
        tmpdir = tempfile.mkdtemp()

        # Create non-.txt file
        other_file = os.path.join(tmpdir, "words.md")
        with open(other_file, 'w') as f:
            f.write("hello\n")

        try:
            count = build_db_from_dir(tmpdir, temp_db_path)
            assert count == 0
        finally:
            os.unlink(other_file)
            os.rmdir(tmpdir)

    def test_build_db_idempotent(self, temp_wordlist_dir, temp_db_path):
        """Test that running build_db twice is idempotent."""
        build_db_from_dir(temp_wordlist_dir, temp_db_path)

        # Check word count after first build
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM words")
        count_first = cursor.fetchone()[0]
        conn.close()

        # Build again
        build_db_from_dir(temp_wordlist_dir, temp_db_path)

        # Check word count after second build
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM words")
        count_second = cursor.fetchone()[0]
        conn.close()

        # Counts should be equal (no duplicates)
        assert count_first == count_second

    def test_build_db_nonexistent_directory(self, temp_db_path):
        """Test building from nonexistent directory."""
        with pytest.raises(OSError):
            build_db_from_dir("/nonexistent/directory", temp_db_path)

    def test_build_db_unknown_language_code(self, temp_db_path):
        """Test handling of unknown language codes."""
        tmpdir = tempfile.mkdtemp()

        # Create file with unknown language code
        unknown_file = os.path.join(tmpdir, "xx_xx.txt")
        with open(unknown_file, 'w') as f:
            f.write("word1\nword2\n")

        try:
            count = build_db_from_dir(tmpdir, temp_db_path)
            assert count == 1

            # Words should be in 'other' language
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM words WHERE lang='other'")
            count = cursor.fetchone()[0]
            assert count >= 2
            conn.close()
        finally:
            os.unlink(unknown_file)
            os.rmdir(tmpdir)
