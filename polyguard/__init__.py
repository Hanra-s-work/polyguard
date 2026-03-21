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
# FILE: __init__.py
# CREATION DATE: 13-03-2026
# LAST Modified: 20:8:17 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: File in charge of easing the import of the program
# // AR
# +==== END polyguard =================+
"""

from .src.polyguard import PolyGuard
from .src.constants import LangConfig

__all__ = [
    "PolyGuard",
    "LangConfig"
]
