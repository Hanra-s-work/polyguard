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
# LAST Modified: 23:1:56 13-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the file that aims to ease the calling of the files contained in the module.
# // AR
# +==== END polyguard =================+
"""

from .polyguard import PolyGuard

__all__ = [
    "PolyGuard"
]
