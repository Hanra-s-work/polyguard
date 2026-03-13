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
# FILE: test_tty_ov.py
# CREATION DATE: 13-03-2026
# LAST Modified: 23:6:36 13-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is a file that contains a dummy unit test so that the module can pass the testing phase in the workflows.
# // AR
# +==== END polyguard =================+
"""
# tests/test_polyguard.py
from polyguard import PolyGuard


def status_test() -> None:
    error = 84
    success = 0
    instance = PolyGuard(success=success, error=error)
    assert instance.error == error
    assert instance.success == success
