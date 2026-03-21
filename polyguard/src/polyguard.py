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
# LAST Modified: 1:10:32 21-03-2026
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

from warnings import warn

from . import constants as POLY_CONST
from .sqlite_handler import SQLiteHandler


class PolyGuard:
    def __init__(self, langs: POLY_CONST.LangConfig, db_path: str | None = None, success: int = 0, error: int = 1, log: bool = True, debug: bool = False) -> None:
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

    def __call__(self, *args: Any, **kwds: Any) -> int:
        return self.main()

    def is_a_swearword(self, word: str, *, languages_to_check: Optional[POLY_CONST.LangConfig] = None) -> bool:
        warn("This function is not yet implemented, it is here so you can put it in you code, it will return false as to not prevent flow run")
        return False

    def main(self) -> int:
        warn("This function is not implemented yet, it will return 0 as a default response, this is the one you call to initialise lang loading.")
        return 0


if __name__ == "__main__":
    CONF = POLY_CONST.LangConfig()
    sys.exit(PolyGuard(CONF)())
