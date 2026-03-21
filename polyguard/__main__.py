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
# LAST Modified: 20:9:35 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the entrypoint of the program when it get called as a module instead of imported.
# // AR
# +==== END polyguard =================+
"""

import sys
try:
    from .src.cli import main
except ImportError:
    try:
        from src.cli import main
    except ImportError as e:
        raise ImportError("Failed to import required files to run") from e

if __name__ == "__main__":
    sys.exit(main(sys.argv))
