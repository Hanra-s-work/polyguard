"""Unit tests for the PolyGuard main module."""

import tempfile
import pytest
import os
from polyguard.src import constants as POLY_CONST
from polyguard.src.sqlite_handler import SQLiteHandler
from polyguard.src.polyguard import PolyGuard


class TestPolyGuard:
    """Test suite for PolyGuard class ."""

    @pytest.fixture
    def temp_db_with_words(self):
        """Create a temporary database with test words."""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)

        # Populate database with test words
        handler = SQLiteHandler(path, readonly=False, log=False)
        handler.connect()
        handler.create_schema()

        mapping = {
            POLY_CONST.Langs.EN: ["hell", "damn", "crap"],
            POLY_CONST.Langs.FR: ["merde", "connard"],
            POLY_CONST.Langs.DE: ["verdammt", "scheiße"],
        }
        handler.bulk_insert(mapping)
        handler.close()

        yield path

        if os.path.exists(path):
            os.unlink(path)

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset PolyGuard singleton between tests."""
        yield
        PolyGuard._instance = None

    def test_initialization_default(self, temp_db_with_words):
        """Test PolyGuard initialization with defaults."""
        langs = POLY_CONST.LangConfig(en=True, fr=False)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.db_path == temp_db_with_words
        assert guard.default_choice == langs

    def test_initialization_custom_db_path(self):
        """Test PolyGuard initialization with custom DB path."""
        langs = POLY_CONST.LangConfig()
        custom_path = "/custom/path/to/db.sqlite"
        guard = PolyGuard(langs, db_path=custom_path, log=False)

        assert guard.db_path == custom_path

    def test_initialization_default_db_path(self):
        """Test PolyGuard initialization uses default DB path when None."""
        langs = POLY_CONST.LangConfig()
        guard = PolyGuard(langs, db_path=None, log=False)

        assert guard.db_path == POLY_CONST.DEFAULT_DB_PATH

    def test_is_a_swearword_single_word_match(self, temp_db_with_words):
        """Test detecting a single swearword."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("hell") is True
        assert guard.is_a_swearword("damn") is True
        assert guard.is_a_swearword("crap") is True

    def test_is_a_swearword_single_word_no_match(self, temp_db_with_words):
        """Test that non-swearwords are not detected."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("hello") is False
        assert guard.is_a_swearword("world") is False

    def test_is_a_swearword_case_insensitive(self, temp_db_with_words):
        """Test that detection is case-insensitive."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("HELL") is True
        assert guard.is_a_swearword("Hell") is True
        assert guard.is_a_swearword("hElL") is True

    def test_is_a_swearword_with_whitespace(self, temp_db_with_words):
        """Test detection with leading/trailing whitespace."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("  hell  ") is True
        assert guard.is_a_swearword("\thell\n") is True

    def test_is_a_swearword_multiple_words(self, temp_db_with_words):
        """Test detection in phrases with multiple words."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        # Should detect "hell" in "what the hell"
        assert guard.is_a_swearword("what the hell") is True
        # Should detect "damn" in "damn it"
        assert guard.is_a_swearword("damn it") is True

    def test_is_a_swearword_phrase_no_match(self, temp_db_with_words):
        """Test phrase with no swearwords."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("hello my friend") is False

    def test_is_a_swearword_multiple_languages(self, temp_db_with_words):
        """Test detection across multiple languages."""
        langs = POLY_CONST.LangConfig(en=True, fr=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("hell") is True
        assert guard.is_a_swearword("merde") is True
        assert guard.is_a_swearword("connard") is True

    def test_is_a_swearword_language_disabled(self, temp_db_with_words):
        """Test that disabled languages are not checked."""
        langs = POLY_CONST.LangConfig(en=True, fr=False)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("hell") is True  # EN is enabled
        assert guard.is_a_swearword("merde") is False  # FR is disabled

    def test_is_a_swearword_empty_string(self, temp_db_with_words):
        """Test that empty strings are handled."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("") is False
        assert guard.is_a_swearword("   ") is False
        assert guard.is_a_swearword(None) is False

    def test_is_a_swearword_no_languages_enabled(self, temp_db_with_words):
        """Test behavior when no languages are enabled."""
        langs = POLY_CONST.LangConfig(en=False, fr=False, de=False)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        assert guard.is_a_swearword("hell") is False
        assert guard.is_a_swearword("merde") is False

    def test_cache_functionality(self, temp_db_with_words):
        """Test that caching works."""
        langs = POLY_CONST.LangConfig(en=True)
        guard = PolyGuard(langs, db_path=temp_db_with_words, log=False)

        # First call loads from DB and caches
        result1 = guard.is_a_swearword("hell")
        assert result1 is True

        # Cache should have EN language
        assert POLY_CONST.Langs.EN in guard._lang_cache

        # Second call should use cache
        result2 = guard.is_a_swearword("damn")
        assert result2 is True

    def test_custom_language_config(self, temp_db_with_words):
        """Test with custom language configuration."""
        langs_to_check = POLY_CONST.LangConfig(de=True, fr=False)
        default_langs = POLY_CONST.LangConfig(en=True)

        guard = PolyGuard(default_langs, db_path=temp_db_with_words, log=False)

        # Using default config (EN only)
        assert guard.is_a_swearword("hell") is True

        # Using custom config (DE only)
        assert guard.is_a_swearword(
            "verdammt", languages_to_check=langs_to_check) is True
        # FR is not in custom config
        assert guard.is_a_swearword(
            "merde", languages_to_check=langs_to_check) is False

    def test_status(self) -> None:
        """Legacy placeholder test."""
        error = 84
        success = 0
        langs = POLY_CONST.LangConfig()
        instance = PolyGuard(langs, log=False, error=error, success=success)
        assert instance.error == error
        assert instance.success == success
