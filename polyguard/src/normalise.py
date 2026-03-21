"""Normalisation utilities for language word-lists.

Provides the `Normalise` class for cleaning and loading newline-delimited
word lists. No compatibility wrappers are included — callers should import
the class directly.
"""
from typing import Iterable, Dict, Set


class Normalise:
    """Group of explicit normalisation utilities.

    Methods are intentionally simple and easy to test. They do not mutate
    external state.
    """

    @staticmethod
    def normalize(words: Iterable[str]) -> Set[str]:
        """Return a set of cleaned, lowercase words from an iterable.

        Skips None, empty and whitespace-only entries.
        """
        result: Set[str] = set()

        for w in words:
            if w is None:
                continue

            text = w.strip()

            if not text:
                continue

            result.add(text.lower())

        return result

    @staticmethod
    def load_from_file(filepath: str, encoding: str = "utf-8") -> Set[str]:
        """Load newline-delimited words from `filepath` and return a normalized set.

        Missing files produce an empty set.
        """
        try:
            with open(filepath, "r", encoding=encoding) as fh:
                lines = fh.readlines()
        except FileNotFoundError:
            return set()

        return Normalise.normalize(lines)

    @staticmethod
    def load_mapping(mapping: "dict") -> Dict[object, Set[str]]:
        """Normalize a mapping of keys -> iterables(words) into key -> set(words).

        The function does not assume any particular key type; callers should
        validate keys where necessary.
        """
        out: Dict[object, Set[str]] = {}

        for key, words in mapping.items():
            if words is None:
                out[key] = set()
                continue

            out[key] = Normalise.normalize(words)

        return out
