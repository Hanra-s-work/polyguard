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
# FILE: polyguard.py
# CREATION DATE: 13-03-2026
# LAST Modified: 3:36:1 22-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the entry file of the module.
# // AR
# +==== END polyguard =================+
"""

import sys
from typing import Any, Optional, List, Set, Dict
from threading import Lock
from collections import OrderedDict

import sqlite3
from display_tty import Disp, initialise_logger
from warnings import warn

from . import constants as POLY_CONST
from .sqlite_handler import SQLiteHandler


class PolyGuard:
    """Singleton profanity filter with multilingual support and LRU caching.

    Manages a persistent connection to an SQLite database of language-specific
    word lists. Provides thread-safe word detection with per-language caching
    to optimize repeated lookups. Supports configurable language subsets and
    can check single words or phrases.

    Note:
        This class uses the singleton pattern. Multiple instantiations return
        the same instance.
    """

    _instance: Optional["PolyGuard"] = None
    _class_lock: Lock = Lock()
    disp: Disp = initialise_logger(__qualname__, False)

    def __new__(cls, *args, **kwargs) -> "PolyGuard":
        """Create or return singleton instance.

        Returns:
            PolyGuard: The singleton instance.
        """
        with cls._class_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, langs: POLY_CONST.LangConfig, db_path: Optional[str] = None, success: int = 0, error: int = 1, log: bool = True, debug: bool = False) -> None:
        """Initialize the PolyGuard instance.

        On first call, attempts to establish a persistent database connection.
        If the connection fails, the instance will attempt to reconnect on demand.

        Args:
            langs (LangConfig): LangConfig instance specifying which languages to check.
            db_path (Optional[str]): Path to the SQLite database. Default: None (package default).
            success (int): Exit code for successful initialization. Default: 0.
            error (int): Exit code for failures. Default: 1.
            log (bool): Enable logging output. Default: True.
            debug (bool): Enable debug-level logging. Default: False.
        """
        # Lock instance to prevent racing calls
        self._function_lock: Lock = Lock()
        # Inherited calls
        self.success = success
        self.error = error
        self.log = log
        self.debug = debug
        self.default_choice: POLY_CONST.LangConfig = langs
        # Determine DB path: use provided override or fall back to package default
        if db_path is None:
            self.db_path = POLY_CONST.DEFAULT_DB_PATH
        else:
            self.db_path = db_path

        # Lazy SQLite handler; do not connect automatically.
        self.sqlite: Optional[SQLiteHandler] = None
        # Indicates whether the configured DB was successfully probed.
        self._db_ready: bool = False
        self.disp.update_disp_debug(debug=debug)
        # LRU cache for loaded languages -> set(words)
        self._cache_limit: int = int(POLY_CONST.DEFAULT_CACHE_MAX_LANGS)
        self._lang_cache: "OrderedDict[POLY_CONST.Langs, set]" = OrderedDict()

        self.disp.log_info(
            f"PolyGuard initialised; db_path={self.db_path}; cache_limit={self._cache_limit}")
        # Try to establish a persistent connection now (middleware)
        if not self.ensure_connection():
            self.disp.log_warning(
                "Initial DB connection failed; will attempt on demand")

    def __call__(self, *args: Any, **kwds: Any) -> int:
        """Callable interface. Delegates to main().

        Returns:
            int: Result code from main() (0 for success, non-zero for error).
        """
        return self.main()

    def _sanify_word(self, word: str) -> Optional[str]:
        """Sanitize and normalize input word for processing.

        Strips whitespace, converts to lowercase, and validates non-empty.

        Args:
            word (str): Raw input word or phrase to sanitize.

        Returns:
            Optional[str]: Lowercased, stripped word, or None if empty/invalid.
        """
        # Quick sanity checks
        if word is None:
            return None

        text = word.strip()

        if not text:
            return None

        # If the input contains whitespace, check each token individually
        text_low = text.lower()
        return text_low

    def _ensure_initialized(self) -> bool:
        """Ensure database is initialized on first use."""
        if not self._db_ready:
            return self.main() == self.success
        return True

    def _determine_language_set(self, language: Optional[POLY_CONST.LangConfig]) -> POLY_CONST.LangConfig:
        """Resolve language configuration, falling back to default if needed.

        Args:
            language (Optional[LangConfig]): Language config override. Default: None.

        Returns:
            LangConfig: Provided language config or default instance config.
        """
        if language is None:
            return self.default_choice
        return language

    def _tokenify(self, text: str) -> List[str]:
        """Tokenize text by splitting on whitespace after removing delimiters.

        Uses pre-computed translation table for fast processing. Employs CPython's
        optimized .split() fast-path (any-whitespace split with empty filtering).

        Args:
            text (str): Text to tokenize (assumed already lowercased).

        Returns:
            List[str]: List of non-empty token strings.
        """
        split_data = text.translate(POLY_CONST.TOKENISER_TABLE).split()
        return split_data

    def extract_swearword_if_present(self, word: str, *, languages_to_check: Optional[POLY_CONST.LangConfig] = None) -> Optional[str]:
        """Extract first profanity match from word or phrase.

        Tokenizes input and checks each token against enabled language word lists.
        Returns immediately on first match for efficiency.

        Args:
            word (str): The word or phrase to check.
            languages_to_check (Optional[LangConfig]): Language config override. Default: None.

        Returns:
            Optional[str]: First matching swearword token found, or None if none detected.
        """
        initialised = self._ensure_initialized()
        if not initialised:
            self.disp.log_error("Initial caching failed, retuning early")
            return None
        word_san = self._sanify_word(word)
        if word_san is None:
            return None
        languages = self._determine_language_set(languages_to_check)
        tokens = self._tokenify(word_san)
        for tok in tokens:
            if self._check_token(tok, languages):
                return tok
        return None

    def is_a_swearword(self, word: str, *, languages_to_check: Optional[POLY_CONST.LangConfig] = None) -> bool:
        """Check if a word or phrase contains profanity.

        Checks individual tokens in phrases and the full phrase itself.
        Uses per-language LRU cache to optimize repeated lookups.

        Args:
            word (str): The word or phrase to check (whitespace-stripped).
            languages_to_check (Optional[LangConfig]): Language config override. Default: None.

        Returns:
            bool: True if any enabled language contains the word, False otherwise.
        """
        self.disp.log_debug(f"is_a_swearword called with word={word!r}")
        initialised = self._ensure_initialized()
        if not initialised:
            self.disp.log_error("Initial caching failed, retuning early")
            return False
        word_san = self._sanify_word(word)
        if word_san is None:
            return False

        languages = self._determine_language_set(languages_to_check)
        tokens = self._tokenify(word_san)
        for tok in tokens:
            if self._check_token(tok, languages):
                return True
        return False

    def get_list_of_swearwords(self, *, languages: Optional[POLY_CONST.LangConfig] = None) -> Dict[str, Set]:
        """Retrieve all swearwords for enabled languages.

        Returns cached word sets if loaded, otherwise queries database.
        Useful for inspection, testing, or bulk operations.

        Args:
            languages (Optional[LangConfig]): Language config override. Default: None.

        Returns:
            Dict[str, Set]: Dictionary mapping language names to sets of profanity words.
                Empty dict if database connection unavailable.
        """
        final = {}
        language_check = self._determine_language_set(languages)
        if not self.ensure_connection() or not self.sqlite:
            self.disp.log_error(
                "No DB connection available; aborting check"
            )
            return final
        for lang in POLY_CONST.Langs:
            lang_state = getattr(language_check, lang.value, None)
            if lang_state is None:
                self.disp.log_warning(f"{lang.value} is defined but not set")
                continue
            if lang_state is not None and lang_state is False:
                self.disp.log_debug(f"{lang.value} is set to not be retrieved")
                continue
            cache_node = self._lang_cache.get(lang, None)
            if cache_node is not None:
                final[str(lang.name)] = cache_node
            else:
                final[str(lang.name)] = self.sqlite.get_words(lang)
        return final

    def _check_token(self, text_low: str, languages: POLY_CONST.LangConfig) -> bool:
        """Check if a single token exists in any enabled language's word list.

        Internal method that performs the actual word lookup using cache and
        database queries. Token must already be lowercased.

        Args:
            text_low (str): Lowercased token to search for.
            languages (LangConfig): LangConfig specifying which languages to query.

        Returns:
            bool: True if token found in any enabled language, False otherwise.

        Raises:
            RuntimeError: If database connection becomes unavailable mid-check.
        """
        # Build list of languages enabled in the provided config
        to_check = []
        for lang in POLY_CONST.Langs:
            try:
                if getattr(languages, lang.value):
                    to_check.append(lang)
            except AttributeError:
                continue

        if not to_check:
            return False

        # First consult in-memory cache under short lock sections
        missing = []
        for lang in to_check:
            with self._function_lock:
                cached = self._lang_cache.get(lang)
                if cached is not None:
                    # mark as recently used
                    try:
                        self._lang_cache.move_to_end(lang)
                    except (KeyError, AttributeError):
                        pass

                    if text_low in cached:
                        self.disp.log_debug(f"Cache hit for lang={lang.value}")
                        return True
                else:
                    missing.append(lang)

        if not missing:
            return False

        # Ensure persistent connection before DB access
        if not self.ensure_connection() or not self.sqlite:
            self.disp.log_error(
                "No DB connection available; aborting check"
            )
            return False

        try:
            loaded = {}
            for lang in missing:
                # type: ignore[attr-defined]
                words = self.sqlite.get_words(lang)
                loaded[lang] = words

        except (sqlite3.Error, RuntimeError) as exc:  # pragma: no cover - defensive
            self.disp.log_error(f"DB access failed in is_a_swearword: {exc}")
            if self.log:
                warn(f"PolyGuard DB access failed: {exc}")
            return False

        # Update cache under lock and test loaded sets
        for lang, words in loaded.items():
            with self._function_lock:
                self._lang_cache[lang] = words  # type: ignore[attr-defined]
                try:
                    self._lang_cache.move_to_end(lang)
                except (KeyError, AttributeError):
                    pass

                # Enforce cache size limit
                while len(self._lang_cache) > self._cache_limit:
                    try:
                        evicted_lang, _ = self._lang_cache.popitem(last=False)
                        self.disp.log_debug(
                            f"Evicted lang from cache: {evicted_lang.value}")
                    except (KeyError, IndexError):
                        break

            if text_low in words:
                self.disp.log_debug(
                    f"Match found after DB load for lang={lang.value}"
                )
                return True

        return False

    def main(self) -> int:
        """Probe the database and preload enabled languages into cache.

        Attempts to verify database accessibility, then preloads up to
        cache_limit languages into memory for faster lookup.

        Returns:
            int: Success code (0) if DB ready, error code otherwise.
        """
        # Probe the configured DB to ensure it is accessible and usable.
        self.disp.log_debug("main() called to probe DB")
        # Ensure persistent connection
        conn_status = self.ensure_connection()
        if not conn_status or not self.sqlite:
            self._db_ready = False  # type: ignore[attr-defined]
            self.disp.log_error("DB probe failed: cannot connect")
            return self.error

        try:
            # Simple probe using the persistent handler
            # type: ignore[attr-defined]
            _ = self.sqlite.get_words(next(iter(POLY_CONST.Langs)))

            # Optionally preload enabled languages into cache up to the cache limit
            to_preload = []
            for lang in POLY_CONST.Langs:
                try:
                    if getattr(self.default_choice, lang.value):
                        to_preload.append(lang)
                except AttributeError:
                    continue

            loaded_count = 0
            for lang in to_preload:
                if loaded_count >= self._cache_limit:
                    break
                # type: ignore[attr-defined]
                words = self.sqlite.get_words(lang)
                with self._function_lock:
                    self._lang_cache[lang] = words
                    try:
                        self._lang_cache.move_to_end(lang)
                    except (KeyError, AttributeError):
                        pass
                    loaded_count += 1

            self._db_ready = True
            self.disp.log_info("DB probe successful; ready")
            return self.success

        except (sqlite3.Error, RuntimeError) as exc:  # pragma: no cover - defensive
            self._db_ready = False
            self.disp.log_error(f"DB probe failed: {exc}")
            if self.log:
                warn(f"PolyGuard failed to open DB '{self.db_path}': {exc}")

            return self.error

    def ensure_connection(self) -> bool:
        """Ensure a persistent SQLiteHandler is created and connected.

        Creates a new handler if needed or reconnects an existing one.
        Cleans up stale connections gracefully.

        Returns:
            bool: True if connection is now open and usable, False otherwise.
        """
        with self._function_lock:
            if self.sqlite is not None:
                try:
                    self.sqlite.connect()
                    return True
                except (sqlite3.Error, RuntimeError):
                    try:
                        self.sqlite.close()
                    except (sqlite3.Error, RuntimeError):
                        pass
                    self.sqlite = None

            try:
                handler = SQLiteHandler(
                    str(self.db_path), readonly=True, log=self.log)
                handler.connect()
                self.sqlite = handler
                return True
            except (sqlite3.Error, RuntimeError) as exc:  # pragma: no cover - defensive
                self.disp.log_error(f"ensure_connection failed: {exc}")
                self.sqlite = None
                return False


if __name__ == "__main__":
    CONF = POLY_CONST.LangConfig()
    instance = PolyGuard(langs=CONF)
    sys.exit(instance())
