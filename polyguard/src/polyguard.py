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
# LAST Modified: 23:5:54 13-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the entry file of the module.
# // AR
# +==== END polyguard =================+
"""

import sys
from typing import Any


class PolyGuard:
    def __init__(self, success: int = 0, error: int = 1, log: bool = True, debug: bool = False) -> None:
        self.success = success
        self.error = error
        self.log = log
        self.debug = debug

    def __call__(self, *args: Any, **kwds: Any) -> int:
        return self.main()

    def main(self) -> int:
        return 0


if __name__ == "__main__":
    sys.exit(PolyGuard()())
