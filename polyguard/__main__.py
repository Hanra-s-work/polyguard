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
# FILE: __main__.py
# CREATION DATE: 13-03-2026
# LAST Modified: 18:2:47 13-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the entrypoint of the program when it get called as a module instead of imported.
# // AR
# +==== END polyguard =================+
"""
from .polyguard import PolyGuard

if __name__ == "__main__":
    ERR = 84
    ERROR = ERR
    SUCCESS = 0
    PI = PolyGuard()
    PI.main()
    # TTYI.load_basics()
    # TTYI.mainloop("Test session")
    # TTYI.unload_basics()
