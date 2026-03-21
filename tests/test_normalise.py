"""Unit tests for the Normalise module."""

import pytest
import tempfile
import os
from pathlib import Path

from polyguard.src.normalise import Normalise


class TestNormalise:
    """Test suite for Normalise utility class."""

    def test_normalize_empty_list(self):
        """Test normalization of empty list."""
        result = Normalise.normalize([])
        assert result == set()

    def test_normalize_simple_words(self):
        """Test normalization of simple words."""
        words = ["hello", "world", "test"]
        result = Normalise.normalize(words)
        assert result == {"hello", "world", "test"}

    def test_normalize_converts_to_lowercase(self):
        """Test that normalization converts to lowercase."""
        words = ["HELLO", "World", "TeSt"]
        result = Normalise.normalize(words)
        assert result == {"hello", "world", "test"}

    def test_normalize_strips_whitespace(self):
        """Test that normalization strips leading/trailing whitespace."""
        words = ["  hello  ", "\tworld\n", "  test  "]
        result = Normalise.normalize(words)
        assert result == {"hello", "world", "test"}

    def test_normalize_skips_empty_strings(self):
        """Test that normalization skips empty and whitespace-only strings."""
        words = ["hello", "", "  ", "\t\n", "world"]
        result = Normalise.normalize(words)
        assert result == {"hello", "world"}

    def test_normalize_skips_none(self):
        """Test that normalization skips None values."""
        words = ["hello", None, "world", None]
        result = Normalise.normalize(words)
        assert result == {"hello", "world"}

    def test_normalize_deduplicates(self):
        """Test that normalization removes duplicates."""
        words = ["hello", "Hello", "HELLO", "world", "World"]
        result = Normalise.normalize(words)
        assert result == {"hello", "world"}

    def test_normalize_preserves_non_ascii(self):
        """Test that normalization preserves non-ASCII characters."""
        words = ["café", "naïve", "Müller"]
        result = Normalise.normalize(words)
        assert "café" in result
        assert "naïve" in result
        assert "müller" in result

    def test_load_from_file_basic(self):
        """Test loading words from a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("hello\nworld\ntest\n")
            temp_path = f.name

        try:
            result = Normalise.load_from_file(temp_path)
            assert result == {"hello", "world", "test"}
        finally:
            os.unlink(temp_path)

    def test_load_from_file_with_whitespace(self):
        """Test loading file with extra whitespace."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("  hello  \n\nworld\n\t\ttest\t\t\n")
            temp_path = f.name

        try:
            result = Normalise.load_from_file(temp_path)
            assert result == {"hello", "world", "test"}
        finally:
            os.unlink(temp_path)

    def test_load_from_file_not_found(self):
        """Test loading from non-existent file returns empty set."""
        result = Normalise.load_from_file("/nonexistent/path/to/file.txt")
        assert result == set()

    def test_load_from_file_utf8(self):
        """Test loading UTF-8 encoded file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write("café\nnaïve\nMüller\n")
            temp_path = f.name

        try:
            result = Normalise.load_from_file(temp_path, encoding='utf-8')
            assert "café" in result
            assert "naïve" in result
            assert "müller" in result
        finally:
            os.unlink(temp_path)

    def test_load_mapping_empty(self):
        """Test load_mapping with empty dict."""
        result = Normalise.load_mapping({})
        assert result == {}

    def test_load_mapping_basic(self):
        """Test load_mapping with basic mappings."""
        mapping = {
            "en": ["hello", "world"],
            "fr": ["bonjour", "monde"],
        }
        result = Normalise.load_mapping(mapping)
        assert result["en"] == {"hello", "world"}
        assert result["fr"] == {"bonjour", "monde"}

    def test_load_mapping_with_none_value(self):
        """Test load_mapping with None values."""
        mapping = {
            "en": ["hello", "world"],
            "fr": None,
        }
        result = Normalise.load_mapping(mapping)
        assert result["en"] == {"hello", "world"}
        assert result["fr"] == set()

    def test_load_mapping_normalizes_values(self):
        """Test that load_mapping normalizes values properly."""
        mapping = {
            "en": ["HELLO", "  world  ", ""],
            "fr": ["BONJOUR", None, "  MONDE  "],
        }
        result = Normalise.load_mapping(mapping)
        assert result["en"] == {"hello", "world"}
        assert result["fr"] == {"bonjour", "monde"}

    def test_load_mapping_deduplicates_within_values(self):
        """Test that load_mapping deduplicates within each value set."""
        mapping = {
            "en": ["Hello", "hello", "HELLO", "world"],
        }
        result = Normalise.load_mapping(mapping)
        assert len(result["en"]) == 2
        assert result["en"] == {"hello", "world"}
