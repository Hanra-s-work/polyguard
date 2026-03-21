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
# LAST Modified: 15:10:4 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the entry file of the module.
# // AR
# +==== END polyguard =================+
"""

import sys
from typing import Any, Optional
from threading import Lock
from collections import OrderedDict

import sqlite3
from display_tty import Disp, initialise_logger
from warnings import warn

from . import constants as POLY_CONST
from .sqlite_handler import SQLiteHandler


class PolyGuard:

    _instance: Optional["PolyGuard"] = None
    _class_lock: Lock = Lock()
    disp: Disp = initialise_logger(__qualname__, False)

    def __new__(cls, *args, **kwargs) -> "PolyGuard":
        with cls._class_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, langs: POLY_CONST.LangConfig, db_path: str | None = None, success: int = 0, error: int = 1, log: bool = True, debug: bool = False) -> None:
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
        self.sqlite: SQLiteHandler | None = None
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
        return self.main()

    def is_a_swearword(self, word: str, *, languages_to_check: Optional[POLY_CONST.LangConfig] = None) -> bool:
        self.disp.log_debug(f"is_a_swearword called with word={word!r}")

        # Quick sanity checks
        if word is None:
            return False

        text = word.strip()

        if not text:
            return False

        text_low = text.lower()

        # Resolve languages to check
        languages = languages_to_check or self.default_choice

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
        if not self.ensure_connection():
            self.disp.log_error(
                # type: ignore[attr-defined]
                "No DB connection available in is_a_swearword; aborting check")
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
                    f"Match found after DB load for lang={lang.value}")
                return True

        return False

    def main(self) -> int:
        # Probe the configured DB to ensure it is accessible and usable.
        self.disp.log_debug("main() called to probe DB")
        # Ensure persistent connection
        if not self.ensure_connection():
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

        Returns True if a usable connection exists, False otherwise.
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
