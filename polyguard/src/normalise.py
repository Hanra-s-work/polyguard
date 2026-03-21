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
# FILE: normalise.py
# CREATION DATE: 21-03-2026
# LAST Modified: 14:36:24 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: Normalisation utilities for language word-lists.
# Provides the `Normalise` class for cleaning and loading newline-delimited
# word lists. No compatibility wrappers are included — callers should import
# the class directly.
# // AR
# +==== END polyguard =================+
"""

from typing import Iterable, Dict, Set, Optional
from threading import Lock
from display_tty import Disp, initialise_logger


class Normalise:
    """Group of explicit normalisation utilities.

    Methods are intentionally simple and easy to test. They do not mutate
    external state.
    """
    _instance_lock: Lock = Lock()
    _instance: Optional["Normalise"] = None
    disp: Disp = initialise_logger(__qualname__, False)

    def __new__(cls) -> "Normalise":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def normalize(words: Iterable[str]) -> Set[str]:
        """Return a set of cleaned, lowercase words from an iterable.

        Skips None, empty and whitespace-only entries.
        Uses a small class-level lock to avoid interleaved logging output.
        """
        Normalise.disp.log_debug("normalize() called")

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
        Normalise.disp.log_debug(f"load_from_file called for {filepath}")

        try:
            with open(filepath, "r", encoding=encoding) as fh:
                lines = fh.readlines()
        except FileNotFoundError:
            Normalise.disp.log_warning(f"Wordlist file not found: {filepath}")
            return set()

        return Normalise.normalize(lines)

    @staticmethod
    def load_mapping(mapping: "dict") -> Dict[object, Set[str]]:
        """Normalize a mapping of keys -> iterables(words) into key -> set(words).

        The function does not assume any particular key type; callers should
        validate keys where necessary.
        """
        Normalise.disp.log_debug("load_mapping called")

        out: Dict[object, Set[str]] = {}

        for key, words in mapping.items():
            if words is None:
                out[key] = set()
                continue

            out[key] = Normalise.normalize(words)

        Normalise.disp.log_info(f"load_mapping produced {len(out)} entries")
        return out
